# Team Swipe Review (Vercel)

Three reviewers (1. مرتضی, 2. ایمان, 3. کاوه) each go through their own third of the
1,858 Apify LinkedIn posts once and mark each one keep or reject. Every decision is saved
straight away to a shared Neon database, so anyone can stop and continue later from any
device.

- **UI:** `public/index.html`, a single page for phone and laptop. Swipe right or press ✓ for keep, swipe left or press ✕ for reject, ↩ to undo.
- **API:** `server.js` (Express). Routes: `POST /api/login`, `GET /api/sets`, `GET /api/posts?set=N`, `PUT /api/decision`, `GET /api/export`.
- **DB:** Neon database `_saintiment_swipe_team_db`. It has three tables: `reviewers`, `posts` (with `reviewer_id` and `position`), and `decisions`.

The post text lives only in Neon, never in this public repo. Everything except the login
needs the team-password session cookie.

## One-time setup

1. Seed the DB from the local three-layer SQLite (fixed-seed shuffle, giving sets of 620 / 619 / 619):
   ```bash
   python3 src/ingest/build_team_swipe_db.py
   ```
   The script refuses to reseed once decisions exist; `--force` wipes them.
2. Vercel project `kercel274/sentiment-analysis-ai` settings:
   - **Root Directory:** empty (repo root, where `vercel.json` lives)
   - **Framework Preset:** Services
   - **Deployment Protection:** off for production. Otherwise teammates hit a Vercel login wall before the team password.
3. Environment variables (Production + Preview):
   | Name | Value |
   |---|---|
   | `DATABASE_URL` | output of `python3 src/ingest/build_team_swipe_db.py --print-url` |
   | `TEAM_PASSWORD` | the shared team password |
   | `SESSION_SECRET` | random, e.g. `openssl rand -hex 32` |

## Local run

```bash
cd web/swipe && npm install
node --env-file=/path/to/swipe.env server.js   # http://localhost:3000
```

## Getting results back into the pipeline

```bash
python3 src/ingest/export_team_decisions.py
python3 src/ingest/build_curated_db.py data/local/linkedin-apify-2026-10-17/saintiment_swipe_decisions.json --push-neon
```
