# Saintiment project map

Structure adopted: 2026-09-17. Start at the [root README](../README.md) for current status. This file defines locations and traceability, not research approval or individual team roles.

## Where things belong

| Location                      | Responsibility                                                                               | Visibility               |
| ----------------------------- | -------------------------------------------------------------------------------------------- | ------------------------ |
| `README.md`                   | Short current status and next actions; entry point                                           | Public                   |
| `research/README.md`          | Research navigation and current versus historical methods                                    | Public                   |
| `research/notes.md`           | Working questions and synthesis; decisions link to evidence                                  | Public                   |
| `research/keywords/`          | Literature queries, discourse retrieval and coding vocabulary kept distinct                  | Public                   |
| `research/access/`            | Access applications, conditions and privacy reviews; no credentials                          | Public summaries         |
| `research/team/`              | Authorized correspondence and confirmed decisions; dated, not inferred from drafts           | Public-safe records      |
| `research/references.md`      | Stable source IDs, citations, links and reading limitations                                  | Public                   |
| `research/project-log.md`     | Material actions, decisions, reasons, verification and open issues                           | Public                   |
| `research/initial-scratch.md` | Original research sketch; preserve bytes                                                     | Public historical source |
| `src/`                        | Shared editable code, each component with status, dependencies and entry-point documentation | Public                   |
| `experiments/`                | Dated plans and immutable completed/failed run records                                       | Public-safe metadata     |
| `data/README.md`              | Dataset registry and handling rules; no personal records                                     | Public                   |
| `data/local/`                 | Versioned raw/derived inputs and experiment artifacts, created when needed                   | Ignored                  |
| `writing/`                    | Article and thesis; both cite the same source and experiment IDs                             | Public drafts            |
| `assets/`                     | Public artwork and its provenance, not data dumps                                            | Public                   |
| `docs/`                       | Project navigation and public derived presentations; HTML catalog is dated                   | Public                   |
| `_local/submissions/`         | Preserved incoming packages plus provenance and extracts                                     | Ignored                  |
| `_local/archive/`             | Dated past reports, reviews and team summaries                                               | Ignored                  |
| `_local/work/`                | Editable work for a named experiment, created when needed                                    | Ignored                  |
| `_local/scraper/`             | Historical local helpers and logs; not the main pipeline                                     | Ignored                  |
| `tmp/pdfs/`                   | Existing private access evidence and temporary renders                                       | Ignored                  |
| `.venv/`                      | Local environment, not a source or dependency specification                                  | Ignored                  |

Only `_local/README.md` is tracked under `_local/`. Local-only links are available on this machine, not in a fresh public clone. Git ignore is neither encryption nor backup nor permission to retain personal data. Existing source-specific deletion requirements still apply to archives and backups.

## Find a task

