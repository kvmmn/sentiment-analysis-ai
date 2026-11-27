// Saintiment Team Qualitative Coding Studio API (Express on Vercel).
// Static UI lives in public/; every /api/coding route except login requires the shared swipe_session cookie.
// Env: DATABASE_URL (or CODING_DATABASE_URL), TEAM_PASSWORD, SESSION_SECRET.
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import express from 'express';
import { neon } from '@neondatabase/serverless';

const COOKIE = 'swipe_session';
const SESSION_DAYS = 30;
const CODER_IDS = new Set([1, 2, 3]);
const CODING_DB = '_saintiment_coding_db';
const THIS_FILE = fileURLToPath(import.meta.url);

function codingDbUrl() {
  if (process.env.CODING_DATABASE_URL) return process.env.CODING_DATABASE_URL;
  const base = process.env.DATABASE_URL;
  if (!base) throw new Error('DATABASE_URL is not set');
  const u = new URL(base);
  u.pathname = `/${CODING_DB}`;
  return u.toString();
}

let sqlClient;
function sql() {
  sqlClient ??= neon(codingDbUrl());
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

function parseCoderId(raw) {
  const n = Number(raw);
  return CODER_IDS.has(n) ? n : null;
}

const app = express();
app.disable('x-powered-by');
app.use(express.json({ limit: '64kb' }));
app.use('/api/coding', (req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

app.post('/api/coding/login', async (req, res) => {
  const expected = process.env.TEAM_PASSWORD;
  if (!expected) return res.status(500).json({ error: 'TEAM_PASSWORD is not set' });
  const given = String(req.body?.password || '');
  if (!safeEqual(given, expected)) {
    await new Promise(r => setTimeout(r, 600));
    return res.status(401).json({ error: 'wrong_password' });
  }
  const secure = req.headers['x-forwarded-proto'] === 'https' ? '; Secure' : '';
  res.set(
    'Set-Cookie',
    `${COOKIE}=${makeToken()}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${SESSION_DAYS * 86400}${secure}`
  );
  res.json({ ok: true });
});

app.post('/api/coding/logout', (req, res) => {
  res.set('Set-Cookie', `${COOKIE}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`);
  res.json({ ok: true });
});

app.get('/api/coding/me', requireSession, (req, res) => res.json({ ok: true }));

app.get('/api/coding/coders', requireSession, async (req, res, next) => {
  try {
    const rows = await sql()`
      SELECT c.id, c.name, c.name_en,
             (SELECT count(*)::int FROM coding_posts) AS total_posts,
             (SELECT count(*)::int FROM coding_post_status s WHERE s.coder_id = c.id AND s.is_coded) AS coded_count,
             (SELECT count(*)::int FROM coding_codes cd WHERE cd.coder_id = c.id) AS codes_count,
             (SELECT count(*)::int FROM coding_highlights h WHERE h.coder_id = c.id) AS highlights_count,
             (SELECT max(s.updated_at) FROM coding_post_status s WHERE s.coder_id = c.id) AS last_activity
      FROM coders c
      ORDER BY c.id`;
    res.json({ coders: rows });
  } catch (e) {
    next(e);
  }
});

app.get('/api/coding/workspace', requireSession, async (req, res, next) => {
  const coderId = parseCoderId(req.query.coder);
  if (!coderId) return res.status(400).json({ error: 'bad_coder' });
  try {
    const [posts, externalSources, themes, codes, highlights, postStatus] = await Promise.all([
      // Blind post projection: omits reviewer_set, matched_families, matched_query_codes
      sql()`
        SELECT sample_id, source_post_id, posted_at, post_text, text_chars,
               author_type, author_name, author_headline, post_url,
               reactions, comments, shares,
               has_external_link, external_url_count, newsletter_title, newsletter_url
        FROM coding_posts
        ORDER BY sample_id`,
      sql()`
        SELECT id, sample_id, source_kind, original_url, resolved_url, domain,
               title, extracted_text, extracted_chars, fetch_status, http_status
        FROM coding_external_sources
        ORDER BY sample_id, id`,
      sql()`
        SELECT id, name, sort_order, created_at
        FROM coding_themes
        WHERE coder_id = ${coderId}
        ORDER BY sort_order, id`,
      sql()`
        SELECT id, label, color_idx, theme_id, created_at, updated_at
        FROM coding_codes
        WHERE coder_id = ${coderId}
        ORDER BY created_at, id`,
      sql()`
        SELECT id, sample_id, source, external_source_id, paragraph_idx,
               start_offset, end_offset, quote, code_id, created_at, updated_at
        FROM coding_highlights
        WHERE coder_id = ${coderId}
        ORDER BY sample_id, source, paragraph_idx, start_offset, id`,
      sql()`
        SELECT sample_id, is_coded, link_reviewed, coder_notes, updated_at
        FROM coding_post_status
        WHERE coder_id = ${coderId}`,
    ]);
    res.json({
      coder_id: coderId,
      posts,
      external_sources: externalSources,
      themes,
      codes,
      highlights,
      post_status: postStatus,
    });
  } catch (e) {
    next(e);
  }
});

app.post('/api/coding/codes', requireSession, async (req, res, next) => {
  const coderId = parseCoderId(req.body?.coder_id);
  const label = String(req.body?.label || '').trim().slice(0, 120);
  const colorIdx = Math.min(6, Math.max(1, Number(req.body?.color_idx) || 1));
  const themeId = req.body?.theme_id ? Number(req.body.theme_id) : null;
  if (!coderId) return res.status(400).json({ error: 'bad_coder' });
  if (!label) return res.status(400).json({ error: 'missing_label' });
  try {
    const existing = await sql()`
      SELECT id, label, color_idx, theme_id, created_at, updated_at
      FROM coding_codes
      WHERE coder_id = ${coderId} AND lower(label) = lower(${label})
      LIMIT 1`;
    if (existing.length) return res.json({ ok: true, code: existing[0], existed: true });

    const rows = await sql()`
      INSERT INTO coding_codes (coder_id, label, color_idx, theme_id)
      VALUES (${coderId}, ${label}, ${colorIdx}, ${themeId})
      RETURNING id, label, color_idx, theme_id, created_at, updated_at`;
    res.json({ ok: true, code: rows[0], existed: false });
  } catch (e) {
    next(e);
  }
});

app.patch('/api/coding/codes/:id', requireSession, async (req, res, next) => {
  const codeId = Number(req.params.id);
  const coderId = parseCoderId(req.body?.coder_id);
  if (!codeId || !coderId) return res.status(400).json({ error: 'bad_request' });
  try {
    const currentRows = await sql()`
      SELECT id, label, color_idx, theme_id
      FROM coding_codes
      WHERE id = ${codeId} AND coder_id = ${coderId}`;
    if (!currentRows.length) return res.status(404).json({ error: 'not_found' });
    const cur = currentRows[0];

    const label = req.body?.label !== undefined ? String(req.body.label).trim().slice(0, 120) : cur.label;
    if (!label) return res.status(400).json({ error: 'missing_label' });
    const colorIdx = req.body?.color_idx !== undefined
      ? Math.min(6, Math.max(1, Number(req.body.color_idx) || 1))
      : cur.color_idx;
    const themeId = req.body?.theme_id === undefined
      ? cur.theme_id
      : (req.body.theme_id === null ? null : Number(req.body.theme_id));

    const updated = await sql()`
      UPDATE coding_codes
      SET label = ${label}, color_idx = ${colorIdx}, theme_id = ${themeId}, updated_at = now()
      WHERE id = ${codeId} AND coder_id = ${coderId}
      RETURNING id, label, color_idx, theme_id, created_at, updated_at`;
    res.json({ ok: true, code: updated[0] });
  } catch (e) {
    next(e);
  }
});

app.post('/api/coding/codes/:id/merge', requireSession, async (req, res, next) => {
  const sourceId = Number(req.params.id);
  const coderId = parseCoderId(req.body?.coder_id);
  const targetId = Number(req.body?.target_code_id);
  if (!sourceId || !coderId || !targetId || sourceId === targetId) {
    return res.status(400).json({ error: 'bad_request' });
  }
  try {
    const found = await sql()`
      SELECT id FROM coding_codes
      WHERE coder_id = ${coderId} AND id IN (${sourceId}, ${targetId})`;
    if (found.length !== 2) return res.status(404).json({ error: 'not_found' });

    const moved = await sql()`
      UPDATE coding_highlights
      SET code_id = ${targetId}, updated_at = now()
      WHERE coder_id = ${coderId} AND code_id = ${sourceId}
      RETURNING id`;
    await sql()`
      DELETE FROM coding_codes
      WHERE id = ${sourceId} AND coder_id = ${coderId}`;

    res.json({ ok: true, moved_count: moved.length, source_id: sourceId, target_code_id: targetId });
  } catch (e) {
    next(e);
  }
});

app.delete('/api/coding/codes/:id', requireSession, async (req, res, next) => {
  const codeId = Number(req.params.id);
  const coderId = parseCoderId(req.query.coder ?? req.body?.coder_id);
  if (!codeId || !coderId) return res.status(400).json({ error: 'bad_request' });
  try {
    const rows = await sql()`
      DELETE FROM coding_codes
      WHERE id = ${codeId} AND coder_id = ${coderId}
      RETURNING id`;
    if (!rows.length) return res.status(404).json({ error: 'not_found' });
    res.json({ ok: true, id: codeId });
  } catch (e) {
    next(e);
  }
});

app.post('/api/coding/themes', requireSession, async (req, res, next) => {
  const coderId = parseCoderId(req.body?.coder_id);
  const name = String(req.body?.name || '').trim().slice(0, 120);
  if (!coderId || !name) return res.status(400).json({ error: 'bad_request' });
  try {
    const rows = await sql()`
      INSERT INTO coding_themes (coder_id, name)
      VALUES (${coderId}, ${name})
      ON CONFLICT (coder_id, name) DO UPDATE SET name = EXCLUDED.name
      RETURNING id, name, sort_order, created_at`;
    res.json({ ok: true, theme: rows[0] });
  } catch (e) {
    next(e);
  }
});

app.delete('/api/coding/themes/:id', requireSession, async (req, res, next) => {
  const themeId = Number(req.params.id);
  const coderId = parseCoderId(req.query.coder ?? req.body?.coder_id);
  if (!themeId || !coderId) return res.status(400).json({ error: 'bad_request' });
  try {
    const rows = await sql()`
      DELETE FROM coding_themes
      WHERE id = ${themeId} AND coder_id = ${coderId}
      RETURNING id`;
    if (!rows.length) return res.status(404).json({ error: 'not_found' });
    res.json({ ok: true, id: themeId });
  } catch (e) {
    next(e);
  }
});

app.post('/api/coding/highlights', requireSession, async (req, res, next) => {
  const coderId = parseCoderId(req.body?.coder_id);
  const sampleId = String(req.body?.sample_id || '').trim();
  const source = req.body?.source === 'external' ? 'external' : 'post';
  const extSourceId = req.body?.external_source_id ? Number(req.body.external_source_id) : null;
  const pIdx = Number(req.body?.paragraph_idx ?? 0);
  const startOffset = Number(req.body?.start_offset ?? 0);
  const endOffset = Number(req.body?.end_offset ?? 0);
  const quote = String(req.body?.quote || '').slice(0, 2000);
  const codeId = Number(req.body?.code_id);
  if (!coderId || !sampleId || !codeId || !quote) return res.status(400).json({ error: 'bad_request' });

  try {
    const rows = await sql()`
      INSERT INTO coding_highlights (
        coder_id, sample_id, source, external_source_id,
        paragraph_idx, start_offset, end_offset, quote, code_id
      )
      SELECT ${coderId}, ${sampleId}, ${source}, ${extSourceId},
             ${pIdx}, ${startOffset}, ${endOffset}, ${quote}, c.id
      FROM coding_codes c
      WHERE c.id = ${codeId} AND c.coder_id = ${coderId}
      RETURNING id, sample_id, source, external_source_id, paragraph_idx,
                start_offset, end_offset, quote, code_id, created_at, updated_at`;
    if (!rows.length) return res.status(404).json({ error: 'bad_code' });
    res.json({ ok: true, highlight: rows[0] });
  } catch (e) {
    next(e);
  }
});

app.patch('/api/coding/highlights/:id', requireSession, async (req, res, next) => {
  const hlId = Number(req.params.id);
  const coderId = parseCoderId(req.body?.coder_id);
  const codeId = Number(req.body?.code_id);
  if (!hlId || !coderId || !codeId) return res.status(400).json({ error: 'bad_request' });
  try {
    const rows = await sql()`
      UPDATE coding_highlights h
      SET code_id = c.id, updated_at = now()
      FROM coding_codes c
      WHERE h.id = ${hlId} AND h.coder_id = ${coderId}
        AND c.id = ${codeId} AND c.coder_id = ${coderId}
      RETURNING h.id, h.sample_id, h.source, h.external_source_id, h.paragraph_idx,
                h.start_offset, h.end_offset, h.quote, h.code_id, h.created_at, h.updated_at`;
    if (!rows.length) return res.status(404).json({ error: 'not_found' });
    res.json({ ok: true, highlight: rows[0] });
  } catch (e) {
    next(e);
  }
});

app.delete('/api/coding/highlights/:id', requireSession, async (req, res, next) => {
  const hlId = Number(req.params.id);
  const coderId = parseCoderId(req.query.coder ?? req.body?.coder_id);
  if (!hlId || !coderId) return res.status(400).json({ error: 'bad_request' });
  try {
    const rows = await sql()`
      DELETE FROM coding_highlights
      WHERE id = ${hlId} AND coder_id = ${coderId}
      RETURNING id`;
    if (!rows.length) return res.status(404).json({ error: 'not_found' });
    res.json({ ok: true, id: hlId });
  } catch (e) {
    next(e);
  }
});

app.put('/api/coding/post-status', requireSession, async (req, res, next) => {
  const coderId = parseCoderId(req.body?.coder_id);
  const sampleId = String(req.body?.sample_id || '').trim();
  if (!coderId || !sampleId) return res.status(400).json({ error: 'bad_request' });
  const isCoded = Boolean(req.body?.is_coded);
  const linkReviewed = Boolean(req.body?.link_reviewed);
  const coderNotes = String(req.body?.coder_notes || '').slice(0, 4000);
  try {
    const rows = await sql()`
      INSERT INTO coding_post_status (coder_id, sample_id, is_coded, link_reviewed, coder_notes)
      VALUES (${coderId}, ${sampleId}, ${isCoded}, ${linkReviewed}, ${coderNotes})
      ON CONFLICT (coder_id, sample_id) DO UPDATE
        SET is_coded = EXCLUDED.is_coded,
            link_reviewed = EXCLUDED.link_reviewed,
            coder_notes = EXCLUDED.coder_notes,
            updated_at = now()
      RETURNING sample_id, is_coded, link_reviewed, coder_notes, updated_at`;
    res.json({ ok: true, status: rows[0] });
  } catch (e) {
    next(e);
  }
});

app.get('/api/coding/export', requireSession, async (req, res, next) => {
  try {
    const [coders, posts, externalSources, themes, codes, highlights, statuses] = await Promise.all([
      sql()`SELECT id, name, name_en FROM coders ORDER BY id`,
      sql()`SELECT * FROM coding_posts ORDER BY sample_id`,
      sql()`SELECT * FROM coding_external_sources ORDER BY sample_id, id`,
      sql()`SELECT * FROM coding_themes ORDER BY coder_id, sort_order, id`,
      sql()`SELECT * FROM coding_codes ORDER BY coder_id, id`,
      sql()`SELECT * FROM coding_highlights ORDER BY coder_id, sample_id, id`,
      sql()`SELECT * FROM coding_post_status ORDER BY coder_id, sample_id`,
    ]);
    res.set('Content-Disposition', 'attachment; filename="saintiment_coding_50_export.json"');
    res.json({
      project: 'Saintiment',
      database: CODING_DB,
      exported_at: new Date().toISOString(),
      coders,
      posts,
      external_sources: externalSources,
      themes,
      codes,
      highlights,
      post_status: statuses,
    });
  } catch (e) {
    next(e);
  }
});

app.use('/api/coding', (req, res) => res.status(404).json({ error: 'not_found' }));

const PUBLIC_DIR = path.join(path.dirname(THIS_FILE), 'public');
// Shared self-hosted fonts for every page of the app (swipe pages load them from /code/fonts too).
// Font files have unique names and are cached for 7 days; fonts.css is revalidated on every load
// so a change of typeface reaches everyone at once.
app.use('/code/fonts', express.static(path.join(PUBLIC_DIR, 'fonts'), {
  maxAge: '7d',
  setHeaders: (res, file) => { if (file.endsWith('.css')) res.set('Cache-Control', 'no-cache'); },
}));
app.use('/code/fonts', (req, res) => res.status(404).end());
// Compare page: all coders side by side. Clean address /code/compare; the old .html address redirects.
// HTML is never cached: on Vercel every file has the same old Last-Modified date, so a cached page
// could otherwise survive a deploy. Fonts and other assets keep their own cache rules.
const HTML_HEADERS = { 'Cache-Control': 'no-store, max-age=0' };
const noStoreHtml = (res, file) => { if (file.endsWith('.html')) res.set(HTML_HEADERS); };
const sendHtml = (res, name) => res.sendFile(path.join(PUBLIC_DIR, name), { headers: HTML_HEADERS, etag: false, lastModified: false });
app.get(['/code/compare', '/code/compare/'], (req, res) => sendHtml(res, 'compare.html'));
app.get('/code/compare.html', (req, res) => res.redirect(301, '/code/compare'));
// Code map: every code of one coder on one page, apart from the post texts.
app.get(['/code/codes', '/code/codes/'], (req, res) => sendHtml(res, 'codes.html'));
app.use('/code', express.static(PUBLIC_DIR, { maxAge: 0, setHeaders: noStoreHtml }));
app.use(express.static(PUBLIC_DIR, { maxAge: 0, setHeaders: noStoreHtml }));
app.get(['/code', '/code/{*splat}', '/{*splat}'], (req, res) => sendHtml(res, 'index.html'));

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'server_error', message: String(err.message || err) });
});

if (!process.env.VERCEL) {
  const port = Number(process.env.PORT || 3001);
  app.listen(port, () => console.log(`Coding studio on http://localhost:${port}/code`));
}

export default app;
