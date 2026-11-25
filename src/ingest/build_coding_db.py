"""Seed `_saintiment_coding_db` on Neon for the team's 50-post initial coding studio
and politely extract readable text from external links/articles attached to the
50 sampled posts.

Safety & Provenance:
- Isolated Neon database `_saintiment_coding_db` (never touches `_saintiment_swipe_team_db`).
- Permanent append-only `coding_events` table + PostgreSQL triggers on
  `coding_themes`, `coding_codes`, `coding_highlights`, and `coding_post_status`
  so zero edits or deletions can ever be lost.
- Refuses to overwrite existing coding data unless `--force` is passed.

Usage:
    /Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python3 src/ingest/build_coding_db.py
    /Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python3 src/ingest/build_coding_db.py --force
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path

WORKTREE_ROOT = Path(__file__).resolve().parents[2]
MAIN_REPO_ROOT = Path("/Users/kaveh/Desktop/base/_LIBRARY/_saintimental")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_curated_db import make_db_url  # noqa: E402

CODING_DB = "_saintiment_coding_db"
CODERS = [(1, "مرتضی", "Morteza"), (2, "ایمان", "Iman"), (3, "کاوه", "Kaveh")]

URL_RE = re.compile(r"https?://[^\s)\]>\"',]+")
SKIP_HOST_SUBSTRS = (
    "media.licdn.com",
    "static.licdn.com",
    "dms.licdn.com",
    "licdn.com/dms/",
)
PAYWALL_HINTS = (
    "subscribe to continue",
    "subscription required",
    "sign in to read",
    "create a free account to continue",
    "this article is for subscribers",
    "become a member to read",
)
CAPTCHA_HINTS = (
    "verify you are human",
    "captcha",
    "cf-turnstile",
    "enable javascript and cookies to continue",
    "just a moment...",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS coders (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL,
    name_en TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS coding_posts (
    sample_id TEXT PRIMARY KEY,
    source_post_id TEXT UNIQUE NOT NULL,
    reviewer_set TEXT NOT NULL,
    primary_family TEXT NOT NULL,
    matched_families TEXT,
    matched_query_codes TEXT,
    posted_at TEXT,
    post_text TEXT NOT NULL,
    text_chars INTEGER NOT NULL,
    author_type TEXT,
    author_name TEXT,
    author_headline TEXT,
    post_url TEXT,
    reactions INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    has_external_link BOOLEAN NOT NULL DEFAULT FALSE,
    external_url_count INTEGER NOT NULL DEFAULT 0,
    newsletter_title TEXT,
    newsletter_url TEXT
);

CREATE TABLE IF NOT EXISTS coding_external_sources (
    id BIGSERIAL PRIMARY KEY,
    sample_id TEXT NOT NULL REFERENCES coding_posts(sample_id) ON DELETE CASCADE,
    source_kind TEXT NOT NULL,
    original_url TEXT NOT NULL,
    resolved_url TEXT,
    domain TEXT,
    title TEXT,
    extracted_text TEXT,
    extracted_chars INTEGER NOT NULL DEFAULT 0,
    fetch_status TEXT NOT NULL,
    http_status INTEGER,
    UNIQUE (sample_id, original_url)
);

CREATE TABLE IF NOT EXISTS coding_themes (
    id BIGSERIAL PRIMARY KEY,
    coder_id SMALLINT NOT NULL REFERENCES coders(id),
    name TEXT NOT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (coder_id, name)
);

CREATE TABLE IF NOT EXISTS coding_codes (
    id BIGSERIAL PRIMARY KEY,
    coder_id SMALLINT NOT NULL REFERENCES coders(id),
    label TEXT NOT NULL,
    color_idx SMALLINT NOT NULL DEFAULT 1,
    theme_id BIGINT REFERENCES coding_themes(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (coder_id, label)
);

CREATE TABLE IF NOT EXISTS coding_highlights (
    id BIGSERIAL PRIMARY KEY,
    coder_id SMALLINT NOT NULL REFERENCES coders(id),
    sample_id TEXT NOT NULL REFERENCES coding_posts(sample_id) ON DELETE CASCADE,
    source TEXT NOT NULL CHECK (source IN ('post', 'external')),
    external_source_id BIGINT REFERENCES coding_external_sources(id) ON DELETE SET NULL,
    paragraph_idx INTEGER NOT NULL DEFAULT 0,
    start_offset INTEGER NOT NULL DEFAULT 0,
    end_offset INTEGER NOT NULL DEFAULT 0,
    quote TEXT NOT NULL,
    code_id BIGINT NOT NULL REFERENCES coding_codes(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS coding_post_status (
    coder_id SMALLINT NOT NULL REFERENCES coders(id),
    sample_id TEXT NOT NULL REFERENCES coding_posts(sample_id) ON DELETE CASCADE,
    is_coded BOOLEAN NOT NULL DEFAULT FALSE,
    link_reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    coder_notes TEXT DEFAULT '',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (coder_id, sample_id)
);

CREATE TABLE IF NOT EXISTS coding_events (
    id BIGSERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('insert', 'update', 'delete')),
    coder_id SMALLINT,
    record_id TEXT NOT NULL,
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS coding_ext_sample_idx ON coding_external_sources (sample_id);
CREATE INDEX IF NOT EXISTS coding_codes_coder_idx ON coding_codes (coder_id);
CREATE INDEX IF NOT EXISTS coding_hl_coder_sample_idx ON coding_highlights (coder_id, sample_id);
CREATE INDEX IF NOT EXISTS coding_events_coder_idx ON coding_events (coder_id, changed_at);

CREATE OR REPLACE FUNCTION log_coding_event() RETURNS TRIGGER AS $$
DECLARE
    v_coder SMALLINT;
    v_record TEXT;
BEGIN
    IF TG_TABLE_NAME = 'coding_post_status' THEN
        IF TG_OP = 'DELETE' THEN
            v_coder := OLD.coder_id;
            v_record := OLD.coder_id::TEXT || ':' || OLD.sample_id;
        ELSE
            v_coder := NEW.coder_id;
            v_record := NEW.coder_id::TEXT || ':' || NEW.sample_id;
        END IF;
    ELSE
        IF TG_OP = 'DELETE' THEN
            v_coder := OLD.coder_id;
            v_record := OLD.id::TEXT;
        ELSE
            v_coder := NEW.coder_id;
            v_record := NEW.id::TEXT;
        END IF;
    END IF;

    IF TG_OP = 'INSERT' THEN
        INSERT INTO coding_events (table_name, action, coder_id, record_id, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'insert', v_coder, v_record, NULL, to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO coding_events (table_name, action, coder_id, record_id, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'update', v_coder, v_record, to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO coding_events (table_name, action, coder_id, record_id, old_data, new_data)
        VALUES (TG_TABLE_NAME, 'delete', v_coder, v_record, to_jsonb(OLD), NULL);
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_coding_themes_audit ON coding_themes;
CREATE TRIGGER trg_coding_themes_audit
    AFTER INSERT OR UPDATE OR DELETE ON coding_themes
    FOR EACH ROW EXECUTE FUNCTION log_coding_event();

DROP TRIGGER IF EXISTS trg_coding_codes_audit ON coding_codes;
CREATE TRIGGER trg_coding_codes_audit
    AFTER INSERT OR UPDATE OR DELETE ON coding_codes
    FOR EACH ROW EXECUTE FUNCTION log_coding_event();

DROP TRIGGER IF EXISTS trg_coding_highlights_audit ON coding_highlights;
CREATE TRIGGER trg_coding_highlights_audit
    AFTER INSERT OR UPDATE OR DELETE ON coding_highlights
    FOR EACH ROW EXECUTE FUNCTION log_coding_event();

DROP TRIGGER IF EXISTS trg_coding_post_status_audit ON coding_post_status;
CREATE TRIGGER trg_coding_post_status_audit
    AFTER INSERT OR UPDATE OR DELETE ON coding_post_status
    FOR EACH ROW EXECUTE FUNCTION log_coding_event();
"""


