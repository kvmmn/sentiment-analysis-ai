# Apify LinkedIn query round — 2026-10-17

Status: **working list for this round**. Query version 1 is not frozen. No Apify run has been started from this list. This is not a collection licence and not an ethics or terms-of-service clearance.

Actor, when a run is separately authorized: `harvestapi/linkedin-post-search`. The machine-readable input is [`queries.json`](queries.json), produced by [`build_queries.py`](build_queries.py). Re-run the script after any term edit so the JSON stays the executable copy.

## What this round is for

The 17 October group note accepts two constraints at once.

- Morteza’s reproducibility point: the third pillar, skill and cognition, has to be inside the query, not only in a later filter.
- The 7 October Apify tests: LinkedIn content search returned no posts once a query had six or more `AND` / `OR` operators, and returned posts at five or fewer. See project log section 40.

Iman’s uploaded suggestion (`Iman Sug.json`) puts three to four terms in every parenthesis of a three-layer query. Those parent strings have 7 to 11 operators. They are the received sketch. They are not the strings to paste into Apify. Two of the four “version A” parents already have five operators and are covered, in split form, by the tier-2 list below.

The group asked for two sets in one run:

1. Three-layer queries: domain or tool, and AI, and a skill term.
2. Two-layer option A: domain or tool, and AI, without a skill term, because practice talk often names the software instead of the word skill.

A file described in the group note as the 19 clean option-A queries (“فایل ve”) was not in this repository and was not found in Drive by title or by the option-A terms. Tier 2 below is the reconstruction of that compact option A from the agreed term lists. It has 19 queries. If the original 19 differ, replace tier 2 and keep the five-operator ceiling.

## Keyword list for this round

Terms not on this list are not added. Stable Diffusion, DALL·E, and LookX stay in the August lexicon and are not in this round. `judgment` is the American spelling used in the group note; `judgement` is not added.

| Pillar | Group | Terms |
| --- | --- | --- |
| Domain and tools | Profession and software | architect, architecture, architectural, BIM, Revit, Rhino, Grasshopper, Parametric, "generative design", Rendering |
| Technology | Generic and named | AI, GenAI, "generative AI", "artificial intelligence", Midjourney, ChatGPT, Copilot |
| Labor / competency | Direct skill | skill, skills, upskilling, deskilling, reskilling |
| Labor / competency | Cognition and design | creativity, "critical thinking", judgment, intuition, authorship |
| Labor / competency | Process and work | workflow, automation, replace |

`"generative design"` stays in the tool pillar. The lexicon keeps that phrase for the older computational-design sense and does not merge it with generative AI.

## How a query is allowed to look

A three-layer query can carry only two terms in each parenthesis:

`(A OR B) AND (C OR D) AND (E OR F)` = five operators.

A two-layer query can carry two and two, or a longer side only when the other side is shorter. Four terms on both sides is six or more operators and is the form that returned nothing on 7 October.

`NOT` is an operator too, so the software-architecture exclusions are a post-filter, not part of the search string. Code them after download. Do not delete them from the raw export.

Post-filter lexicon, not searched:

software architect, software architecture, enterprise architect, enterprise architecture, solution architect, solutions architect, GitHub Copilot, cloud architect, data architect, security architect.

`replace` and bare `architecture` and bare `AI` stay in the list because the group included them. They are noisy. The three-layer queries prefer `architect` / `architectural` over bare `architecture`. Bare `architecture` appears only beside a tool or a skill term.

## Tier 1 — three layers (36)

Every skill chunk is crossed with `architect OR architectural` and with one tool pair, and with both `GenAI OR "generative AI"` and `Midjourney OR ChatGPT`. Four extra queries place `AI`, `"artificial intelligence"`, and `Copilot`, which that grid does not contain. This is a covering set, not the full Cartesian product of every term. The full product of the same groups, split to pairs, is 192 queries; that expansion is specified by the same chunk rule if this round under-returns.

