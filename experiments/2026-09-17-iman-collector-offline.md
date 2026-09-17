# Experiment: Iman collector offline integration

## Status and question

- Experiment: `2026-09-17-iman-collector-offline`; retrospective record dated 2026-09-17.
- Invocation: `001-integration`; this file is the public-safe record for that single attempt.
- Outcome: **four fake-browser scenarios passed; duplicate-upsert reporting probe FAILED**. Saved status: `mocked-flow-passed-with-upsert-reporting-defect`. No fixes were applied; the whole collector is not validated.
- Question: does the submitted Python control flow, including query/scroll loops, login-guard branches, error handling, SQLite persistence and CSV export, behave as asserted with synthetic browser responses? Can duplicate persistence accurately report an update?
- Separate from [live collector 001](runs/2026-09-17-iman-live-pilot/001-collector.md), which was interrupted, and live-pilot analysis 002, which remains blocked and not run. Mocked tests are not a substitute for live evidence.

## Evidence, code and inputs

Existing ignored run root: `_local/work/2026-09-17-iman-collector-offline/runs/001-integration/`.

- [Harness: test_integration.py](../_local/work/2026-09-17-iman-collector-offline/runs/001-integration/test_integration.py).
- [Saved result: result.json](../_local/work/2026-09-17-iman-collector-offline/runs/001-integration/result.json), including scenario results, failed probe, artifact paths, recorded hashes and sizes.
- [stdout.log](../_local/work/2026-09-17-iman-collector-offline/runs/001-integration/stdout.log) and [stderr.log](../_local/work/2026-09-17-iman-collector-offline/runs/001-integration/stderr.log): recorded capture locations; hash caveat below.

Links are local-only and do not resolve in a fresh public clone. This documentation task read the existing harness and complete result; it did not rerun either the test or collector.

Preserved source: `_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/collector.py`. Saved source SHA-256: `cd31372b9d0bdff414c0e427b754e0fb52011eb00db604a28142f4a43f61fa37`. Harness SHA-256: `77f41c11e9e502cf8e6608630d67d3037cbc3842336884a12c9df2699f323650`. These are recorded result values, not fresh hashes generated for this amendment. `source_unchanged: true` records the harness's before/after comparison; the original remained unchanged.

The harness reads and parses the full source AST, removes only the `playwright.sync_api` import, executes the remaining module in synthetic module namespaces (not as `__main__`), then explicitly calls its real Python `main()` in each scenario's private CWD. This is not merely an extracted helper-function unit test, and not a normal unmodified module import or live browser execution. Browser dependencies are replaced with fakes; only browser I/O, `time.sleep` and `random.uniform` behavior are patched. Sleeps become no-ops and random delays become the range midpoint. Submitted Python loop, data-processing, SQLite and CSV code executes against synthetic records.

`page.evaluate` returns fake records or counts a scroll: **real DOM JavaScript is NOT run**, even though the parser-script argument is checked. No Playwright import, browser process, actual login or network access is requested by the harness. This is mocked I/O, not verified OS/network sandboxing. Scenario names describe synthetic states, not the live user's authentication state.

Fixtures are generated in the harness: per-query synthetic records and one repeated shared record, using `example.invalid` URLs. No personal post dump, live dataset or train/validation/test split is involved. Fixture identity is tied to the recorded harness hash; no scientific sampling protocol or frozen query version is established.

## Execution and provenance

- Start: **2026-09-17T20:53:36.102645Z**.
- End: **2026-09-17T20:53:36.568489Z**.
- These are harness-recorded boundaries (`+00:00` in the result), not independently captured shell process boundaries; the end field is assigned before artifact enumeration and final result printing.
- Launch CWD: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/_local/work/2026-09-17-iman-collector-offline/runs/001-integration`.
- Command from that CWD: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python test_integration.py > stdout.log 2> stderr.log` (repository `.venv/bin/python`). Terminal context records **exit 0 despite the semantic failed probe**.
- Result records Python **3.13.11**, Clang 17.0.0 build. Existing repository `.venv` was reused, not a dedicated experiment environment.
- Offline-run branch, execution/base commit, dirty diff, exact OS/browser version and per-run full package inventory were not captured in this result: **unavailable/TODO**. Do not assign live collector 001's commit or inventory to this separate invocation without evidence. No browser version applies to the fake implementation.

## Observed results

All counts below concern synthetic fixtures only; none is a live collection count.

| Fake-browser scenario    | Scenario assertions                                                     | Attempted queries | Parser calls / scrolls | SQLite rows | Fake browser closed |
| ------------------------ | ----------------------------------------------------------------------- | ----------------: | ---------------------: | ----------: | ------------------- |
| `already-authenticated`  | Passed                                                                  |                24 |              840 / 840 |          25 | Yes                 |
| `manual-login-completes` | Passed                                                                  |                24 |              840 / 840 |          25 | Yes                 |
| `login-timeout`          | Passed; expected `Synthetic login timeout`                              |                 0 |                  0 / 0 |           0 | Yes                 |
| `first-query-fails`      | Passed; simulated first navigation failure, continued remaining queries |                24 |              805 / 805 |          24 | Yes                 |

The harness checks SQLite integrity, deduplicated row counts, shared-record query provenance, engagement totals and CSV row-count parity for scenarios with successful queries. The timeout scenario expects no CSV. Browser closure is a fake object's flag, not a real process-lifecycle assertion.

**Separate duplicate-upsert reporting probe: FAILED.** On a fresh probe DB, the first `persist_record` call returned `inserted`; the second call for the same record with another query also returned `inserted`, whereas the expected second return was `updated`. This is evidence of a return-status/reporting defect, not proof that every database update failed. The harness records the boolean failure and mixed status instead of raising an assertion for that probe, so shell exit 0 does not mean all checks passed. No correction or rerun is claimed.

## Artifacts and hash limitations

The result inventory records synthetic DB/CSV/application logs under the four scenario directories, `already-authenticated/upsert_probe.db`, top-level stdout/stderr, and the harness, with SHA-256 and byte sizes. The timeout scenario has a DB and application-log entry, but no CSV. Raw artifacts remain ignored/local; `result.json` is excluded from its own inventory.

**Capture-time hash caveat:** the harness hashes artifacts in its `finally` block before the final `print` and before stdout/stderr and logging streams have finally closed. The result/manifest inventory's hash for the then-live `stdout.log` is therefore not a final-output hash (it records an empty file before printing the result). Other still-open log hashes are capture-time values, not certified final hashes. Some per-scenario application logs are recorded as empty; do not infer no scenario activity from that. No hashes or original artifacts were silently replaced, and no final rehash was performed by this documentation task.

## Interpretation and next steps

This supports only the asserted Python paths with these synthetic responses. It does not validate real DOM selectors/parser JavaScript, Playwright integration, Chrome lifecycle, actual login, network access, extraction quality, live collection totals, scientific validity or platform permission. It does not resolve the interrupted live collector's missing end/exit provenance or analysis handoff.

Record the reporting defect for a separately authorized fix and a new run ID; preserve this mixed result. Any subsequent real-browser test requires its own scope and access review. Analysis 002 remains blocked pending reviewed, nonempty, consistent upstream input; no analysis was run here. No code changes, commands, tests, installs, browser actions, commits or pushes were performed by this documentation update.
