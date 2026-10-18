# Apify LinkedIn query round — 2026-10-17 (finalized 2026-10-18)

Status: **final confirmed three-layer keyword and query list (confirmed 2026-10-18)**. Contains 55 keywords across 3 layers and 48 executable three-layer queries (`<= 5` Boolean operators per query). No Apify run has been started in this commit.

Actor, when a run is separately authorized: `harvestapi/linkedin-post-search`. The clean three-layer list, with every keyword and every query written out for the team, is [`keywords-and-queries.md`](keywords-and-queries.md). The machine-readable record is [`queries.json`](queries.json), produced by [`build_queries.py`](build_queries.py).

## What this round is for

The 17 October group note accepts two constraints at once:

- Morteza’s reproducibility point: the third pillar, skill and cognition, has to be inside the query, not only in a later filter.
- The 7 October Apify tests: LinkedIn content search returned no posts once a query had six or more `AND` / `OR` operators, and returned posts at five or fewer. See project log section 40.

Iman’s uploaded suggestion (`Iman Sug.json`) puts three to four terms in every parenthesis of a three-layer query. Those parent strings have 7 to 11 operators. They are the received sketch. They are not the strings to paste into Apify.

The three-layer queries follow:
**Domain or tool AND AI AND a skill/cognition/process term (48 queries).**

## What was strengthened in v2 (without changing the team structure)

A cross-repository review of [`keyword-lexicon.md`](../keyword-lexicon.md), the [8 September team consensus](../../../_local/archive/2026-09-08-telegram-team-update/saintiment-update-Sep8.md), Kaveh’s [15 September feedback letter](../../team/team-feedback-to-team-2026-09-15-FA.md), Iman’s [`02_SEARCH_QUERY_MATRIX_AND_TAXONOMY`](../../../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/02_SEARCH_QUERY_MATRIX_AND_TAXONOMY.txt), the [25 September Run 013 synthesis](../../../docs/team-meeting-guide-2026-09-25.md), and the [7 October Apify pilot](../linkedin-boolean-2026-10-07/decompose.py) identified four surgical improvements:

1. **Removed redundant third-leg repetitions inside the original 36 queries (0 extra queries needed):**
   - In the first draft, `reskilling` appeared in both `(upskilling OR reskilling)` and `(deskilling OR reskilling)`, `judgment` appeared in both `(creativity OR judgment)` and `(authorship OR judgment)`, and `automation` appeared in both `(workflow OR automation)` and `(replace OR automation)`.
   - Replacing those three duplicate slots with `"skill loss"` (`deskilling OR "skill loss"`), `"design thinking"` (`creativity OR "design thinking"`), and `augmentation` (`replace OR augmentation`) covers three missing Core Lexicon lemmas and balances Substitution vs. Augmentation inside the query itself.
2. **Reduced software-architecture noise in `Rendering` queries:**
   - Replaced bare `architecture` with `archviz` in the creativity/rendering block (`Rendering OR archviz`) while retaining `architecture` alongside `"architectural design"` in process queries. Added plural `architects` (which rarely collides with IT job titles like `software architect`).
