# Experiment: Iman live collector pilot

## Current status and question — 18 September 2026 local

Experiment `2026-09-17-iman-live-pilot` was registered on 17 September (exact registration time unavailable). Question: can the collector produce a usable local database, and can analysis process a separate consistent snapshot? **Collection resume and guarded analysis completed as engineering runs, with missing metadata; no stakeholder inference, scientific findings or access approval.** All execution timestamps below are **2026-09-17 UTC**, corresponding to local September 18 for these events.

Workflow: [per-invocation guide](runs/README.md), [experiment guide](README.md), [data handling](../data/README.md).

## Current invocation results

| Run                                                                                     | Verified outcome                                                                                                                                             |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [001-collector](runs/2026-09-17-iman-live-pilot/001-collector.md)                       | Historical assistant-initiated interruption without user stop request; end/exit and login/count unknown                                                      |
| [005-collector-readiness](runs/2026-09-17-iman-live-pilot/005-collector-readiness.md)   | Watchdog stopped at 22:26:31.760Z; DB 1,181, last CSV 1,178                                                                                                  |
| [007-collector-resume](runs/2026-09-17-iman-live-pilot/007-collector-resume.md)         | 22:36:41.264–22:41:36.978Z, exit 0; queries 23 and 24 each completed 35 scrolls (23 replayed); DB/CSV 1,237 and 1,237 distinct IDs; quick_check ok           |
| [002-analysis](runs/2026-09-17-iman-live-pilot/002-analysis.md)                         | Separate snapshot from 007, not 001; 22:44:09.999–22:44:54.104Z, exit 1: empty contingency ValueError; enriched CSV/Parquet 1,237 preserved, input unchanged |
| [008-analysis-guarded](runs/2026-09-17-iman-live-pilot/008-analysis-guarded.md)         | Separate guarded derivative, same logical/hash input; 22:54:15.663–22:54:20.167Z, exit 0; CSV/Parquet 1,237, unique matching IDs, all `Unclassified`         |
| [009-analysis-guard-tests](runs/2026-09-17-iman-live-pilot/009-analysis-guard-tests.md) | Synthetic guards 8/8 pass; no live collection                                                                                                                |

003 failed on the old selector with zero rows; 004 was prepared but not run; 006 diagnosed a signed-in feed with changed navigation classes. Session copies are explicit deviations from the original fresh-profile plan, not changes to the default policy. Upstream artifact hashes validated; parent 005 hash remained unchanged. The actual 007 database increase is **+56**, not the inflated “new 62” upsert counter. Stored-ID uniqueness does not establish semantic deduplication.

008 produced five-aspect descriptives, contingency CSV, LaTeX tables 1 and 3, and inferential-status JSON. **Kruskal, Dunn and chi-square were all skipped for insufficient stakeholder data.** The guarded run preserves useful engineering outputs but does not repair missing fields or supply statistical findings.

## Metadata limitation and next action

All **1,237 `author_headline` values are empty**. CSV `author_name` is nonempty in 189 rows, including 138 `Unknown`; profile URL is nonempty in 1,099 rows. These fields do not rescue stakeholder inference: all 1,237 rows are `Unclassified`.

Source diagnosis: whitespace is normalized before splitting on newline, preventing next-line headline extraction. An isolated synthetic Node expression reproduced the defect **ad hoc, not as a full DOM test**. Recommend a **separate tested collector derivative before any recollection**. No metadata collector fix, checkpoint implementation or further live run was made; prior assistant proposals are not completed work. The earlier 005 readiness change is distinct from this unimplemented metadata fix.

Baselines are intact; no new dependencies. Raw data, private scripts, profiles and sensitive evidence remain ignored/local-only. Git synchronization is pending; this update claims no commit or push. Research access, retention and privacy obligations remain unresolved; technical execution and user authorization are not platform approval.

## Historical original plan and 001 amendment — 17 September 2026

**Everything below preserves the original plan and the earlier 001 interruption amendment, not current status.** In particular, “002 blocked/not run,” its planned 001 input, pending handoff and fresh-profile assumptions were superseded by the results and deviations above. Historical preparation hashes and 001 evidence gaps remain valid for those specific snapshots/attempts, not later derivatives. The separate run records retain failures rather than replacing them with 008's success.

## Authorization and scope

The user explicitly authorized the local live collector run on 2026-09-17. **User authorization is not platform permission.** No LinkedIn permission, research/API approval, runtime consent, or retention exception is established by this instruction, the source code, or the earlier login-guard check. See the [access record](../research/access/linkedin-application-worksheet.md). Access conditions and unresolved permission evidence must remain explicit in the execution record.

Source review identified **24 embedded queries and 35 scrolls**; these are configuration values, not observed retrieval counts. Query version 1 is **not frozen**. The pilot does not adopt a scientific sampling protocol. Use a fresh browser profile; do not reuse cookies, previous sessions, databases, or legacy scraper CSVs. Actual fresh-profile use remains to be verified at launch. Do not bypass access challenges; record interruptions and stop conditions rather than treating login success as permission.

## Registered invocations

