# Saintiment — Iman Live Pilot: Complete Status Report for Team Meeting

**18 September 2026** · Merges Kaveh's 10 September feedback with 12-run execution evidence

---

## Executive Summary

We ran Iman Sheikhansari's collector and analysis pipeline for the first time — **12 runs** across two days. The collector works: we collected **1,043–1,237 posts** per full run across 24 LinkedIn search queries. But the data is incomplete: **zero headlines** were extracted, making stakeholder-level analysis impossible.

This report merges two sources of evidence:
1. **Kaveh's 10 September feedback** — a detailed review of the query design, methodology, codebook, and scripts before any code was run
2. **12-run execution evidence (17–18 September)** — what actually happened when we ran the code

The feedback predicted several problems that execution confirmed. Execution also found new issues the feedback didn't anticipate. Together they give us a clear picture of what needs to change before the next collection.

**Bottom line:** The pipeline is functional but needs fixes in three areas — query design (from the feedback), data extraction (from execution), and methodology (from both). All fixes are identified. None require starting over.

---

## 1. What We Started With

Iman submitted two Python scripts and three documents extracted from Google Docs:

| File | Purpose |
|------|---------|
| `collector.py` | Opens Chrome, logs into LinkedIn, runs 24 search queries, scrolls 35 times each, saves posts to SQLite + CSV |
| `analysis_pipeline.py` | Reads the database, classifies stakeholders by headline, scores sentiment per aspect, runs Kruskal-Wallis / Dunn / Chi-Square tests, exports tables and LaTeX |
| `01_STUDY_PROTOCOL` | Research protocol and methodology |
| `02_SEARCH_QUERY_MATRIX` | Query vectors mapped to research questions |
| `03_ANNOTATION_CODEBOOK` | Annotation guidelines with examples |

We **never edited the originals**. Every run used a separate copy. All changes are tracked with SHA-256 hashes.

---

## 2. All 12 Runs at a Glance

### Collection Runs

| Run | Date/Time (UTC) | What | Result | Rows | Headlines |
|-----|----------------|------|--------|------|-----------|
| **001** | Sep 17, 20:49 | First attempt | Interrupted by assistant (mistake) | Unknown | — |
| **003** | Sep 17, 21:08 | Retry with original code | **Failed** — old login selector | 0 | — |
| **005** | Sep 17, 21:26–22:26 | Fixed login check | Watchdog stopped at query 23 | **1,181** | 0 |
| **007** | Sep 17, 22:36–22:41 | Resume queries 23–24 | Completed, exit 0 | **1,237** | 0 |
| **011** | Sep 18, 09:41–10:37 | Second full run (original code) | Completed, exit 0 | **1,043** | 0 |
| **012** | Sep 18, ~12:42–13:53 | Fixed headline collector | **Rate-limited** mid-run | **257** | 0 |

### Analysis & Test Runs

| Run | Date/Time (UTC) | What | Result |
|-----|----------------|------|--------|
| **002** | Sep 17, 22:44 | Original analysis on 1,237 rows | **Crashed** — empty contingency table |
| **008** | Sep 17, 22:54 | Guarded analysis (same data) | Completed; all 3 tests **skipped** (no stakeholder data) |
| **009** | Sep 17 | Synthetic guard tests | **8/8 passed** |
| **010** | Sep 17 | Headline fix synthetic tests | **3/3 passed** |

### Diagnostic Runs

| Run | What | Result |
|-----|------|--------|
| **004** | Diagnostic prep | Not executed |
| **006** | Browser diagnostic | Confirmed login works; LinkedIn changed HTML classes |

---

## 3. Cross-Reference: Feedback Predictions vs. Execution Evidence

Kaveh's 10 September feedback identified issues in three categories. Here's what execution confirmed, what it didn't, and what it found that the feedback didn't predict.

### 3.1 Issues the Feedback Predicted — Confirmed by Execution ✅

