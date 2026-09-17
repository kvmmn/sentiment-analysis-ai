# Run 007 — continue queries 23–24

Registered 2026-09-18: **prepared; execution pending**.

- User requested continuation from interrupted [run 005](005-collector-readiness.md). Parent remains preserved, including its incomplete CSV.
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/007-collector-resume/`.
- Parent code SHA-256: `a874e7cf93d7747ab9df9bb6c6e38c05a1f581c945543739a25d18dbd13bc673`.
- Resume code SHA-256: `0279dfa7829fb54bcdace5dc4275d9f095e87b2bd8df96c755bb86abe20bde06`.
- Only collector change from 005: enumerate `QUERY_VECTORS[22:]`, starting at label 23. Replay query 23 from its top, then query 24; 35 scrolls each. There is no saved browser scroll checkpoint. Queries 1–22 are not repeated.
- Input preparation: SQLite backup from a read-only connection to closed 005; verify quick_check and 1,181 rows before/after. Source SHA-256 expected `3e7115cbb2253b648ae746e0aa1c4e77fabecb504d075346842782a52458131e`. Actual input hash and validation saved in private `preparation.json`.
- Separate local copy of closed 005's session, deliberately overriding the default fresh-profile recommendation for this user-requested resume. No credentials printed or shared. No parent DB/profile writes intended.
- Existing upsert prevents duplicate stored post IDs, but does not prove semantic deduplication. Known status-reporting defect and repeated query-provenance append remain unchanged. Counts must come from SQLite, not the “new” counter. Engagement for reobserved IDs may update; source ordering/content may differ.
- Invocation: experiment `run-once.cjs 007-collector-resume collector.py`, which runs repository `.venv/bin/python -u code/collector.py` in the private CWD. Full inventory, branch/dirty state, UTC lifecycle and artifact hashes are captured in private manifest. Two-hour watchdog for this two-query continuation, not the prior one-hour cutoff. No unattended scheduler.
- Validation before launch: exact code diff, Python syntax and query-slice assertions; SQLite snapshot checks. Runtime success remains unverified until completion. Final check: full log query outcomes, database integrity and ID counts, CSV count, preserved parent hash, code-before/after hashes.
- Access challenges must not be bypassed. User authorization is not platform approval. Folders and venv are not a security sandbox. Raw data, profiles and logs remain local-only; retention remains unresolved.
- Analysis is separate and has not started. Final result, net additional records and synchronization: pending.
