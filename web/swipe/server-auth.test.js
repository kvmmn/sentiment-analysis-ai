import assert from 'node:assert/strict';
import http from 'node:http';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';

process.env.SESSION_SECRET ??= 'test-session-secret-32chars-long';
process.env.TEAM_PASSWORD ??= 'test-team-password';
delete process.env.DATABASE_URL;
delete process.env.VERCEL;

const { default: app } = await import('./server.js');
const html = readFileSync(new URL('./public/index.html', import.meta.url), 'utf8');

function listen() {
  const server = http.createServer(app);
  return new Promise(resolve => {
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function withServer(fn) {
  const server = await listen();
  try {
    const { port } = server.address();
    return await fn(`http://127.0.0.1:${port}`);
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
}

test('kept API requires the session cookie', async () => {
  await withServer(async base => {
    for (const pathName of ['/api/kept', '/api/kept/export', '/api/kept/export?by=1']) {
      const res = await fetch(base + pathName);
      assert.equal(res.status, 401, pathName);
      assert.deepEqual(await res.json(), { error: 'unauthorized' });
    }
  });
});

async function loginCookie(base) {
  const login = await fetch(base + '/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password: process.env.TEAM_PASSWORD }),
  });
  assert.equal(login.status, 200);
  const cookie = login.headers.getSetCookie?.()[0] || login.headers.get('set-cookie');
  assert.match(cookie, /swipe_session=/);
  return cookie.split(';')[0];
}

test('login then kept export still needs the database, not an anonymous dump', async () => {
  await withServer(async base => {
    const cookie = await loginCookie(base);
    const res = await fetch(base + '/api/kept/export', { headers: { cookie } });
    assert.equal(res.status, 500);
    const body = await res.json();
    assert.equal(body.error, 'server_error');
  });
});

test('kept export rejects an unknown reviewer without querying', async () => {
  await withServer(async base => {
    const cookie = await loginCookie(base);
    const res = await fetch(base + '/api/kept/export?by=9', { headers: { cookie } });
    assert.equal(res.status, 400);
    assert.deepEqual(await res.json(), { error: 'bad_set' });
  });
});

test('public UI has the kept page, who-kept filter, and download control', () => {
  assert.match(html, /id="keptScreen"/);
  assert.match(html, /class="text-btn kept-link" href="\/kept"/);
  assert.match(html, /id="setsGrid"/);
  assert.ok(html.indexOf('id="setsGrid"') < html.indexOf('href="/kept"'));
  assert.ok(html.indexOf('href="/kept"') < html.indexOf('href="/api/export"'));
  assert.doesNotMatch(html, /class="kept-entry"/);
  assert.doesNotMatch(html, /closest\('a\[href="\/kept"\]'\)/);
  assert.doesNotMatch(html, /id="setTitle"[\s\S]{0,80}href="\/kept"/);
  assert.match(html, /id="keptByFilter"/);
  assert.match(html, /downloadKept\(/);
  assert.match(html, /دانلود پست‌های نگه داشته‌شده/);
  assert.match(html, /چه کسی نگه داشته/);
  assert.match(html, /id="reviewScreen"/);
  assert.match(html, /\/api\/export/);
  assert.match(html, /onclick="decide\('keep'\)"/);
  assert.match(html, /window\.history\.pushState/);
});

test('Express serves /kept as the same app shell', async () => {
  await withServer(async base => {
    const res = await fetch(base + '/kept');
    assert.equal(res.status, 200);
    const text = await res.text();
    assert.match(text, /id="keptScreen"/);
    assert.match(text, /id="reviewScreen"/);
  });
});