| Feedback Item | What the Feedback Said | What Execution Found |
|---------------|----------------------|---------------------|
| **Fragile DOM selectors** (§6.3) | "LinkedIn's page structure changes regularly and selectors need updating" | **Confirmed.** `nav.global-nav` no longer exists. Run 003 timed out after 5 minutes. Fixed in Run 005 with a JS-based readiness check. |
| **Engagement metrics may be zero** (§6.2) | "The script uses old LinkedIn regex patterns; metrics may all be stored as zero" | **Partially confirmed.** Metrics are being extracted but we haven't independently verified their accuracy against visible LinkedIn counts. |
| **Missing post dates** (§6.1) | "No field exists to store post publication date; temporal trend analysis is lost" | **Confirmed.** The `CorpusRecord` dataclass has no date field. Only `harvested_at_utc` (when we collected it) is stored. |
| **Analysis lexicon overlaps with search terms** (§3.6) | "Words like `deskill`, `replace`, `homogenize` are both search keywords AND negative sentiment markers — circular" | **Confirmed by source review.** The polarity lexicon and search queries share vocabulary. Every post found via `deskilling` automatically gets a negative sentiment score. |
| **Stance label inconsistency** (§3.7) | "Protocol says `Neutral`, keyword doc says `Pragmatic/Reformer`, code says `Pragmatic/Evaluative`" | **Confirmed.** Three different names for the same stance category across three files. |
| **Minimum text length mismatch** (§3.7) | "Protocol: 40 words or 200 chars. Code: 120 chars." | **Confirmed.** `MIN_TEXT_LENGTH_CHAR = 120` in the code vs. 200 in the protocol document. |
| **Analysis pipeline is lexicon-only prototype** (§6) | "Current pipeline assigns one global score to all aspects; ABSA and LLM methods are planned" | **Confirmed.** `score_aspect_sentiment` computes one base polarity and copies it to all 5 aspects. True aspect-based scoring is not implemented. |
| **No bimodality test for H1** (§5.6) | "Kruskal-Wallis cannot prove bimodality; need bimodality coefficient or stance frequency analysis" | **Confirmed.** The pipeline only has Kruskal-Wallis, Dunn, and Chi-Square. No bimodality test exists. |

### 3.2 Issues the Feedback Predicted — Not Yet Addressed in Code 🔴

| Feedback Item | What the Feedback Said | Current Status |
|---------------|----------------------|----------------|
| **OR parentheses bug** (§3.1) | `"AI" architecture "sustainability" OR "energy modeling"` is parsed wrong by LinkedIn | **Not fixed.** The 24 queries in the code still have the unparenthesized OR. |
| **Missing Adaptation branch** (§3.2) | Zero queries for upskilling/reskilling/co-pilot; `downskilling` term missing | **Not fixed.** Query list unchanged from original. |
| **Education vector bias** (§3.3) | `"deskilling"` in the education query pre-proves H4 (academics are pessimistic) | **Not fixed.** Query 22 still combines education + deskilling. |
| **Three-pillar compliance gaps** (§3.4) | 2 vectors lack GenAI terms; 6 use generic "AI" instead of "generative AI" | **Not fixed.** |
| **Deskilling vs. Replacement not separated** (§3.5) | Codebook merges skill atrophy with job displacement | **Not fixed.** Aspect 1 in the code still combines both. |
| **Missing key tools in queries** (§3.10) | ChatGPT, Stable Diffusion, DALL·E, LLM — all absent from 24 queries | **Not fixed.** |
| **Software architecture noise** (§3.4) | 15 of 24 queries use bare `architecture` without NOT filter | **Not fixed.** No NOT operator used. |
| **PRISMA-S claim** (§3.8) | "Full compliance with PRISMA-S" is indefensible for LinkedIn scraping | **Not fixed.** Header comment still claims PRISMA-S compliance. |
| **API naming** (§3.8) | "LinkedIn Content Search API" doesn't exist | **Not fixed.** |
| **Scopus query** (§3.9) | Missing NOT filters for software/computer architecture | **Not fixed.** Separate from collector — Scopus query not in codebase. |
| **Kappa target too high** (§7.7) | κ ≥ 0.85 is unrealistic for complex LinkedIn variables | **Not addressed.** Code imports Cohen's Kappa but never calls it. |

### 3.3 Issues Execution Found — Not in the Feedback 🆕

| Issue | What We Found | Severity |
|-------|--------------|----------|
| **Headline extraction broken** | `cleanStr()` collapses newlines before `.split('\n')` — zero headlines across 2,280 posts | 🔴 Critical |
| **Author name extraction failing** | Only ~17% of names extracted; 75% of those are "Unknown" | 🔴 Critical |
| **UPSERT counter wrong** | Reports "1,084 new" when only 1,043 stored. SQLite rowcount bug. | 🟡 Important |
| **No scroll checkpointing** | Interruption means restarting current query from scroll 1 | 🟡 Important |
| **Rate limiting** | 3 back-to-back runs triggered LinkedIn anti-scraping detection | 🟡 Important |
| **Row counts vary between runs** | 1,237 vs 1,043 across two full runs — LinkedIn results change over time | 🟢 Expected |
| **Analysis crashes on empty data** | Unguarded `chi2_contingency` crashes when no stakeholders classified | 🟡 Fixed in Run 008 |
| **`datetime.utcnow()` deprecated** | Warning only, doesn't affect results | 🟢 Minor |

