# Experiments

Start with the **[per-invocation run guide](runs/README.md)** and **[Iman live-pilot record](2026-09-17-iman-live-pilot.md)**. **Current status — 18 September local / 17 September UTC executions:** watchdog-stopped [005](runs/2026-09-17-iman-live-pilot/005-collector-readiness.md) was followed by completed [007 resume](runs/2026-09-17-iman-live-pilot/007-collector-resume.md): 1,237 DB/CSV rows and unique stored IDs, net +56. Analysis 002 failed on an empty contingency table; separate [008 guarded analysis](runs/2026-09-17-iman-live-pilot/008-analysis-guarded.md) completed with enriched data and descriptive/status outputs. [009 synthetic guards](runs/2026-09-17-iman-live-pilot/009-analysis-guard-tests.md) passed 8/8 without live collection.

**Engineering completion with missing metadata, not scientific findings:** all 1,237 headlines are empty and all stakeholder labels are `Unclassified`; Kruskal/Dunn/chi-square were skipped for insufficient stakeholder data. Guards do not repair missing fields. A source newline/whitespace defect was reproduced only in an isolated synthetic Node expression, not a full DOM test. Prepare a separate tested collector derivative before any recollection; no metadata fix, checkpoint implementation or further live run was completed. Baselines are intact, no new dependencies were added, and Git sync is pending. Raw data, private scripts and profiles remain ignored/local-only. User authorization is not platform permission.

The separate **[offline collector experiment](2026-09-17-iman-collector-offline.md)** records invocation `001-integration`: four fake-browser scenarios passed, but the duplicate-upsert reporting probe **FAILED** despite exit 0. Real Python loop/SQLite/CSV paths ran; real DOM JavaScript did not. No fixes or whole-collector validation are claimed, and mocked tests do not substitute for live evidence. Two earlier synthetic/static checks remain in [project-log section 36](../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17); do not relabel these checks, the September scraper tests or the sent letter as completed live-pilot runs.

Use one Markdown file per experiment, named `YYYY-MM-DD-short-name.md`, adding a suffix if necessary to keep names unique. Copy the template below, and register every invocation using the [run template](runs/TEMPLATE.md). For the current pilot, private artifacts belong under `_local/work/2026-09-17-iman-live-pilot/runs/<run-id>/`, not the optional archive destination in the general template. Its reused repository `.venv` is an explicit deviation from the dedicated-environment recommendation. Collector 001's inventory and launch metadata are recorded; its original manifest remains stale `running` with a separate interruption note, not a fabricated finalized outcome. Missing fields remain explicit in each record.

## How to start a professional experiment

