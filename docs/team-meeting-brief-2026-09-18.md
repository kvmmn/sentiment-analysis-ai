# Saintiment — Iman Live Pilot: Team Meeting Brief

**18 September 2026** · Prepared for team discussion

---

## Executive Summary

We ran Iman Sheikhansari's collector and analysis pipeline for the first time. **12 runs** across two days. The collector works — we collected **1,043–1,237 posts** per full run across 24 LinkedIn search queries. But we found **three critical bugs** that prevent the analysis from producing stakeholder-level results. Two are fixed, one needs more work. The headline fix is ready but couldn't be verified on real LinkedIn due to rate limiting.

**Bottom line for the meeting:** The pipeline is functional but the data it produces is incomplete. We know exactly what's broken and how to fix it. The question is: do we fix and recollect, or adjust the research approach?

---

## 1. What We Ran

Iman submitted two Python scripts extracted from Google Docs:

| Script                 | Purpose                                                                                                                                                       | Lines |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| `collector.py`         | Opens Chrome, logs into LinkedIn, runs 24 search queries, scrolls 35 times each, saves posts to SQLite + CSV                                                  | ~490  |
| `analysis_pipeline.py` | Reads the database, classifies stakeholders by headline, scores sentiment per aspect, runs Kruskal-Wallis / Dunn / Chi-Square tests, exports tables and LaTeX | ~290  |

We **never edited the originals**. Every run used a separate copy in its own folder. All changes are tracked with SHA-256 hashes.

---

## 2. All 12 Runs at a Glance

### Collection Runs

| Run     | Date/Time (UTC)      | What                            | Result                             | Rows      | Headlines |
| ------- | -------------------- | ------------------------------- | ---------------------------------- | --------- | --------- |
| **001** | Sep 17, 20:49        | First attempt                   | Interrupted by assistant (mistake) | Unknown   | —         |
| **003** | Sep 17, 21:08        | Retry with original code        | **Failed** — old login selector    | 0         | —         |
| **005** | Sep 17, 21:26–22:26  | Fixed login check               | Watchdog stopped at query 23       | **1,181** | 0         |
| **007** | Sep 17, 22:36–22:41  | Resume queries 23–24            | Completed, exit 0                  | **1,237** | 0         |
| **011** | Sep 18, 09:41–10:37  | Second full run (original code) | Completed, exit 0                  | **1,043** | 0         |
| **012** | Sep 18, ~12:42–13:53 | Fixed headline collector        | **Rate-limited** mid-run           | **257**   | 0         |

### Analysis & Test Runs

| Run     | Date/Time (UTC) | What                            | Result                                                   |
| ------- | --------------- | ------------------------------- | -------------------------------------------------------- |
| **002** | Sep 17, 22:44   | Original analysis on 1,237 rows | **Crashed** — empty contingency table                    |
| **008** | Sep 17, 22:54   | Guarded analysis (same data)    | Completed; all 3 tests **skipped** (no stakeholder data) |
| **009** | Sep 17          | Synthetic guard tests           | **8/8 passed**                                           |
| **010** | Sep 17          | Headline fix synthetic tests    | **3/3 passed**                                           |

### Diagnostic Runs

| Run     | What               | Result                                               |
| ------- | ------------------ | ---------------------------------------------------- |
| **004** | Diagnostic prep    | Not executed                                         |
| **006** | Browser diagnostic | Confirmed login works; LinkedIn changed HTML classes |

---

## 3. The Three Bugs We Found

### Bug 1: Login Selector — LinkedIn Changed Their HTML ✅ FIXED

**What happened:** The original code waits for `nav.global-nav` to appear. LinkedIn no longer uses that CSS class. The collector timed out after 5 minutes.

**The fix (Run 005):** Replaced the CSS selector with a JavaScript function that checks:

