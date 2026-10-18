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
Neon contents (Apify portion of the multi-provider DB): run `tKJavW6tIKBOP7NlO`, queries 105, raw_items 1,486, master_posts 1,137, post_query_hits 1,486. Full DB as of 2026-10-16 also holds Coresignal and Bright Data (see below); Apify counts re-verified by SQL on 2026-10-16
Apify retention: 7-day dataset retention; as of 2026-10-16 the Apify dataset is expected to have expired (~2026-10-14); Neon `raw_items` for this run is the durable copy
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

The Neon schema (tables `runs`, `queries`, `raw_items`, `master_posts`, `post_query_hits`) was written from the Apify load and reused for later providers; connection details are never recorded in git.

### Apify LinkedIn post search, 48 three-layer queries (2026-10-18)

Provider collection using the finalized 55-keyword, 48-query three-layer set (`research/keywords/linkedin-apify-2026-10-17/`). See [project log section 51](../research/project-log.md#51-apify-48-query-three-layer-run-executed-and-loaded-into-neon-2026-10-18). Contains personal data (author names, headlines, profile URLs, post text); none of it is in git.

```text
Dataset name / ID: apify-linkedin-post-search-2026-10-18 (Apify dataset WUsK3RRYo7nKEOUbA)
Origin / provider: Apify actor harvestapi/linkedin-post-search (actor ID buIWk2uOUzTmcLsuB, build 9BWuRUTT3NouYMxcU), run X2gdX05u8rP41b4rG
Source URL: LinkedIn post search, as scraped by the actor
License and access conditions: TODO (ethics/ToS review open)
Permitted use and redistribution: TODO (do not share outside the team)
Version / release / retrieval date: 2026-10-18, run 17:49:12.622Z to 17:53:47.096Z UTC (~274.5 s)
Query provenance: 48 three-layer queries (Domain/Tools ∧ AI ∧ Skill/Cognition/Process/Education, <= 5 Boolean operators per query); see research/keywords/linkedin-apify-2026-10-17/queries.json (SHA-256 01eeb4346725f17e09f81c19e6121c0394408ea792bf66dd338f7f1eb832f0a4)
Local raw/derived artifact paths: data/local/linkedin-apify-2026-10-17/apify_raw/WUsK3RRYo7nKEOUbA.jsonl (2,158 lines, 9,778,702 bytes, SHA-256 e68471e3d0b4a7031221dfd2d666f67a37862d575d190d4a184df8daa4d5c47c) and data/local/linkedin-apify-2026-10-17/master_posts_apify_2026-10-18.csv (3,354 total master_posts rows across all providers, 10,194,385 bytes, SHA-256 56dbfa361a661c89a0afc699c01b493ef4fc98f6e56bc1ab88fc4d2bb89844e3); git-ignored
Durable copy: Neon Postgres, project cool-cake-91875024 (_saintimental), database _saintiment_db
Neon contents: run `X2gdX05u8rP41b4rG`, queries 48, raw_items 2,158, post_query_hits 2,158; 1,858 unique posts in this run (1,817 net-new unique Apify posts added to the 1,137 from 2026-10-07, bringing Apify master_posts to 2,954 and total master_posts across Apify + Coresignal + Bright Data to 3,354)
Processing code commit and scripts: src/ingest/apify_to_neon.py (updated with 250-item batched executemany), src/ingest/export_master_csv.py
Environment/interpreter: .venv/bin/python (Python 3.13, psycopg 3.3.6)
Contents and labels: 2,158 result items across all 48 queries (48/48 queries returned >= 10 posts; 37/48 queries hit the maxPosts=50 cap; min 10, median 50, max 50); 1,858 unique post IDs; post dates 2023-01-10 to 2026-10-18
Cost: USD 4.31605 (2,158 post events at USD 0.002 + start event USD 0.00005), covered by the FREE plan monthly allowance
```

### Coresignal Employee Posts collect (2026-10-08)

Provider test collection, not an approved research corpus. See [project log section 45](../research/project-log.md#45-coresignal-employee-posts-200-collect-2026-10-08). Personal data; none in git.

```text
Dataset name / ID: coresignal-employee-posts-2026-10-08-200
Origin / provider: Coresignal Employee Posts API (ES DSL search + collect-by-ID)
Source URL: LinkedIn employee posts, as returned by Coresignal
License and access conditions: TODO (not reviewed)
Permitted use and redistribution: TODO (do not share outside the team)
Version / release / retrieval date: 2026-10-08
Query provenance: narrower three-block Boolean on article_body (architectural|architects) ∧ (generative AI|ChatGPT|Midjourney|GenAI) ∧ (skills|deskilling|critical thinking|role of the architect); 9,550 IDs searched; first 200 collected
Local raw/derived artifact paths: _local/work/2026-10-08-coresignal-posts/ (git-ignored)
Durable copy: Neon _saintiment_db, run coresignal-employee-posts-2026-10-08-200; master_posts 200, raw_items 200 (verified SQL 2026-10-16)
Cost: 200 collect credits (trial balance 1,960 → 1,760); search free
Known limitations: not the full 105-subquery Apify frame; author_headline empty on all 200; no relevance coding
```

### Bright Data Marketplace LinkedIn posts filter (2026-10-08)

Provider test collection, not an approved research corpus. See [project log section 46](../research/project-log.md#46-bright-data-marketplace-filter-200-posts-2026-10-08). Personal data; none in git.

```text
Dataset name / ID: brightdata-marketplace-posts-2026-10-08-200 (snapshot snap_mv00q3kw1p5pkzceb2)
Origin / provider: Bright Data Marketplace filter on LinkedIn posts dataset gd_lyy3tktm25m4avu764
Source URL: pre-collected LinkedIn posts filtered by post_text includes
License and access conditions: TODO (not reviewed)
Permitted use and redistribution: TODO (do not share outside the team)
Version / release / retrieval date: 2026-10-08
Query provenance: tighter three-block includes (no bare AI / bare architecture); input recorded locally under _local/work/2026-10-08-brightdata/scraper/filter-200-input.json
Local raw/derived artifact paths: _local/work/2026-10-08-brightdata/ (git-ignored)
Durable copy: Neon _saintiment_db, run brightdata-marketplace-posts-2026-10-08-200; master_posts 200, raw_items 200 (verified SQL 2026-10-16)
Cost: snapshot status reported 0; list price noted USD 2.50 / 1,000 returned records
Known limitations: Marketplace corpus ≠ live keyword search; profile/scraper/browser paths tested and not kept as the comparison sample
```

### Three-source review pack (2026-10-09)

Local-only comparison extracts (200 posts per source). See [project log section 47](../research/project-log.md#47-three-source-review-pack-of-200-posts-each-2026-10-09). Paths: `_local/work/2026-10-09-review-sheets/` and `_local/work/2026-10-09-review-complete/`. Not in git.

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