class ReadableHTMLParser(HTMLParser):
    """Minimal stdlib HTML parser extracting page <title> and clean article paragraphs."""

    SKIP_TAGS = {"script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form"}
    BLOCK_TAGS = {"p", "h1", "h2", "h3", "h4", "li", "blockquote"}

    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.in_article = False
        self.current_tag: str | None = None
        self.current_buf: list[str] = []
        self.article_blocks: list[str] = []
        self.all_blocks: list[str] = []
        self.og_title: str | None = None
        self.og_desc: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        t = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if t == "meta":
            prop = attr_map.get("property", "").lower() or attr_map.get("name", "").lower()
            content = attr_map.get("content", "").strip()
            if prop in {"og:title", "twitter:title"} and content and not self.og_title:
                self.og_title = content
            elif prop in {"og:description", "description", "twitter:description"} and content and not self.og_desc:
                self.og_desc = content
        if t in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if t == "title":
            self.in_title = True
        if t == "article":
            self.in_article = True
        if self.skip_depth == 0 and t in self.BLOCK_TAGS:
            self._flush_block()
            self.current_tag = t

    def handle_endtag(self, tag: str):
        t = tag.lower()
        if t in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1
            return
        if t == "title":
            self.in_title = False
        if t == "article":
            self.in_article = False
        if t == self.current_tag:
            self._flush_block()
            self.current_tag = None

    def handle_data(self, data: str):
        if self.in_title:
            self.title_parts.append(data)
        elif self.skip_depth == 0 and self.current_tag:
            self.current_buf.append(data)

    def _flush_block(self):
        if not self.current_buf:
            return
        text = " ".join(html.unescape("".join(self.current_buf)).split())
        self.current_buf = []
        if len(text) < 35:
            return
        # Drop cookie/promo noise
        low = text.lower()
        if any(noise in low for noise in ("accept cookies", "cookie policy", "all rights reserved", "sign in to view more")):
            return
        if self.in_article:
            self.article_blocks.append(text)
        self.all_blocks.append(text)


