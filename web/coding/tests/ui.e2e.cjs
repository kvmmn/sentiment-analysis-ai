// End-to-end UI test for the Coding Studio (web/coding/public/index.html).
// Runs the real page in Chromium against an in-memory mock of /api/coding/*.
// The mock returns BIGINT ids as *strings*, exactly like the Neon driver does in production.
// Usage: node tests/ui.e2e.cjs   (needs `playwright` resolvable; set SHOTS=dir to save screenshots)
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const HTML = fs.readFileSync(path.join(__dirname, '..', 'public', 'index.html'), 'utf8');
const POST1 = 'Our team tried the new AI assistant for a month. It saved hours on boring reports.\n\nBut I still worry about accuracy. Trust has to be earned!';
const P0 = POST1.split('\n\n')[0];
const POST2 = 'Short second post about layoffs and automation.';

function mockDb() {
  let seq = 100;
  const id = () => String(++seq); // BIGSERIAL -> string
  return {
    codes: [{ id: '11', label: 'productivity', color_idx: 2, theme_id: null }],
    themes: [{ id: '21', name: 'Benefits', sort_order: 0 }],
    hls: [{ id: '31', sample_id: 'S01', source: 'post', external_source_id: null, paragraph_idx: 0, start_offset: P0.indexOf('It saved'), end_offset: P0.length, quote: 'It saved hours on boring reports.', code_id: '11' }],
    status: [],
    id,
    calls: [],
  };
}

async function installMock(page, db) {
  await page.route('**/api/coding/**', async route => {
    const req = route.request();
    const url = new URL(req.url());
    const p = url.pathname.replace('/api/coding', '');
    const m = req.method();
    const body = req.postDataJSON?.() || null;
    db.calls.push(`${m} ${p}`);
    const ok = data => route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, ...data }) });
    const fail = (s, e) => route.fulfill({ status: s, contentType: 'application/json', body: JSON.stringify({ error: e }) });
    if (p === '/me') return ok({});
    if (p === '/coders') return ok({ coders: [{ id: 1, name: 'Kawe', total_posts: 2, coded_count: 0, codes_count: db.codes.length, highlights_count: db.hls.length }, { id: 2, name: 'Sara', total_posts: 2, coded_count: 0, codes_count: 0, highlights_count: 0 }] });
    if (p === '/workspace') return ok({ coder_id: 1,
      posts: [{ sample_id: 'S01', post_text: POST1, author_name: 'A', author_type: 'person', has_external_link: false },
              { sample_id: 'S02', post_text: POST2, author_name: 'B', author_type: 'company', has_external_link: false }],
      external_sources: [], themes: db.themes, codes: db.codes, highlights: db.hls, post_status: db.status });
    if (p === '/codes' && m === 'POST') {
      const ex = db.codes.find(c => c.label.toLowerCase() === body.label.toLowerCase());
      if (ex) return ok({ code: ex, existed: true });
      const c = { id: db.id(), label: body.label, color_idx: body.color_idx, theme_id: body.theme_id ?? null };
      db.codes.push(c); return ok({ code: c, existed: false });
    }
    let r;
    if ((r = p.match(/^\/codes\/(\d+)\/merge$/))) {
      const moved = db.hls.filter(h => h.code_id === r[1]);
      moved.forEach(h => { h.code_id = String(body.target_code_id); });
      db.codes = db.codes.filter(c => c.id !== r[1]);
      return ok({ moved_count: moved.length });
    }
    if ((r = p.match(/^\/codes\/(\d+)$/))) {
      const c = db.codes.find(x => x.id === r[1]);
      if (!c) return fail(404, 'not_found');
      if (m === 'PATCH') {
        if ('label' in body) c.label = body.label;
        if ('color_idx' in body) c.color_idx = body.color_idx;
        if ('theme_id' in body) c.theme_id = body.theme_id == null ? null : String(body.theme_id);
        return ok({ code: c });
      }
      if (m === 'DELETE') { db.codes = db.codes.filter(x => x.id !== r[1]); db.hls = db.hls.filter(h => h.code_id !== r[1]); return ok({ id: r[1] }); }
    }
    if (p === '/themes' && m === 'POST') { const t = { id: db.id(), name: body.name, sort_order: 0 }; db.themes.push(t); return ok({ theme: t }); }
    if ((r = p.match(/^\/themes\/(\d+)$/)) && m === 'DELETE') { db.themes = db.themes.filter(t => t.id !== r[1]); db.codes.forEach(c => { if (c.theme_id === r[1]) c.theme_id = null; }); return ok({ id: r[1] }); }
    if (p === '/highlights' && m === 'POST') {
      const h = { ...body, id: db.id(), code_id: String(body.code_id) }; delete h.coder_id;
      db.hls.push(h); return ok({ highlight: h });
    }
    if ((r = p.match(/^\/highlights\/(\d+)$/))) {
      const h = db.hls.find(x => x.id === r[1]);
      if (!h) return fail(404, 'not_found');
      if (m === 'PATCH') { h.code_id = String(body.code_id); return ok({ highlight: h }); }
      if (m === 'DELETE') { db.hls = db.hls.filter(x => x.id !== r[1]); return ok({ id: r[1] }); }
    }
    if (p === '/post-status' && m === 'PUT') {
      const st = { sample_id: body.sample_id, is_coded: body.is_coded, link_reviewed: body.link_reviewed, coder_notes: body.coder_notes };
      db.status = db.status.filter(s => s.sample_id !== body.sample_id).concat(st); return ok({ status: st });
    }
    return fail(404, 'not_found');
  });
}

