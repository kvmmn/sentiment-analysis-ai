# Local workspace index

Updated: 2026-09-17. **Git tracks only this README.** Other contents are ignored and are not available in a fresh public clone. Ignore rules are not encryption, backup, or permission to retain personal data.

## Find Iman’s code

The complete submission moved from `archive/` to **[submissions/2026-09-06-iman-protocol-drafts/](submissions/2026-09-06-iman-protocol-drafts/)**.

- [Collector](submissions/2026-09-06-iman-protocol-drafts/working-copies/collector.py)
- [Analysis pipeline](submissions/2026-09-06-iman-protocol-drafts/working-copies/analysis_pipeline.py)
- [Source provenance](submissions/2026-09-06-iman-protocol-drafts/SOURCE.md) and [relocation/hashes](submissions/2026-09-06-iman-protocol-drafts/RELOCATION.md)
- [Code index and pre-test checklist](../src/README.md)

These are preserved, unrun submission extracts. The inherited name `working-copies/` does not make them the active editing location. Keep the baseline intact; prepare an experiment-specific derivative when a test task begins.

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
