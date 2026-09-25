# Saintiment code index

Updated: 2026-09-18 local (executions on 2026-09-17 UTC). Start here to find code; use the [experiment guide](../experiments/README.md), [per-invocation run guide](../experiments/runs/README.md) and [live-pilot record](../experiments/2026-09-17-iman-live-pilot.md) before running it. Organization is not collection permission.

**Current engineering state:** after watchdog-stopped 005, [007](../experiments/runs/2026-09-17-iman-live-pilot/007-collector-resume.md) completed with 1,237 DB/CSV rows and unique stored IDs (net +56). Analysis 002 failed on an empty contingency table; separate [008 guarded analysis](../experiments/runs/2026-09-17-iman-live-pilot/008-analysis-guarded.md) completed with 1,237 enriched rows and descriptive/status outputs. [009 synthetic guards](../experiments/runs/2026-09-17-iman-live-pilot/009-analysis-guard-tests.md) passed 8/8 without live collection. All author headlines are empty and all stakeholder labels are `Unclassified`: no stakeholder inference is possible. The guard skips unsupported tests; it does not repair metadata.

A source bug normalizes whitespace before splitting on newline, preventing next-line headline extraction. An isolated synthetic Node expression reproduced this, not a full DOM test. A separate tested collector derivative is recommended before recollection; no metadata fix, checkpoint implementation or further live run was completed. Baselines remain intact; no new dependencies. No scientific findings or access approval are claimed. Private scripts, raw data and profiles stay ignored/local-only; Git sync is pending.

**Historical evidence:** initial 001/002 preparation changed line endings only; later derivatives have their own provenance. 001's interruption remains incompletely finalized. The [offline collector test](../experiments/2026-09-17-iman-collector-offline.md) passed four fake-browser scenarios but failed its duplicate-upsert reporting probe, without running real DOM JavaScript. Earlier AST/static checks remain in [project-log section 36](../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17); none establishes whole-collector validation.

| Component                    | Location                                                                                                                                                                  | Status                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Existing LinkedIn scraper    | [README](linkedin-scraper/README.md), [script](linkedin-scraper/scraper.py), [requirements](linkedin-scraper/requirements.txt), [keywords](linkedin-scraper/keywords.txt) | Legacy exploratory; engineering runs in September; not an approved research pipeline |
| Iman’s collector             | See submission links below                                                                                                                                                | Baseline intact; 007 resume completed; missing metadata; not adopted                 |
| Iman’s analysis pipeline     | See submission links below                                                                                                                                                | 002 failed; separate 008 guards completed; no stakeholder inference                  |
| Kaveh's analytical pipeline  | [README](analysis/README.md), [script](analysis/kaveh_analytical_pipeline.py), [tests](analysis/tests/test_kaveh_pipeline.py)                                               | Verified independent implementation; 7/7 unit tests pass; pilot run on Run 013      |
| Earlier local helper scripts | `_local/scraper/scripts/`                                                                                                                                                 | Historical utilities; path assumptions need review before reuse                      |

## Iman’s submission (local-only)

**Package:** `_local/submissions/2026-09-06-iman-protocol-drafts/`

- [Collector Python extract](../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/collector.py)
- [Analysis pipeline Python extract](../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/analysis_pipeline.py)
- [Protocol](../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/01_STUDY_PROTOCOL_AND_METHODOLOGY.txt)
- [Query matrix and taxonomy](../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/02_SEARCH_QUERY_MATRIX_AND_TAXONOMY.txt)
- [Annotation codebook](../_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/03_ANNOTATION_CODEBOOK_AND_GUIDELINES.txt)
- [Original provenance](../_local/submissions/2026-09-06-iman-protocol-drafts/SOURCE.md)
- [Relocation and integrity record](../_local/submissions/2026-09-06-iman-protocol-drafts/RELOCATION.md)

These links intentionally target ignored local material; they will not work in a fresh public clone. The `.py.docx` files are Word exports of Google Docs; `working-copies/*.py` are preserved Python extracts, not a separate validated release. Despite the old folder name, **do not edit these baseline extracts in place**.

### Before a test

1. Identify the question and whether the test is offline/synthetic or needs live external access. No live collection is authorized by this index.
2. Create an experiment plan/branch following the [experiment guide](../experiments/README.md). Preserve the submission. Use a clearly recorded derivative under `_local/work/<experiment-id>/runs/<run-id>/code/`; the current pilot's prepared snapshots are identified in its plan.
3. Review imports, side effects, dependencies and file paths before executing or importing. Both submitted scripts use CWD-relative `corpus_data/`; imports can create directories. Ignore rules protect that name but do not isolate execution or make it safe.
4. Record baseline and derivative SHA-256, code changes, environment, working directory and inputs/outputs. Use permitted synthetic inputs for the first offline check. Do not silently reuse the legacy personal-data CSV.
5. Promote only reviewed, publishable code into a named `src/<component>/` with its own dependency specification and entry-point documentation. Do not publish the private submission manifest or pretend code has been tested.

The earlier reorganization introduced no dependencies, harness or script execution. Historical preparation/checks remain in section 36; later attempts and current limitations are in the linked pilot/run records. Collector 001's original manifest and separate interruption note retain its incomplete finalization; later completion does not fill those gaps. This documentation update makes no source changes or experiment executions. See the [project map](../docs/project-map.md) for stable filing and provenance rules.