Keep this path small: git + this template. Do not add CI, experiment databases, or research-agent workspaces unless the team later adopts them. [OpenResearch](https://github.com/alphaXiv/OpenResearch) is only an optional later suggestion in Kaveh’s [sent letter](../research/team/team-feedback-to-team-2026-09-15-FA.md); it is not required here. See the [code index and submission-review path](../src/README.md) and [project migration map](../docs/project-map.md).

1. **Update `main`.** With a clean working tree, fetch remote changes, switch to local `main`, and fast-forward it to `origin/main`. Stop and reconcile if the branches have diverged; do not discard local changes or check out `origin/main` as a detached HEAD. This keeps the run based on the current shared record.
2. **New branch per experiment.** Create `experiment/YYYY-MM-DD-short-name` from that `main`. Do not mix two experimental questions on one branch. Do not commit results onto `main` until the record is filled and reviewed.
3. **Record before you run.** Copy the template into `experiments/YYYY-MM-DD-short-name.md`. Fill **Question or Hypothesis**, **Data** (planned dataset ID, version, split), and **Configuration and Execution** (method, parameters, commands) while they are still plans. Link the [data guide](../data/README.md) and any dataset entry.
4. **Review submissions before adoption.** Iman’s package is now at `_local/submissions/2026-09-06-iman-protocol-drafts/`; follow the review path in the [code index](../src/README.md). Treat archived/submitted extracts, including folders named `working-copies/`, as immutable evidence: never edit or run them in place. Use `_local/work/<experiment-id>/` as the editable **LOCAL** workspace convention for a reviewed copy; record its source path, source SHA-256, changes, and resulting code hash. Local copies are not automatically adopted code under `src/`.
5. **Code version.** After the branch exists, record the commit that will be executed (`git rev-parse HEAD`). If you change code on the branch, record the commit you actually ran, not an earlier one. Point at adopted files under `src/` (legacy scraper: `src/linkedin-scraper/`) or explicitly identified local working copies. A repository commit alone does not identify ignored local code; record exact file SHA-256 hashes too.
6. **Separate test plans and permissions.** Plan offline synthetic tests separately from any live collection, with separate records, inputs, and outputs. Offline tests must not log in, access live platforms, or use personal post dumps, and cannot establish live retrieval quality or access permission. A query list is not a collection licence. The LinkedIn DSA case remains Open on last evidence. Exploratory scraper CSVs stay git-ignored and are not an approved research corpus. Any live pilot requires a separately reviewed plan and permitted access; this guide authorizes no collection or execution.
7. **Record after a permitted run.** Fill actual execution details, input/output hashes and artifact paths, results, and limitations. Leave unmeasured values as TODO. If the run fails, keep the record with status `failed` and link a follow-up file; do not overwrite the failed record with a later success. Planned per-experiment output location: `data/local/experiments/<id>/`; no directories or artifacts are created by this guide.
8. **Private data stays out.** Credentials, session files, and personal post dumps do not belong in the record or in git. Describe paths and row counts without pasting profile text.

The 2026-09-03/04 scraper sessions in the [project log](../research/project-log.md), under **“24. Integrate team scraper and run first controlled test (2026-09-03)”**, are engineering tests. The log retains another historical section numbered 24, so use the full heading to identify this record. If a similar run is repeated as a professional experiment, start a **new** branch and a **new** file here; do not silently replace those log notes.

Both the [article](../writing/article.md) and [thesis](../writing/thesis.md) should reference these records when reporting results.

## Experiment Template

```text
# Experiment: TODO

## Status and Date
TODO: planned / running / completed / failed; date of execution.

## Git
TODO: branch name (`experiment/YYYY-MM-DD-short-name`);
base commit of main; commit actually executed.

## Question or Hypothesis
TODO: what this experiment is intended to test.

## Data
TODO: dataset ID, exact version, preprocessing, and train/validation/test splits.
Link to the dataset documentation in ../data/README.md.
If no permitted dataset exists yet, say so; do not invent one.
TODO: offline synthetic inputs or separately permitted live collection;
input artifact paths and SHA-256 hashes; source provenance and access conditions.

## Code Version
TODO: commit ID of the code that ran, plus the files/scripts used.
TODO: original submission/archive source path and source SHA-256, if applicable;
editable local copy path (_local/work/<experiment-id>/), changes from source,
and SHA-256 of each executed file (including code not tracked by git).

## Configuration and Execution
TODO: method, parameters, random seeds, evaluation metrics, command or steps,
launch working directory, actual start/end time and execution outcome.
TODO: environment identifier/path, OS and architecture, interpreter/runtime version,
exact dependency versions and dependency manifest/lockfile path and SHA-256
(or a version inventory if no lockfile exists), and relevant hardware.

## Results
TODO: actual measurements and links to supporting artifacts.
TODO: output artifact paths and SHA-256 hashes, including logs and failure artifacts;
planned local output directory: data/local/experiments/<id>/.
Leave unmeasured results and hashes as TODO; do not substitute expected values.

## Interpretation and Limitations
TODO: observations, uncertainty, failures, and limits on conclusions.

## Next Steps
TODO: follow-up questions or links to subsequent experiment records.
```