- **Read or test Iman’s submission:** [code index](../src/README.md#imans-submission-local-only); open the preserved script, then plan a test. Do not execute a submission in place.
- **Find the current retrieval decision:** [research index](../research/README.md), not the historical HTML catalog.
- **Find what was actually sent:** [15 September letter](../research/team/team-feedback-to-team-2026-09-15-FA.md); the September 10 local letter is a superseded draft.
- **Start a run:** [experiment guide](../experiments/README.md), [per-invocation run guide](../experiments/runs/README.md), and [current live-pilot plan](../experiments/2026-09-17-iman-live-pilot.md). No run is implied by creating a folder or plan; user authorization is not platform permission.
- **Locate earlier September scraper results:** [local archive index](../_local/README.md). These are engineering reports, not findings from an approved corpus.
- **Check access status:** [application record](../research/access/linkedin-application-worksheet.md). Last evidence is not a live inbox check.

Current pilot private roots are `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/` and `002-analysis/` under the same `runs/` directory. Public records are `experiments/runs/2026-09-17-iman-live-pilot/001-collector.md` and `002-analysis.md`; each invocation gets its own record and workspace. Collector 001 was interrupted; its original `manifest.json` is preserved with stale `running` status and a separate `interruption-note.md`, not silently finalized. Analysis remains blocked and not run pending a reviewed nonempty, consistent snapshot. The separate [offline collector record](../experiments/2026-09-17-iman-collector-offline.md) points to existing ignored `_local/work/2026-09-17-iman-collector-offline/runs/001-integration/` artifacts; it is not live-run validation. See the linked records for outcomes and evidence gaps.

## Source → code → experiment → writing

1. **Receive:** use `_local/submissions/YYYY-MM-DD-short-name/`. Keep source exports and extracts together; `SOURCE.md` records source, receipt/export dates and limitations. Preserve original bytes. Add a separate manifest rather than rewriting the submitted text.
2. **Review:** distinguish submitted claims from verified facts. Record which protocol, query matrix and codebook versions are being considered. A received document is not an adopted protocol.
3. **Prepare:** use experiment ID `YYYY-MM-DD-short-name`, record in `experiments/<id>.md`, branch `experiment/<id>`. An offline synthetic check and a live collection pilot are separate questions/records. Keep local editable submission derivatives in `_local/work/<id>/`; publish reviewed derivatives under a clearly named `src/<component>/` only when appropriate.
4. **Trace:** record source path and SHA-256, derivative changes and hash/commit, exact dependencies/environment, working directory, configuration/seed, permitted input ID/version/split, execution steps and output locations/hashes. Untracked code needs hashes in addition to the repository commit. Never imply a hash validates extraction fidelity or scientific correctness.
5. **Preserve:** raw inputs are not overwritten by preprocessing. Planned data layout is `data/local/<dataset-id>/<version>/raw/` and `derived/`; experiment artifacts use `data/local/experiments/<experiment-id>/`. Create only when needed. Keep failed records and link follow-up attempts.
6. **Report:** the article and thesis cite references and completed experiment records; figures/tables record generating code and input versions. Publish only reviewed, permitted aggregates/assets, not personal raw data. Mark unsupported claims TODO.

## Status and naming rules

Use explicit labels: **submitted**, **draft**, **working choice**, **planned**, **running**, **completed**, **failed**, **superseded**. A code component may be **legacy exploratory** without being production-ready. Include a date and supporting record for a status change. Do not infer individual ownership or authorship.

Keep stable names after registration. Revisions to shared working documents use Git history; new submitted versions receive new dated folders. Do not use ambiguous `final`, `latest`, or `v2-final` names for future records. Keep original incoming filenames inside their identified package. Never overwrite an earlier execution record with a later success.

Avoid duplicate current-status documents: root README is the short dashboard; topic notes hold detail; project log is the history. Index files provide links rather than copied evidence. Update indexes and links whenever a material move is necessary. Do not add empty taxonomy folders or infrastructure just to match this map.

## Relocations — 17 September 2026

| Previous path                                     | Stable current path                                                                           |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `linkedin-scraper/`                               | `src/linkedin-scraper/` (whole package, including ignored runtime artifacts)                  |
| `_local/archive/2026-09-06-iman-protocol-drafts/` | `_local/submissions/2026-09-06-iman-protocol-drafts/` (whole submission, unchanged originals) |
| `research/keyword-systems.md`                     | `research/keywords/keyword-systems.md`                                                        |
| `research/keyword-lexicon.md`                     | `research/keywords/keyword-lexicon.md`                                                        |
| `research/keyword-discourse-catalog.md`           | `research/keywords/keyword-discourse-catalog.md`                                              |
| `research/keyword-literature-strings.md`          | `research/keywords/keyword-literature-strings.md`                                             |
| `research/keyword-source-identification.md`       | `research/keywords/keyword-source-identification.md`                                          |
| `research/keywords-search-storage.md`             | `research/keywords/keywords-search-storage.md`                                                |
| `research/linkedin-application-worksheet.md`      | `research/access/linkedin-application-worksheet.md`                                           |
| `research/linkedin-data-access-review.md`         | `research/access/linkedin-data-access-review.md`                                              |
| `research/privacy-policy-review.md`               | `research/access/privacy-policy-review.md`                                                    |
| `research/team-feedback-to-team-2026-09-15-FA.md` | `research/team/team-feedback-to-team-2026-09-15-FA.md`                                        |

Earlier September moves: `_local/scraper-test-log.md`, `_local/full-run-2026-09-04.md`, and `_local/coordination-meeting-report.md` now belong to `_local/archive/2026-09-04-scraper-reports/`; `_local/analyze_csv.py` is `_local/scraper/scripts/analyze_csv.py`. Archived prose may retain paths at the time. Consult this mapping rather than creating duplicate copies or executing historical commands unchanged.

The existing scraper retains outputs/session files beside its script as a **legacy exception**, protected by ignore rules. Its local helper scripts may still assume older paths; they were not repaired or executed by this organization task. A later test must review path assumptions explicitly. No code behavior, extraction fidelity or runtime compatibility is certified by these moves.
