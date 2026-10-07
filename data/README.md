# Data

No approved research dataset has been established. Historic exploratory LinkedIn data exists locally under `src/linkedin-scraper/` and is git-ignored; it is not an approved research corpus. See the [legacy scraper guide](../src/linkedin-scraper/README.md). This directory is reserved for local data; its contents are ignored by version control except for this guide.

## Planned storage convention

- Dataset versions: `data/local/<dataset-id>/<version>/`, with separate `raw/` and `derived/` subdirectories. Preserve original inputs; record transformations and exact versions separately.
- Per-experiment outputs: `data/local/experiments/<id>/`, linked from the corresponding [experiment record](../experiments/README.md).
- These are planned paths, not directories or datasets created by this documentation change. Legacy scraper runtime artifacts remain beside the script as a documented exception; no data is moved here.

The earlier raw-layout proposal (`data/local/raw/{platform}/{batch_id}/`), item schema, and retention discussion remain in [keywords-search-storage.md](../research/keywords/keywords-search-storage.md). Use the versioned convention above for new plans; neither document authorizes collection or establishes a retention entitlement. See the [project migration map](../docs/project-map.md) for relocated files.

Record each dataset below when selected. Keep only non-sensitive metadata here. Confirm permitted access, use, and sharing before acquiring data. Never place credentials or personal records in this document.

## Recorded datasets

### Apify LinkedIn post search, 105 sub-queries (2026-10-07)

Provider test collection, not an approved research corpus. No permission, ethics or terms-of-service review is recorded (see [project log section 40](../research/project-log.md#40-provider-pilot-apify-small-tests-and-boolean-query-limit-2026-10-07)). Contains personal data (author names, headlines, profile URLs, post text); none of it is in git.

```text
Dataset name / ID: apify-linkedin-post-search-2026-10-07 (Apify dataset XeYe0ReCWPpyZpG91)
Origin / provider: Apify actor harvestapi/linkedin-post-search (actor ID buIWk2uOUzTmcLsuB, build 0.0.114), run tKJavW6tIKBOP7NlO, started via MCP
Source URL: LinkedIn post search, as scraped by the actor
License and access conditions: TODO (not reviewed; the provider-comparison page notes LinkedIn terms do not permit scraping)
Permitted use and redistribution: TODO (undecided; do not share outside the team)
Version / release / retrieval date: 2026-10-07, run 14:04:12 to 14:11:14 UTC (about 421 s on 256 MB)
Query provenance: 105 sub-queries of the agreed three-block Boolean query; see research/keywords/linkedin-boolean-2026-10-07/ (decompose.py generates subqueries.json; each sub-query has at most 5 AND/OR/NOT operators; together they cover all 10 x 5 x 13 = 650 term triples)
Local raw/derived artifact paths: data/local/linkedin-boolean-2026-10-07/apify_raw/XeYe0ReCWPpyZpG91.jsonl (1,486 lines, 6.6 MB) and master_posts_apify.csv (1,137 rows); git-ignored and present only on the cloud-agent VM that ran the work, not backed up elsewhere
Durable copy: Neon Postgres, project cool-cake-91875024 (_saintimental), database _saintiment_db (branch production, AWS eu-central-1, Postgres 18, free plan)
Neon contents: runs 1, queries 105, raw_items 1,486, master_posts 1,137, post_query_hits 1,486; about 18 MB; counts checked by SQL against the local JSONL
Apify retention: the account's data retention is 7 days, so the Apify dataset is expected to be deleted around 2026-10-14 (not confirmed in the console); the Neon raw_items payloads are the durable copy
Acquisition steps (without credentials): run the actor once with the 105 sub-queries; read dataset pages of 25-50 items through the Apify API; load with src/ingest/apify_to_neon.py using DATABASE_URL from the environment
Source/input SHA-256 and artifact paths: TODO (not computed)
Derived/output SHA-256 and artifact paths: TODO (not computed)
Processing code commit, source-file SHA-256, and experiment record: src/ingest/apify_to_neon.py, src/ingest/export_master_csv.py (commit in PR #8); no experiment record
Environment/interpreter and exact dependency versions: Python 3.12, psycopg 3 (binary); exact versions not recorded
Contents and labels: 1,486 result items (all type post; 1,388 profile authors, 98 company authors); 1,137 unique post IDs; 218 posts returned by more than one sub-query; post dates 2022-12-28 to 2026-10-07; 10 items with empty text; no labels
Cost: 1,486 post events at USD 0.002 + one start event at USD 0.00005 = USD 2.97205 (run usage); Apify monthly usage reported 3.19 of a 5 USD cap on 2026-10-07 (cycle ends 2026-10-10)
Privacy or ethical considerations: personal data of named individuals; keep out of git and shared documents; Sheets export deferred
Preprocessing and split definitions: none beyond NUL-character removal at load time (one payload contained NUL, which Postgres cannot store); no splits
Known limitations: 93 of 105 sub-queries returned exactly 15 posts, so the pull is probably capped and not a census; relevance to architecture not assessed; engagement counts are a snapshot at scrape time; no reactions or comments collected; some author headlines are follower counts rather than job titles (seen in the earlier pilot)
```

The Neon schema (tables `runs`, `queries`, `raw_items`, `master_posts`, `post_query_hits`) was written from this one dataset and may change; connection details are never recorded in git.

## Dataset Template

```text
Dataset name / ID: TODO
Origin / provider: TODO
Source URL: TODO
License and access conditions: TODO
Permitted use and redistribution: TODO
Version / release / retrieval date: TODO
Local raw/derived artifact paths: TODO (data/local/<dataset-id>/<version>/)
Acquisition steps (without credentials): TODO
Source/input SHA-256 and artifact paths: TODO
Derived/output SHA-256 and artifact paths: TODO
Processing code commit, source-file SHA-256, and experiment record: TODO
Environment/interpreter and exact dependency versions: TODO
Contents and labels: TODO
Privacy or ethical considerations: TODO
Preprocessing and split definitions: TODO
Known limitations: TODO
```

Reference the dataset ID and exact version in [experiment records](../experiments/README.md). Document transformations separately from original data so results can be reproduced.