def load_env_file() -> None:
    for base in (WORKTREE_ROOT, MAIN_REPO_ROOT):
        env_path = base / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def find_data_dir() -> Path:
    for base in (WORKTREE_ROOT, MAIN_REPO_ROOT):
        candidate = base / "data/local/linkedin-apify-2026-10-17"
        if (candidate / "apify_three_layer_2026-10-18.db").exists():
            return candidate
    raise SystemExit("Local data directory not found.")


def extract_urls_from_media(media_raw: str | None) -> tuple[list[tuple[str, str]], str | None]:
    """Return ([(kind, url), ...], article_title_if_any) from article/link/document media JSON."""
    if not media_raw:
        return [], None
    try:
        m = json.loads(media_raw)
    except Exception:
        return [], None
    if not isinstance(m, dict):
        return [], None
    found: list[tuple[str, str]] = []
    title_hint: str | None = None

    # Only inspect article / link / document keys (never video streams or image thumbnails)
    for key in ("article", "link", "document"):
        sub = m.get(key)
        if isinstance(sub, dict):
            if not title_hint and isinstance(sub.get("title"), str) and sub["title"].strip():
                title_hint = sub["title"].strip()
            for field in ("url", "link", "externalUrl"):
                val = sub.get(field)
                if isinstance(val, str) and val.startswith(("http://", "https://")):
                    if not any(s in val for s in SKIP_HOST_SUBSTRS):
                        found.append((key, val))
        elif isinstance(sub, str) and sub.startswith(("http://", "https://")):
            if not any(s in sub for s in SKIP_HOST_SUBSTRS):
                found.append((key, sub))

    # Some media records have a top-level external article link when type == 'article'
    if str(m.get("type") or "").lower() == "article":
        if not title_hint and isinstance(m.get("title"), str) and m["title"].strip():
            title_hint = m["title"].strip()
        for field in ("url", "link"):
            val = m.get(field)
            if isinstance(val, str) and val.startswith(("http://", "https://")):
                if not any(s in val for s in SKIP_HOST_SUBSTRS):
                    found.append(("article", val))

    return found, title_hint


