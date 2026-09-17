# Saintiment code index

Updated: 2026-09-17. Start here to find code; use the [experiment guide](../experiments/README.md) before running it. Organization is not an execution result or collection permission.

| Component                    | Location                                                                                                                                                                  | Status                                                                               |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Existing LinkedIn scraper    | [README](linkedin-scraper/README.md), [script](linkedin-scraper/scraper.py), [requirements](linkedin-scraper/requirements.txt), [keywords](linkedin-scraper/keywords.txt) | Legacy exploratory; engineering runs in September; not an approved research pipeline |
| Iman’s collector             | See submission links below                                                                                                                                                | Submitted Python extract; unrun here; not adopted shared implementation              |
| Iman’s analysis pipeline     | See submission links below                                                                                                                                                | Submitted prototype; unrun here; not verified results                                |
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
2. Create an experiment plan/branch following the [experiment guide](../experiments/README.md). Preserve the submission. Make a clearly recorded editable derivative under `_local/work/<experiment-id>/` when implementation work begins; none has been created by this reorganization.
3. Review imports, side effects, dependencies and file paths before executing or importing. Both submitted scripts use CWD-relative `corpus_data/`; imports can create directories. Ignore rules protect that name but do not isolate execution or make it safe.
4. Record baseline and derivative SHA-256, code changes, environment, working directory and inputs/outputs. Use permitted synthetic inputs for the first offline check. Do not silently reuse the legacy personal-data CSV.
5. Promote only reviewed, publishable code into a named `src/<component>/` with its own dependency specification and entry-point documentation. Do not publish the private submission manifest or pretend code has been tested.

No new dependencies, test harness, code modifications or script execution were introduced. See the [project map](../docs/project-map.md) for stable filing and provenance rules.