3. **Added missing consensus lemmas across Pillars 1–3 (+8 queries):**
   - **Direct skill:** `downskilling` (explicitly agreed by Morteza & Iman on Sep 8 and Kaveh on Sep 15), `"skill loss"`, and `expertise`.
   - **Cognition:** `"cognitive offloading"` and `overreliance` (the #1 empirical finding of both Iman’s 300-post coding and Run 013 analysis).
   - **Adaptation & agency:** `augmentation`, `replacement`, `"human-in-the-loop"`, and `"role of the architect"`.
   - **Visual/AEC GenAI tools:** `"Stable Diffusion"`, `DALL-E`, and `"AI rendering"` (which achieved the highest on-domain precision in the Oct 7 Apify pilot).
4. **Closed the RQ3a & RQ4 gap (+4 queries):**
   - Added 2 queries for **RQ3a (Technical & Environmental hard skills)**: `"technical skills"`, `"environmental design"`, `"building performance"`, `"energy modeling"`.
   - Added 2 neutral queries for **RQ4 (Architectural education & students)**: `"architectural education"`, `"architecture students"` paired neutrally with `curriculum`, `learning`, `skills`, and `"critical thinking"` (avoiding H4 confirmation bias per Kaveh’s Sep 15 §3.2 rule).

## Keyword list for this round (55 terms across 3 pillars)

| Pillar | Group | Terms |
| --- | --- | --- |
| Domain and tools (16) | Profession, software, education | architect, architects, architecture, architectural, "architectural design", "computational design", BIM, Revit, Rhino, Grasshopper, Parametric, "generative design", Rendering, archviz, "architectural education", "architecture students" |
| Technology (10) | Generic and named GenAI | AI, GenAI, "generative AI", "artificial intelligence", Midjourney, ChatGPT, Copilot, "Stable Diffusion", DALL-E, "AI rendering" |
| Labor / competency (8) | Direct skill | skill, skills, upskilling, deskilling, reskilling, downskilling, "skill loss", expertise |
| Labor / competency (8) | Cognition and design (RQ2a/2b) | creativity, "design thinking", "critical thinking", judgment, intuition, authorship, "cognitive offloading", overreliance |
| Labor / competency (7) | Process, adaptation, and work | workflow, automation, replace, replacement, augmentation, "human-in-the-loop", "role of the architect" |
| Labor / competency (6) | Technical, environmental & pedagogy (RQ3a/RQ4) | "technical skills", "environmental design", "building performance", "energy modeling", curriculum, learning |

## How a query is allowed to look

A three-layer query can carry at most two terms in each parenthesis:

`(A OR B) AND (C OR D) AND (E OR F)` = five operators.

`NOT` is an operator too, so software-architecture exclusions remain a post-filter after download:

`software architect`, `software architecture`, `enterprise architect`, `enterprise architecture`, `solution architect`, `solutions architect`, `GitHub Copilot`, `cloud architect`, `data architect`, `security architect`, `systems architect`, `network architect`.

## Three-layer queries (48)

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
| Q09 | direct | (architect OR architectural) AND (GenAI OR "generative AI") AND (deskilling OR "skill loss") |
| Q10 | direct | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (deskilling OR "skill loss") |
| Q11 | direct | (Parametric OR "generative design") AND (GenAI OR "generative AI") AND (deskilling OR "skill loss") |
| Q12 | direct | (Parametric OR "generative design") AND (Midjourney OR ChatGPT) AND (deskilling OR "skill loss") |
| Q13 | cognition | (architect OR architectural) AND (GenAI OR "generative AI") AND (creativity OR "design thinking") |
| Q14 | cognition | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (creativity OR "design thinking") |
| Q15 | cognition | (Rendering OR archviz) AND (GenAI OR "generative AI") AND (creativity OR "design thinking") |
| Q16 | cognition | (Rendering OR archviz) AND (Midjourney OR ChatGPT) AND (creativity OR "design thinking") |
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
| Q29 | process | (architect OR architectural) AND (GenAI OR "generative AI") AND (replace OR augmentation) |
| Q30 | process | (architect OR architectural) AND (Midjourney OR ChatGPT) AND (replace OR augmentation) |
| Q31 | process | (Rendering OR architecture) AND (GenAI OR "generative AI") AND (replace OR augmentation) |
| Q32 | process | (Rendering OR architecture) AND (Midjourney OR ChatGPT) AND (replace OR augmentation) |
| Q33 | direct | (architect OR architectural) AND (AI OR "artificial intelligence") AND (skill OR skills) |
| Q34 | process | (BIM OR Revit) AND (AI OR "artificial intelligence") AND (workflow OR automation) |
| Q35 | process | (BIM OR Revit) AND (Copilot OR ChatGPT) AND (workflow OR automation) |
| Q36 | direct | (Rhino OR Grasshopper) AND Copilot AND (skill OR skills) |
| Q37 | direct | (architect OR architects) AND (GenAI OR "generative AI") AND (downskilling OR deskilling) |
| Q38 | direct | ("architectural design" OR "computational design") AND (GenAI OR ChatGPT) AND (skills OR expertise) |
| Q39 | cognition | (architect OR architectural) AND (GenAI OR "generative AI") AND ("cognitive offloading" OR overreliance) |
| Q40 | cognition | (architect OR architects) AND (Midjourney OR ChatGPT) AND ("cognitive offloading" OR overreliance) |
| Q41 | cognition | (architect OR architectural) AND ("Stable Diffusion" OR DALL-E) AND (creativity OR authorship) |
| Q42 | cognition | (Rendering OR archviz) AND ("AI rendering" OR Midjourney) AND (creativity OR judgment) |
| Q43 | process | (architect OR architects) AND (GenAI OR "generative AI") AND ("human-in-the-loop" OR "role of the architect") |
| Q44 | process | ("architectural design" OR architecture) AND (GenAI OR "generative AI") AND (replacement OR augmentation) |
| Q45 | technical_and_pedagogy | (architect OR architectural) AND (GenAI OR "generative AI") AND ("technical skills" OR "environmental design") |
| Q46 | technical_and_pedagogy | (BIM OR "architectural design") AND (AI OR "generative AI") AND ("building performance" OR "energy modeling") |
| Q47 | technical_and_pedagogy | ("architectural education" OR "architecture students") AND (GenAI OR "generative AI") AND (curriculum OR learning) |
| Q48 | technical_and_pedagogy | ("architectural education" OR "architecture students") AND (Midjourney OR ChatGPT) AND (skills OR "critical thinking") |

## Actor settings if a run is authorized

| Input | Value | Why |
| --- | --- | --- |
| `searchQueries` | the 48 three-layer strings in `queries.json` | Full three-layer query set |
| `maxPosts` | 50 per query | Raises the 15-post cap seen on 7 October without an unbounded pull |
| `postedLimitDate` | `2022-11-30` | ChatGPT public launch |
| `sortBy` | `date` | Avoids LinkedIn top-engagement ranking bias |
| `scrapeComments` | false | 16 October group note: comments stay out of this pass |
| `scrapeReactions` | false | Posts only, same as the October pilot |
| `profileScraperMode` | `short` | Headlines without the full-profile charge |
| `contentType` | `all` | No media filter |
