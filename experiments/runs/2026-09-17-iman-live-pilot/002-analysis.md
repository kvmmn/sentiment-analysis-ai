# Run: 2026-09-17-iman-live-pilot/002-analysis

## 2026-09-18 — revised handoff before first execution

The earlier blocked registration below is historical. Analysis 002 has never executed; its intended upstream is now **completed collector 007**, not 001. The user requested continued work after collection. A separate SQLite backup of 007 will be validated before launch: 1,237 rows, matching CSV count, required schema, quick_check, preserved parent 005 hash and upstream artifact hashes. Private `preparation.json` records actual verification and source/input hashes. No browser profile is used by analysis.

The unchanged prepared pipeline will execute through the existing wrapper in its own CWD, with private stdout/stderr and manifest. Known source-reviewed risk: the unguarded chi-square calculation can fail if no rows match target stakeholder cohorts. Failures and partial outputs will be retained, not patched silently. Enriched CSV/Parquet contain personal data and stay local. This is an engineering pilot, not validated inference; access and retention decisions remain unresolved. Actual execution outcome is pending.

## Identity and lifecycle

- [Experiment plan](../../2026-09-17-iman-live-pilot.md) · [Run guide](../README.md) · [Upstream collector](001-collector.md).
- Question: can the prepared analysis pipeline process a separate, consistent, nonempty DB snapshot from collector run 001? Entry point: `code/analysis_pipeline.py`.
- Status: **blocked — waiting for an actual nonempty, consistent DB and input review**. No analysis execution or results are claimed.
- Registered date: 2026-09-17; exact registration time and operator/reviewer: TODO. Actual UTC start/end: not started.
- Mode: planned local analysis of live-pilot output, not an offline synthetic test. User authorization to run the live collector does not establish platform permission or permission for every downstream use.
- Upstream: `2026-09-17-iman-live-pilot/001-collector`; not a retry.
- Private workspace and required launch CWD: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/`.
- Existing [private preparation record](../../../_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/README.md) is local-only. Pending manifest: `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/manifest.json`; not present at documentation inspection.

## Preflight and input handoff

- [x] Prepared code snapshot exists; source/snapshot hashes and newline-only difference documented from preparation evidence.
- [ ] Collector has exited and closed the DB; actual nonempty input, schema and consistency verified.
- [ ] Input provenance and applicable access/use/privacy conditions reviewed. User authorization is not platform permission; no approved research corpus is implied.
- [ ] A consistent SQLite snapshot preserves committed WAL content; procedure and stable source/destination hashes recorded. Separate copy placed at this run's `corpus_data/architectural_discourse.db`.
- [ ] Dataset ID/version, source retrieval window, schema, row counts and input SHA-256 recorded; split stated explicitly (none established yet).
- [ ] Actual branch/base/execution commit, dirty state/diff, frozen code hashes, exact invocation and environment inventory captured.
- [ ] Fresh output workspace, log capture, retention/deletion and expected-output validation reviewed.

Never analyze the live writable collector DB or silently substitute legacy personal data. Preserve the consistent upstream input snapshot independently because analysis may write enriched data/tables; record expected changes and compare hashes after execution. Do not label intended analysis writes as proof that the preserved upstream snapshot changed.

## Code and configuration

- Preserved source: `_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/analysis_pipeline.py`.
- Original SHA-256: `9aed216de9d9c758c6b409dd4736c27fa653ffc9568db332da30cfa28ec02c0f`.
- Prepared snapshot: `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/code/analysis_pipeline.py`.
- Snapshot SHA-256: `1b5d21e6445e5ffc9e4eb190657ec6b1e926c83a02af1f8e5220b9a8b03eb8ad`.
- Change: CRLF-to-LF normalization only, not byte-identical preservation. Source scripts were not modified by this documentation task. Reverify frozen snapshot before/after execution.
- Exact taxonomy/thresholds, options, seed or absence of seed, codebook/protocol version and review status: TODO in manifest. Source claims are not verified methodology.
- Upstream configuration was source-reviewed as 24 queries and 35 scrolls; query version 1 is not frozen. Those are configuration facts, not measured data coverage.

## Environment and execution

- Reused repository environment: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv`; intended interpreter `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python`, Python **3.13.11**; reported host macOS **26.6.2**, **arm64**. Capture actual executed interpreter and relevant hardware per run.
- Reported installations completed: `numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `scikit-posthocs`, `scikit-learn`, `jinja2`. Exact versions, full dependency inventory/path/hash: pending manifest.
- Deviation: existing `.venv` reused rather than a dedicated experiment environment. Installation success does not verify pipeline compatibility. Do not change packages mid-run.
- Exact invocation and actual CWD, UTC start/end, duration, exit code/signal, events/warnings/exceptions: pending, not executed.
- Planned capture root: `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/logs/`; actual stdout/stderr/application-log filenames and hashes: TODO.
- Isolation: organizational/package isolation only; no verified filesystem/network boundary. Reviewed entrypoint has no network request requirement, but that is not enforced network denial. No browser/session reuse is needed for analysis.

## Expected artifacts and validation

These are planned paths relative to the private run workspace, not produced-file claims.

| Artifact                                                                | Actual presence / hash / validation                                         |
| ----------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `corpus_data/architectural_discourse.db` (separate analysis input copy) | Not supplied; consistent snapshot, schema, nonempty rows and hashes pending |
| Enriched data/tables and other pipeline outputs under `corpus_data/`    | Actual names, hashes, sizes, counts and validation pending execution        |
| Captured files under `logs/`                                            | Directory prepared; actual capture files pending                            |
| `manifest.json`                                                         | Pending actual metadata, input/output/code/log hashes and execution outcome |

Validate schema and expected versus actual tables/rows, warnings and input/output provenance; preserve failures and partial artifacts without replacing earlier outcomes. Record before/after input-copy hashes and confirm the independently preserved upstream snapshot remains unchanged. Add local-only links only when files are confirmed present; private links will not resolve in a public clone.

Measured results: **none**. The earlier seven synthetic stakeholder tests used only an AST-extracted taxonomy/function, not this pipeline entrypoint or a DB; they cannot validate statistical methods, sentiment validity or real-data processing. No scientific findings, platform permission or runtime consent are established.

Retention/deletion, permitted downstream use, approved backup (if any), privacy/completeness reviewer and date remain TODO. Keep raw data, credentials and private manifests out of Git. Finalize only from actual evidence after the handoff gates are met; every invocation/retry needs a distinct record.

## Dated amendments

### 2026-09-17 — upstream interruption; analysis not run

Collector 001 actually started and was then interrupted by the assistant without a user request to stop; see its [amendment](001-collector.md#dated-amendments). Its exact end time/exit outcome and final DB count/consistency remain unestablished. PID absence is not a verified clean DB closure or a validated snapshot handoff.

Analysis 002 remains **blocked and not run**. No reviewed nonempty, consistent DB snapshot, input hashes or completed preflight is established; no analysis start/end, exit code or result is claimed. The separate [offline fake-browser collector test](../../2026-09-17-iman-collector-offline.md) did not execute this pipeline and does not satisfy its input gates. Existing preparation sections remain plans, not completed checks.
