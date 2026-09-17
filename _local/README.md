# Local workspace index

Updated: 2026-09-17. **Git tracks only this README.** Other contents are ignored and are not available in a fresh public clone. Ignore rules are not encryption, backup, or permission to retain personal data.

## Find Iman’s code

The complete submission moved from `archive/` to **[submissions/2026-09-06-iman-protocol-drafts/](submissions/2026-09-06-iman-protocol-drafts/)**.

- [Collector](submissions/2026-09-06-iman-protocol-drafts/working-copies/collector.py)
- [Analysis pipeline](submissions/2026-09-06-iman-protocol-drafts/working-copies/analysis_pipeline.py)
- [Source provenance](submissions/2026-09-06-iman-protocol-drafts/SOURCE.md) and [relocation/hashes](submissions/2026-09-06-iman-protocol-drafts/RELOCATION.md)
- [Code index and pre-test checklist](../src/README.md)

These are preserved submission extracts, not entrypoints to run in place. The inherited name `working-copies/` does not make them the active editing location. Keep the baseline intact; use separate experiment-specific snapshots.

## Current run workspaces

Use the [per-invocation guide](../experiments/runs/README.md) and [live-pilot plan](../experiments/2026-09-17-iman-live-pilot.md).

- `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/`: LF-normalized snapshot was launched, then interrupted by the assistant without a user request to stop; see [public record](../experiments/runs/2026-09-17-iman-live-pilot/001-collector.md). Exact end/exit provenance is incomplete; login/count unknown. The [original manifest](work/2026-09-17-iman-live-pilot/runs/001-collector/manifest.json) remains stale `running`; read with the separate [interruption note](work/2026-09-17-iman-live-pilot/runs/001-collector/interruption-note.md).
- `_local/work/2026-09-17-iman-live-pilot/runs/002-analysis/`: prepared LF-normalized snapshot; [public record](../experiments/runs/2026-09-17-iman-live-pilot/002-analysis.md) remains blocked and not run pending reviewed nonempty, consistent input. No finalized input handoff is established.
- `_local/work/2026-09-17-iman-collector-offline/runs/001-integration/`: existing [harness](work/2026-09-17-iman-collector-offline/runs/001-integration/test_integration.py) and [result](work/2026-09-17-iman-collector-offline/runs/001-integration/result.json); see [offline record](../experiments/2026-09-17-iman-collector-offline.md). Four fake-browser scenarios passed; duplicate-upsert reporting probe failed; no real DOM JavaScript or fixes. The offline test's still-open log hashes are capture-time, not certified final values.
- Collector launch metadata, package inventory and logs are present; missing final hashes/end/exit fields are not fabricated. Analysis metadata remains pending execution. Fresh-profile and separate consistent DB-copy requirements are not inferred to be verified merely from launch.
- Earlier synthetic check: [test script](work/2026-09-17-iman-analysis-unit/runs/001-stakeholder/test_stakeholder.py) and [result](work/2026-09-17-iman-analysis-unit/runs/001-stakeholder/result.json); seven cases passed, not a full pipeline run. See [section 36](../research/project-log.md#36-document-earlier-checks-and-register-the-live-pilot-2026-09-17) for CWD deviation and the separate ad-hoc static check's missing metadata.

## Layout

| Path                                 | What belongs here                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| `submissions/YYYY-MM-DD-short-name/` | Incoming source packages, original exports, reading extracts and provenance     |
| `archive/YYYY-MM-DD-short-name/`     | Historical reviews, reports and team summaries; not current implementation      |
| `work/<experiment-id>/`              | Editable local derivatives for one recorded experiment; create only when needed |
| `scraper/scripts/`                   | Earlier local helper scripts; review old path assumptions before reuse          |
| `scraper/logs/`                      | Historical engineering logs                                                     |

Do not store new work at the root of `_local/`. A stray out-of-scope file is not a project artifact; ask before moving it outside this project or deleting it.

## Preserved records

| Location                                                        | Contents and status                                                                                                                         |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [Iman submission](submissions/2026-09-06-iman-protocol-drafts/) | Protocol, matrix, codebook, manifest, collector and analysis exports/extracts; submitted, not an adopted release                            |
| [Quality review](archive/2026-09-10-quality-review/)            | Critique, meeting brief, one-pagers, whole-package summary and optional OpenResearch note; dated working material                           |
| [Telegram summary](archive/2026-09-08-telegram-team-update/)    | Summary plus provenance; not signed minutes. Companion drafts are now in the submission folder                                              |
| [Scraper reports](archive/2026-09-04-scraper-reports/)          | Engineering tests, full-run report and checkpoint; historic results, not an approved research corpus                                        |
| `archive/2026-09-10-csv-history-purge/`                         | Private backup associated with the CSV history purge; retention/access conditions still apply; contents not inspected during reorganization |

The registered [sent 15 September letter](../research/team/team-feedback-to-team-2026-09-15-FA.md) supersedes the local September 10 feedback draft. Keep the earlier draft as history, not a second current letter.

## Boundaries

- [Project map](../docs/project-map.md) defines stable locations and the old → new mapping. Archived text may retain paths that were valid when written; consult the mapping rather than executing old commands unchanged.
- Private developer-console evidence and renders remain in `tmp/pdfs/`; datasets belong under `data/local/` when permitted.
- `src/linkedin-scraper/` contains the shared legacy script and ignored runtime files as a documented exception. Nothing from its session, DB, CSV or logs should be published.
- Do not add secrets to documents. Use environment variables or an ignored root `.env` for configuration, with appropriate access controls.
- Publish only reviewed, authorized derivatives to `src/`, `research/`, or `experiments/`; preserve source provenance. Do not publish private source manifests wholesale.
- Preserve historical evidence subject to source-specific privacy and retention requirements. Do not silently overwrite or delete originals; record authorized corrections/deletions when required.
