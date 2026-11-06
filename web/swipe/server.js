// Saintiment Team Swipe Review API (Express on Vercel).
// Static UI lives in public/; every /api route except login requires the signed session cookie.
// Env: DATABASE_URL (Neon _saintiment_swipe_team_db), TEAM_PASSWORD, SESSION_SECRET.
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';
import { neon } from '@neondatabase/serverless';

const COOKIE = 'swipe_session';
const SESSION_DAYS = 30;
const REVIEWER_IDS = new Set([1, 2, 3]);

let sqlClient;
function sql() {
  if (!process.env.DATABASE_URL) throw new Error('DATABASE_URL is not set');
  sqlClient ??= neon(process.env.DATABASE_URL);
  return sqlClient;
}

function secret() {
  const s = process.env.SESSION_SECRET;
  if (!s || s.length < 16) throw new Error('SESSION_SECRET is not set (min 16 chars)');
  return s;
}

function sign(payload) {
  return crypto.createHmac('sha256', secret()).update(payload).digest('base64url');
}

function safeEqual(a, b) {
  const ba = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  return ba.length === bb.length && crypto.timingSafeEqual(ba, bb);
}

function makeToken() {
  const payload = Buffer.from(JSON.stringify({ exp: Date.now() + SESSION_DAYS * 864e5 })).toString('base64url');
  return `${payload}.${sign(payload)}`;
}

function validToken(token) {
  if (!token || !token.includes('.')) return false;
  const [payload, mac] = token.split('.');
  if (!safeEqual(mac, sign(payload))) return false;
  try {
    return JSON.parse(Buffer.from(payload, 'base64url').toString()).exp > Date.now();
  } catch {
    return false;
  }
}

function readCookie(req, name) {
  for (const part of String(req.headers.cookie || '').split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return decodeURIComponent(v.join('='));
  }
  return null;
}

function requireSession(req, res, next) {
  if (validToken(readCookie(req, COOKIE))) return next();
  res.status(401).json({ error: 'unauthorized' });
}