---

## 4. Data Quality: What 2,280 Posts Actually Contain

```
                    Run 005+007    Run 011
                    ───────────    ───────
Total posts           1,237         1,043
Unique IDs             1,237         1,043
SQLite integrity         ok            ok
                                    
Author names             15%           18%
  (of which "Unknown")   73%           75%
Profile URLs             89%           87%
Headlines                 0%            0%
Post dates                0%            0%
                                    
Usable for analysis?     NO            NO
```

**What we have:** Post content, engagement metrics, and profile URLs — enough for content analysis and aspect-based sentiment scoring.

**What we don't have:** Stakeholder identities, post publication dates, verified engagement counts, or any way to do group comparisons.

---

## 5. Bug Details and Fix Status

### Bug 1: Login Selector — LinkedIn Changed HTML ✅ FIXED

**Predicted by feedback §6.3** ("DOM selectors are fragile")

The original code waits for `nav.global-nav`. LinkedIn no longer uses that CSS class. Fixed in Run 005 with a JavaScript function that checks for visible navigation elements, correct URL, and no password field. Works reliably.

### Bug 2: Headline Extraction — Whitespace Collapse 🔧 FIX READY, NEEDS LIVE TEST

**Not predicted by feedback** — discovered during execution

```javascript
// BROKEN (original):
const fullCard = cleanStr(card.innerText);  // collapses ALL whitespace
const textLines = fullCard.split('\n')...   // only 1 line — no "next line" for headline

// FIXED (Run 010):
const textLines = (card.innerText || '').split('\n')...  // split FIRST, clean each line
```

3/3 synthetic tests passed. Could not verify on real LinkedIn due to rate limiting (Run 012). The fix is correct in principle but needs a clean live test.

### Bug 3: Author Name Extraction — ~17% Success Rate 🔴 NOT FIXED

**Not predicted by feedback** — discovered during execution

Only 15–18% of posts have a nonempty author name. Of those, 73–75% are "Unknown." The headline lookup depends on finding the author name first — so this bug compounds with Bug 2. Profile URLs are the most reliable field (87–89% populated), suggesting the DOM elements exist but the text extraction isn't matching them.

### Bug 4: UPSERT Counter — Reports Inflated Numbers 🟡 NOT FIXED

SQLite `UPSERT` returns `rowcount = 1` for both inserts AND updates. The code interprets both as "new." Always count the database, not the application log.

---

## 6. What the Analysis Can and Cannot Do

### What Works
- Loads the database and enriches all rows
- Scores aspect-based sentiment (5 aspects, though all get the same global polarity)
- Produces descriptive statistics per aspect
- Exports enriched CSV, Parquet, and LaTeX tables

### What Doesn't Work (Without Headlines)
- **Stakeholder classification** — all rows are `Unclassified`
- **Kruskal-Wallis test** — needs ≥2 stakeholder groups with ≥3 members each
- **Dunn post-hoc test** — needs significant Kruskal result
- **Chi-Square test** — needs a non-empty stakeholder × stance contingency table
- **Bimodality test (H1)** — not implemented at all (feedback §5.6)

The guarded analysis (Run 008) handles missing data gracefully — it skips unsupported tests and records why in a JSON file, rather than crashing.

---

## 7. Consolidated Priority: What Needs to Change Before Next Collection

This merges the feedback's recommendations with execution evidence into one prioritized list.

### 🔴 Must Fix Before Recollection

| # | Item | Source | Effort |
|---|------|--------|--------|
| 1 | **Fix headline extraction** (Bug 2) — verify on real LinkedIn | Execution | Already coded, needs live test |
| 2 | **Fix author name extraction** (Bug 3) — investigate DOM mismatch | Execution | Needs DOM inspection |
| 3 | **Fix OR parentheses** (§3.1) — add parens around OR groups | Feedback | Edit query strings |
| 4 | **Add Adaptation queries** (§3.2) — 2–3 vectors for upskilling/reskilling/co-pilot + downskilling | Feedback | Add 3–4 query strings |
| 5 | **Fix education vector** (§3.3) — remove `deskilling` from education query; classify stakeholders from full dataset | Feedback | Edit 1 query string |
| 6 | **Add post date extraction** (§6.1) — new field in CorpusRecord + DOM extraction | Feedback | Schema change + JS |
| 7 | **Separate search lexicon from sentiment lexicon** (§3.6) — remove circular scoring | Feedback | Edit polarity lists |

### 🟡 Should Fix

