import csv
import hashlib
import logging
import re
import sqlite3
import time
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ============================================================
# CONFIG
# ============================================================

BASE_URL = "https://www.linkedin.com"
SCRIPT_DIR = Path(__file__).parent.resolve()
SESSION_DIR = SCRIPT_DIR / "linkedin_session"
DB_PATH = SCRIPT_DIR / "linkedin_posts.db"
CSV_PATH = SCRIPT_DIR / "linkedin_posts.csv"
LOG_PATH = SCRIPT_DIR / "scraper.log"
DEBUG_DIR = SCRIPT_DIR / "debug"
KEYWORDS_FILE = SCRIPT_DIR / "keywords.txt"

MAX_POSTS_PER_KEYWORD = 30
MAX_SCROLLS = 35
INITIAL_WAIT_MS = 7000
SCROLL_WAIT_MS = 2200
HEADLESS = False

DEFAULT_KEYWORDS = [
    '"generative AI" architecture',
    '"AI rendering" architect',
    '"Midjourney" architect',
    '"ChatGPT" architecture',
    '"AI assisted design"',
    '"future of architects"',
    '"deskilling" architecture',
]

# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("linkedin_scraper")

# ============================================================
# DATABASE
# ============================================================

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS posts (
    post_key TEXT PRIMARY KEY,
    keyword TEXT,
    author TEXT,
    author_url TEXT,
    author_headline TEXT,
    connection_degree TEXT,
    posted_relative TEXT,
    is_edited INTEGER DEFAULT 0,
    url TEXT,
    post_type TEXT,
    text TEXT,
    hashtags TEXT,
    mentions TEXT,
    reactions INTEGER,
    comments INTEGER,
    reposts INTEGER,
    engagement_total INTEGER,
    image_count INTEGER DEFAULT 0,
    video_count INTEGER DEFAULT 0,
    has_image INTEGER DEFAULT 0,
    has_video INTEGER DEFAULT 0,
    collected_at TEXT DEFAULT CURRENT_TIMESTAMP
)
"""

REQUIRED_COLUMNS = {
    "keyword": "TEXT",
    "author": "TEXT",
    "author_url": "TEXT",
    "author_headline": "TEXT",
    "connection_degree": "TEXT",
    "posted_relative": "TEXT",
    "is_edited": "INTEGER DEFAULT 0",
    "url": "TEXT",
    "post_type": "TEXT",
    "text": "TEXT",
    "hashtags": "TEXT",
    "mentions": "TEXT",
    "reactions": "INTEGER",
    "comments": "INTEGER",
    "reposts": "INTEGER",
    "engagement_total": "INTEGER",
    "image_count": "INTEGER DEFAULT 0",
    "video_count": "INTEGER DEFAULT 0",
    "has_image": "INTEGER DEFAULT 0",
    "has_video": "INTEGER DEFAULT 0",
    "collected_at": "TEXT DEFAULT CURRENT_TIMESTAMP",
}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    cur.execute("PRAGMA table_info(posts)")
    existing = {row["name"] for row in cur.fetchall()}

    for column, definition in REQUIRED_COLUMNS.items():
        if column not in existing:
            logger.info("Adding missing DB column: %s", column)
            cur.execute(f"ALTER TABLE posts ADD COLUMN {column} {definition}")

    conn.commit()
    conn.close()


def normalize_text(value):
    if value is None:
        return ""
    value = str(value).replace("\u00a0", " ")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def merge_keywords(old_value, new_keyword):
    values = []
    if old_value:
        values.extend(x.strip() for x in str(old_value).split(" || ") if x.strip())
    if new_keyword and new_keyword not in values:
        values.append(new_keyword)
    return " || ".join(values)


def make_post_key(post):
    url = normalize_text(post.get("url"))
    if url:
        return "url:" + url

    raw = " | ".join(
        [
            normalize_text(post.get("author")),
            normalize_text(post.get("posted_relative")),
            normalize_text(post.get("text")),
        ]
    )
    return "hash:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def save_post(post, keyword):
    conn = get_db()
    cur = conn.cursor()
    post_key = make_post_key(post)

    cur.execute("SELECT keyword FROM posts WHERE post_key = ?", (post_key,))
    existing = cur.fetchone()
    merged_keyword = merge_keywords(existing["keyword"] if existing else "", keyword)

    values = (
        post_key,
        merged_keyword,
        post.get("author", ""),
        post.get("author_url", ""),
        post.get("author_headline", ""),
        post.get("connection_degree", ""),
        post.get("posted_relative", ""),
        int(bool(post.get("is_edited"))),
        post.get("url", ""),
        post.get("post_type", ""),
        post.get("text", ""),
        post.get("hashtags", ""),
        post.get("mentions", ""),
        post.get("reactions"),
        post.get("comments"),
        post.get("reposts"),
        post.get("engagement_total"),
        post.get("image_count", 0),
        post.get("video_count", 0),
        int(bool(post.get("has_image"))),
        int(bool(post.get("has_video"))),
        post.get("collected_at", ""),
    )

    columns = [
        "post_key", "keyword", "author", "author_url", "author_headline",
        "connection_degree", "posted_relative", "is_edited", "url", "post_type",
        "text", "hashtags", "mentions", "reactions", "comments", "reposts",
        "engagement_total", "image_count", "video_count", "has_image", "has_video",
        "collected_at",
    ]
    placeholders = ", ".join(["?"] * len(columns))

    if existing:
        assignments = ", ".join(f"{c} = ?" for c in columns[1:])
        cur.execute(
            f"UPDATE posts SET {assignments} WHERE post_key = ?",
            values[1:] + (post_key,),
        )
        action = "updated"
    else:
        cur.execute(
            f"INSERT INTO posts ({', '.join(columns)}) VALUES ({placeholders})",
            values,
        )
        action = "inserted"

    conn.commit()
    conn.close()
    return action


def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY collected_at DESC")
    rows = cur.fetchall()

    if not rows:
        conn.close()
        return

    headers = rows[0].keys()
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row[h] for h in headers])

    conn.close()
    logger.info("CSV exported: %s (%d rows)", CSV_PATH.resolve(), len(rows))

# ============================================================
# KEYWORDS
# ============================================================


def load_keywords():
    if not KEYWORDS_FILE.exists():
        KEYWORDS_FILE.write_text("\n".join(DEFAULT_KEYWORDS), encoding="utf-8")
        logger.info("Created %s with default keywords.", KEYWORDS_FILE)
    else:
        logger.info("Loaded keywords from %s.", KEYWORDS_FILE)

    keywords = []
    for line in KEYWORDS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        keywords.append(line)
    return keywords

# ============================================================
# DIRECT LINKEDIN SEARCH URL
# ============================================================


def make_search_url(keyword):
    # Directly opens the exact LinkedIn content-search URL.
    return (
        f"{BASE_URL}/search/results/content/"
        f"?keywords={quote(keyword)}"
        f"&origin=SWITCH_SEARCH_VERTICAL"
    )

# ============================================================
# LOGIN
# ============================================================


def is_logged_in(page):
    selectors = [
        "nav.global-nav",
        '[data-testid="typeahead-input"]',
        'a[href*="/feed/"]',
        'a[href*="/mynetwork/"]',
    ]

    for selector in selectors:
        try:
            if page.locator(selector).count() > 0:
                return True
        except Exception:
            pass
    return False


def ensure_login(page):
    page.goto(BASE_URL + "/feed/", wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    if is_logged_in(page):
        logger.info("LinkedIn login detected.")
        return True

    logger.warning("LinkedIn login is required.")
    logger.warning("Log in manually in the opened browser. Waiting up to 5 minutes...")

    deadline = time.time() + 300
    while time.time() < deadline:
        if is_logged_in(page):
            logger.info("Login detected.")
            return True
        page.wait_for_timeout(2000)

    logger.error("Login was not detected.")
    return False

# ============================================================
# SEARCH PAGE
# ============================================================


def open_search(page, keyword):
    url = make_search_url(keyword)

    logger.info("=" * 70)
    logger.info("SEARCH: %s", keyword)
    logger.info("DIRECT URL: %s", url)

    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(INITIAL_WAIT_MS)

    logger.info("Current URL: %s", page.url)
    return verify_search_results(page)


def verify_search_results(page):
    try:
        posts_filter = page.locator('[role="radio"][aria-label="Filter by Posts"]')
        if posts_filter.count() > 0:
            checked = posts_filter.first.get_attribute("aria-checked")
            logger.info("Posts filter found. aria-checked=%s", checked)
    except Exception as exc:
        logger.debug("Posts filter check failed: %s", exc)

    try:
        page.locator('main [role="listitem"]').first.wait_for(state="visible", timeout=15000)
        logger.info("Search result list detected.")
        return True
    except PlaywrightTimeoutError:
        logger.warning("Result list not detected within timeout.")
        DEBUG_DIR.mkdir(exist_ok=True)
        try:
            page.screenshot(path=str(DEBUG_DIR / "search_timeout.png"), full_page=True)
            (DEBUG_DIR / "search_timeout.html").write_text(page.content(), encoding="utf-8")
        except Exception:
            pass
        return False

# ============================================================
# EXPAND "MORE"
# ============================================================


def expand_posts(page):
    buttons = page.locator('button[data-testid="expandable-text-button"]')
    count = buttons.count()
    clicked = 0

    for i in range(count):
        try:
            button = buttons.nth(i)
            if not button.is_visible():
                continue

            spans = button.locator("span")
            if spans.count() > 0:
                spans.last.click(timeout=1500, force=True)
            else:
                button.click(timeout=1500, force=True)
            clicked += 1
        except Exception:
            continue

    if clicked:
        page.wait_for_timeout(500)
    return clicked

# ============================================================
# EXTRACTION FROM CURRENT LINKEDIN SDUI DOM
# ============================================================

EXTRACT_JS = r"""
() => {
    const clean = (value) => {
        if (!value) return "";
        return String(value)
            .replace(/\u00a0/g, " ")
            .replace(/[ \t]+/g, " ")
            .replace(/\n{3,}/g, "\n\n")
            .trim();
    };

    const parseNumber = (value) => {
        if (!value) return null;
        const s = String(value).toLowerCase().replace(/,/g, "").trim();
        const match = s.match(/(\d+(?:\.\d+)?)\s*([km])?/i);
        if (!match) return null;
        let n = Number(match[1]);
        if (match[2] === "k") n *= 1000;
        if (match[2] === "m") n *= 1000000;
        return Math.round(n);
    };

    const extractMetric = (text, kind) => {
        // Strategy 1: LinkedIn social-action buttons with aria-label
        // e.g., "Like 123", "Comment 45", "Repost 7"
        const ariaPatterns = {
            reactions: [/like\s+(\d[\d,.]*)/i, /(\d[\d,.]*)\s+likes?/i, /(\d[\d,.]*)\s+reactions?/i],
            comments: [/comment\s+(\d[\d,.]*)/i, /(\d[\d,.]*)\s+comments?/i],
            reposts: [/repost\s+(\d[\d,.]*)/i, /(\d[\d,.]*)\s+reposts?/i]
        };

        // Try aria-label patterns first
        for (const pattern of (ariaPatterns[kind] || [])) {
            const match = text.match(pattern);
            if (match) return parseNumber(match[1]);
        }

        // Strategy 2: LinkedIn 2026 DOM — last 3 standalone numbers are reactions, comments, reposts
        // Cards end with lines like: "164", "31", "5" (no labels)
        const lines = text.split(/\n+/).map(l => l.trim()).filter(Boolean);
        const numberLines = [];
        for (let i = lines.length - 1; i >= 0 && numberLines.length < 3; i--) {
            const line = lines[i];
            if (/^\d[\d,]*$/.test(line)) {
                numberLines.unshift(line);
            }
        }

        if (numberLines.length >= 3) {
            if (kind === 'reactions') return parseNumber(numberLines[0]);
            if (kind === 'comments') return parseNumber(numberLines[1]);
            if (kind === 'reposts') return parseNumber(numberLines[2]);
        }

        // Strategy 3: Classic regex on full text (fallback)
        const textPatterns = {
            reactions: [/(\d[\d,.]*\s*[km]?)\s+reactions?/i, /(\d[\d,.]*\s*[km]?)\s+likes?/i],
            comments: [/(\d[\d,.]*\s*[km]?)\s+comments?/i],
            reposts: [/(\d[\d,.]*\s*[km]?)\s+reposts?/i, /(\d[\d,.]*\s*[km]?)\s+shares?/i]
        };

        for (const pattern of (textPatterns[kind] || [])) {
            const match = text.match(pattern);
            if (match) return parseNumber(match[1]);
        }

        return null;
    };

    const getLines = (element) => {
        return clean(element.innerText || element.textContent || "")
            .split(/\n+/)
            .map(x => clean(x))
            .filter(Boolean);
    };

    const getAuthor = (card) => {
        const menu = card.querySelector('button[aria-label*="Open control menu for post by"]');
        if (menu) {
            const label = menu.getAttribute("aria-label") || "";
            const match = label.match(/post by\s+(.+)$/i);
            if (match) return clean(match[1]);
        }

        const profile = card.querySelector('a[href*="/in/"]');
        return profile ? clean(profile.innerText) : "";
    };

    const getAuthorUrl = (card) => {
        const links = Array.from(card.querySelectorAll('a[href*="/in/"]'));
        for (const link of links) {
            const href = link.href || "";
            if (href.includes("/in/")) return href.split("?")[0];
        }
        return "";
    };

    const getHeaderLines = (card) => {
        const lines = getLines(card);
        const box = card.querySelector('[data-testid="expandable-text-box"]');
        const postText = box ? clean(box.innerText || box.textContent || "") : "";

        if (!postText) return lines;

        const exactIndex = lines.findIndex(x => x === postText);
        if (exactIndex > 0) return lines.slice(0, exactIndex);

        const result = [];
        for (const line of lines) {
            if (line === postText) break;
            result.push(line);
        }
        return result;
    };

    const getDegree = (headerLines, cardText) => {
        const match = (headerLines.join(" ") + " " + cardText).match(/(?:•|·)\s*(1st|2nd|3rd(?:\+)?)/i);
        return match ? match[1] : "";
    };

    const getPostedRelative = (headerLines, fullCardText) => {
        // LinkedIn 2026 format: "2d •", "16h •", "3w •", "1mo •"
        const shortPattern = /^(\d+\s*[smhdwy]|\d+\s*mo)\b/i;

        // Search header lines first
        for (const line of headerLines) {
            const value = clean(line);
            if (!value || value.length > 30) continue;
            const match = value.match(shortPattern);
            if (match) return match[1];
        }

        // Fallback: search full card text for relative time near the top
        if (fullCardText) {
            const topPortion = fullCardText.split('\n').slice(0, 15).join(' ');
            const match = topPortion.match(shortPattern);
            if (match) return match[1];
        }

        return "";
    };

    const getHeadline = (headerLines, author) => {
        let authorIndex = -1;

        for (let i = 0; i < headerLines.length; i++) {
            if (author && headerLines[i].toLowerCase() === author.toLowerCase()) {
                authorIndex = i;
                break;
            }
        }

        if (authorIndex < 0) return "";

        const reject = [
            /^\d+\s*(?:mo|yr|s|m|h|d|w|y)$/i,
            /^\d+\s*(?:secs?|mins?|hours?|days?|weeks?|months?|years?)$/i,
            /^edited$/i,
            /^follow$/i,
            /^connect$/i,
            /^send$/i
        ];

        for (let i = authorIndex + 1; i < headerLines.length; i++) {
            const line = clean(headerLines[i]);
            if (!line || line.includes("•")) continue;
            if (reject.some(pattern => pattern.test(line))) continue;
            if (line.length > 250) continue;
            if (/reactions?|comments?|reposts?|likes?/i.test(line)) continue;
            return line;
        }
        return "";
    };

    const getPostUrl = (card) => {
        const links = Array.from(card.querySelectorAll("a[href]"));
        for (const a of links) {
            const href = a.href || "";
            if (
                href.includes("/posts/") ||
                href.includes("/feed/update/") ||
                href.includes("/pulse/")
            ) return href.split("?")[0];
        }
        return "";
    };

    const getPostText = (card) => {
        const box = card.querySelector('[data-testid="expandable-text-box"]');
        return box ? clean(box.innerText || box.textContent || "") : "";
    };

    const getHashtags = (card, text) => {
        const set = new Set();
        const links = card.querySelectorAll('a[href*="keywords=%23"], a[href*="keywords=#"]');
        for (const link of links) {
            const value = clean(link.innerText || "");
            if (value.startsWith("#")) set.add(value);
        }
        const matches = text.match(/#[A-Za-z0-9_\-]+/g) || [];
        for (const item of matches) set.add(item);
        return Array.from(set).join(" | ");
    };

    const getMentions = (text) => {
        const matches = text.match(/@[A-Za-z0-9._-]+/g) || [];
        return Array.from(new Set(matches)).join(" | ");
    };

    const cards = Array.from(document.querySelectorAll('main [role="listitem"]'));
    const output = [];

    for (const card of cards) {
        const heading = card.querySelector("h2");
        const headingText = clean(heading ? heading.innerText : "");
        if (!/Feed post/i.test(headingText)) continue;

        const fullText = clean(card.innerText || "");
        const text = getPostText(card);
        if (!text) continue;

        const author = getAuthor(card);
        const authorUrl = getAuthorUrl(card);
        const headerLines = getHeaderLines(card);

        const reactions = extractMetric(fullText, "reactions");
        const comments = extractMetric(fullText, "comments");
        const reposts = extractMetric(fullText, "reposts");
        const engagementTotal = (reactions || 0) + (comments || 0) + (reposts || 0);

        const postUrl = getPostUrl(card);
        let postType = "feed_post";
        if (/\/pulse\//i.test(postUrl)) postType = "article";
        else if (/\/jobs\//i.test(postUrl)) postType = "job";

        const images = Array.from(card.querySelectorAll("img")).filter(img => {
            return (img.getAttribute("src") || "") || (img.getAttribute("alt") || "");
        });
        const videos = Array.from(card.querySelectorAll("video"));

        output.push({
            author,
            author_url: authorUrl,
            author_headline: getHeadline(headerLines, author),
            connection_degree: getDegree(headerLines, fullText),
            posted_relative: getPostedRelative(headerLines, fullText),
            is_edited: /\bEdited\b/i.test(fullText) ? 1 : 0,
            url: postUrl,
            post_type: postType,
            text,
            hashtags: getHashtags(card, text),
            mentions: getMentions(text),
            reactions,
            comments,
            reposts,
            engagement_total: engagementTotal,
            image_count: images.length,
            video_count: videos.length,
            has_image: images.length > 0 ? 1 : 0,
            has_video: videos.length > 0 ? 1 : 0
        });
    }

    return output;
}
"""


def extract_posts(page):
    try:
        result = page.evaluate(EXTRACT_JS)
        return result if isinstance(result, list) else []
    except Exception as exc:
        logger.error("Extraction failed: %s", exc)
        return []

# ============================================================
# SCRAPE ONE KEYWORD
# ============================================================


def scrape_keyword(page, keyword):
    if not open_search(page, keyword):
        logger.warning("Skipping keyword because search results failed: %s", keyword)
        return 0

    local_seen = set()
    inserted_count = 0
    observed_count = 0
    no_progress_rounds = 0
    last_height = 0

    for scroll_number in range(1, MAX_SCROLLS + 1):
        expanded = expand_posts(page)
        if expanded:
            logger.info("Expanded %d post(s) on scroll %d", expanded, scroll_number)

        posts = extract_posts(page)
        new_this_round = 0

        for post in posts:
            key = make_post_key(post)
            if key in local_seen:
                continue

            local_seen.add(key)
            new_this_round += 1
            observed_count += 1
            post["collected_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

            action = save_post(post, keyword)
            if action == "inserted":
                inserted_count += 1

            logger.info(
                "[%d] %s | %s | %s | reactions=%s comments=%s reposts=%s",
                observed_count,
                post.get("author") or "Unknown",
                post.get("posted_relative") or "",
                action,
                post.get("reactions"),
                post.get("comments"),
                post.get("reposts"),
            )

        logger.info(
            "Scroll %d/%d | visible=%d | unique=%d | new=%d",
            scroll_number,
            MAX_SCROLLS,
            len(posts),
            len(local_seen),
            new_this_round,
        )

        if len(local_seen) >= MAX_POSTS_PER_KEYWORD:
            logger.info("Reached MAX_POSTS_PER_KEYWORD=%d", MAX_POSTS_PER_KEYWORD)
            break

        try:
            height = page.evaluate("() => document.body.scrollHeight")
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(SCROLL_WAIT_MS)
        except Exception as exc:
            logger.warning("Scroll failed: %s", exc)
            break

        if height == last_height and new_this_round == 0:
            no_progress_rounds += 1
        else:
            no_progress_rounds = 0

        last_height = height

        if no_progress_rounds >= 4:
            logger.info("No new posts/page height for 4 rounds; stopping keyword.")
            break

    logger.info(
        "Finished keyword: %s | observed=%d | newly inserted=%d",
        keyword,
        observed_count,
        inserted_count,
    )
    return inserted_count

# ============================================================
# MAIN
# ============================================================


def main():
    init_db()
    keywords = load_keywords()

    if not keywords:
        logger.error("No keywords found.")
        return

    DEBUG_DIR.mkdir(exist_ok=True)
    logger.info("Loaded %d keyword(s).", len(keywords))

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            channel="chrome",
            headless=HEADLESS,
            viewport={"width": 1440, "height": 1000},
            locale="en-US",
        )

        page = browser.pages[0] if browser.pages else browser.new_page()

        try:
            if not ensure_login(page):
                return

            total_inserted = 0

            for index, keyword in enumerate(keywords, start=1):
                logger.info("\n########## KEYWORD %d/%d ##########\n%s\n", index, len(keywords), keyword)
                try:
                    total_inserted += scrape_keyword(page, keyword)
                except Exception as exc:
                    logger.exception("Unexpected error for keyword '%s': %s", keyword, exc)
                export_csv()

            logger.info("=" * 70)
            logger.info("DONE | newly inserted this run=%d", total_inserted)
            logger.info("Database: %s", DB_PATH.resolve())
            logger.info("CSV: %s", CSV_PATH.resolve())

        finally:
            try:
                browser.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()