| ID | Family | Query |
| --- | --- | --- |
| Q01 | direct | (architect OR architectural) AND (GenAI OR "generative AI") AND (skill OR skills) |
| Q02 | direct | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (skill OR skills) |
| Q03 | direct | (BIM OR Revit) AND (GenAI OR "generative AI") AND (skill OR skills) |
| Q04 | direct | (BIM OR Revit) AND (Midjourney OR ChatGPT) AND (skill OR skills) |
| Q05 | direct | (architect OR architectural) AND (GenAI OR "generative AI") AND (upskilling OR reskilling) |
| Q06 | direct | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling) |
| Q07 | direct | (Rhino OR Grasshopper) AND (GenAI OR "generative AI") AND (upskilling OR reskilling) |
| Q08 | direct | (Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (upskilling OR reskilling) |
| Q09 | direct | (architect OR architectural) AND (GenAI OR "generative AI") AND (deskilling OR reskilling) |
| Q10 | direct | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling) |
| Q11 | direct | (Parametric OR "generative design") AND (GenAI OR "generative AI") AND (deskilling OR reskilling) |
| Q12 | direct | (Parametric OR "generative design") AND (Midjourney OR ChatGPT) AND (deskilling OR reskilling) |
| Q13 | cognition | (architect OR architectural) AND (GenAI OR "generative AI") AND (creativity OR judgment) |
| Q14 | cognition | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (creativity OR judgment) |
| Q15 | cognition | (Rendering OR architecture) AND (GenAI OR "generative AI") AND (creativity OR judgment) |
| Q16 | cognition | (Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (creativity OR judgment) |
| Q17 | cognition | (architect OR architectural) AND (GenAI OR "generative AI") AND ("critical thinking" OR intuition) |
| Q18 | cognition | (architect OR architectural) AND (Midjourney OR ChatGPT) AND ("critical thinking" OR intuition) |
| Q19 | cognition | (BIM OR Revit) AND (GenAI OR "generative AI") AND ("critical thinking" OR intuition) |
| Q20 | cognition | (BIM OR Revit) AND (Midjourney OR ChatGPT) AND ("critical thinking" OR intuition) |
| Q21 | cognition | (architect OR architectural) AND (GenAI OR "generative AI") AND (authorship OR judgment) |
| Q22 | cognition | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (authorship OR judgment) |
| Q23 | cognition | (Rhino OR Grasshopper) AND (GenAI OR "generative AI") AND (authorship OR judgment) |
| Q24 | cognition | (Rhino OR Grasshopper) AND (Midjourney OR ChatGPT) AND (authorship OR judgment) |
| Q25 | process | (architect OR architectural) AND (GenAI OR "generative AI") AND (workflow OR automation) |
| Q26 | process | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (workflow OR automation) |
| Q27 | process | (Parametric OR "generative design") AND (GenAI OR "generative AI") AND (workflow OR automation) |
| Q28 | process | (Parametric OR "generative design") AND (Midjourney OR ChatGPT) AND (workflow OR automation) |
| Q29 | process | (architect OR architectural) AND (GenAI OR "generative AI") AND (replace OR automation) |
| Q30 | process | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (replace OR automation) |
| Q31 | process | (Rendering OR architecture) AND (GenAI OR "generative AI") AND (replace OR automation) |
| Q32 | process | (Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (replace OR automation) |
| Q33 | direct | (architect OR architectural) AND (AI OR "artificial intelligence") AND (skill OR skills) |
| Q34 | process | (BIM OR Revit) AND (AI OR "artificial intelligence") AND (workflow OR automation) |
| Q35 | process | (BIM OR Revit) AND (Copilot OR ChatGPT) AND (workflow OR automation) |
| Q36 | direct | (Rhino OR Grasshopper) AND Copilot AND (skill OR skills) |

## Tier 2 — two layers, option A (19)

Five domain pairs cover the ten domain and tool terms. Four technology sides cover the seven AI terms. That grid has 20 cells. The omitted cell is `(architect OR architectural) AND Copilot`. Profession titles plus Copilot are the GitHub Copilot collision. Copilot remains next to the tool terms, including `architecture OR BIM`.

| ID | Query |
| --- | --- |
| Q37 | (architect OR architectural) AND (Midjourney OR ChatGPT) |
| Q38 | (architect OR architectural) AND (GenAI OR "generative AI") |
| Q39 | (architect OR architectural) AND (AI OR "artificial intelligence") |
| Q40 | (architecture OR BIM) AND (Midjourney OR ChatGPT) |
| Q41 | (architecture OR BIM) AND (GenAI OR "generative AI") |
| Q42 | (architecture OR BIM) AND (AI OR "artificial intelligence") |
| Q43 | (architecture OR BIM) AND Copilot |
| Q44 | (Revit OR Rhino) AND (Midjourney OR ChatGPT) |
| Q45 | (Revit OR Rhino) AND (GenAI OR "generative AI") |
| Q46 | (Revit OR Rhino) AND (AI OR "artificial intelligence") |
| Q47 | (Revit OR Rhino) AND Copilot |
| Q48 | (Grasshopper OR Parametric) AND (Midjourney OR ChatGPT) |
| Q49 | (Grasshopper OR Parametric) AND (GenAI OR "generative AI") |
| Q50 | (Grasshopper OR Parametric) AND (AI OR "artificial intelligence") |
| Q51 | (Grasshopper OR Parametric) AND Copilot |
| Q52 | ("generative design" OR Rendering) AND (Midjourney OR ChatGPT) |
| Q53 | ("generative design" OR Rendering) AND (GenAI OR "generative AI") |
| Q54 | ("generative design" OR Rendering) AND (AI OR "artificial intelligence") |
| Q55 | ("generative design" OR Rendering) AND Copilot |

## Actor settings if a run is authorized

These are recommendations from the actor schema and the October pilot. They were not executed with this list.

| Input | Value | Why |
| --- | --- | --- |
| `searchQueries` | the 55 strings in `queries.json` | One run, both tiers, as the group asked |
| `maxPosts` | 50 per query | The 7 October run stopped at 15 posts for 93 of 105 queries. The current actor prefills 20 and documents 0 as “all posts”. 50 raises the old cap without an unbounded pull |
| `postedLimitDate` | `2022-11-30` | Existing proposal: ChatGPT public launch. Not re-decided here |
| `sortBy` | `date` | A dated window is easier to describe than relevance rank. Not tested on this list |
| `scrapeComments` | false | 16 October group note: comments stay out of this pass |
| `scrapeReactions` | false | Posts only, same as the October pilot |
| `profileScraperMode` | `short` | Headlines without the full-profile charge |
| `contentType` | `all` | No media filter |

Deduplicate on the post URL after the run. Overlap across the 55 queries is expected and is not a failed query.

Spend is not estimated here as a budget approval. The October pilot was about USD 0.002 per post on the free plan, plus a small charge for a query that returns nothing. Fifty-five queries at 50 posts would be a different order of cost from the October pilot if most queries fill the cap. Set the cap before starting.

## What this list does not do

- It does not rerun the 105 sub-queries from 7 October.
- It does not treat the September precision vectors as this round’s input.
- It does not freeze query version 1.
- It does not authorize collection. The LinkedIn DSA case was Open on the last recorded receipt.