| # | Item | Source |
|---|------|--------|
| 8 | Add ChatGPT/Stable Diffusion/DALL·E to queries (§3.10) | Feedback |
| 9 | Add `NOT ("software architecture" OR "enterprise architecture")` to queries (§3.4) | Feedback |
| 10 | Add scroll checkpointing | Execution |
| 11 | Fix UPSERT counter | Execution |
| 12 | Add inter-query delays (30–60s) to avoid rate limiting | Execution |
| 13 | Unify stance labels across all documents (§3.7) | Feedback |
| 14 | Unify minimum text length threshold (§3.7) | Feedback |
| 15 | Replace `datetime.utcnow()` with `datetime.now(timezone.utc)` | Execution |
| 16 | Fix PRISMA-S claim and API naming (§3.8) | Feedback |

### 🟢 Methodology Decisions (Team Discussion)

| # | Item | Source |
|---|------|--------|
| 17 | Separate Deskilling from Replacement in codebook (§3.5) | Feedback |
| 18 | Add bimodality test for H1 (§5.6) | Feedback |
| 19 | Define polarity target explicitly (§5.2) | Feedback |
| 20 | Document LinkedIn self-promotion bias (§5.3) | Feedback |
| 21 | Document engagement-ranking sampling bias (§5.4) | Feedback |
| 22 | Set time window for data collection (§5.5) | Feedback |
| 23 | Lower Kappa target to realistic level (§7.7) | Feedback |
| 24 | Freeze query version — apply team's agreed changes | Both |

---

## 8. Decision Table for the Meeting

Kaveh's 10 September feedback included this decision table. Updated with execution evidence:

| # | Decision | Previous Status | Execution Evidence | Recommendation |
|:-:|----------|----------------|-------------------|----------------|
| 1 | **Cover all 3 pillar branches** | Focus on Loss & Agency | Confirmed: 0 Adaptation queries → skewed data | Add Adaptation queries before next run |
| 2 | **Vectors without GenAI** | 2 generic vectors exist | Not yet tested separately | Keep with "exploratory" label, analyze separately |
| 3 | **Language scope** | English assumed | Confirmed: all collected posts are English | Formalize as inclusion criterion |
| 4 | **Time window** | Undefined | Confirmed: no post dates collected | Add date extraction to collector |
| 5 | **Which script to run** | Two versions exist | 005 (login fix) works; 010 (headline fix) ready | Merge both fixes + query changes into one version |
| 6 | **Platform focus** | Multi-platform planned | LinkedIn-only so far | Keep Phase 1 LinkedIn-only |
| 7 | **Pilot before full run** | 2–3 vector test proposed | 12 runs done but no targeted pilot | Run 2–3 vectors with ALL fixes before full 24 |

---

## 9. Key Numbers

| Metric | Value |
|--------|-------|
| Total runs executed | 12 |
| Successful full collections | 2 (005+007 combined, 011) |
| Total posts collected | 2,280 |
| Posts with headlines | **0** |
| Posts with usable author names | ~35 |
| Bugs found | 7 (2 fixed, 1 ready, 4 not fixed) |
| Feedback items confirmed by execution | 8 |
| Feedback items not yet addressed | 11 |
| New issues found (not in feedback) | 8 |
| Rate limit incidents | 1 |
| Time per full collection | ~57–75 minutes |

---

## 10. Recommended Next Steps

### This Week
1. **Wait for rate limit cooldown** (at least until tomorrow)
2. **Inspect real LinkedIn DOM** for author name extraction — understand why only 17% of names are found
3. **Apply query fixes** from feedback (§3.1–3.4): OR parentheses, Adaptation branch, education vector, three-pillar gaps
4. **Merge all fixes** into one collector version: login fix + headline fix + query changes + date extraction
5. **Run a 2–3 vector pilot** with the merged collector to verify all fixes work

### Before Full Collection
6. Add post date field to schema and extraction
7. Separate search lexicon from sentiment lexicon
8. Add inter-query delays (30–60 seconds)
9. Add scroll checkpointing
10. Freeze the final query list with team approval

### Research & Writing
11. Resolve methodology decisions (deskilling vs. replacement, bimodality test, polarity target, platform bias documentation)
12. Address LinkedIn access/retention questions
13. Update protocol and codebook to match the executed pipeline

---

## 11. File References

| Document | Location |
|----------|----------|
| **This report** | `docs/team-meeting-brief-2026-09-18.md` |
| Full technical report (with diagrams) | `docs/iman-live-pilot-technical-report.md` |
| Kaveh's 10 September feedback (Persian) | `_local/archive/2026-09-10-quality-review/final-feedback-to-team-FA.md` |
| Experiment plan & run table | `experiments/2026-09-17-iman-live-pilot.md` |
| Per-run workflow guide | `experiments/runs/README.md` |
| Individual run records | `experiments/runs/2026-09-17-iman-live-pilot/0XX-*.md` |
| Project log (full history) | `research/project-log.md` |
| Iman's original submission | `_local/submissions/2026-09-06-iman-protocol-drafts/` (local only) |

