# Run 011 — second full collection (original code)

Status: **completed; confirms headline bug is reproducible**. Local date 2026-09-18.

- Second independent full collection using the same 005 code (readiness fix, no headline fix). Fresh database, fresh browser session. All 24 queries, 35 scrolls each.
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/011-collector-second-run/`.
- Code SHA-256: `a874e7cf93d7747ab9df9bb6c6e38c05a1f581c945543739a25d18dbd13bc673` (identical to 005, unchanged before/after).
- Invocation: experiment `run-once.cjs 011-collector-second-run collector.py`, 2-hour watchdog.
- Start `2026-09-18T09:41:08.116Z`; end `2026-09-18T10:37:48.923Z`; duration ~57 minutes; exit **0**; watchdog not triggered.

## Results

| Metric                   | Run 011          | First run (005+007)           |
| ------------------------ | ---------------- | ----------------------------- |
| DB rows                  | **1,043**        | 1,237                         |
| Unique IDs               | 1,043            | 1,237                         |
| SQLite quick_check       | ok               | ok                            |
| CSV rows                 | 1,043            | 1,237                         |
| Headlines populated      | **0**            | **0**                         |
| Author names populated   | 186 (18%)        | 189 (15%)                     |
| Unknown author names     | 140              | 138                           |
| Profile URLs populated   | 903 (87%)        | 1,099 (89%)                   |
| All 24 queries completed | ✅               | ✅ (005 partial + 007 resume) |
| "New records" counter    | 1,084 (inflated) | 62 (inflated)                 |

## Key findings

1. **Headline bug confirmed:** 0 of 1,043 headlines populated — identical to the first run. The `cleanStr`-before-split defect is real and reproducible.

2. **Author name extraction consistently poor:** Only ~17% of names extracted across both runs, with ~75% of those being "Unknown." This is a separate extraction problem beyond the headline fix.

3. **Row count varies between runs:** 1,043 vs 1,237. LinkedIn search results change over time — different ranking, different posts available. This is expected for live search without a frozen index.

4. **UPSERT counter still wrong:** Reports 1,084 "new" vs 1,043 actual rows. Same defect as before.

5. **No watchdog issues:** 57 minutes for all 24 queries fits comfortably in the 2-hour limit.

## Comparison with first run

The second run collected 194 fewer posts (1,043 vs 1,237). Both runs confirm the same bugs: zero headlines, poor author name extraction, inflated "new" counter. The headline fix from Run 010 has not been applied here — this run intentionally used the original code to verify the problems are consistent.

No stakeholder inference is possible from this data. The headline fix (Run 010) and author name extraction improvements are needed before any recollection that could support analysis.