const app = express();
app.disable('x-powered-by');
app.use(express.json({ limit: '32kb' }));
app.use('/api', (req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

app.post('/api/login', async (req, res) => {
  const expected = process.env.TEAM_PASSWORD;
  if (!expected) return res.status(500).json({ error: 'TEAM_PASSWORD is not set' });
  const given = String(req.body?.password || '');
  if (!safeEqual(given, expected)) {
    await new Promise(r => setTimeout(r, 600)); // slow down guessing
    return res.status(401).json({ error: 'wrong_password' });
  }
  const secure = req.headers['x-forwarded-proto'] === 'https' ? '; Secure' : '';
  res.set(
    'Set-Cookie',
    `${COOKIE}=${makeToken()}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}${secure}`
  );
  res.json({ ok: true });
});

app.post('/api/logout', (req, res) => {
  res.set('Set-Cookie', `${COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`);
  res.json({ ok: true });
});

app.get('/api/me', requireSession, (req, res) => res.json({ ok: true }));

app.get('/api/sets', requireSession, async (req, res, next) => {
  try {
    const rows = await sql()`
      SELECT r.id, r.name, r.name_en,
             count(p.source_post_id)::int AS total,
             count(d.source_post_id) FILTER (WHERE d.status = 'keep')::int AS keep,
             count(d.source_post_id) FILTER (WHERE d.status = 'reject')::int AS reject,
             max(d.updated_at) AS last_activity
      FROM reviewers r
      LEFT JOIN posts p ON p.reviewer_id = r.id
      LEFT JOIN decisions d ON d.source_post_id = p.source_post_id
      GROUP BY r.id, r.name, r.name_en
      ORDER BY r.id`;
    res.json({ sets: rows });
  } catch (e) {
    next(e);
  }
});

app.get('/api/posts', requireSession, async (req, res, next) => {
  const set = Number(req.query.set);
  if (!REVIEWER_IDS.has(set)) return res.status(400).json({ error: 'bad_set' });
  try {
    const rows = await sql()`
      SELECT p.source_post_id, p.position, p.post_type, p.post_url, p.posted_at, p.post_text, p.text_chars,
             p.author_type, p.author_name, p.author_headline, p.author_url,
             p.reactions, p.comments, p.shares, p.media,
             p.matched_query_count, p.matched_query_codes, p.matched_families,
             d.status AS decision, d.updated_at AS decided_at, d.decided_by
      FROM posts p
      LEFT JOIN decisions d ON d.source_post_id = p.source_post_id
      WHERE p.reviewer_id = ${set}
      ORDER BY p.position`;
    res.json({ set, posts: rows });
  } catch (e) {
    next(e);
  }
});

app.put('/api/decision', requireSession, async (req, res, next) => {
  const id = String(req.body?.source_post_id || '');
  const status = req.body?.status ?? null;
  const by = REVIEWER_IDS.has(Number(req.body?.by)) ? Number(req.body.by) : null;
  if (!id) return res.status(400).json({ error: 'missing_id' });
  if (status !== null && status !== 'keep' && status !== 'reject') {
    return res.status(400).json({ error: 'bad_status' });
  }
  try {
    if (status === null) {
      await sql()`DELETE FROM decisions WHERE source_post_id = ${id}`;
      return res.json({ ok: true, source_post_id: id, status: null });
    }
    const rows = await sql()`
      INSERT INTO decisions (source_post_id, reviewer_id, status, decided_by)
      SELECT p.source_post_id, p.reviewer_id, ${status}, ${by} FROM posts p WHERE p.source_post_id = ${id}
      ON CONFLICT (source_post_id) DO UPDATE
        SET status = EXCLUDED.status, decided_by = EXCLUDED.decided_by, updated_at = now()
      RETURNING source_post_id, status, updated_at`;
    if (!rows.length) return res.status(404).json({ error: 'unknown_post' });
    res.json({ ok: true, ...rows[0] });
  } catch (e) {
    next(e);
  }
});

app.get('/api/export', requireSession, async (req, res, next) => {
  try {
    const rows = await sql()`
      SELECT d.source_post_id, d.status, d.updated_at, d.reviewer_id, d.decided_by, r.name_en
      FROM decisions d JOIN reviewers r ON r.id = d.reviewer_id
      ORDER BY d.source_post_id`;
    const [{ total }] = await sql()`SELECT count(*)::int AS total FROM posts`;
    const decisions = {};
    for (const r of rows) {
      decisions[r.source_post_id] = {
        status: r.status,
        timestamp: new Date(r.updated_at).toISOString(),
        set: r.reviewer_id,
        set_name: r.name_en,
        decided_by: r.decided_by,
      };
    }
    const kept = rows.filter(r => r.status === 'keep').length;
    res.set('Content-Disposition', 'attachment; filename="saintiment_swipe_decisions.json"');
    res.json({
      project: 'Saintiment',
      source: 'neon:_saintiment_swipe_team_db',
      source_run_id: 'X2gdX05u8rP41b4rG',
      source_dataset_id: 'WUsK3RRYo7nKEOUbA',
      exported_at: new Date().toISOString(),
      summary: { total_posts: total, kept, rejected: rows.length - kept },
      decisions,
    });
  } catch (e) {
    next(e);
  }
});

app.use('/api', (req, res) => res.status(404).json({ error: 'not_found' }));

// The UI is a single static page. In services mode it isn't emitted to the CDN,
// so Express serves it (the file is bundled into the function).
const PUBLIC_DIR = path.join(path.dirname(fileURLToPath(import.meta.url)), 'public');
app.use(express.static(PUBLIC_DIR, { maxAge: 0 }));
app.get('/{*splat}', (req, res) => res.sendFile(path.join(PUBLIC_DIR, 'index.html')));

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'server_error', message: String(err.message || err) });
});

// Local run: `node --env-file=.env.local server.js`. On Vercel the exported app is used.
if (!process.env.VERCEL) {
  const port = Number(process.env.PORT || 3000);
  app.listen(port, () => console.log(`Swipe review on http://localhost:${port}`));
}

export default app;