---

*All raw data, browser profiles, and private artifacts remain local-only. No credentials or personal post content are in any public document. No scientific findings or platform permissions are claimed.*

---

## 1. What We Started With

Iman submitted two Python scripts and three documents extracted from Google Docs:

| File | Purpose |
|------|---------|
| `collector.py` | Opens Chrome, logs into LinkedIn, runs 24 search queries, scrolls 35 times each, saves posts to SQLite + CSV |
| `analysis_pipeline.py` | Reads the database, classifies stakeholders by headline, scores sentiment per aspect, runs Kruskal-Wallis / Dunn / Chi-Square tests, exports tables and LaTeX |
| `01_STUDY_PROTOCOL` | Research protocol and methodology |
| `02_SEARCH_QUERY_MATRIX` | Query vectors mapped to research questions |
| `03_ANNOTATION_CODEBOOK` | Annotation guidelines with examples |

We **never edited the originals**. Every run used a separate copy. All changes are tracked with SHA-256 hashes.

---

## 2. All 12 Runs at a Glance

### Collection Runs

| Run | Date/Time (UTC) | What | Result | Rows | Headlines |
|-----|----------------|------|--------|------|-----------|
| **001** | Sep 17, 20:49 | First attempt | Interrupted by assistant (mistake) | Unknown | — |
| **003** | Sep 17, 21:08 | Retry with original code | **Failed** — old login selector | 0 | — |
| **005** | Sep 17, 21:26–22:26 | Fixed login check | Watchdog stopped at query 23 | **1,181** | 0 |
| **007** | Sep 17, 22:36–22:41 | Resume queries 23–24 | Completed, exit 0 | **1,237** | 0 |
| **011** | Sep 18, 09:41–10:37 | Second full run (original code) | Completed, exit 0 | **1,043** | 0 |
| **012** | Sep 18, ~12:42–13:53 | Fixed headline collector | **Rate-limited** mid-run | **257** | 0 |

### Analysis & Test Runs

| Run | Date/Time (UTC) | What | Result |
|-----|----------------|------|--------|
| **002** | Sep 17, 22:44 | Original analysis on 1,237 rows | **Crashed** — empty contingency table |
| **008** | Sep 17, 22:54 | Guarded analysis (same data) | Completed; all 3 tests **skipped** (no stakeholder data) |
| **009** | Sep 17 | Synthetic guard tests | **8/8 passed** |
| **010** | Sep 17 | Headline fix synthetic tests | **3/3 passed** |

### Diagnostic Runs

| Run | What | Result |
|-----|------|--------|
| **004** | Diagnostic prep | Not executed |
| **006** | Browser diagnostic | Confirmed login works; LinkedIn changed HTML classes |

---

## 3. Cross-Reference: Feedback Predictions vs. Execution Evidence

Kaveh's 10 September feedback identified issues in three categories. Here's what execution confirmed, what it didn't, and what it found that the feedback didn't predict.

### 3.1 Issues the Feedback Predicted — Confirmed by Execution ✅

| Feedback Item | What the Feedback Said | What Execution Found |
|---------------|----------------------|---------------------|
| **Fragile DOM selectors** (§6.3) | "LinkedIn's page structure changes regularly and selectors need updating" | **Confirmed.** `nav.global-nav` no longer exists. Run 003 timed out after 5 minutes. Fixed in Run 005 with a JS-based readiness check. |
| **Engagement metrics may be zero** (§6.2) | "The script uses old LinkedIn regex patterns; metrics may all be stored as zero" | **Partially confirmed.** Metrics are being extracted but we haven't independently verified their accuracy against visible LinkedIn counts. |
| **Missing post dates** (§6.1) | "No field exists to store post publication date; temporal trend analysis is lost" | **Confirmed.** The `CorpusRecord` dataclass has no date field. Only `harvested_at_utc` (when we collected it) is stored. |
| **Analysis lexicon overlaps with search terms** (§3.6) | "Words like `deskill`, `replace`, `homogenize` are both search keywords AND negative sentiment markers — circular" | **Confirmed by source review.** The polarity lexicon and search queries share vocabulary. Every post found via `deskilling` automatically gets a negative sentiment score. |
| **Stance label inconsistency** (§3.7) | "Protocol says `Neutral`, keyword doc says `Pragmatic/Reformer`, code says `Pragmatic/Evaluative`" | **Confirmed.** Three different names for the same stance category across three files. |
| **Minimum text length mismatch** (§3.7) | "Protocol: 40 words or 200 chars. Code: 120 chars." | **Confirmed.** `MIN_TEXT_LENGTH_CHAR = 120` in the code vs. 200 in the protocol document. |
| **Analysis pipeline is lexicon-only prototype** (§6) | "Current pipeline assigns one global score to all aspects; ABSA and LLM methods are planned" | **Confirmed.** `score_aspect_sentiment` computes one base polarity and copies it to all 5 aspects. True aspect-based scoring is not implemented. |
| **No bimodality test for H1** (§5.6) | "Kruskal-Wallis cannot prove bimodality; need bimodality coefficient or stance frequency analysis" | **Confirmed.** The pipeline only has Kruskal-Wallis, Dunn, and Chi-Square. No bimodality test exists. |

