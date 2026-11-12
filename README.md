# Saintiment

Shared research project for a scientific article and a master's thesis. Both outputs use the same research notes, code, data documentation, and experiment records.

Kaveh intends to use this research in his master's dissertation at **Arden University**. That integration is not finalized. This repository does not claim university approval, sponsorship, or responsibility for the research.

Project and LinkedIn app display name: **Saintiment**, chosen by Kaveh on 2026-08-28. Earlier names **Sentiment AI** and **GenAI Architecture Discourse Research** stay in historical records. The repository URL and the local folder name are unchanged.

Shared reference: [kvmmn/sentiment-analysis-ai](https://github.com/kvmmn/sentiment-analysis-ai).

## Team

- [Iman Sheikhansari](https://www.linkedin.com/in/imansheikhansari/)
- [Morteza Hazbei](https://www.linkedin.com/in/morteza-hazbei/)
- [Kaveh Momeni](https://linkedin.com/in/kvmmn)

Roles, publication author order, and thesis authorship are not specified.

Project and privacy contact: Kaveh Momeni — [kaveh.momeni@gmail.com](mailto:kaveh.momeni@gmail.com) is his confirmed primary contact; [25199053@ardenuniversity.ac.uk](mailto:25199053@ardenuniversity.ac.uk) is an additional contact. Kaveh supplied both for publication. Other members' email addresses will be added when provided and authorized. An email address does not establish institutional sponsorship.

The Telegram group **Sentiment Analysis AI** is the team's main communication channel for now.

## Review the posts

The hosted team app is [https://saintiment.vercel.app/](https://saintiment.vercel.app/). Sign in with the shared team password. Each person reviews an assigned share of the 1,858 Apify posts and marks keep or reject. Decisions are stored in Neon `_saintiment_swipe_team_db`.

Kept posts, one at a time, with a filter for who kept the post: [https://saintiment.vercel.app/kept](https://saintiment.vercel.app/kept). The download from that page is `saintiment_kept_posts.json` for the current filter. It contains post fields and does not include who selected the post.

How the app is built: [web/swipe/README.md](web/swipe/README.md). Post text stays in Neon, not in this public repository.

The HTML page [docs/swipe-review.html](docs/swipe-review.html) is a separate local review screen. It is not the Vercel app. As of the database read on 12 November 2026, its Neon table `curation_decisions` on `_saintiment_apify_three_layer_db` had **0 rows**. The keep/reject counts below are from the team app database, not from that local screen.

## Screening counts

Read on **12 November 2026** from Neon project `cool-cake-91875024`, database `_saintiment_swipe_team_db`. Counts only; no post text was read. Every assigned post had one decision. The latest `decided_at` in that table was **2026-11-12 16:48 UTC**. `decided_by` matched the assigned reviewer on every row.

| | Posts | Keep | Reject |
| --- | ---: | ---: | ---: |
| All three reviewers | 1,858 | 471 | 1,387 |
| Morteza (stored name مرتضی, reviewer 1) | 620 | 130 | 490 |
| Iman (stored name ایمان, reviewer 2) | 619 | 167 | 452 |
| Kaveh (stored name کاوه, reviewer 3) | 619 | 174 | 445 |

These marks are the team's keep/reject screening. They are not a finished relevance codebook, and they are not a scientific finding. An earlier read of the same totals is in [project log §55](research/project-log.md#55-kept-posts-link-moved-to-the-bottom-of-the-sets-screen-2026-11-12). This README uses the 12 November read above.

## Queries

The complete reading guide, the prose-number to Q-ID map, and the per-query hit counts are in **[research/keywords/README.md](research/keywords/README.md)**. Boolean strings are not copied into this page.

### How to read a query file

- **Q01–Q48** are the `id` values in [`queries.json`](research/keywords/linkedin-apify-2026-10-17/queries.json), in that array order. `searchQueries` is the same 48 strings in the same order, without family or operator fields. Use `queries[]` when the family matters.
- [`keywords-and-queries.md`](research/keywords/linkedin-apify-2026-10-17/keywords-and-queries.md) contains the same 48 strings, grouped by family. Its numbers 1–48 follow that grouped order. Number 13 in that file is **not** Q13. The map is in [`queries.md`](research/keywords/linkedin-apify-2026-10-17/queries.md).
- A quoted term is stored with the quote characters included, for example `"generative AI"`.
- `post_filters_not_in_the_query` was not part of the executed Boolean string.
- The JSON field `status` still says no run was started in that commit, and the key `recommended_actor_input_not_executed` still has that name. [Project log §51](research/project-log.md#51-apify-48-query-three-layer-run-executed-and-loaded-into-neon-2026-10-18) records that this list was executed on 18 October 2026 with `maxPosts` 50, `postedLimitDate` `2022-11-30`, and `sortBy` `date`. The exports below copy those fields as stored.
- The 7 October file is a JSON array of strings. It has no ids. A number in its Markdown or Word file is 1-based file order only.

### Executed list: 48 three-layer queries (18 October 2026)

This is the list behind the 1,858-post screening set. Run `X2gdX05u8rP41b4rG`, dataset `WUsK3RRYo7nKEOUbA`. On 12 November 2026, `_saintiment_apify_three_layer_db` still had 48 `queries`, 2,158 `raw_items`, and 1,858 `master_posts`.

| Format | File |
| --- | --- |
| JSON | [queries.json](research/keywords/linkedin-apify-2026-10-17/queries.json) |
| Markdown, Q-ID order | [queries.md](research/keywords/linkedin-apify-2026-10-17/queries.md) |
| Markdown, family groups | [keywords-and-queries.md](research/keywords/linkedin-apify-2026-10-17/keywords-and-queries.md) |
| YAML | [queries.yaml](research/keywords/linkedin-apify-2026-10-17/queries.yaml) |
| Word | [queries.docx](research/keywords/linkedin-apify-2026-10-17/queries.docx) |

On GitHub, open the file and use Raw or Download. These paths are the files in the repository; there is no separate download app.

YAML, `queries.md`, and the Word file were generated from `queries.json` on 12 November 2026. A check with a local YAML parser loaded the YAML back to the same JSON object. The Word file contains every Q ID and every Boolean string. No query was added. The Word file was written with Python's standard library, not a new project dependency.

### Keywords in that executed list (55)

The 55 terms are the `keywords` object in `queries.json`, the same terms as section 1 of `keywords-and-queries.md`. The 12 post-filters are in the same downloads, under `post_filters_not_in_the_query`. They were not part of the Boolean strings. No term was added.

| Format | File |
| --- | --- |
| JSON | [keywords.json](research/keywords/linkedin-apify-2026-10-17/keywords.json) |
| Markdown | [keywords.md](research/keywords/linkedin-apify-2026-10-17/keywords.md) |
| YAML | [keywords.yaml](research/keywords/linkedin-apify-2026-10-17/keywords.yaml) |
| Word | [keywords.docx](research/keywords/linkedin-apify-2026-10-17/keywords.docx) |

`keywords.yaml` loads back to the same JSON object as `keywords.json`. The Word file lists every term in those groups and every post-filter. Python's standard library wrote the Word file.

Family totals from `queries.raw_hits_count` and distinct `post_query_hits.post_id`, same database read. Distinct posts overlap across families, so the last column does not sum to 1,858.

| Family | Queries | Raw hits | Distinct posts |
| --- | ---: | ---: | ---: |
| direct | 16 | 602 | 544 |
| cognition | 16 | 756 | 681 |
| process | 12 | 600 | 538 |
| technical_and_pedagogy | 4 | 200 | 190 |
| All | 48 | 2,158 | 1,858 |

1,618 posts matched one query code and 240 matched more than one. For each single Q ID, the distinct-post count equalled `raw_hits_count`. Thirty-seven queries are at the cap of 50; eleven are below it (Q07 13, Q08 11, Q10 34, Q11 14, Q12 10, Q20 47, Q23 30, Q24 37, Q36 32, Q37 38, Q40 42). The full Q-ID table is in the [query index](research/keywords/README.md#hit-counts).

[docs/index.html](docs/index.html) prints different family raw-hit cells (686, 732, 540, 200). Its distinct-post cells match the table above. Use the Neon figures in this README for raw hits. That HTML page also links to `docs/layer2-query-decision-2026-10-16.html`, which is **not in this repository**. TODO: the 16 October note, if the team still has it.

### Earlier executed list: 105 sub-queries (7 October 2026)

This is the decomposition used for Apify run `tKJavW6tIKBOP7NlO` (1,486 raw items, 1,137 unique posts in [project log §42](research/project-log.md#42-apify-full-run-downloaded-and-loaded-into-neon-2026-10-07)). It is not the list behind the 1,858-post screening set, and it is not Version A or Version B.

| Format | File |
| --- | --- |
| JSON | [subqueries.json](research/keywords/linkedin-boolean-2026-10-07/subqueries.json) |
| Markdown | [subqueries.md](research/keywords/linkedin-boolean-2026-10-07/subqueries.md) |
| YAML | [subqueries.yaml](research/keywords/linkedin-boolean-2026-10-07/subqueries.yaml) |
| Word | [subqueries.docx](research/keywords/linkedin-boolean-2026-10-07/subqueries.docx) |

Markdown, YAML, and Word were generated from `subqueries.json` on 12 November 2026. The YAML loads back to the same 105 strings. Recomputed from those strings, each has 3–5 `AND` / `OR` / `NOT` operators.

The three term lists that `decompose.py` multiplies into those 105 strings are separate downloads. Counts in the source: domain 10, AI 5, labor/competency 13. No term was added.

| Format | File |
| --- | --- |
| JSON | [term-blocks.json](research/keywords/linkedin-boolean-2026-10-07/term-blocks.json) |
| Markdown | [term-blocks.md](research/keywords/linkedin-boolean-2026-10-07/term-blocks.md) |
| YAML | [term-blocks.yaml](research/keywords/linkedin-boolean-2026-10-07/term-blocks.yaml) |
| Word | [term-blocks.docx](research/keywords/linkedin-boolean-2026-10-07/term-blocks.docx) |

### Version A (19) and Version B (85)

The team has not yet decided these lists. They are **not in this repository**, so this page does not link a download for them.

- **Version A, 19 sub-queries.** [Project log §49](research/project-log.md#49-apify-query-list-for-the-next-round-2026-10-17) says a file referred to as the 19 option-A queries was not in the repository and was not found in Drive. `build_queries.py` on this branch writes only the 48 three-layer queries. Commit `4d14c48` is not on `main`. It is on `cursor/apify-query-round-c795` (tip `ce2e6f0`), whose README calls its 19 option-A strings a reconstruction because the original file was missing. Those strings are Q37–Q55 with tier `tier2_two_layer` on that branch only. They are not copied here, and they are not relabeled as the missing 16 October file. `subqueries_version_a.json` is still absent. TODO: the original 19 strings, when the team supplies the file.
- **Version B, 85 queries.** No file on any branch is named `subqueries_version_b.json`. No project-log entry in this repository names an 85-query list. TODO.

Query version 1 is not frozen.

## Collected posts

Not an approved research corpus. Ethics and terms of use are still open. No scientific finding is claimed from these loads.

| Database | What was re-read on 12 November 2026 |
| --- | --- |
| `_saintiment_apify_three_layer_db` | 1,858 `master_posts`, 2,158 `raw_items`, 48 `queries`, 0 `curation_decisions` |
| `_saintiment_db` | 3,354 `master_posts` (Apify 2,954, Coresignal 200, Bright Data 200), 4,044 `raw_items` |
| `_saintiment_swipe_team_db` | 1,858 posts, 471 keep, 1,387 reject |

The 18 October run record, costs, and file hashes remain in [project log §51](research/project-log.md#51-apify-48-query-three-layer-run-executed-and-loaded-into-neon-2026-10-18) and [data/README.md](data/README.md). Post text and author names are not in git.

## Earlier records

The September pilot numbers, including the Run 013 analysis of 1,076 posts, stay in the meeting documents. They are not restated here.

- [Research index](research/README.md)
- [Project log](research/project-log.md)
- [25 September meeting guide](docs/team-meeting-guide-2026-09-25.html)
- [25 September technical benchmark](docs/team-meeting-analysis-2026-09-25.html)
- [Methodology draft](docs/kaveh-independent-methodology.md)
- [Code index](src/README.md), including [Iman's local submission](src/README.md#imans-submission-local-only)
- [Experiment workflow](experiments/README.md) and [live-pilot plan](experiments/2026-09-17-iman-live-pilot.md)
- [15 September team letter](research/team/team-feedback-to-team-2026-09-15-FA.md)
- Keyword-instrument downloads (literature strings, discourse catalog, lexicon, legacy scraper phrases) are linked from the [research index](research/README.md#historical-keyword-instruments--august-proposals). The lists are not copied onto this page. The annotation codebook stays in the local submission and is not in this public repository, so it has no download here.

## Where files belong

| Location | Purpose |
| --- | --- |
| [Project map](docs/project-map.md) | Locations, provenance, relocation map |
| [Query index](research/keywords/README.md) | How to read query files, downloads, hit counts |
| [Research](research/README.md) | Questions, keywords, access, correspondence |
| [Code](src/README.md) | Shared code and local-only submissions |
| [Experiments](experiments/README.md) | Plans and run records |
| [Data](data/README.md) | Dataset registry; private rows stay local |
| [Article](writing/article.md) / [Thesis](writing/thesis.md) | Separate writing outputs |
| [Swipe app](web/swipe/README.md) | Vercel review app |
| [Project log](research/project-log.md) | Dated decisions and verification |
| [Working principles](AGENTS.md) / [Privacy policy](PRIVACY.md) | Collaboration rules and public notice |

## Open

1. Decide what the 471 kept posts are for. The screening marks are recorded; a relevance protocol is not.
2. Supply Version A (19) and Version B (85) if those lists are still wanted. They cannot be exported until the strings are in the repository.
3. Keep query version 1 unfrozen until the team says otherwise.
4. Ethics and terms of use before treating any pull as a research corpus. LinkedIn access approval is not established on the last recorded evidence.
5. Article, thesis, university requirements, and publication venue remain open.

## Working format

Plain Markdown. Add a tool only when the task needs it. One evidence base for both writing outputs. Relative links.

GitHub is the shared reference for publishable work. Commit completed changes and report a sync failure. No background synchronization service is configured.

Local dataset contents and common credential files are excluded by `.gitignore`. Ignore rules do not detect every secret. Personal research data and credentials do not belong in this public repository.