- URL is `linkedin.com/feed`
- A visible navigation bar exists
- No password field is visible (meaning we're already logged in)

**Status:** Fixed and verified. Works reliably.

---

### Bug 2: Headline Extraction — Whitespace Collapses Before Line Split 🔧 FIX NEEDS LIVE TEST

**What happened:** All 2,280 posts across two full runs had **zero headlines**. The analysis crashed because it couldn't classify any stakeholders.

**Root cause — one line of JavaScript:**

```javascript
// WHAT THE CODE DOES (broken):
const fullCard = cleanStr(card.innerText);
// cleanStr collapses ALL whitespace → "Kaveh Momeni Architect Post text"
const textLines = fullCard.split('\n')...  // Only 1 line! No "next line" for headline

// WHAT IT SHOULD DO (fixed):
const textLines = (card.innerText || '').split('\n')...  // Split FIRST, then clean each line
// Result: ["Kaveh Momeni", "Architect", "Post text"] — 3 lines, headline found!
```

**The fix (Run 010):** One expression changed. 3/3 synthetic tests passed (Node.js unit, Playwright browser, SQLite persistence).

**Status:** Fix is ready but **not verified on real LinkedIn**. Run 012 (which had the fix) was rate-limited before we could check.

---

### Bug 3: Author Name Extraction — Only ~17% Success Rate 🔴 NOT FIXED

**What we found across two full runs:**

|                     | Run 005+007 | Run 011   |
| ------------------- | ----------- | --------- |
| Total posts         | 1,237       | 1,043     |
| Author names found  | 189 (15%)   | 186 (18%) |
| Of those, "Unknown" | 138 (73%)   | 140 (75%) |
| Profile URLs found  | 1,099 (89%) | 903 (87%) |
| **Headlines found** | **0**       | **0**     |

The author name extraction is failing **independently** of the headline bug. Even when a name is found, 3 out of 4 times it's "Unknown." The headline lookup depends on finding the author name first, then taking the next line — so both problems compound.

Profile URLs are the most reliable field (~88% populated). This suggests the DOM elements exist but the text extraction logic isn't matching them.

---

## 4. Other Issues Found

### UPSERT Counter Is Wrong

The collector reports "1,084 new records" when only 1,043 were actually stored. The SQLite `UPSERT` returns `rowcount = 1` for both inserts AND updates. **Always count the database, not the application log.**

### No Scroll Checkpointing

If the collector is interrupted mid-query, it restarts that query from scroll 1. Run 007 replayed query 23 from the top. A simple file-based checkpoint would prevent this.

### Rate Limiting

Three back-to-back runs triggered LinkedIn's anti-scraping detection:

> _"Our systems have detected unusual search traffic. Search activity has been paused."_

Run 012 collected only 257 posts before being blocked. We need:

- Longer delays between queries (currently 4–8 seconds)
- Time between runs (hours, not minutes)
- Possibly fewer queries per session

### Row Counts Vary Between Runs

1,237 vs 1,043 posts across two full runs. LinkedIn search results change over time — different ranking, different available posts. This is expected for live search.

---

## 5. What the Analysis Can and Cannot Do

### What Works

- Loads the database and enriches all rows
- Scores aspect-based sentiment (5 aspects: Deskilling, Creativity, Cognitive Judgment, Technical/Environmental, Representation/BIM)
- Produces descriptive statistics per aspect
- Exports enriched CSV, Parquet, and LaTeX tables

### What Doesn't Work (Without Headlines)

- **Stakeholder classification** — all rows are `Unclassified`
- **Kruskal-Wallis test** — needs ≥2 stakeholder groups with ≥3 members each
- **Dunn post-hoc test** — needs significant Kruskal result
- **Chi-Square test** — needs a non-empty stakeholder × stance contingency table

The guarded analysis (Run 008) handles all these gracefully — it skips unsupported tests and records why, rather than crashing.

---

## 6. Data Quality Summary

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

Usable for analysis?     NO            NO
```

**The data is structurally valid but semantically incomplete.** We have post content, engagement metrics, and URLs — enough for content analysis. But we cannot do stakeholder-level statistics.

---

## 7. What We Recommend

### Short-term (this week)

1. **Wait for rate limit cooldown** (at least until tomorrow)
2. **Test the headline fix on a single query** with a fresh session and longer delays
3. **Investigate author name extraction** — inspect the real LinkedIn DOM to understand why names aren't being found
4. **If the fix works:** run a full collection with the fixed collector
5. **If it doesn't:** consider alternative approaches (manual annotation, different extraction strategy)

### Medium-term

6. **Add scroll checkpointing** to the collector
7. **Fix the UPSERT counter**
8. **Add inter-query delays** (30–60 seconds) to avoid rate limiting
9. **Freeze the query list** — the team's proposed changes (OR parentheses, Adaptation + downskilling, education/H4, three-pillar labels) should be applied before the next full collection

### Research decisions needed

10. **Is stakeholder classification from headlines the right approach?** If headlines are inherently unreliable, we may need manual annotation or a different strategy.
11. **What's the minimum viable dataset?** Do we need all 24 queries, or can we start with a subset?
12. **Access and retention:** LinkedIn DSA case is still open. What's our plan if formal access isn't granted?

---

## 8. Key Numbers for the Meeting

| Metric                         | Value                              |
| ------------------------------ | ---------------------------------- |
| Total runs executed            | 12                                 |
| Successful full collections    | 2 (005+007, 011)                   |
| Total posts collected          | 2,280 (across both full runs)      |
| Posts with headlines           | **0**                              |
| Posts with usable author names | ~35 (across both runs)             |
| Bugs found                     | 3 (1 fixed, 1 ready, 1 needs work) |
| Rate limit incidents           | 1                                  |
| Time per full collection       | ~57–75 minutes                     |
| Code changes made              | 2 (login fix, headline fix)        |
| Original code preserved        | Yes — never edited                 |

---

## 9. Files to Reference

| Document                              | Location                                                           |
| ------------------------------------- | ------------------------------------------------------------------ |
| Full technical report (with diagrams) | `docs/iman-live-pilot-technical-report.md`                         |
| Experiment plan & run table           | `experiments/2026-09-17-iman-live-pilot.md`                        |
| Per-run workflow guide                | `experiments/runs/README.md`                                       |
| Individual run records                | `experiments/runs/2026-09-17-iman-live-pilot/0XX-*.md`             |
| Project log (full history)            | `research/project-log.md`                                          |
| Iman's original submission            | `_local/submissions/2026-09-06-iman-protocol-drafts/` (local only) |

---

_All raw data, browser profiles, and private artifacts remain local-only. No credentials or personal post content are in any public document. No scientific findings or platform permissions are claimed._