// Select characters [a,b) of paragraph p by building a DOM range over its text nodes.
async function selectText(page, p, a, b) {
  await page.evaluate(([p, a, b]) => {
    const el = document.querySelector(`#prose p[data-p="${p}"]`);
    const walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let n, pos = 0, start, end;
    while ((n = walk.nextNode())) {
      const len = n.data.length;
      if (!start && a <= pos + len) start = [n, a - pos];
      if (!end && b <= pos + len) { end = [n, b - pos]; break; }
      pos += len;
    }
    const r = document.createRange(); r.setStart(...start); r.setEnd(...end);
    const s = getSelection(); s.removeAllRanges(); s.addRange(r);
    el.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
  }, [p, a, b]);
  await page.waitForSelector('#comboInput');
}

const toastText = page => page.locator('#toast').innerText();

(async () => {
  const browser = await chromium.launch();
  const shots = process.env.SHOTS;
  let failures = 0;
  const check = async (name, fn) => {
    try { await fn(); console.log('ok  -', name); }
    catch (e) { failures++; console.log('FAIL-', name, '\n   ', e.message.split('\n')[0]); }
  };

  const db = mockDb();
  const page = await browser.newPage({ viewport: { width: 1360, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.route('http://studio.test/code/', r => r.fulfill({ contentType: 'text/html', body: HTML }));
  await page.route('https://fonts.**', r => r.abort());
  await installMock(page, db);
  await page.goto('http://studio.test/code/');

  await check('picker lists coders and opens the studio', async () => {
    await page.click('[data-action="open-coder"][data-id="1"]');
    await page.waitForSelector('#prose p[data-p="0"]');
    assert.equal(await page.locator('#prose p[data-p="0"]').innerText(), POST1.split('\n\n')[0]);
    assert.equal(await page.locator('#prose .hl').count(), 1, 'existing highlight (string ids) renders');
  });

  await check('add a new code to a selection (type + Enter)', async () => {
    const para = POST1.split('\n\n')[1];
    const a = para.indexOf('I still worry'), b = para.indexOf('accuracy') + 'accuracy'.length;
    await selectText(page, 1, a, b);
    assert.equal(await page.locator('.quote').innerText(), 'I still worry about accuracy');
    await page.fill('#comboInput', 'accuracy concern');
    assert.match(await page.locator('.opt.create').innerText(), /accuracy concern/);
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.querySelectorAll('#prose .hl').length === 2);
    const h = db.hls.find(x => x.quote === 'I still worry about accuracy');
    assert.ok(h, 'highlight saved');
    assert.equal(h.paragraph_idx, 1); assert.equal(h.start_offset, a); assert.equal(h.end_offset, b);
    assert.equal(para.slice(h.start_offset, h.end_offset), h.quote, 'offsets match the stored text');
    assert.ok(db.codes.some(c => c.label === 'accuracy concern'));
  });

  await check('apply an existing code by clicking it', async () => {
    await selectText(page, 0, 0, 33);
    await page.fill('#comboInput', 'prod');
    await page.click('.opt:has-text("productivity")');
    await page.waitForFunction(() => document.querySelectorAll('#prose .hl').length >= 3);
    assert.equal(db.hls.filter(h => h.code_id === '11').length, 2);
    assert.equal(db.codes.length, 2, 'no duplicate code created');
  });

  await check('typing an existing name in another case reuses it', async () => {
    await selectText(page, 1, 0, 3);
    await page.fill('#comboInput', 'PRODUCTIVITY');
    assert.equal(await page.locator('.opt.create').count(), 0, 'no "create" row for an existing name');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#comboInput').count(), 0, 'Esc closes the coding panel');
  });

  await check('click a coded segment, swap its code (PATCH)', async () => {
    await page.locator('#prose .hl', { hasText: 'I still worry' }).click();
    await page.waitForSelector('.cur-code');
    await page.click('.cur-code [data-action="swap"]');
    await page.fill('#comboInput', 'trust');
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.querySelector('.cur-code .code-tag')?.textContent === 'trust');
    const h = db.hls.find(x => x.quote === 'I still worry about accuracy');
    assert.equal(db.codes.find(c => c.id === h.code_id).label, 'trust');
  });

  await check('add a second code to the same segment', async () => {
    await page.fill('#comboInput', 'accuracy');
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.querySelectorAll('.cur-code').length === 2);
    assert.equal(db.hls.filter(x => x.quote === 'I still worry about accuracy').length, 2);
  });

  await check('remove a code from a segment, then undo', async () => {
    const before = db.hls.length;
    await page.locator('.cur-code', { hasText: 'trust' }).locator('[data-action="remove-hl"]').click();
    await page.waitForFunction(() => document.querySelectorAll('.cur-code').length === 1);
    assert.equal(db.hls.length, before - 1);
    assert.match(await toastText(page), /برداشته شد/);
    await page.click('#toast button');
    await page.waitForFunction(n => window.S.hls.length === n, before);
    assert.equal(db.hls.length, before, 'undo re-created the highlight');
    await page.keyboard.press('Escape');
  });

  await check('rename a code from the codebook (Enter saves)', async () => {
    await page.click('[data-tab="book"]');
    await page.click('[data-action="toggle-code"]:has-text("productivity")');
    await page.fill('#renameInput', 'time saving');
    await page.keyboard.press('Enter');
    await page.waitForSelector('[data-action="toggle-code"]:has-text("time saving")');
    assert.equal(db.codes.find(c => c.id === '11').label, 'time saving');
    assert.match(await page.locator('#prose .hl').first().getAttribute('title'), /time saving/);
  });

  await check('recolour a code', async () => {
    await page.click('[data-action="recolor"][data-id="11"][data-color="5"]');
    await page.waitForFunction(() => window.S.codes.find(c => c.id === 11).color_idx === 5);
    assert.equal(db.codes.find(c => c.id === '11').color_idx, 5);
    assert.equal(await page.locator('[data-action="recolor"][data-id="11"][data-color="5"]').getAttribute('aria-checked'), 'true');
  });

  await check('assign a theme to a code', async () => {
    await page.selectOption('.book-edit select[data-action="set-theme"]', '21');
    await page.waitForFunction(() => window.S.codes.find(c => c.id === 11).theme_id === 21);
    assert.equal(db.codes.find(c => c.id === '11').theme_id, '21');
  });

  await check('jump from a codebook quote to the text', async () => {
    await page.locator('.quotes button').first().click();
    await page.waitForSelector('.cur-code');
    await page.keyboard.press('Escape');
  });

  await check('renaming onto an existing name offers a merge', async () => {
    await page.click('[data-tab="book"]');
    await page.click('[data-action="toggle-code"]:has-text("accuracy concern")');
    await page.fill('#renameInput', 'Trust');
    await page.keyboard.press('Enter');
    await page.waitForSelector('dialog[open]');
    await page.click('#dlgOk');
    await page.waitForFunction(() => !window.S.codes.some(c => c.label === 'accuracy concern'));
    assert.ok(!db.codes.some(c => c.label === 'accuracy concern'));
  });

  await check('merge a code into another from the menu', async () => {
    await selectText(page, 0, 0, 8);
    await page.fill('#comboInput', 'temp code');
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => window.S.codes.some(c => c.label === 'temp code'));
    await page.click('[data-tab="book"]');
    await page.click('[data-action="toggle-code"]:has-text("temp code")');
    const target = db.codes.find(c => c.label === 'trust').id;
    await page.selectOption('#mergeTarget', target);
    await page.click('[data-action="merge"]');
    await page.click('#dlgOk');
    await page.waitForFunction(() => !window.S.codes.some(c => c.label === 'temp code'));
    assert.ok(!db.codes.some(c => c.label === 'temp code'));
  });

  await check('delete a code (with confirm) removes its segments', async () => {
    const row = page.locator('[data-action="toggle-code"]:has-text("trust")');
    if ((await row.getAttribute('aria-expanded')) !== 'true') await row.click(); // merge leaves the target open
    const id = db.codes.find(c => c.label === 'trust').id;
    await page.click(`[data-action="delete-code"][data-id="${id}"]`);
    await page.waitForSelector('dialog[open]');
    await page.click('#dlgOk');
    await page.waitForFunction(i => !window.S.codes.some(c => c.id === i), Number(id));
    assert.ok(!db.codes.some(c => c.id === id));
    assert.ok(!db.hls.some(h => h.code_id === id));
  });

  await check('remove from the post segment list', async () => {
    const n = db.hls.length;
    await page.locator('#segList [data-action="remove-hl"]').first().click();
    await page.waitForFunction(k => window.S.hls.length === k - 1, n);
    assert.equal(db.hls.length, n - 1);
  });

  await check('click a sentence to start coding it', async () => {
    await page.locator('#prose p[data-p="1"]').click({ position: { x: 30, y: 10 } });
    await page.waitForSelector('#comboInput');
    const q = await page.locator('.quote').innerText();
    assert.ok(POST1.split('\n\n')[1].includes(q) && q.length > 5, 'quote is a sentence: ' + q);
    await page.keyboard.press('Escape');
  });

  await check('themes tab: create and delete a theme', async () => {
    await page.click('[data-tab="themes"]');
    await page.fill('#themeInput', 'Risks');
    await page.keyboard.press('Enter');
    await page.waitForSelector('.theme-group h4:has-text("Risks")');
    const id = db.themes.find(t => t.name === 'Risks').id;
    await page.click(`[data-action="delete-theme"][data-id="${id}"]`);
    await page.waitForFunction(() => !window.S.themes.some(t => t.name === 'Risks'));
  });

  await check('mark post as coded and move to the next post', async () => {
    await page.click('#markBtn');
    await page.waitForFunction(() => document.querySelector('#markBtn').getAttribute('aria-pressed') === 'true');
    assert.equal(db.status.find(s => s.sample_id === 'S01').is_coded, true);
    await page.click('[data-action="next"]');
    assert.equal(await page.locator('#pSid').innerText(), 'S02');
  });

  await check('server error shows a clear toast, nothing changes', async () => {
    await page.route('**/api/coding/highlights', r => r.fulfill({ status: 500, contentType: 'application/json', body: '{"error":"server_error"}' }), { times: 1 });
    await selectText(page, 0, 0, 5);
    await page.fill('#comboInput', 'x');
    await page.keyboard.press('Enter');
    await page.waitForSelector('#toast.error');
    assert.match(await toastText(page), /ذخیره نشد/);
    assert.equal(await page.locator('#prose .hl').count(), 0);
    await page.keyboard.press('Escape');
  });

  await check('no uncaught page errors', async () => assert.deepEqual(errors, []));

  if (shots) {
    fs.mkdirSync(shots, { recursive: true });
    await page.click('[data-action="prev"]');
    await page.click('[data-tab="book"]');
    await page.screenshot({ path: path.join(shots, 'desktop.png') });
    await selectText(page, 1, 0, 30);
    await page.screenshot({ path: path.join(shots, 'desktop-coding.png') });
    const m = await browser.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
    await m.route('http://studio.test/code/', r => r.fulfill({ contentType: 'text/html', body: HTML }));
    await m.route('https://fonts.**', r => r.abort());
    await installMock(m, db);
    await m.goto('http://studio.test/code/#coder-1');
    await m.waitForSelector('#prose p');
    await m.screenshot({ path: path.join(shots, 'mobile.png') });
    await selectText(m, 1, 0, 30);
    await m.waitForTimeout(300);
    await m.screenshot({ path: path.join(shots, 'mobile-coding.png') });
  }

  await browser.close();
  console.log(failures ? `\n${failures} failed` : '\nall passed');
  process.exit(failures ? 1 : 0);
})();
