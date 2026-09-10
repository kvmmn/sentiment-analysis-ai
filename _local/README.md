# `_local/`

Local-only workspace. **Git tracks only this README.** Everything else here stays on this machine.

## Layout

| Path | What belongs here |
| --- | --- |
| `archive/` | Keep: team notes, run reports, transcripts we may reuse |
| `scraper/` | Helper scripts and leftover logs from LinkedIn scraper tests |
| `out-of-scope/` | Files that landed in this folder by mistake (not Saintiment work) |

Scratch scripts can sit under `scraper/scripts/` until they graduate to `src/` or `experiments/`. Do not put credentials here.

## Archive index (2026-09-10)

| Folder | Contents |
| --- | --- |
| `archive/2026-09-10-quality-review/` | Critique memo; meeting brief; file01–03 one-pagers; **whole Iman-package summary**; OpenResearch note |
| `archive/2026-09-08-telegram-team-update/` | Telegram discussion summary (`saintiment-update-Sep8.md`) plus provenance |
| `archive/2026-09-06-iman-protocol-drafts/` | Iman’s Drive folder snapshot (protocol, query matrix, codebook, manifest, collector/analysis scripts). Review copies in `working-copies/`. Not run. |
| `archive/2026-09-04-scraper-reports/` | Controlled scraper tests, full run, session checkpoint, Persian narrative of those tests |

## Relationship to other folders

| Folder | Visibility | Purpose |
| --- | --- | --- |
| `_local/` | Local only | Scratch work and local archive |
| `tmp/pdfs/` | Git-ignored | LinkedIn form/app evidence PDFs and one-off renders |
| `data/` | Git-ignored contents | Structured datasets (`data/README.md`) |
| `linkedin-scraper/` | Mixed | Shared script/README/keywords; session, DB, and logs ignored |
| `experiments/` | Tracked | Reproducible experiment records |
| `src/` | Tracked | Project source code |

## Rules

- Do not put credentials, API keys, or secrets here — use environment variables or a gitignored `.env` at the project root.
- When work matures, copy the publishable part to `src/`, `experiments/`, or `research/` and commit that copy.
- Keep `archive/` until the source is in the shared record or Kaveh says it can go.
