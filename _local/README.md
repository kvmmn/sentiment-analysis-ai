# \_local/

This folder is for **local-only work** that stays on your machine and is never committed to GitHub.

## Purpose

- Temporary scripts, notebooks, and experiments not ready for the shared repository
- Local configuration overrides and environment-specific files
- Draft notes, scratch work, and personal reference material
- Test outputs and intermediate results before they graduate to `data/` or `experiments/`

## Rules

- **Everything in this folder is git-ignored** except this README.
- Do not put credentials, API keys, or secrets here — use environment variables or a `.env` file (also git-ignored at the project root).
- When work here matures, move it to the appropriate shared location (`src/`, `experiments/`, `research/`, etc.) and commit it properly.
- Delete stale files; this is not a permanent archive.

## Relationship to other folders

| Folder         | Visibility           | Purpose                                              |
| -------------- | -------------------- | ---------------------------------------------------- |
| `_local/`      | Local only           | Scratch work, temporary experiments                  |
| `data/`        | Git-ignored contents | Structured datasets (documented in `data/README.md`) |
| `experiments/` | Tracked              | Reproducible experiment records                      |
| `src/`         | Tracked              | Project source code                                  |
| `tmp/`         | Git-ignored          | Temporary PDFs and one-off files                     |
