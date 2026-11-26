/* eslint-disable @typescript-eslint/no-explicit-any */
import type { Code, Coder, ExtSource, Highlight, NewHighlight, Post, PostStatus, Theme, Workspace } from './types';
import { DEMO_CODERS, DEMO_POSTS, DEMO_EXT, demoSeed } from './demoData';
import { safeStorage } from './text';

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(code: string, status = 0) {
    super(code);
    this.code = code;
    this.status = status;
  }
}

export interface Backend {
  mode: 'remote' | 'demo';
  login(password: string): Promise<void>;
  logout(): Promise<void>;
  coders(): Promise<Coder[]>;
  workspace(coderId: number): Promise<Workspace>;
  createCode(coderId: number, label: string, colorIdx: number, themeId: number | null): Promise<{ code: Code; existed: boolean }>;
  updateCode(coderId: number, id: number, patch: Partial<Pick<Code, 'label' | 'color_idx' | 'theme_id'>>): Promise<Code>;
  mergeCode(coderId: number, sourceId: number, targetId: number): Promise<number>;
  deleteCode(coderId: number, id: number): Promise<void>;
  createTheme(coderId: number, name: string): Promise<Theme>;
  deleteTheme(coderId: number, id: number): Promise<void>;
  createHighlight(coderId: number, h: NewHighlight): Promise<Highlight>;
  updateHighlight(coderId: number, id: number, codeId: number): Promise<Highlight>;
  deleteHighlight(coderId: number, id: number): Promise<void>;
  putStatus(coderId: number, s: PostStatus): Promise<PostStatus>;
  exportAll(): Promise<unknown>;
  resetDemo?(): void;
}

// ---- Normalisers. Neon returns BIGINT ids as strings; everything is coerced with Number() here, once.
const nn = (v: unknown) => (v === null || v === undefined || v === '' ? null : Number(v));
export const normCode = (c: any): Code => ({ id: Number(c.id), label: String(c.label ?? ''), color_idx: Number(c.color_idx) || 1, theme_id: nn(c.theme_id), created_at: c.created_at });
export const normTheme = (t: any): Theme => ({ id: Number(t.id), name: String(t.name ?? ''), sort_order: Number(t.sort_order) || 0 });
export const normHl = (h: any): Highlight => ({
  id: Number(h.id), sample_id: String(h.sample_id), source: h.source === 'external' ? 'external' : 'post',
  external_source_id: nn(h.external_source_id), paragraph_idx: Number(h.paragraph_idx ?? 0),
  start_offset: Number(h.start_offset ?? 0), end_offset: Number(h.end_offset ?? 0), quote: String(h.quote ?? ''),
  code_id: Number(h.code_id), created_at: h.created_at,
});
const normExt = (e: any): ExtSource => ({ ...e, id: Number(e.id), sample_id: String(e.sample_id), extracted_chars: nn(e.extracted_chars), http_status: nn(e.http_status) });
const normPost = (p: any): Post => ({ ...p, sample_id: String(p.sample_id), post_text: String(p.post_text ?? ''), reactions: nn(p.reactions), comments: nn(p.comments), shares: nn(p.shares), text_chars: nn(p.text_chars), external_url_count: nn(p.external_url_count), has_external_link: Boolean(p.has_external_link) });
const normStatus = (s: any): PostStatus => ({ sample_id: String(s.sample_id), is_coded: Boolean(s.is_coded), link_reviewed: Boolean(s.link_reviewed), coder_notes: String(s.coder_notes ?? '') });
const normCoder = (c: any): Coder => ({ id: Number(c.id), name: String(c.name ?? ''), name_en: c.name_en ?? null, total_posts: Number(c.total_posts) || 0, coded_count: Number(c.coded_count) || 0, codes_count: Number(c.codes_count) || 0, highlights_count: Number(c.highlights_count) || 0, last_activity: c.last_activity ?? null });

function toWorkspace(r: any): Workspace {
  const status: Record<string, PostStatus> = {};
  for (const s of r.post_status || []) { const ns = normStatus(s); status[ns.sample_id] = ns; }
  return {
    posts: (r.posts || []).map(normPost),
    ext: (r.external_sources || []).map(normExt),
    themes: (r.themes || []).map(normTheme),
    codes: (r.codes || []).map(normCode),
    highlights: (r.highlights || []).map(normHl),
    status,
  };
}

// ---- Remote (the Express API in web/coding/server.js)
async function req<T = any>(url: string, opts: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(url, { credentials: 'same-origin', ...opts, headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) } });
  } catch {
    throw new ApiError('network');
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(body.error || (res.status === 401 ? 'unauthorized' : `http_${res.status}`), res.status);
  }
  return res.json();
}
const body = (o: unknown) => JSON.stringify(o);