### 3.2 Issues the Feedback Predicted — Not Yet Addressed in Code 🔴

| Feedback Item | What the Feedback Said | Current Status |
|---------------|----------------------|----------------|
| **OR parentheses bug** (§3.1) | `"AI" architecture "sustainability" OR "energy modeling"` is parsed wrong by LinkedIn | **Not fixed.** The 24 queries in the code still have the unparenthesized OR. |
| **Missing Adaptation branch** (§3.2) | Zero queries for upskilling/reskilling/co-pilot; `downskilling` term missing | **Not fixed.** Query list unchanged from original. |
| **Education vector bias** (§3.3) | `"deskilling"` in the education query pre-proves H4 (academics are pessimistic) | **Not fixed.** Query 22 still combines education + deskilling. |
| **Three-pillar compliance gaps** (§3.4) | 2 vectors lack GenAI terms; 6 use generic "AI" instead of "generative AI" | **Not fixed.** |
| **Deskilling vs. Replacement not separated** (§3.5) | Codebook merges skill atrophy with job displacement | **Not fixed.** Aspect 1 in the code still combines both. |
| **Missing key tools in queries** (§3.10) | ChatGPT, Stable Diffusion, DALL·E, LLM — all absent from 24 queries | **Not fixed.** |
| **Software architecture noise** (§3.4) | 15 of 24 queries use bare `architecture` without NOT filter | **Not fixed.** No NOT operator used. |
| **PRISMA-S claim** (§3.8) | "Full compliance with PRISMA-S" is indefensible for LinkedIn scraping | **Not fixed.** Header comment still claims PRISMA-S compliance. |
| **API naming** (§3.8) | "LinkedIn Content Search API" doesn't exist | **Not fixed.** |
| **Scopus query** (§3.9) | Missing NOT filters for software/computer architecture | **Not fixed.** Separate from collector — Scopus query not in codebase. |
| **Kappa target too high** (§7.7) | κ ≥ 0.85 is unrealistic for complex LinkedIn variables | **Not addressed.** Code imports Cohen's Kappa but never calls it. |

### 3.3 Issues Execution Found — Not in the Feedback 🆕

| Issue | What We Found | Severity |
|-------|--------------|----------|
| **Headline extraction broken** | `cleanStr()` collapses newlines before `.split('\n')` — zero headlines across 2,280 posts | 🔴 Critical |
| **Author name extraction failing** | Only ~17% of names extracted; 75% of those are "Unknown" | 🔴 Critical |
| **UPSERT counter wrong** | Reports "1,084 new" when only 1,043 stored. SQLite rowcount bug. | 🟡 Important |
| **No scroll checkpointing** | Interruption means restarting current query from scroll 1 | 🟡 Important |
| **Rate limiting** | 3 back-to-back runs triggered LinkedIn anti-scraping detection | 🟡 Important |
| **Row counts vary between runs** | 1,237 vs 1,043 across two full runs — LinkedIn results change over time | 🟢 Expected |
| **Analysis crashes on empty data** | Unguarded `chi2_contingency` crashes when no stakeholders classified | 🟡 Fixed in Run 008 |
| **`datetime.utcnow()` deprecated** | Warning only, doesn't affect results | 🟢 Minor |

---

## 4. Data Quality: What 2,280 Posts Actually Contain

```
                    Run 005+007    Run 011
                    ───────────    ───────
Total posts           1,237         1,043
Unique IDs             1,237         1,043
SQLite integrity         ok            ok
                                    
Author names             15%           18%
  (of which "Unknown")   73%           75%
Profile URLs             89%           87%
Headlines                 0%            0%
Post dates                0%            0%
                                    
Usable for analysis?     NO            NO
```

