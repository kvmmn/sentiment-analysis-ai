# Per-execution run workflow

Every invocation gets a new run ID and record, including retries, failed starts, imports used as tests, and analysis of an earlier collection. An experiment defines a question; a run records one attempt to answer it. Folder preparation is not execution.

## Current queue

**Updated 18 September local.** Two independent full collections confirm the headline bug is reproducible: first run (005+007) 1,237 rows, second run (011) 1,043 rows — both with **0 headlines**. Guarded analysis 008 completed with all stakeholder tests skipped. No stakeholder inference is possible. Git sync pending; no scientific findings or access approval.

| Experiment                                                   | Run record                                                                             | State                                                                                                                                              |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Live pilot](../2026-09-17-iman-live-pilot.md)               | [001-collector](2026-09-17-iman-live-pilot/001-collector.md)                           | Historical assistant-initiated interruption; end/exit and login/count unknown                                                                      |
| Live pilot                                                   | [005-collector-readiness](2026-09-17-iman-live-pilot/005-collector-readiness.md)       | Watchdog stop 22:26:31.760Z; DB 1,181, last CSV 1,178                                                                                              |
| Live pilot                                                   | [007-collector-resume](2026-09-17-iman-live-pilot/007-collector-resume.md)             | 22:36:41.264–22:41:36.978Z, exit 0; queries 23/24 each 35 scrolls, query 23 replay; net +56, not reported “new 62”; quick_check ok                 |
| Live pilot                                                   | [002-analysis](2026-09-17-iman-live-pilot/002-analysis.md)                             | Separate 007 snapshot; 22:44:09.999–22:44:54.104Z, exit 1, empty contingency ValueError; enriched CSV/Parquet 1,237 preserved                      |
| Live pilot                                                   | [008-analysis-guarded](2026-09-17-iman-live-pilot/008-analysis-guarded.md)             | Same logical/hash input; 22:54:15.663–22:54:20.167Z, exit 0; CSV/Parquet 1,237 unique matching IDs; descriptive outputs, stakeholder tests skipped |
| Live pilot                                                   | [009-analysis-guard-tests](2026-09-17-iman-live-pilot/009-analysis-guard-tests.md)     | Synthetic guards 8/8 pass; no live collection                                                                                                      |
| Live pilot                                                   | [010-collector-headline-fix](2026-09-17-iman-live-pilot/010-collector-headline-fix.md) | 3/3 synthetic headline fix tests passed; no live collection                                                                                        |
| Live pilot                                                   | [011-collector-second-run](2026-09-17-iman-live-pilot/011-collector-second-run.md)     | Second full collection, original code; 09:41–10:37 UTC, exit 0; DB/CSV 1,043, 0 headlines — confirms bug reproducible                              |
| [Offline collector](../2026-09-17-iman-collector-offline.md) | [001-integration](../2026-09-17-iman-collector-offline.md#execution-and-provenance)    | Four fake-browser scenarios passed; duplicate-upsert reporting probe FAILED despite exit 0                                                         |

Retry 003 failed at the old selector with zero rows; diagnostic 004 was prepared but not run; 006 observed a signed-in feed. The local session copies in these later attempts are recorded deviations from the fresh-session default, not approval to copy profiles. Upstream artifact hashes validated, parent 005 hash remained unchanged, and analysis input integrity was preserved. Baselines are intact; no new dependencies.

**Next:** a separate tested collector derivative before any recollection. The newline/whitespace source defect was reproduced with an isolated synthetic Node expression only, not a full DOM test. No metadata collector fix, checkpoint implementation or further live run was completed; earlier proposals remain proposals. Private scripts, raw data and profiles stay ignored/local-only.

Earlier synthetic/static checks remain in [project-log section 36](../../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17). The offline integration did not execute real DOM JavaScript or validate the whole collector. Every new invocation requires its own record.

The reused repository `.venv` remains a deviation from the dedicated-environment default below. Collector 001's original manifest retains stale `running` alongside an interruption note; later success does not repair its missing finalization or the offline run's missing full inventory. User authorization is not platform permission.

## Stable layout

- Experiment plan: `experiments/<experiment-id>.md`.
- Public-safe execution record: `experiments/runs/<experiment-id>/<run-id>.md`, copied from [TEMPLATE.md](TEMPLATE.md).
- Private execution workspace: `_local/work/<experiment-id>/runs/<run-id>/`.
- Within each private workspace: `code/` holds this attempt's code snapshot; `logs/` holds terminal output; `corpus_data/` holds the submitted scripts' inputs/outputs. A local `README.md` links to the authoritative public-safe run record. Create artifact folders only when needed.
- **Launch CWD is the run workspace itself**, not the repository root, `code/`, or the original submission. Both scripts resolve `./corpus_data` from CWD. The collector and analysis must have different run workspaces.
- If artifacts are later archived in `data/local/experiments/<experiment-id>/<run-id>/`, record source/destination and hashes; do not silently leave two competing current copies. No archive is required just to launch.

Use date-prefixed experiment IDs and never-reused sequential run IDs such as `001-collector`, `002-collector-retry`. Use a new experiment for a different question or access mode. Dates identify registration, not a fabricated execution date. Link all attempts from the experiment's run table.

## Before each attempt

1. Start an experiment branch from current local `main` as described in the [experiment guide](../README.md). Documentation preparation can be published on `main`; execution and experimental code changes use the experiment branch.
2. Register the new run and choose a **new, unused** workspace. Do not resume an old DB, overwrite tables, reuse logs, or share a browser profile across runs. A deliberate resume is a new run with an explicit parent and input snapshot.
3. Copy only reviewed source files into this run's `code/`. Never run, import, or edit preserved submissions in place. Record source and snapshot SHA-256; list all changes. Freeze the snapshot when execution starts. Fixes/retries require another run.
4. Record exact interpreter path/version, OS/architecture, dependency versions, environment identity, code commit and dirty state, configuration (including embedded constants), seed or lack of one, and a redacted exact invocation and CWD. Use a dedicated virtual environment for the experiment when execution is approved, record its package inventory per run, and do not change it mid-run. A virtual environment isolates packages, not network or filesystem access.
5. Identify permitted input ID/version/split, origin, privacy/access constraints, local path and SHA-256. For an analysis of a previous collection, close the collector DB first, take a consistent SQLite snapshot (including committed WAL content), hash it, and place a separate copy at the analysis workspace's `corpus_data/architectural_discourse.db`. Record the upstream experiment/run and snapshot hashes. Never analyze the live writable DB or silently substitute legacy personal data.
6. Fill all preflight fields in the run template before changing status to `running`. Unresolved execution prerequisites mean `blocked` or `planned`, not an implicit approval. Do not record guessed package versions or invented permission evidence.

## Isolation and permission gates

A folder and `.gitignore` are **not a security sandbox**, encryption, or backup. This workflow isolates artifacts by convention; it does not enforce network denial or prevent code writing elsewhere. Review code before running. Do not describe an offline test as network-isolated unless an actual boundary was configured and verified.

The submitted collector's `main()` opens Chrome and accesses LinkedIn. It has no offline CLI mode and runs its embedded query list. Do not launch it for a folder check or a synthetic test. A later offline collector test needs a reviewed harness/derivative that avoids live entrypoints, fresh synthetic fixtures, and its own record. Live collection needs documented permitted access and a reviewed scope; the current DSA status is not approval.

Importing either submission can create directories; importing the collector also sets up a file log. Analysis reads a DB and writes enriched data/tables, so it needs permitted inputs even though its reviewed entrypoint does not request network access. Scientific claims in source headers are not validation.

Never copy existing browser cookies into a run. Do not capture login secrets. Sessions, logs, personal text, DBs, CSVs and enriched data stay ignored and local; retention and deletion rules still apply. Public records contain only reviewed, non-sensitive metadata. Keep sensitive commands/paths or manifests locally and link a redacted summary; never publish raw traces or package indexes containing tokens.

## During and after each attempt

- Record actual UTC start/end, operator when confirmed, command/CWD, exit code or signal, warnings, exceptions and interruptions. Capture stdout/stderr into separate files under `logs/` without secrets; do not overwrite previous attempts. No unattended scheduler is configured.
- Preserve partial artifacts on failure, subject to privacy rules. Record the failure, not a replacement success. An interrupted process is `interrupted`; a process never started stays `planned`/`blocked`.
- Hash stable inputs before/after, code before/after, output files and reviewed log artifacts after the process exits. Check the input DB did not change unexpectedly. Record row counts/schema checks and expected versus actual outputs. Do not checksum or publish credential material as a reproducibility artifact.
- Finalize the record with measured results, limitations, deviations and validation outcomes. An exit code of zero alone does not establish scientific correctness. Mark unavailable values explicitly and explain why; a closed record with missing evidence is documented as incomplete, not reproducible.
- Review any public summaries/aggregates for privacy, update the experiment run table and material project history, then commit/push reviewed metadata. Raw artifacts and private code snapshots are not backed up by GitHub; arrange only approved local backup/retention separately.
- Once closed, do not overwrite history. Add dated corrections with reasons; link new run IDs for retries. Article and thesis claims cite the exact experiment and run, not just a folder or branch.