def canonical_url_key(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    qs = urllib.parse.parse_qsl(p.query, keep_blank_values=False)
    filtered_qs = [(k, v) for k, v in qs if k.lower() not in {"trackingid", "trk", "utm_source", "utm_medium", "utm_campaign"}]
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/"), urllib.parse.urlencode(filtered_qs), ""))


def discover_external_links(post_row: dict) -> list[dict]:
    """Discover deduplicated external links / newsletters / articles for a post."""
    candidates: list[tuple[str, str]] = []
    for u in URL_RE.findall(post_row.get("post_text") or ""):
        u = u.rstrip(".,;:!?)")
        if not any(s in u for s in SKIP_HOST_SUBSTRS):
            candidates.append(("inline_url", u))
    if post_row.get("newsletter_url"):
        candidates.append(("newsletter", post_row["newsletter_url"].strip()))
    media_links, title_hint = extract_urls_from_media(post_row.get("media"))
    candidates.extend(media_links)

    deduped: list[dict] = []
    seen: set[str] = set()
    for kind, u in candidates:
        parsed = urllib.parse.urlsplit(u)
        if parsed.netloc.lower().endswith("linkedin.com") and any(
            parsed.path.startswith(p) for p in ("/in/", "/company/", "/school/", "/feed/", "/posts/")
        ):
            continue
        ckey = canonical_url_key(u)
        if ckey in seen:
            continue
        seen.add(ckey)
        deduped.append({
            "source_kind": kind,
            "original_url": u,
            "title_hint": post_row.get("newsletter_title") or title_hint,
        })
    return deduped


def curl_fetch(url: str) -> tuple[int | None, str, str, str]:
    """Fetch URL with system curl (macOS trust store). Returns (http_status, final_url, content_type, body)."""
    marker = "__CURL_META__"
    cmd = [
        "curl", "-sL", "--max-time", "12", "--max-filesize", "2000000",
        "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: en-US,en;q=0.9",
        "-w", f"\n{marker}%{{http_code}}\t%{{url_effective}}\t%{{content_type}}",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0 and not proc.stdout:
        return None, url, "", ""
    out = proc.stdout.decode("utf-8", errors="replace")
    idx = out.rfind(f"\n{marker}")
    if idx == -1:
        return None, url, "", out
    body = out[:idx]
    meta = out[idx + len(marker) + 1:].strip().split("\t")
    try:
        status = int(meta[0]) if meta and meta[0].isdigit() else None
    except Exception:
        status = None
    final_url = meta[1] if len(meta) > 1 and meta[1] else url
    ctype = (meta[2] if len(meta) > 2 else "").lower()
    return status, final_url, ctype, body


def fetch_external_source(item: dict) -> dict:
    url = item["original_url"]
    parsed_orig = urllib.parse.urlsplit(url)
    base_result = {
        "source_kind": item["source_kind"],
        "original_url": url,
        "resolved_url": url,
        "domain": parsed_orig.netloc.lower(),
        "title": item.get("title_hint") or "",
        "extracted_text": "",
        "extracted_chars": 0,
        "fetch_status": "failed",
        "http_status": None,
    }

    low_url = url.lower()
    if any(x in low_url for x in (".pdf", "youtube.com/", "youtu.be/", "vimeo.com/")):
        base_result["fetch_status"] = "pdf_or_media"
        return base_result

    status, final_url, ctype, body = curl_fetch(url)

    # Unwrap LinkedIn lnkd.in interstitial redirect page if present
    if "lnkd.in" in url.lower() and body:
        m = re.search(r'data-tracking-control-name="external_url_click"[^>]+href="(https?://[^"]+)"', body)
        if not m:
            m = re.search(r'<a[^>]+href="(https?://(?!www\.linkedin\.com|lnkd\.in)[^"]+)"[^>]*>[^<]*</a>', body)
        if m:
            ext_target = html.unescape(m.group(1))
            status, final_url, ctype, body = curl_fetch(ext_target)

    base_result["resolved_url"] = final_url
    base_result["domain"] = urllib.parse.urlsplit(final_url).netloc.lower()
    base_result["http_status"] = status

    if status is None:
        base_result["fetch_status"] = "failed"
        return base_result
    if "pdf" in ctype or final_url.lower().endswith(".pdf"):
        base_result["fetch_status"] = "pdf_or_media"
        return base_result
    if status in (401, 403) or any(x in final_url.lower() for x in ("linkedin.com/uas/login", "linkedin.com/authwall", "/login", "/signup")):
        base_result["fetch_status"] = "login_required"
        return base_result
    if status >= 400:
        base_result["fetch_status"] = "failed"
        return base_result
    if "html" not in ctype and "text" not in ctype and ctype:
        base_result["fetch_status"] = "pdf_or_media"
        return base_result

    low_body = body.lower()
    if any(h in low_body for h in CAPTCHA_HINTS):
        base_result["fetch_status"] = "login_required"
        return base_result

    parser = ReadableHTMLParser()
    try:
        parser.feed(body)
    except Exception:
        pass

    title = (parser.og_title or " ".join(parser.title_parts).strip() or item.get("title_hint") or "").strip()
    title = html.unescape(" ".join(title.split()))[:300]
    base_result["title"] = title

    blocks = parser.article_blocks if len("\n\n".join(parser.article_blocks)) >= 300 else parser.all_blocks
    dedup_blocks: list[str] = []
    seen_b: set[str] = set()
    for b in blocks:
        if b not in seen_b:
            seen_b.add(b)
            dedup_blocks.append(b)
    text = "\n\n".join(dedup_blocks)[:15000].strip()

    if any(h in low_body for h in PAYWALL_HINTS) and len(text) < 700:
        base_result["fetch_status"] = "paywalled"
        base_result["extracted_text"] = text or (parser.og_desc or "")
        base_result["extracted_chars"] = len(base_result["extracted_text"])
        return base_result

    if len(text) >= 220:
        base_result["fetch_status"] = "extracted"
        base_result["extracted_text"] = text
        base_result["extracted_chars"] = len(text)
    elif title or parser.og_desc:
        base_result["fetch_status"] = "metadata_only"
        base_result["extracted_text"] = (parser.og_desc or "").strip()
        base_result["extracted_chars"] = len(base_result["extracted_text"])
    else:
        base_result["fetch_status"] = "metadata_only"

    return base_result


def ensure_database(base_url: str) -> None:
    import psycopg

    with psycopg.connect(make_db_url(base_url, "neondb"), autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (CODING_DB,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{CODING_DB}"')
            print(f"Created Neon database {CODING_DB}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="Wipe existing coding data and reseed.")
    ap.add_argument("--skip-fetch", action="store_true", help="Skip HTTP extraction of external links.")
    args = ap.parse_args()

    load_env_file()
    base_url = os.environ.get("DATABASE_URL")
    if not base_url:
        raise SystemExit("DATABASE_URL not found in environment or .env.")

    data_dir = find_data_dir()
    manifest_path = data_dir / "coding_sample_50_2026-11-25/initial_coding_50_manifest.json"
    sqlite_path = data_dir / "apify_three_layer_2026-10-18.db"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sample_items = manifest["sample_posts"]
    sample_ids = {p["source_post_id"]: p for p in sample_items}

    conn_sq = sqlite3.connect(str(sqlite_path))
    conn_sq.row_factory = sqlite3.Row
    rows = conn_sq.execute(
        """
        SELECT source_post_id, posted_at, post_text, text_chars, author_type, author_name,
               author_headline, post_url, reactions, comments, shares,
               matched_query_codes, matched_families, newsletter_title, newsletter_url, media
        FROM master_posts
        """
    ).fetchall()
    conn_sq.close()

    by_id = {str(r["source_post_id"]): dict(r) for r in rows if str(r["source_post_id"]) in sample_ids}
    if len(by_id) != 50:
        raise SystemExit(f"Expected 50 sampled posts in SQLite, found {len(by_id)}")

    posts_payload = []
    external_rows = []
    status_counts: dict[str, int] = {}

    for meta in sample_items:
        pid = meta["source_post_id"]
        r = by_id[pid]
        links = discover_external_links(r)
        fetched_for_post = []
        if not args.skip_fetch:
            seen_resolved = set()
            for item in links:
                res = fetch_external_source(item)
                rkey = canonical_url_key(res["resolved_url"] or res["original_url"])
                if rkey in seen_resolved:
                    continue
                seen_resolved.add(rkey)
                fetched_for_post.append(res)
                status_counts[res["fetch_status"]] = status_counts.get(res["fetch_status"], 0) + 1
        else:
            for item in links:
                fetched_for_post.append({
                    "source_kind": item["source_kind"],
                    "original_url": item["original_url"],
                    "resolved_url": item["original_url"],
                    "domain": urllib.parse.urlsplit(item["original_url"]).netloc.lower(),
                    "title": item.get("title_hint") or "",
                    "extracted_text": "",
                    "extracted_chars": 0,
                    "fetch_status": "metadata_only",
                    "http_status": None,
                })

        has_ext = bool(fetched_for_post) or bool(r.get("newsletter_url")) or ("article" in (r.get("media") or "").lower())
        posts_payload.append((
            meta["sample_id"],
            pid,
            meta["reviewer_set"],
            meta["primary_family"],
            r.get("matched_families") or "",
            r.get("matched_query_codes") or "",
            (r.get("posted_at") or "")[:10],
            (r.get("post_text") or "").replace("\x00", ""),
            int(r.get("text_chars") or 0),
            r.get("author_type") or "",
            r.get("author_name") or "",
            r.get("author_headline") or "",
            r.get("post_url") or "",
            int(r.get("reactions") or 0),
            int(r.get("comments") or 0),
            int(r.get("shares") or 0),
            has_ext,
            len(fetched_for_post),
            r.get("newsletter_title") or "",
            r.get("newsletter_url") or "",
        ))
        for ext in fetched_for_post:
            external_rows.append((
                meta["sample_id"],
                ext["source_kind"],
                ext["original_url"],
                ext["resolved_url"],
                ext["domain"],
                ext["title"],
                ext["extracted_text"].replace("\x00", ""),
                ext["extracted_chars"],
                ext["fetch_status"],
                ext["http_status"],
            ))

    import psycopg

    ensure_database(base_url)
    coding_url = make_db_url(base_url, CODING_DB)

    with psycopg.connect(coding_url) as conn, conn.cursor() as cur:
        cur.execute(SCHEMA)
        cur.execute("SELECT count(*) FROM coding_highlights")
        n_hl = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM coding_codes")
        n_codes = cur.fetchone()[0]
        if (n_hl or n_codes) and not args.force:
            raise SystemExit(
                f"Existing coding data found ({n_codes} codes, {n_hl} highlights) in {CODING_DB}; refusing to reseed without --force."
            )

        cur.execute("DELETE FROM coding_external_sources")
        cur.execute("DELETE FROM coding_posts")
        cur.executemany(
            "INSERT INTO coders (id, name, name_en) VALUES (%s, %s, %s) "
            "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, name_en = EXCLUDED.name_en",
            CODERS,
        )
        cur.executemany(
            """
            INSERT INTO coding_posts (
                sample_id, source_post_id, reviewer_set, primary_family, matched_families,
                matched_query_codes, posted_at, post_text, text_chars, author_type, author_name,
                author_headline, post_url, reactions, comments, shares, has_external_link,
                external_url_count, newsletter_title, newsletter_url
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            posts_payload,
        )
        cur.executemany(
            """
            INSERT INTO coding_external_sources (
                sample_id, source_kind, original_url, resolved_url, domain,
                title, extracted_text, extracted_chars, fetch_status, http_status
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            external_rows,
        )
        conn.commit()

        cur.execute("SELECT count(*) FROM coding_posts")
        p_cnt = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM coding_posts WHERE has_external_link")
        ext_post_cnt = cur.fetchone()[0]
        cur.execute("SELECT fetch_status, count(*) FROM coding_external_sources GROUP BY fetch_status ORDER BY count(*) DESC")
        ext_breakdown = cur.fetchall()
        cur.execute(
            "SELECT c.relname, t.tgname FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid "
            "WHERE NOT t.tgisinternal AND c.relname LIKE 'coding_%' ORDER BY c.relname"
        )
        triggers = cur.fetchall()

    print(f"Seeded {p_cnt} posts into {CODING_DB} ({ext_post_cnt} flagged has_external_link).")
    print("External link extraction breakdown:", ext_breakdown)
    print("Audit triggers active:", triggers)


if __name__ == "__main__":
    main()
