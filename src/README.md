# Saintiment code index

Updated: 2026-10-16. Start here to find code; use the [experiment guide](../experiments/README.md), [per-invocation run guide](../experiments/runs/README.md) and [live-pilot record](../experiments/2026-09-17-iman-live-pilot.md) before running it. Organization is not collection permission.

**Current engineering state:** Neon `_saintiment_db` holds the three-provider pilot (Apify + Coresignal + Bright Data; see [project log §48](../research/project-log.md#48-complete-three-provider-set-synced-2026-10-16)). September Iman live-pilot closeout remains historical: after watchdog-stopped 005, [007](../experiments/runs/2026-09-17-iman-live-pilot/007-collector-resume.md) completed with 1,237 DB/CSV rows; [008](../experiments/runs/2026-09-17-iman-live-pilot/008-analysis-guarded.md) / [009](../experiments/runs/2026-09-17-iman-live-pilot/009-analysis-guard-tests.md) documented empty headlines and `Unclassified` stakeholders.

A source bug normalizes whitespace before splitting on newline, preventing next-line headline extraction. An isolated synthetic Node expression reproduced this, not a full DOM test. A separate tested collector derivative is recommended before recollection; no metadata fix, checkpoint implementation or further live run was completed. Baselines remain intact; no new dependencies. No scientific findings or access approval are claimed. Private scripts, raw data and profiles stay ignored/local-only; Git sync is pending.

**Historical evidence:** initial 001/002 preparation changed line endings only; later derivatives have their own provenance. 001's interruption remains incompletely finalized. The [offline collector test](../experiments/2026-09-17-iman-collector-offline.md) passed four fake-browser scenarios but failed its duplicate-upsert reporting probe, without running real DOM JavaScript. Earlier AST/static checks remain in [project-log section 36](../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17); none establishes whole-collector validation.

| Component                    | Location                                                                                                                                                                  | Status                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Existing LinkedIn scraper    | [README](linkedin-scraper/README.md), [script](linkedin-scraper/scraper.py), [requirements](linkedin-scraper/requirements.txt), [keywords](linkedin-scraper/keywords.txt) | Legacy exploratory; engineering runs in September; not an approved research pipeline |
| Iman’s collector             | See submission links below                                                                                                                                                | Baseline intact; 007 resume completed; missing metadata; not adopted                 |
| Iman’s analysis pipeline     | See submission links below                                                                                                                                                | 002 failed; separate 008 guards completed; no stakeholder inference                  |
| Kaveh's analytical pipeline  | [README](analysis/README.md), [script](analysis/kaveh_analytical_pipeline.py), [tests](analysis/tests/test_kaveh_pipeline.py)                                               | Verified independent implementation; 7/7 unit tests pass; pilot run on Run 013      |
| Provider-data ingest (Apify to Neon) | [load script](ingest/apify_to_neon.py), [CSV export](ingest/export_master_csv.py) | Apify load 2026-10-07; Coresignal and Bright Data loaded 2026-10-08 by local/ad-hoc scripts (not yet promoted to `src/ingest/`); Neon holds apify 1,137 + coresignal 200 + brightdata 200 master posts (verified 2026-10-16); needs `psycopg[binary]` and `DATABASE_URL` (secret, never committed); no tests |
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
