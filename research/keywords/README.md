# Query index

Updated: 2026-11-12. This page is the place to read the query files precisely and to download them. It does not freeze a query version. The homepage summary is the [root README](../../README.md#queries).

## Which list is which

| List | Count | Role | In the repository |
| --- | ---: | --- | --- |
| Q01–Q48 three-layer | 48 | Executed 2026-10-18. Source of the 1,858 posts in the team screening app | Yes |
| 7 October sub-queries | 105 | Executed 2026-10-07. Separate earlier pull (1,137 unique posts) | Yes |
| Version A | 19 | Still waiting on the team | **No file. TODO** |
| Version B | 85 | Still waiting on the team | **No file. TODO** |

Version A and Version B have no JSON in this repository, so no Markdown, YAML, or Word export was generated for them. Inventing those strings would be a new query list.

[Project log §49](../project-log.md#49-apify-query-list-for-the-next-round-2026-10-17) records that a file referred to as the 19 option-A queries was not in the repository and was not found in Drive. `linkedin-apify-2026-10-17/build_queries.py` mentions a Tier 2 two-layer Option A in its header and writes only the 48 three-layer queries. No project-log entry names an 85-query list.

## Downloads

Generated from the existing JSON on 12 November 2026. YAML was loaded back to the same object or the same 105 strings. The Word files contain the same strings. Word was written with Python's standard library (a `.docx` zip). No document package was added to the project.

On GitHub, open a file and use Raw or Download.

### Q01–Q48

| Format | File |
| --- | --- |
| JSON (source) | [queries.json](linkedin-apify-2026-10-17/queries.json) |
| Markdown in Q-ID order, plus the prose-number map | [queries.md](linkedin-apify-2026-10-17/queries.md) |
| Markdown grouped by family | [keywords-and-queries.md](linkedin-apify-2026-10-17/keywords-and-queries.md) |
| YAML | [queries.yaml](linkedin-apify-2026-10-17/queries.yaml) |
| Word | [queries.docx](linkedin-apify-2026-10-17/queries.docx) |

Round note: [linkedin-apify-2026-10-17/README.md](linkedin-apify-2026-10-17/README.md).

### 105 sub-queries

| Format | File |
| --- | --- |
| JSON (source) | [subqueries.json](linkedin-boolean-2026-10-07/subqueries.json) |
| Markdown | [subqueries.md](linkedin-boolean-2026-10-07/subqueries.md) |
| YAML | [subqueries.yaml](linkedin-boolean-2026-10-07/subqueries.yaml) |
| Word | [subqueries.docx](linkedin-boolean-2026-10-07/subqueries.docx) |

The generator is [decompose.py](linkedin-boolean-2026-10-07/decompose.py). The JSON array has no ids.

## How to read Q01–Q48

Open `queries` in the JSON or YAML. Each object has:

| Field | Meaning |
| --- | --- |
| `id` | `Q01`–`Q48`, assigned in file order |
| `query` | The Boolean string |
| `family` | `direct`, `cognition`, `process`, or `technical_and_pedagogy` |
| `tier` | `tier1_three_layer` on every row of this file |
| `operators` | Count of `AND` / `OR` / `NOT` stored with the string. 5 on every row except Q36, which is 4 |
| `layers` | 3 on every row |

`searchQueries` repeats `query` in the same order and omits the other fields. It is not a second list.

`keywords` groups the 55 terms. A term that was searched as a phrase is stored with its quote characters, for example `"generative AI"`.

`post_filters_not_in_the_query` is a post-filter list. Those phrases were not added to the Boolean strings.

Two fields are stale relative to the run record and are copied unchanged into the YAML and Word notes:

- `status` says no run was started in that commit.
- `recommended_actor_input_not_executed` holds `maxPosts` 50, `postedLimitDate` `2022-11-30`, and `sortBy` `date`.

[Project log §51](../project-log.md#51-apify-48-query-three-layer-run-executed-and-loaded-into-neon-2026-10-18) records that those parameters were the 18 October execution.

`keywords-and-queries.md` numbers the same strings from 1 to 48 inside family groups. That number is not the Q ID. Example: prose number 13 is Q33, and Q13 is prose number 17. The full map is at the bottom of [queries.md](linkedin-apify-2026-10-17/queries.md).

## How to read the 105 sub-queries

The JSON and YAML are a sequence of 105 strings. File order is the order `decompose.py` wrote. The Markdown and Word numbers are that order, starting at 1. They were not stored in the JSON.

Each string was checked again on 12 November 2026 with the same operator pattern the generator uses, `\b(AND|OR|NOT)\b`: minimum 3, maximum 5.

## Hit counts

Source: Neon project `cool-cake-91875024`, database `_saintiment_apify_three_layer_db`, read on **12 November 2026**. `queries.raw_hits_count` and `COUNT(DISTINCT post_query_hits.post_id)`. No post text was read.

For every Q ID, the distinct-post count equalled `raw_hits_count`, so the table has one hit column. Across queries, 1,618 posts matched one query code and 240 matched more than one (1,858 posts with a hit).

Family distinct-post counts overlap, so they do not sum to 1,858. Raw hits do sum to 2,158.

| Family | Queries | Raw hits | Distinct posts |
| --- | ---: | ---: | ---: |
| direct | 16 | 602 | 544 |
| cognition | 16 | 756 | 681 |
| process | 12 | 600 | 538 |
| technical_and_pedagogy | 4 | 200 | 190 |

[docs/index.html](../../docs/index.html) shows family raw hits 686, 732, 540, and 200. Those four numbers were not reproduced by `SUM(raw_hits_count)`. The distinct-post cells on that page (544, 681, 538, 190) match this read. Use the table above for raw hits.

`docs/index.html` links to `docs/layer2-query-decision-2026-10-16.html`. That file is not in the repository. TODO.

### Per query

A hit count of 50 is the `maxPosts` cap recorded for the run. Eleven queries are below the cap.

| ID | Family | Operators | Hits |
| --- | --- | ---: | ---: |
| Q01 | direct | 5 | 50 |
| Q02 | direct | 5 | 50 |
| Q03 | direct | 5 | 50 |
| Q04 | direct | 5 | 50 |
| Q05 | direct | 5 | 50 |
| Q06 | direct | 5 | 50 |
| Q07 | direct | 5 | 13 |
| Q08 | direct | 5 | 11 |
| Q09 | direct | 5 | 50 |
| Q10 | direct | 5 | 34 |
| Q11 | direct | 5 | 14 |
| Q12 | direct | 5 | 10 |
| Q13 | cognition | 5 | 50 |
| Q14 | cognition | 5 | 50 |
| Q15 | cognition | 5 | 50 |
| Q16 | cognition | 5 | 50 |
| Q17 | cognition | 5 | 50 |
| Q18 | cognition | 5 | 50 |
| Q19 | cognition | 5 | 50 |
| Q20 | cognition | 5 | 47 |
| Q21 | cognition | 5 | 50 |
| Q22 | cognition | 5 | 50 |
| Q23 | cognition | 5 | 30 |
| Q24 | cognition | 5 | 37 |
| Q25 | process | 5 | 50 |
| Q26 | process | 5 | 50 |
| Q27 | process | 5 | 50 |
| Q28 | process | 5 | 50 |
| Q29 | process | 5 | 50 |
| Q30 | process | 5 | 50 |
| Q31 | process | 5 | 50 |
| Q32 | process | 5 | 50 |
| Q33 | direct | 5 | 50 |
| Q34 | process | 5 | 50 |
| Q35 | process | 5 | 50 |
| Q36 | direct | 4 | 32 |
| Q37 | direct | 5 | 38 |
| Q38 | direct | 5 | 50 |
| Q39 | cognition | 5 | 50 |
| Q40 | cognition | 5 | 42 |
| Q41 | cognition | 5 | 50 |
| Q42 | cognition | 5 | 50 |
| Q43 | process | 5 | 50 |
| Q44 | process | 5 | 50 |
| Q45 | technical_and_pedagogy | 5 | 50 |
| Q46 | technical_and_pedagogy | 5 | 50 |
| Q47 | technical_and_pedagogy | 5 | 50 |
| Q48 | technical_and_pedagogy | 5 | 50 |

## Other keyword notes

Literature strings, the August discourse catalog, the lexicon, and the September working-frame decision stay in the [research index](../README.md). Those notes are not the executed Apify lists above.
