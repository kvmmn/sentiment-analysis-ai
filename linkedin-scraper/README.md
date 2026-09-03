# LinkedIn Scraper

Initial experimental scraper for collecting LinkedIn posts as part of the Saintiment project's discourse analysis. This is a **pre-API-access trial** — the LinkedIn DSA Researcher Access case remains **Open** and no API approval has been granted.

## Purpose

Collect public LinkedIn posts matching architecture + GenAI keywords to evaluate:

- Whether the keyword strategy retrieves relevant architectural discourse (not software architecture)
- What volume and quality of data is available via public search
- Whether the extraction pipeline captures the fields needed for sentiment analysis

## Prerequisites

- Python 3.9+
- Google Chrome (used via Playwright's persistent context)
- A LinkedIn account (manual login in the opened browser)

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

1. Edit `keywords.txt` — one keyword phrase per line. Lines starting with `#` are ignored.
2. Run the scraper:

```bash
python scraper.py
```

3. A Chrome window opens. Log in to LinkedIn manually if not already authenticated.
4. The scraper searches each keyword, scrolls through results, and extracts posts.
5. Output: `linkedin_posts.db` (SQLite) and `linkedin_posts.csv` (export).

## Configuration

Edit the `CONFIG` section in `scraper.py`:

| Setting                 | Default | Description                                                     |
| ----------------------- | ------- | --------------------------------------------------------------- |
| `MAX_POSTS_PER_KEYWORD` | 30      | Stop after this many unique posts per keyword                   |
| `MAX_SCROLLS`           | 35      | Maximum scroll attempts per keyword                             |
| `HEADLESS`              | `False` | Set to `True` for headless mode (requires pre-existing session) |
| `INITIAL_WAIT_MS`       | 7000    | Wait after opening search page                                  |
| `SCROLL_WAIT_MS`        | 2200    | Wait between scrolls                                            |

## Output

| File                 | Description                         |
| -------------------- | ----------------------------------- |
| `linkedin_posts.db`  | SQLite database (git-ignored)       |
| `linkedin_posts.csv` | CSV export for sharing and analysis |
| `scraper.log`        | Execution log (git-ignored)         |
| `debug/`             | Screenshots on errors (git-ignored) |

### CSV Fields

`post_key`, `keyword`, `author`, `author_url`, `author_headline`, `connection_degree`, `posted_relative`, `is_edited`, `url`, `post_type`, `text`, `hashtags`, `mentions`, `reactions`, `comments`, `reposts`, `engagement_total`, `image_count`, `video_count`, `has_image`, `has_video`, `collected_at`

## Security

- **Never commit `linkedin_session/`** — it contains your LinkedIn cookies. It is git-ignored.
- The CSV contains public post text and author names. Review before sharing.
- Do not commit the SQLite database or log files.

## Limitations

- Only retrieves posts visible via LinkedIn's public content search
- Text extraction may be truncated for long posts (shows `… more`)
- No comment retrieval
- Keyword `"future of architects"` retrieves significant software-architecture noise
- `posted_relative` extraction is unreliable for some post formats

## Status

Experimental — part of the initial data exploration phase. Not a production data pipeline. The keyword list, extraction logic, and storage format will evolve as the research design matures.