export function createRemoteBackend(): Backend {
  return {
    mode: 'remote',
    async login(password) { await req('/api/coding/login', { method: 'POST', body: body({ password }) }); },
    async logout() { await req('/api/coding/logout', { method: 'POST' }).catch(() => {}); },
    async coders() { const r = await req('/api/coding/coders'); return (r.coders || []).map(normCoder); },
    async workspace(coderId) { return toWorkspace(await req(`/api/coding/workspace?coder=${coderId}`)); },
    async createCode(coderId, label, color_idx, theme_id) {
      const r = await req('/api/coding/codes', { method: 'POST', body: body({ coder_id: coderId, label, color_idx, theme_id }) });
      return { code: normCode(r.code), existed: Boolean(r.existed) };
    },
    async updateCode(coderId, id, patch) {
      const r = await req(`/api/coding/codes/${id}`, { method: 'PATCH', body: body({ coder_id: coderId, ...patch }) });
      return normCode(r.code);
    },
    async mergeCode(coderId, sourceId, targetId) {
      const r = await req(`/api/coding/codes/${sourceId}/merge`, { method: 'POST', body: body({ coder_id: coderId, target_code_id: targetId }) });
      return Number(r.moved_count) || 0;
    },
    async deleteCode(coderId, id) { await req(`/api/coding/codes/${id}?coder=${coderId}`, { method: 'DELETE' }); },
    async createTheme(coderId, name) { const r = await req('/api/coding/themes', { method: 'POST', body: body({ coder_id: coderId, name }) }); return normTheme(r.theme); },
    async deleteTheme(coderId, id) { await req(`/api/coding/themes/${id}?coder=${coderId}`, { method: 'DELETE' }); },
    async createHighlight(coderId, h) { const r = await req('/api/coding/highlights', { method: 'POST', body: body({ coder_id: coderId, ...h }) }); return normHl(r.highlight); },
    async updateHighlight(coderId, id, codeId) { const r = await req(`/api/coding/highlights/${id}`, { method: 'PATCH', body: body({ coder_id: coderId, code_id: codeId }) }); return normHl(r.highlight); },
    async deleteHighlight(coderId, id) { await req(`/api/coding/highlights/${id}?coder=${coderId}`, { method: 'DELETE' }); },
    async putStatus(coderId, s) { const r = await req('/api/coding/post-status', { method: 'PUT', body: body({ coder_id: coderId, ...s }) }); return normStatus(r.status); },
    async exportAll() { return req('/api/coding/export'); },
  };
}

// ---- Demo: in-memory copy of the API's behaviour (string ids on purpose, like Neon)
interface DemoDb { seq: number; themes: any[]; codes: any[]; highlights: any[]; status: any[] }
const DEMO_KEY = 'saintiment_coding_v2_demo';

