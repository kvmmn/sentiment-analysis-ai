# LinkedIn Scraper — Legacy Exploratory Code

This is the legacy exploratory LinkedIn scraper used in Saintiment's pre-API-access trials, not an approved research pipeline. The LinkedIn DSA Researcher Access case remains **Open on last evidence (2026-08-28)**; no API approval or new collection permission is established here.

The folder moved intact from root `linkedin-scraper/` to `src/linkedin-scraper/`. Relocation did not modify or validate script behavior. No runtime execution, imports, dependency installation, or live collection was performed as part of this documentation repair. See the [project migration map](../../docs/project-map.md) and [code index](../README.md).

## Historical purpose

The initial trials explored public LinkedIn posts matching architecture + GenAI keywords to evaluate:

- Whether the keyword strategy retrieves relevant architectural discourse (not software architecture)
- What volume and quality of data is available via public search
- Whether the extraction pipeline captures the fields needed for sentiment analysis

These aims and the historical setup/usage notes below are not permission to repeat collection. Any future live run requires separately established permitted access, review, and an [experiment record](../../experiments/README.md). Offline synthetic tests must be planned separately from live collection.

## Historical prerequisites (not revalidated)

- Python 3.9+
- Google Chrome (used via Playwright's persistent context)
- A LinkedIn account (manual login in the opened browser)

## Historical setup and launch convention

The original setup used `pip install -r requirements.txt` and `playwright install chromium`. These are retained as historical reference, not instructions to install or collect now; the dependency constraints do not record an exact reproducible environment.

For any separately approved future run, the launch working directory (CWD) must be the script directory: `<project-root>/src/linkedin-scraper/`, not the repository root. The historical invocation is `python scraper.py` from that directory. This documents the legacy path convention without changing or validating the implementation.

The legacy flow reads `keywords.txt` (one phrase per line, `#` comments ignored), opens a persistent Chrome context for manual login, searches and scrolls results, and writes `linkedin_posts.db` and `linkedin_posts.csv`. Do not initiate that flow merely because the folder was relocated.

## Historical configuration (not revalidated)

The original guide documented these settings in the `CONFIG` section of `scraper.py`; this table is not a new verification of the implementation:

| Setting                 | Default | Description                                                     |
| ----------------------- | ------- | --------------------------------------------------------------- |
| `MAX_POSTS_PER_KEYWORD` | 30      | Stop after this many unique posts per keyword                   |
| `MAX_SCROLLS`           | 35      | Maximum scroll attempts per keyword                             |
| `HEADLESS`              | `False` | Set to `True` for headless mode (requires pre-existing session) |
| `INITIAL_WAIT_MS`       | 7000    | Wait after opening search page                                  |
| `SCROLL_WAIT_MS`        | 2200    | Wait between scrolls                                            |

## Legacy runtime and output locations

Runtime artifacts are retained beside `scraper.py` under `src/linkedin-scraper/` as a **documented legacy exception** to the [planned data layout](../../data/README.md). This includes the session profile, DB, CSV, logs, and debug files when present. They were not migrated to `data/local/`, and their presence does not establish an approved dataset or permission to reuse personal data. No new runtime artifacts are created by this documentation change.

| File                 | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `linkedin_posts.db`  | SQLite database (git-ignored)                                     |
| `linkedin_posts.csv` | CSV export (git-ignored since 2026-09-10: contains personal data) |
| `linkedin_session/`  | Persistent browser profile and cookies (git-ignored)              |
| `scraper.log`        | Execution log (git-ignored)                                       |
| `debug/`             | Screenshots on errors (git-ignored)                               |

### CSV Fields

`post_key`, `keyword`, `author`, `author_url`, `author_headline`, `connection_degree`, `posted_relative`, `is_edited`, `url`, `post_type`, `text`, `hashtags`, `mentions`, `reactions`, `comments`, `reposts`, `engagement_total`, `image_count`, `video_count`, `has_image`, `has_video`, `collected_at`

## Security

- **Never commit `linkedin_session/`** — it contains your LinkedIn cookies. It is git-ignored.
- The CSV contains personal data. Do not commit or publish it; share only reviewed, permitted aggregates.
- Do not commit the SQLite database or log files.

## Limitations

- Only retrieves posts visible via LinkedIn's public content search
- Text extraction may be truncated for long posts (shows `… more`)
- No comment retrieval
- Keyword `"future of architects"` retrieves significant software-architecture noise
- `posted_relative` extraction is unreliable for some post formats

## Status

Legacy exploratory code, moved intact and not revalidated during relocation. Not a production data pipeline or an approved research dataset. Any future changes, tests, or collection require a separate task and provenance record; no new collection is permitted by this guide.