**What we have:** Post content, engagement metrics, and profile URLs — enough for content analysis and aspect-based sentiment scoring.

**What we don't have:** Stakeholder identities, post publication dates, verified engagement counts, or any way to do group comparisons.

---

## 5. Bug Details and Fix Status

### Bug 1: Login Selector — LinkedIn Changed HTML ✅ FIXED

**Predicted by feedback §6.3** ("DOM selectors are fragile")

The original code waits for `nav.global-nav`. LinkedIn no longer uses that CSS class. Fixed in Run 005 with a JavaScript function that checks for visible navigation elements, correct URL, and no password field. Works reliably.

### Bug 2: Headline Extraction — Whitespace Collapse 🔧 FIX READY, NEEDS LIVE TEST

**Not predicted by feedback** — discovered during execution

```javascript
// BROKEN (original):
const fullCard = cleanStr(card.innerText);  // collapses ALL whitespace
const textLines = fullCard.split('\n')...   // only 1 line — no "next line" for headline

// FIXED (Run 010):
const textLines = (card.innerText || '').split('\n')...  // split FIRST, clean each line
```

3/3 synthetic tests passed. Could not verify on real LinkedIn due to rate limiting (Run 012). The fix is correct in principle but needs a clean live test.

### Bug 3: Author Name Extraction — ~17% Success Rate 🔴 NOT FIXED

**Not predicted by feedback** — discovered during execution

Only 15–18% of posts have a nonempty author name. Of those, 73–75% are "Unknown." The headline lookup depends on finding the author name first — so this bug compounds with Bug 2. Profile URLs are the most reliable field (87–89% populated), suggesting the DOM elements exist but the text extraction isn't matching them.

### Bug 4: UPSERT Counter — Reports Inflated Numbers 🟡 NOT FIXED

SQLite `UPSERT` returns `rowcount = 1` for both inserts AND updates. The code interprets both as "new." Always count the database, not the application log.

---

## 6. What the Analysis Can and Cannot Do

### What Works
- Loads the database and enriches all rows
- Scores aspect-based sentiment (5 aspects, though all get the same global polarity)
- Produces descriptive statistics per aspect
- Exports enriched CSV, Parquet, and LaTeX tables

### What Doesn't Work (Without Headlines)
- **Stakeholder classification** — all rows are `Unclassified`
- **Kruskal-Wallis test** — needs ≥2 stakeholder groups with ≥3 members each
- **Dunn post-hoc test** — needs significant Kruskal result
- **Chi-Square test** — needs a non-empty stakeholder × stance contingency table
- **Bimodality test (H1)** — not implemented at all (feedback §5.6)

The guarded analysis (Run 008) handles missing data gracefully — it skips unsupported tests and records why in a JSON file, rather than crashing.

---

## 7. Consolidated Priority: What Needs to Change Before Next Collection

This merges the feedback's recommendations with execution evidence into one prioritized list.

### 🔴 Must Fix Before Recollection

| # | Item | Source | Effort |
|---|------|--------|--------|
| 1 | **Fix headline extraction** (Bug 2) — verify on real LinkedIn | Execution | Already coded, needs live test |
| 2 | **Fix author name extraction** (Bug 3) — investigate DOM mismatch | Execution | Needs DOM inspection |
| 3 | **Fix OR parentheses** (§3.1) — add parens around OR groups | Feedback | Edit query strings |
| 4 | **Add Adaptation queries** (§3.2) — 2–3 vectors for upskilling/reskilling/co-pilot + downskilling | Feedback | Add 3–4 query strings |
| 5 | **Fix education vector** (§3.3) — remove `deskilling` from education query; classify stakeholders from full dataset | Feedback | Edit 1 query string |
| 6 | **Add post date extraction** (§6.1) — new field in CorpusRecord + DOM extraction | Feedback | Schema change + JS |
| 7 | **Separate search lexicon from sentiment lexicon** (§3.6) — remove circular scoring | Feedback | Edit polarity lists |

### 🟡 Should Fix

| # | Item | Source |
|---|------|--------|
| 8 | Add ChatGPT/Stable Diffusion/DALL·E to queries (§3.10) | Feedback |
| 9 | Add `NOT ("software architecture" OR "enterprise architecture")` to queries (§3.4) | Feedback |
| 10 | Add scroll checkpointing | Execution |
| 11 | Fix UPSERT counter | Execution |
| 12 | Add inter-query delays (30–60s) to avoid rate limiting | Execution |
| 13 | Unify stance labels across all documents (§3.7) | Feedback |
| 14 | Unify minimum text length threshold (§3.7) | Feedback |
| 15 | Replace `datetime.utcnow()` with `datetime.now(timezone.utc)` | Execution |
| 16 | Fix PRISMA-S claim and API naming (§3.8) | Feedback |