export function createDemoBackend(): Backend {
  const store = safeStorage();
  let db: DemoDb;
  try { db = JSON.parse(store?.getItem(DEMO_KEY) || 'null') || demoSeed(); } catch { db = demoSeed(); }
  const save = () => { try { store?.setItem(DEMO_KEY, JSON.stringify(db)); } catch { /* sandboxed */ } };
  const id = () => String(++db.seq);
  const wait = <T,>(v: T) => new Promise<T>(r => setTimeout(() => r(v), 140));
  const now = () => new Date().toISOString();
  const mine = (coderId: number) => (x: any) => x.coder_id === coderId;

  return {
    mode: 'demo',
    async login() { return wait(undefined); },
    async logout() { return wait(undefined); },
    async coders() {
      return wait(DEMO_CODERS.map(c => normCoder({
        ...c, total_posts: DEMO_POSTS.length,
        coded_count: db.status.filter(s => s.coder_id === c.id && s.is_coded).length,
        codes_count: db.codes.filter(mine(c.id)).length,
        highlights_count: db.highlights.filter(mine(c.id)).length,
        last_activity: db.status.filter(mine(c.id)).map(s => s.updated_at).sort().pop() || null,
      })));
    },
    async workspace(coderId) {
      return wait(toWorkspace({
        posts: DEMO_POSTS, external_sources: DEMO_EXT,
        themes: db.themes.filter(mine(coderId)), codes: db.codes.filter(mine(coderId)),
        highlights: db.highlights.filter(mine(coderId)), post_status: db.status.filter(mine(coderId)),
      }));
    },
    async createCode(coderId, label, color_idx, theme_id) {
      const ex = db.codes.find(c => c.coder_id === coderId && c.label.toLowerCase() === label.toLowerCase());
      if (ex) return wait({ code: normCode(ex), existed: true });
      const c = { id: id(), coder_id: coderId, label, color_idx, theme_id: theme_id === null ? null : String(theme_id), created_at: now() };
      db.codes.push(c); save();
      return wait({ code: normCode(c), existed: false });
    },
    async updateCode(coderId, cid, patch) {
      const c = db.codes.find(x => x.coder_id === coderId && Number(x.id) === cid);
      if (!c) throw new ApiError('not_found', 404);
      if (patch.label !== undefined) c.label = patch.label;
      if (patch.color_idx !== undefined) c.color_idx = patch.color_idx;
      if (patch.theme_id !== undefined) c.theme_id = patch.theme_id === null ? null : String(patch.theme_id);
      save();
      return wait(normCode(c));
    },
    async mergeCode(coderId, src, target) {
      let moved = 0;
      for (const h of db.highlights) if (h.coder_id === coderId && Number(h.code_id) === src) { h.code_id = String(target); moved++; }
      db.codes = db.codes.filter(c => !(c.coder_id === coderId && Number(c.id) === src));
      save();
      return wait(moved);
    },
    async deleteCode(coderId, cid) {
      db.codes = db.codes.filter(c => !(c.coder_id === coderId && Number(c.id) === cid));
      db.highlights = db.highlights.filter(h => !(h.coder_id === coderId && Number(h.code_id) === cid));
      save();
      return wait(undefined);
    },
    async createTheme(coderId, name) {
      const ex = db.themes.find(t => t.coder_id === coderId && t.name === name);
      if (ex) return wait(normTheme(ex));
      const t = { id: id(), coder_id: coderId, name, sort_order: 0 };
      db.themes.push(t); save();
      return wait(normTheme(t));
    },
    async deleteTheme(coderId, tid) {
      db.themes = db.themes.filter(t => !(t.coder_id === coderId && Number(t.id) === tid));
      for (const c of db.codes) if (c.coder_id === coderId && Number(c.theme_id) === tid) c.theme_id = null;
      save();
      return wait(undefined);
    },
    async createHighlight(coderId, h) {
      if (!db.codes.some(c => c.coder_id === coderId && Number(c.id) === h.code_id)) throw new ApiError('bad_code', 404);
      const row = { ...h, id: id(), coder_id: coderId, code_id: String(h.code_id), created_at: now() };
      db.highlights.push(row); save();
      return wait(normHl(row));
    },
    async updateHighlight(coderId, hid, codeId) {
      const h = db.highlights.find(x => x.coder_id === coderId && Number(x.id) === hid);
      if (!h) throw new ApiError('not_found', 404);
      h.code_id = String(codeId); save();
      return wait(normHl(h));
    },
    async deleteHighlight(coderId, hid) {
      db.highlights = db.highlights.filter(h => !(h.coder_id === coderId && Number(h.id) === hid));
      save();
      return wait(undefined);
    },
    async putStatus(coderId, s) {
      db.status = db.status.filter(x => !(x.coder_id === coderId && x.sample_id === s.sample_id));
      db.status.push({ ...s, coder_id: coderId, updated_at: now() }); save();
      return wait(normStatus(s));
    },
    async exportAll() {
      return wait({ project: 'Saintiment', mode: 'demo', exported_at: now(), coders: DEMO_CODERS, posts: DEMO_POSTS, external_sources: DEMO_EXT, ...db });
    },
    resetDemo() { db = demoSeed(); save(); },
  };
}

export type Boot = { backend: Backend; authed: boolean } | { offline: true };

// On the real site the API answers JSON (200 or 401). Anywhere else (a claude.ai artifact, a static preview) it does not.
export async function detectBackend(): Promise<Boot> {
  const params = new URLSearchParams(location.search);
  if (params.has('demo')) return { backend: createDemoBackend(), authed: true };
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 5000);
    const res = await fetch('/api/coding/me', { credentials: 'same-origin', signal: ctrl.signal });
    clearTimeout(timer);
    if ((res.headers.get('content-type') || '').includes('json')) {
      if (res.ok) return { backend: createRemoteBackend(), authed: true };
      if (res.status === 401) return { backend: createRemoteBackend(), authed: false };
    }
  } catch { /* falls through */ }
  // Served from /code but the API did not answer: do not silently switch to demo data.
  if (location.protocol.startsWith('http') && location.pathname.startsWith('/code')) return { offline: true };
  return { backend: createDemoBackend(), authed: true };
}

export function errorText(e: unknown): string {
  const code = e instanceof ApiError ? e.code : '';
  return ({
    unauthorized: 'نشست شما تمام شده؛ دوباره وارد شوید',
    wrong_password: 'رمز اشتباه است',
    missing_label: 'نام کد نمی‌تواند خالی باشد',
    not_found: 'این مورد دیگر وجود ندارد؛ صفحه را تازه کنید',
    bad_code: 'این کد دیگر وجود ندارد؛ صفحه را تازه کنید',
    network: 'اتصال برقرار نشد؛ اینترنت را بررسی کنید',
  } as Record<string, string>)[code] || 'ذخیره نشد؛ دوباره تلاش کنید';
}
