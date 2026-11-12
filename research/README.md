# Saintiment research index

Updated: 2026-11-12. This index separates the current working method from historical proposals and source evidence. It does not authorize collection or freeze queries.

## Current working method

- **Working frame adopted 2026-09-10:** Domain ∧ Technology ∧ Labor/Competency, using Iman’s three-pillar search for the review pass. See the dated decision in [keyword systems](keywords/keyword-systems.md) and [research notes](notes.md#decisions).
- **Apify three-layer keyword and query list (finalized & executed 2026-10-18):** 55 keywords across 3 layers and 48 executable three-layer LinkedIn queries (`<= 5` operators). Run `X2gdX05u8rP41b4rG` (dataset `WUsK3RRYo7nKEOUbA`) collected 2,158 raw items (1,858 unique posts; 48/48 queries returning results) and loaded them into Neon `_saintiment_db` (now 2,954 Apify `master_posts`, 3,354 total across providers). See [the round note](keywords/linkedin-apify-2026-10-17/README.md), [clean shareable list](keywords/linkedin-apify-2026-10-17/keywords-and-queries.md), and [project log §51](project-log.md#51-apify-48-query-three-layer-run-executed-and-loaded-into-neon-2026-10-18).
- **Query index (2026-11-12):** [keywords/README.md](keywords/README.md) is the reading guide for the executed 48 and the 7 October 105, with JSON, Markdown, YAML, and Word downloads generated from those JSON files. Version A (19) and Version B (85) are not in the repository. Screening counts re-read the same day are on the [root README](../README.md#screening-counts).
- **Three-provider LinkedIn pilot (2026-10-07–09), synced 2026-10-16:** Apify 1,137 + Coresignal 200 + Bright Data 200 master posts in Neon; local 200-per-source review packs. See [project log §48](project-log.md#48-complete-three-provider-set-synced-2026-10-16) and [data README](../data/README.md). Not an approved corpus; ethics/ToS still open.
- **Pilot analysis & independent methodology (2026-09-25):** completed pilot on Run 013 (1,076 posts); see [team meeting guide](../docs/team-meeting-guide-2026-09-25.html), [technical benchmark report](../docs/team-meeting-analysis-2026-09-25.html), and [Kaveh's independent methodology draft](../docs/kaveh-independent-methodology.md).
- [Sent team feedback — 15 September](team/team-feedback-to-team-2026-09-15-FA.md): registered Persian letter, with its original Google Doc source. Sent feedback is not a record of implemented changes or verified findings.
- [Iman’s submission](../_local/submissions/2026-09-06-iman-protocol-drafts/): local-only protocol, matrix, codebook, and scripts; not published or merged as an approved protocol.
- [Engineering scraper documentation](../src/linkedin-scraper/README.md): prior engineering runs collected material, but that does not establish an approved research corpus or verified research results. This organization task did not inspect private data or run research code.

## Historical keyword instruments — August proposals

The two-layer architecture + GenAI, then skill-filter sampling proposal is historical, not the September working frame. Terms and query examples remain preserved for comparison; literature retrieval, discourse retrieval, and sentiment coding are distinct instruments.

| Record                                                             | Purpose                                                                                        |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [Keyword systems](keywords/keyword-systems.md)                     | August host evaluation, draft-conflict rulings, and the dated September working-frame decision |
| [Literature strings](keywords/keyword-literature-strings.md)       | August database-query protocol; no frozen query v1 or new search counts                        |
| [Discourse catalog](keywords/keyword-discourse-catalog.md)         | EN/FA/DE retrieval terms and source limitations                                                |
| [Keyword lexicon](keywords/keyword-lexicon.md)                     | Preserved categorized terms and coding vocabulary; not a validated thesaurus                   |
| [Search scope and storage](keywords/keywords-search-storage.md)    | Historical sampling sketches and proposed handling requirements                                |
| [Source identification](keywords/keyword-source-identification.md) | Dated comparison of teammate claims and published analogues, including unresolved evidence     |
| [LinkedIn Boolean sub-queries, 2026-10-07](keywords/linkedin-boolean-2026-10-07/subqueries.json) | 105 executable sub-queries and the script that generated them from the agreed three-block query; terms only, no collected data. Downloads: [JSON](keywords/linkedin-boolean-2026-10-07/subqueries.json), [Markdown](keywords/linkedin-boolean-2026-10-07/subqueries.md), [YAML](keywords/linkedin-boolean-2026-10-07/subqueries.yaml), [Word](keywords/linkedin-boolean-2026-10-07/subqueries.docx). The A/B/C term blocks: [JSON](keywords/linkedin-boolean-2026-10-07/term-blocks.json), [Markdown](keywords/linkedin-boolean-2026-10-07/term-blocks.md), [YAML](keywords/linkedin-boolean-2026-10-07/term-blocks.yaml), [Word](keywords/linkedin-boolean-2026-10-07/term-blocks.docx) |
| [Apify three-layer list, 2026-10-17 / finalized 2026-10-18](keywords/linkedin-apify-2026-10-17/README.md) | Confirmed final list for the Apify pass; the [clean three-layer file](keywords/linkedin-apify-2026-10-17/keywords-and-queries.md) writes all 55 keywords and 48 three-layer queries in full. Query downloads are in the [query index](keywords/README.md#downloads). The 55 keywords plus post-filters: [JSON](keywords/linkedin-apify-2026-10-17/keywords.json), [Markdown](keywords/linkedin-apify-2026-10-17/keywords.md), [YAML](keywords/linkedin-apify-2026-10-17/keywords.yaml), [Word](keywords/linkedin-apify-2026-10-17/keywords.docx) |
| [HTML catalog](../docs/archive/2026-09-25-historical-keyword-catalog.html) | Presentation of the historical August catalog, with current status notice (archived 2026-09-25; `docs/index.html` now redirects to the 2026-09-25 team meeting guide). The working copies are the Markdown instruments below, not this HTML page |

## Downloads for the list files

Generated 2026-11-12 from the file already in that row. JSON, Markdown, YAML, and Word carry the same extracted lists. Word was written with Python's standard library. No term or string was added. Keyword systems, search scope, and source identification are notes, so the Markdown file is the copy.

| List | JSON | Markdown | YAML | Word |
| --- | --- | --- | --- | --- |
| Literature strings | [JSON](keywords/literature-strings.json) | [Markdown](keywords/literature-strings.md) | [YAML](keywords/literature-strings.yaml) | [Word](keywords/literature-strings.docx) |
| Discourse catalog | [JSON](keywords/discourse-terms.json) | [Markdown](keywords/discourse-terms.md) | [YAML](keywords/discourse-terms.yaml) | [Word](keywords/discourse-terms.docx) |
| Lexicon | [JSON](keywords/lexicon.json) | [Markdown](keywords/lexicon.md) | [YAML](keywords/lexicon.yaml) | [Word](keywords/lexicon.docx) |
| Legacy scraper phrases | [JSON](../src/linkedin-scraper/keywords.json) | [Markdown](../src/linkedin-scraper/keywords.md) | [YAML](../src/linkedin-scraper/keywords.yaml) | [Word](../src/linkedin-scraper/keywords.docx) |

The annotation codebook named above is local-only (`_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/03_ANNOTATION_CODEBOOK_AND_GUIDELINES.txt`). It is not in the public tree, so these formats were not generated for it.

Version A (19) and Version B (85) are still not files in this repository. Commit `4d14c48` is on `cursor/apify-query-round-c795`, not on `main`. That branch's README calls its 19 option-A strings a reconstruction. They stay on that branch.

## Access and privacy

- [LinkedIn application record](access/linkedin-application-worksheet.md): last recorded receipt shows Open, not approval; three months refers to requested storage duration.
- [LinkedIn access review](access/linkedin-data-access-review.md): dated documentation review and unresolved permissions.
- [Privacy-policy review](access/privacy-policy-review.md) and [public policy](../PRIVACY.md): historical review and published notice, not collection authorization.

## Shared evidence and writing

- [Research notes](notes.md): working questions, current status, and dated setup history.
- [References](references.md): source records and reading limitations; preserve source IDs and original URLs.
- [Initial scratch](initial-scratch.md): original starting document, unchanged.
- [Project log](project-log.md): chronological actions, decisions and verification.
- [Article](../writing/article.md) and [thesis](../writing/thesis.md): outlines sharing the same research and evidence records.

## Traceability

The ten topic documents were relocated on 2026-09-17 without renaming their basenames: six keyword records to `keywords/`, three access records to `access/`, and the sent letter to `team/`. `notes.md`, `references.md`, `initial-scratch.md`, and `project-log.md` remain at this level. Clearly historical paths and source URLs remain provenance; current navigation uses the new locations. Local-only links will not resolve in a public checkout without those private artifacts.