| Run                                                               | Purpose                                             | Status                                                                        |
| ----------------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------- |
| [001-collector](runs/2026-09-17-iman-live-pilot/001-collector.md) | Live collector attempt in its own private workspace | Interrupted by assistant; end/exit provenance incomplete; login/count unknown |
| [002-analysis](runs/2026-09-17-iman-live-pilot/002-analysis.md)   | Analyze a separate consistent snapshot from 001     | Blocked and not run; nonempty consistent input and review not established     |

Every invocation, including failed starts, imports used as tests and retries, needs its own record. Never overwrite an earlier attempt. Earlier synthetic stakeholder and static login-guard checks are separate historical checks in [project-log section 36](../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17), not executions of these two runs.

## Source and prepared snapshots

Preserved source root: `_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/`. Private run root: `_local/work/2026-09-17-iman-live-pilot/runs/`.

| Script                 | Original SHA-256                                                   | Prepared snapshot SHA-256                                          | Snapshot location under private run root |
| ---------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ | ---------------------------------------- |
| `collector.py`         | `cd31372b9d0bdff414c0e427b754e0fb52011eb00db604a28142f4a43f61fa37` | `5d06c0f9b25501950cede7211b42416fb80719499b0e4a5d341255331f179386` | `001-collector/code/collector.py`        |
| `analysis_pipeline.py` | `9aed216de9d9c758c6b409dd4736c27fa653ffc9568db332da30cfa28ec02c0f` | `1b5d21e6445e5ffc9e4eb190657ec6b1e926c83a02af1f8e5220b9a8b03eb8ad` | `002-analysis/code/analysis_pipeline.py` |

Snapshots already exist. The documented difference is CRLF-to-LF normalization only: hashes differ, so they are not byte-identical originals. No source-script edits are part of this documentation task. Hashes above are supplied preparation evidence, not a fresh verification by this task. Recheck frozen code before/after execution and capture actual metadata in each private `manifest.json`.

## Environment and provenance

**2026-09-17 amendment:** collector 001's existing local manifest records branch `experiment/2026-09-17-iman-live-pilot`, checkout `966de34c010b10f3b711df0e2cd17487ac8d3fe5` with dirty tracked/untracked documentation, actual `.venv/bin/python -u code/collector.py` invocation from the collector CWD, start `2026-09-17T20:49:14.700Z`, code-before/wrapper hashes and exact package inventory. The repository `.venv` was reused: Python **3.13.11**, macOS **26.6.2**, **arm64**, including Playwright **1.62.0**. This remains a deviation from the dedicated-environment recommendation, not validation.

The wrapper was killed before finalization. The original manifest is preserved with stale `running` status; a separate local interruption note records the stop sequence and missing provenance. Exact end, duration, actual exit outcome, post-run code/artifact hashes, browser version and independent profile-freshness verification remain unavailable. Package inventory is no longer pending for 001; do not infer an analysis execution inventory from it. No commands or Git operations are performed by this documentation amendment.

## Input handoff and expected artifacts

Collector CWD: `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/`; analysis CWD: `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/`. Both scripts resolve `corpus_data/` from CWD, not from the source directory.

Do not launch analysis until the collector is closed and an actual nonempty DB has passed schema/consistency and input-access review. Preserve committed SQLite WAL content using a consistent snapshot procedure; hash the stable source snapshot and separate destination copy. Record upstream run, dataset version, row counts, schema, copy procedure and hashes. Do not analyze the live writable DB. No train/validation/test split is established; record actual usage without inventing one.

Collector metadata is present: local [original manifest](../_local/work/2026-09-17-iman-live-pilot/runs/001-collector/manifest.json) and [interruption note](../_local/work/2026-09-17-iman-live-pilot/runs/001-collector/interruption-note.md). Read them together; the note does not rewrite the original manifest. Analysis metadata path remains pending: `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/manifest.json`; analysis has not run. Public summaries must contain no credentials, cookies or personal rows; local evidence links are unavailable in a fresh clone.

## Results, limitations and next steps

The user reported login; no independent login success or failure is established. Before the assistant-initiated stop the last observed application log contained only DB initialization and a manual-login warning; stderr subsequently showed EPIPE. These observations establish neither collected count nor final DB usability. No live DB count/consistency check or analysis result is recorded. Sending TERM and subsequently observing no PID does not establish graceful DB closure; handoff gates remain unmet.

The separate [offline experiment](2026-09-17-iman-collector-offline.md) records four passing fake-browser scenarios using real Python/SQLite/CSV paths and a **failed duplicate-upsert reporting probe**. Real DOM JavaScript was not run. No fixes or whole-collector validation are claimed; mocked tests do not substitute for the interrupted live run. No scientific finding or platform permission follows from either attempt.

Next: preserve the interruption evidence and unknown fields; review access and any potential DB handoff before deciding on further execution. Do not resume 001 or treat a new run as already authorized by this amendment; a retry needs a new ID. Analysis remains blocked and not run. Retention/deletion scope and any approved backup remain TODO; privacy obligations apply to partial outputs and logs too. Raw artifacts remain private and are not backed up by the public repository.
