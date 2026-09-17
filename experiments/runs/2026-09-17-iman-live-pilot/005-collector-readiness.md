# Run 005 — collector readiness fix

Status: **interrupted by the wrapper's one-hour watchdog; partial dataset preserved**. Earlier progress observations below remain historical.

## Verified termination and saved data

- Manifest start: `2026-09-17T21:26:30.869Z`; end: `2026-09-17T22:26:31.760Z` (local date crossed into September 18).
- `watchdog_expired: true`, signal `SIGTERM`, child exit code null; wrapper returned 1. The wrapper timer terminated a progressing run, not a demonstrated page stall or login failure.
- Logs show 22 full 35-scroll sequences. Query 23 reached scroll 28/35; query 24 did not start. No `ERROR`, `interrupted`, or `Traceback` matches were found in stderr during the final check.
- Read-only SQLite `PRAGMA quick_check`: **ok**. Database rows: **1,181**, with **1,181 distinct post_uid values**. This verifies structural consistency and stored-ID uniqueness, not semantic deduplication or extraction quality.
- Last CSV export log reports **1,178 records**, before partial query 23. CSV therefore does not represent the final database; its row count was not independently parsed in this check.
- Manifest records unchanged collector hash before/after and artifact hashes. No completed-run claim, restart, or analysis execution follows from these checks.

## Provenance

- Experiment: [Iman live pilot](../../2026-09-17-iman-live-pilot.md).
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/005-collector-readiness/`.
- Entry point: `.venv/bin/python -u code/collector.py` (absolute interpreter and CWD captured in private manifest); launched through experiment `run-once.cjs`.
- Retry of 003, which exited 1 at `2026-09-17T21:13:36.500Z` after waiting 300000 ms for `nav.global-nav`. Read-only inspection found zero database rows and no CSV in 003.
- Original submission remains unchanged. 003 snapshot SHA-256: `5d06c0f9b25501950cede7211b42416fb80719499b0e4a5d341255331f179386`.
- 005 derivative SHA-256 before launch: `a874e7cf93d7747ab9df9bb6c6e38c05a1f581c945543739a25d18dbd13bc673`.
- Sole collector change: wait for the LinkedIn feed path with visible `main#workspace` and `header nav` (or legacy navigation), and no visible password field. Queries, parsing, SQLite persistence, and limits remain unchanged: 24 queries, 35 scrolls each; random pacing without fixed seed.
- Evidence: separate local diagnostic 006 copied the closed 003 session, opened `/login`, and landed on `/feed/`. Screenshot showed a signed-in feed; structural DOM showed generated navigation classes, not `global-nav`. Diagnostic 006 collected no search corpus. Diagnostic-copy preparation 004 was not executed.
- Session deviation: 005 uses a local copy of closed 003's browser profile, not a fresh login. No corpus database was copied. Credentials were not printed. The generic wrapper's “fresh browser profile” wording is incorrect for this attempt; this amendment and the private README take precedence.
- Python AST syntax and Node wrapper syntax checks passed before launch. Existing repository Python 3.13.11 environment reused; exact inventory, start/end, invocation, branch and dirty state are in the private manifest. Organizational separation is not an OS/network sandbox.

## Observations

- Application log: readiness passed at local `23:26:47` on 2026-09-17.
- Query 1 completed; CSV export logged **59 records** at local `23:29:31`. Query 2 began at `23:29:36` and emitted scroll progress.
- These are intermediate application-log observations, not final independent database validation or research findings.
- Known upsert-status reporting defect remains unfixed; reported “new” counts may include updates. Use final database counts rather than summing those counters.
- `datetime.utcnow()` deprecation warning observed; no fix included in this derivative.
- Terminal wait expired while process continued; this is not a collector failure. Do not terminate the run merely because the terminal wait ended.

## Pending closeout

Lifecycle, quick integrity check and stored row counts are now recorded above. Full schema review, independent artifact-hash verification, CSV parsing, extraction quality and analysis handoff remain pending. Analysis 002 has not run and must have its upstream amended before use. Local authorization is not platform approval; access and retention decisions remain unresolved. Profiles, screenshots, DOM evidence, raw rows, logs and private manifests stay out of shared Git.
