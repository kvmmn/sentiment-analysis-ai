import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ApiError, errorText, type Backend } from './backend';
import type { Code, Highlight, NewHighlight, PostStatus, Workspace } from './types';
import { useToast } from '@/components/Toasts';

export type CodeRef = { id: number } | { label: string };
interface UndoEntry { label: string; run: () => Promise<void> }

export function useStudio(backend: Backend, coderId: number, onUnauthorized: () => void) {
  const toast = useToast();
  const [ws, setWsState] = useState<Workspace | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [pending, setPending] = useState(0);
  const [failed, setFailed] = useState(false);
  const wsRef = useRef<Workspace | null>(null);
  const undoStack = useRef<UndoEntry[]>([]);
  const temp = useRef(-1);

  const setWs = useCallback((fn: (w: Workspace) => Workspace) => {
    setWsState(w => {
      const next = w ? fn(w) : w;
      wsRef.current = next;
      return next;
    });
  }, []);

  const load = useCallback(async () => {
    setLoadError(null);
    setWsState(null);
    try {
      const w = await backend.workspace(coderId);
      wsRef.current = w;
      setWsState(w);
    } catch (e) {
      if (e instanceof ApiError && e.code === 'unauthorized') return onUnauthorized();
      setLoadError(errorText(e));
    }
  }, [backend, coderId, onUnauthorized]);

  useEffect(() => { load(); }, [load]);

  const fail = useCallback((e: unknown) => {
    if (e instanceof ApiError && e.code === 'unauthorized') onUnauthorized();
    toast(errorText(e), { error: true });
  }, [toast, onUnauthorized]);

  async function track<T>(p: Promise<T>): Promise<T> {
    setPending(x => x + 1);
    try {
      const r = await p;
      setFailed(false);
      return r;
    } catch (e) {
      setFailed(true);
      throw e;
    } finally {
      setPending(x => x - 1);
    }
  }

  const pushUndo = (label: string, run: () => Promise<void>) => {
    const entry = { label, run };
    undoStack.current.push(entry);
    if (undoStack.current.length > 30) undoStack.current.shift();
    toast(label, { action: { label: 'بازگردانی', run: () => runUndo(entry) } });
  };
  const runUndo = async (entry: UndoEntry) => {
    undoStack.current = undoStack.current.filter(x => x !== entry);
    try { await entry.run(); toast('بازگردانده شد'); } catch (e) { fail(e); }
  };
  const undo = () => {
    const last = undoStack.current[undoStack.current.length - 1];
    if (last) runUndo(last); else toast('کاری برای بازگردانی نیست');
  };

  const nextColor = () => {
    const codes = wsRef.current?.codes || [];
    const counts = [1, 2, 3, 4, 5, 6].map(c => codes.filter(x => x.color_idx === c).length);
    return counts.indexOf(Math.min(...counts)) + 1;
  };

  const findByLabel = (label: string) => wsRef.current?.codes.find(c => c.label.toLowerCase() === label.trim().toLowerCase());

  async function ensureCode(ref: CodeRef): Promise<{ code: Code; created: boolean }> {
    if ('id' in ref) {
      const c = wsRef.current?.codes.find(x => x.id === ref.id);
      if (!c) throw new ApiError('bad_code');
      return { code: c, created: false };
    }
    const label = ref.label.trim().slice(0, 120);
    if (!label) throw new ApiError('missing_label');
    const local = findByLabel(label);
    if (local) return { code: local, created: false };
    const r = await track(backend.createCode(coderId, label, nextColor(), null));
    setWs(w => (w.codes.some(c => c.id === r.code.id) ? w : { ...w, codes: [...w.codes, r.code] }));
    return { code: r.code, created: !r.existed };
  }

  // ---- highlights
  async function insertHighlight(h: NewHighlight): Promise<Highlight> {
    const tmp: Highlight = { ...h, id: temp.current--, created_at: new Date().toISOString() };
    setWs(w => ({ ...w, highlights: [...w.highlights, tmp] }));
    try {
      const saved = await track(backend.createHighlight(coderId, h));
      setWs(w => ({ ...w, highlights: w.highlights.map(x => (x.id === tmp.id ? saved : x)) }));
      return saved;
    } catch (e) {
      setWs(w => ({ ...w, highlights: w.highlights.filter(x => x.id !== tmp.id) }));
      throw e;
    }
  }

  async function removeHighlightRaw(id: number) {
    const prev = wsRef.current?.highlights.find(h => h.id === id);
    if (!prev) return null;
    setWs(w => ({ ...w, highlights: w.highlights.filter(h => h.id !== id) }));
    try {
      await track(backend.deleteHighlight(coderId, id));
      return prev;
    } catch (e) {
      setWs(w => ({ ...w, highlights: [...w.highlights, prev] }));
      throw e;
    }
  }

  async function addHighlight(draft: Omit<NewHighlight, 'code_id'>, ref: CodeRef) {
    try {
      const { code, created } = await ensureCode(ref);
      const saved = await insertHighlight({ ...draft, code_id: code.id });
      pushUndo(created ? `کد تازهٔ «${code.label}» ساخته و اعمال شد` : `«${code.label}» اعمال شد`, async () => { await removeHighlightRaw(saved.id); });
    } catch (e) { fail(e); }
  }

  async function changeHighlightCode(id: number, ref: CodeRef) {
    const prev = wsRef.current?.highlights.find(h => h.id === id);
    if (!prev) return;
    try {
      const { code } = await ensureCode(ref);
      if (code.id === prev.code_id) return;
      const swap = async (to: number, from: number) => {
        setWs(w => ({ ...w, highlights: w.highlights.map(h => (h.id === id ? { ...h, code_id: to } : h)) }));
        try { await track(backend.updateHighlight(coderId, id, to)); } catch (e) {
          setWs(w => ({ ...w, highlights: w.highlights.map(h => (h.id === id ? { ...h, code_id: from } : h)) }));
          throw e;
        }
      };
      await swap(code.id, prev.code_id);
      pushUndo(`کد به «${code.label}» تغییر کرد`, () => swap(prev.code_id, code.id));
    } catch (e) { fail(e); }
  }

  async function deleteHighlight(id: number) {
    try {
      const prev = await removeHighlightRaw(id);
      if (!prev) return;
      const { id: _drop, created_at: _c, ...rest } = prev;
      void _drop; void _c;
      pushUndo('هایلایت حذف شد', async () => { await insertHighlight(rest); });
    } catch (e) { fail(e); }
  }

  async function deleteHighlights(ids: number[]) {
    const removed: Highlight[] = [];
    try {
      for (const id of ids) { const r = await removeHighlightRaw(id); if (r) removed.push(r); }
    } catch (e) { fail(e); }
    if (!removed.length) return;
    pushUndo(removed.length > 1 ? `${removed.length.toLocaleString('fa-IR')} کد از این عبارت برداشته شد` : 'هایلایت حذف شد', async () => {
      for (const h of removed) { const { id: _i, created_at: _c, ...rest } = h; void _i; void _c; await insertHighlight(rest); }
    });
  }

  // ---- codes
  async function updateCode(id: number, patch: Partial<Pick<Code, 'label' | 'color_idx' | 'theme_id'>>, { quiet = false } = {}) {
    const prev = wsRef.current?.codes.find(c => c.id === id);
    if (!prev) return;
    const apply = async (p: typeof patch, back: typeof patch) => {
      setWs(w => ({ ...w, codes: w.codes.map(c => (c.id === id ? { ...c, ...p } : c)) }));
      try { await track(backend.updateCode(coderId, id, p)); } catch (e) {
        setWs(w => ({ ...w, codes: w.codes.map(c => (c.id === id ? { ...c, ...back } : c)) }));
        throw e;
      }
    };
    const back: typeof patch = {};
    for (const k of Object.keys(patch) as (keyof typeof patch)[]) (back as Record<string, unknown>)[k] = prev[k];
    try {
      await apply(patch, back);
      if (!quiet) pushUndo(patch.label ? `نام کد به «${patch.label}» تغییر کرد` : 'کد به‌روز شد', () => apply(back, patch));
    } catch (e) { fail(e); }
  }

  async function mergeCode(sourceId: number, targetId: number) {
    try {
      const moved = await track(backend.mergeCode(coderId, sourceId, targetId));
      setWs(w => ({
        ...w,
        codes: w.codes.filter(c => c.id !== sourceId),
        highlights: w.highlights.map(h => (h.code_id === sourceId ? { ...h, code_id: targetId } : h)),
      }));
      const t = wsRef.current?.codes.find(c => c.id === targetId);
      toast(`ادغام شد: ${moved.toLocaleString('fa-IR')} قطعه به «${t?.label ?? ''}» منتقل شد`);
    } catch (e) { fail(e); }
  }

  async function deleteCode(id: number) {
    const w0 = wsRef.current;
    const code = w0?.codes.find(c => c.id === id);
    if (!w0 || !code) return;
    const hls = w0.highlights.filter(h => h.code_id === id);
    setWs(w => ({ ...w, codes: w.codes.filter(c => c.id !== id), highlights: w.highlights.filter(h => h.code_id !== id) }));
    try {
      await track(backend.deleteCode(coderId, id));
      pushUndo(`کد «${code.label}» حذف شد`, async () => {
        const r = await track(backend.createCode(coderId, code.label, code.color_idx, code.theme_id));
        setWs(w => ({ ...w, codes: [...w.codes.filter(c => c.id !== r.code.id), r.code] }));
        for (const h of hls) {
          const { id: _i, created_at: _c, ...rest } = h;
          void _i; void _c;
          await insertHighlight({ ...rest, code_id: r.code.id });
        }
      });
    } catch (e) {
      setWs(w => ({ ...w, codes: [...w.codes, code], highlights: [...w.highlights, ...hls] }));
      fail(e);
    }
  }

  async function createCode(label: string) {
    try {
      const existing = findByLabel(label);
      if (existing) { toast(`«${existing.label}» از قبل هست`); return existing; }
      const { code } = await ensureCode({ label });
      toast(`کد «${code.label}» ساخته شد`);
      return code;
    } catch (e) { fail(e); return null; }
  }

  // ---- themes
  async function createTheme(name: string) {
    const clean = name.trim().slice(0, 120);
    if (!clean) return null;
    try {
      const t = await track(backend.createTheme(coderId, clean));
      setWs(w => ({ ...w, themes: w.themes.some(x => x.id === t.id) ? w.themes : [...w.themes, t] }));
      return t;
    } catch (e) { fail(e); return null; }
  }

  async function deleteTheme(id: number) {
    try {
      await track(backend.deleteTheme(coderId, id));
      setWs(w => ({ ...w, themes: w.themes.filter(t => t.id !== id), codes: w.codes.map(c => (c.theme_id === id ? { ...c, theme_id: null } : c)) }));
      toast('تم حذف شد؛ کدهایش «بدون تم» شدند');
    } catch (e) { fail(e); }
  }

  // ---- post status
  const blank = (sid: string): PostStatus => ({ sample_id: sid, is_coded: false, link_reviewed: false, coder_notes: '' });
  async function setStatus(sid: string, patch: Partial<PostStatus>, { undoLabel }: { undoLabel?: string } = {}) {
    const prev = wsRef.current?.status[sid] || blank(sid);
    const next = { ...prev, ...patch, sample_id: sid };
    const write = async (to: PostStatus, from: PostStatus) => {
      setWs(w => ({ ...w, status: { ...w.status, [sid]: to } }));
      try { await track(backend.putStatus(coderId, to)); } catch (e) {
        setWs(w => ({ ...w, status: { ...w.status, [sid]: from } }));
        throw e;
      }
    };
    try {
      await write(next, prev);
      if (undoLabel) pushUndo(undoLabel, () => write({ ...(wsRef.current?.status[sid] || blank(sid)), ...Object.fromEntries(Object.keys(patch).map(k => [k, prev[k as keyof PostStatus]])) } as PostStatus, next));
      return true;
    } catch (e) { fail(e); return false; }
  }

  const sync: 'ok' | 'wait' | 'bad' = pending > 0 ? 'wait' : failed ? 'bad' : 'ok';

  const derived = useMemo(() => {
    if (!ws) return null;
    const codeById = new Map(ws.codes.map(c => [c.id, c]));
    const countByCode = new Map<number, number>();
    for (const h of ws.highlights) countByCode.set(h.code_id, (countByCode.get(h.code_id) || 0) + 1);
    const recent: number[] = [];
    for (const h of [...ws.highlights].sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)))) {
      if (!recent.includes(h.code_id)) recent.push(h.code_id);
    }
    for (const c of ws.codes) if (!recent.includes(c.id)) recent.push(c.id);
    return { codeById, countByCode, recent: recent.filter(id => codeById.has(id)) };
  }, [ws]);

  return {
    ws, derived, loadError, reload: load, sync, undo,
    addHighlight, changeHighlightCode, deleteHighlight, deleteHighlights,
    createCode, updateCode, mergeCode, deleteCode, findByLabel,
    createTheme, deleteTheme, setStatus,
  };
}

export type Studio = ReturnType<typeof useStudio>;