### 🟢 Methodology Decisions (Team Discussion)

| # | Item | Source |
|---|------|--------|
| 17 | Separate Deskilling from Replacement in codebook (§3.5) | Feedback |
| 18 | Add bimodality test for H1 (§5.6) | Feedback |
| 19 | Define polarity target explicitly (§5.2) | Feedback |
| 20 | Document LinkedIn self-promotion bias (§5.3) | Feedback |
| 21 | Document engagement-ranking sampling bias (§5.4) | Feedback |
| 22 | Set time window for data collection (§5.5) | Feedback |
| 23 | Lower Kappa target to realistic level (§7.7) | Feedback |
| 24 | Freeze query version — apply team's agreed changes | Both |

---

## 8. Decision Table for the Meeting

Kaveh's 10 September feedback included this decision table. Updated with execution evidence:

| # | Decision | Previous Status | Execution Evidence | Recommendation |
|:-:|----------|----------------|-------------------|----------------|
| 1 | **Cover all 3 pillar branches** | Focus on Loss & Agency | Confirmed: 0 Adaptation queries → skewed data | Add Adaptation queries before next run |
| 2 | **Vectors without GenAI** | 2 generic vectors exist | Not yet tested separately | Keep with "exploratory" label, analyze separately |
| 3 | **Language scope** | English assumed | Confirmed: all collected posts are English | Formalize as inclusion criterion |
| 4 | **Time window** | Undefined | Confirmed: no post dates collected | Add date extraction to collector |
| 5 | **Which script to run** | Two versions exist | 005 (login fix) works; 010 (headline fix) ready | Merge both fixes + query changes into one version |
| 6 | **Platform focus** | Multi-platform planned | LinkedIn-only so far | Keep Phase 1 LinkedIn-only |
| 7 | **Pilot before full run** | 2–3 vector test proposed | 12 runs done but no targeted pilot | Run 2–3 vectors with ALL fixes before full 24 |

---

## 9. Key Numbers

| Metric | Value |
|--------|-------|
| Total runs executed | 12 |
| Successful full collections | 2 (005+007 combined, 011) |
| Total posts collected | 2,280 |
| Posts with headlines | **0** |
| Posts with usable author names | ~35 |
| Bugs found | 7 (2 fixed, 1 ready, 4 not fixed) |
| Feedback items confirmed by execution | 8 |
| Feedback items not yet addressed | 11 |
| New issues found (not in feedback) | 8 |
| Rate limit incidents | 1 |
| Time per full collection | ~57–75 minutes |

---

## 10. Recommended Next Steps

### This Week
1. **Wait for rate limit cooldown** (at least until tomorrow)
2. **Inspect real LinkedIn DOM** for author name extraction — understand why only 17% of names are found
3. **Apply query fixes** from feedback (§3.1–3.4): OR parentheses, Adaptation branch, education vector, three-pillar gaps
4. **Merge all fixes** into one collector version: login fix + headline fix + query changes + date extraction
5. **Run a 2–3 vector pilot** with the merged collector to verify all fixes work

### Before Full Collection
6. Add post date field to schema and extraction
7. Separate search lexicon from sentiment lexicon
8. Add inter-query delays (30–60 seconds)
9. Add scroll checkpointing
10. Freeze the final query list with team approval

### Research & Writing
11. Resolve methodology decisions (deskilling vs. replacement, bimodality test, polarity target, platform bias documentation)
12. Address LinkedIn access/retention questions
13. Update protocol and codebook to match the executed pipeline

---

## 11. File References

| Document | Location |
|----------|----------|
| **This report** | `docs/team-meeting-brief-2026-09-18.md` |
| Full technical report (with diagrams) | `docs/iman-live-pilot-technical-report.md` |
| Kaveh's 10 September feedback (Persian) | `_local/archive/2026-09-10-quality-review/final-feedback-to-team-FA.md` |
| Experiment plan & run table | `experiments/2026-09-17-iman-live-pilot.md` |
| Per-run workflow guide | `experiments/runs/README.md` |
| Individual run records | `experiments/runs/2026-09-17-iman-live-pilot/0XX-*.md` |
| Project log (full history) | `research/project-log.md` |
| Iman's original submission | `_local/submissions/2026-09-06-iman-protocol-drafts/` (local only) |

---

*All raw data, browser profiles, and private artifacts remain local-only. No credentials or personal post content are in any public document. No scientific findings or platform permissions are claimed.*
