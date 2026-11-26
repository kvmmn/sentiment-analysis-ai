import { useCallback, useEffect, useMemo, useState } from 'react';
import type { Backend } from '@/lib/backend';
import type { Source } from '@/lib/types';
import { useStudio } from '@/lib/useStudio';
import { csvCell, download, fa } from '@/lib/text';
import { PostList, matches, type Filter } from './PostList';
import { Reader, type Draft } from './Reader';
import { Codebook, type ConfirmReq } from './Codebook';
import { ConfirmDialog, ShortcutsDialog } from './Dialogs';
import { useToast } from './Toasts';
import { ThemeToggle } from './ThemeToggle';
import { AppNav } from './AppNav';

interface Props {
  backend: Backend;
  coderId: number;
  coderName: string;
  initialPost: string | null;
  onBack: () => void;
  onUnauthorized: () => void;
  onPostChange: (sid: string) => void;
}

const isTyping = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || el.isContentEditable);
};

export function Studio({ backend, coderId, coderName, initialPost, onBack, onUnauthorized, onPostChange }: Props) {
  const toast = useToast();
  const studio = useStudio(backend, coderId, onUnauthorized);
  const { ws } = studio;
  const [current, setCurrent] = useState<string | null>(initialPost);
  const [filter, setFilter] = useState<Filter>('all');
  const [draft, setDraft] = useState<Draft | null>(null);
  const [flash, setFlash] = useState<number | null>(null);
  const [sourceTab, setSourceTab] = useState<Source>('post');
  const [confirmReq, setConfirmReq] = useState<ConfirmReq | null>(null);
  const [help, setHelp] = useState(false);
  const [panel, setPanel] = useState<null | 'posts' | 'codes'>(null);
  const [focusCode, setFocusCode] = useState<number | null>(null);
  const [menu, setMenu] = useState(false);

  // choose a post once data arrives
  useEffect(() => {
    if (!ws) return;
    if (!current || !ws.posts.some(p => p.sample_id === current)) {
      const first = ws.posts.find(p => !ws.status[p.sample_id]?.is_coded) || ws.posts[0];
      if (first) setCurrent(first.sample_id);
    }
  }, [ws, current]);

  useEffect(() => { if (current) onPostChange(current); }, [current, onPostChange]);

  const visible = useMemo(() => (ws ? ws.posts.filter(p => matches(ws, p.sample_id, filter) || p.sample_id === current) : []), [ws, filter, current]);
  const idx = visible.findIndex(p => p.sample_id === current);
  const post = ws?.posts.find(p => p.sample_id === current) || null;

  const go = useCallback((sid: string, opts: { hl?: number } = {}) => {
    setDraft(null);
    setPanel(null);
    if (sid !== current) { setCurrent(sid); document.getElementById('reader-scroll')?.scrollTo({ top: 0 }); }
    if (opts.hl) {
      const h = ws?.highlights.find(x => x.id === opts.hl);
      if (h) setSourceTab(h.source);
      setFlash(opts.hl);
      setTimeout(() => setFlash(f => (f === opts.hl ? null : f)), 2200);
    } else if (sid !== current) setSourceTab('post');
  }, [current, ws]);

  const step = useCallback((d: number) => {
    if (!visible.length) return;
    const next = visible[Math.max(0, Math.min(visible.length - 1, (idx < 0 ? 0 : idx) + d))];
    if (next && next.sample_id !== current) go(next.sample_id);
  }, [visible, idx, current, go]);

  const toggleDone = useCallback(() => {
    if (!post || !ws) return;
    const was = Boolean(ws.status[post.sample_id]?.is_coded);
    studio.setStatus(post.sample_id, { is_coded: !was }, { undoLabel: was ? 'علامت «تمام شد» برداشته شد' : `${post.sample_id} تمام‌شده علامت خورد` });
  }, [post, ws, studio]);

  // keyboard
  useEffect(() => {
    const fn = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'z' && !e.shiftKey) {
        if (isTyping(e.target)) return;
        e.preventDefault(); studio.undo(); return;
      }
      if (isTyping(e.target) || e.altKey || e.ctrlKey || e.metaKey || confirmReq || help) return;
      if (e.key === 'Escape') { setDraft(null); setPanel(null); setMenu(false); return; }
      if (draft) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); step(-1); }
      else if (e.key.toLowerCase() === 'm') { e.preventDefault(); toggleDone(); }
      else if (e.key === '?') { e.preventDefault(); setHelp(true); }
      else if (e.key === '/') { e.preventDefault(); setPanel('codes'); setTimeout(() => (document.querySelector('[aria-label="جست‌وجوی کد"]') as HTMLInputElement | null)?.focus(), 30); }
    };
    window.addEventListener('keydown', fn);
    return () => window.removeEventListener('keydown', fn);
  }, [studio, step, toggleDone, draft, confirmReq, help]);

  const exportJson = async () => {
    setMenu(false);
    try {
      const data = await backend.exportAll();
      download(`saintiment_coding_export${backend.mode === 'demo' ? '_demo' : ''}.json`, JSON.stringify(data, null, 2), 'application/json');
    } catch { toast('خروجی گرفته نشد', { error: true }); }
  };
  const exportCsv = () => {
    setMenu(false);
    if (!ws) return;
    const codes = new Map(ws.codes.map(c => [c.id, c]));
    const themes = new Map(ws.themes.map(t => [t.id, t.name]));
    const rows = [['coder_id', 'sample_id', 'source', 'paragraph_idx', 'start_offset', 'end_offset', 'code', 'theme', 'quote']];
    for (const h of [...ws.highlights].sort((a, b) => a.sample_id.localeCompare(b.sample_id) || a.paragraph_idx - b.paragraph_idx || a.start_offset - b.start_offset)) {
      const c = codes.get(h.code_id);
      rows.push([String(coderId), h.sample_id, h.source, String(h.paragraph_idx), String(h.start_offset), String(h.end_offset), c?.label || '', (c?.theme_id && themes.get(c.theme_id)) || '', h.quote]);
    }
    download(`saintiment_coder${coderId}_segments${backend.mode === 'demo' ? '_demo' : ''}.csv`, '﻿' + rows.map(r => r.map(csvCell).join(',')).join('\n'), 'text/csv;charset=utf-8');
  };

  const syncText = { ok: 'ذخیره شد', wait: 'در حال ذخیره…', bad: 'ذخیره نشد' }[studio.sync];
  const st = post && ws ? ws.status[post.sample_id] : undefined;
  const coded = ws ? ws.posts.filter(p => ws.status[p.sample_id]?.is_coded).length : 0;

  return (
    <div className={`studio flex h-[100dvh] flex-col ${focusCode ? 'focus-mode' : ''}`} data-focus={focusCode ?? undefined}>
      {/* Top bar */}
      <header className="flex h-12 flex-none items-center gap-2 border-b border-[var(--line)] bg-[var(--card)] px-2 sm:px-3">
        <button type="button" className="icon" onClick={onBack} aria-label="بازگشت به کدگذارها" title="بازگشت به کدگذارها">→</button>
        <div className="flex items-baseline gap-2">
          <span className="ltr hidden font-mono text-[12px] tracking-tight text-[var(--muted)] sm:inline">Saintiment / code</span>
          <h1 className="whitespace-nowrap text-[14px] font-bold">{coderName}</h1>
        </div>
        <span className={`sync sync-${studio.sync}`} role="status" aria-live="polite"><i />{syncText}</span>
        {backend.mode === 'demo' && <span className="demo-badge" title="داده‌ها ساختگی‌اند و فقط در همین مرورگر می‌مانند"><span className="hidden sm:inline">حالت </span>نمایشی</span>}
        {backend.mode === 'remote' && <AppNav className="ms-2 hidden 2xl:flex" />}
        <div className="ms-auto flex items-center gap-0.5 sm:gap-1">
          <button type="button" className="icon-text lg:hidden" onClick={() => setPanel(panel === 'posts' ? null : 'posts')} aria-expanded={panel === 'posts'}>پست‌ها</button>
          <button type="button" className="icon-text xl:hidden" onClick={() => setPanel(panel === 'codes' ? null : 'codes')} aria-expanded={panel === 'codes'}>کدنامه</button>
          <button type="button" className="icon" onClick={() => studio.undo()} aria-label="بازگردانی" title="بازگردانی (Ctrl+Z)">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M15 14l5-5-5-5" /><path d="M20 9H9a5 5 0 0 0 0 10h3" /></svg>
          </button>
          <button type="button" className="icon hidden sm:grid" onClick={() => setHelp(true)} aria-label="میان‌برها" title="میان‌برها (?)">?</button>
          <ThemeToggle />
          <div className="relative">
            <button type="button" className="icon" onClick={() => setMenu(m => !m)} aria-expanded={menu} aria-label="خروجی" title="خروجی">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 3v12M7 10l5 5 5-5M5 21h14" /></svg>
            </button>
            {menu && (
              <div className="pop absolute end-0 top-10 z-50 w-60 p-1 text-[13px]" onMouseLeave={() => setMenu(false)}>
                <button type="button" className="menu-item" onClick={exportCsv}>قطعه‌های من (CSV)</button>
                <button type="button" className="menu-item" onClick={exportJson}>خروجی کامل همه (JSON)</button>
                {backend.resetDemo && <button type="button" className="menu-item text-[var(--danger)]" onClick={() => { backend.resetDemo!(); setMenu(false); studio.reload(); }}>بازنشانی دادهٔ نمایشی</button>}
              </div>
            )}
          </div>
        </div>
      </header>

      {!ws ? (
        <div className="grid flex-1 place-items-center p-6 text-center">
          {studio.loadError ? (
            <div className="grid gap-3"><p className="text-[var(--danger)]">{studio.loadError}</p><button type="button" className="btn" onClick={studio.reload}>تلاش دوباره</button></div>
          ) : <p className="animate-pulse text-[var(--muted)]">در حال بارگذاری پست‌ها و کدها…</p>}
        </div>
      ) : (
        <div className="relative flex min-h-0 flex-1 overflow-hidden">
          {/* Posts column (right side in RTL) */}
          <aside className={`side side-posts ${panel === 'posts' ? 'side-open' : ''}`} aria-label="پست‌ها">
            <PostList ws={ws} current={current} onPick={sid => go(sid)} filter={filter} setFilter={setFilter} />
          </aside>

          {/* Reader */}
          <main className="flex min-w-0 flex-1 flex-col">
            <div id="reader-scroll" className="min-h-0 flex-1 overflow-y-auto">
              {post ? (
                <div data-focus-code={focusCode ?? undefined} className={focusCode ? 'focusing' : ''}>
                  {focusCode && (
                    <div className="sticky top-0 z-30 flex items-center justify-between gap-2 border-b border-[var(--line)] bg-[var(--paper)]/95 px-4 py-1.5 text-[12px] backdrop-blur sm:px-8">
                      <span>فقط <b className="ltr font-mono">{studio.derived!.codeById.get(focusCode)?.label}</b> پررنگ است</span>
                      <button type="button" className="link" onClick={() => setFocusCode(null)}>نمایش همه</button>
                    </div>
                  )}
                  <FocusStyle codeId={focusCode} ws={ws} />
                  <Reader key={post.sample_id} studio={studio} post={post} draft={draft} setDraft={setDraft} flashHlId={flash} sourceTab={sourceTab} setSourceTab={setSourceTab} />
                </div>
              ) : <p className="p-8 text-[var(--muted)]">پستی برای نمایش نیست.</p>}
            </div>
            {/* Footer */}
            <footer className="flex flex-none items-center gap-2 border-t border-[var(--line)] bg-[var(--card)] px-3 py-2 pb-[max(8px,env(safe-area-inset-bottom))] sm:px-5">
              <button type="button" className="nav-btn" onClick={() => step(-1)} disabled={idx <= 0} aria-label="پست قبلی" title="پست قبلی (→)">→</button>
              <span className="min-w-[64px] text-center text-[12px] tabular-nums text-[var(--muted)]">{fa(idx + 1)} / {fa(visible.length)}</span>
              <button type="button" className="nav-btn" onClick={() => step(1)} disabled={idx >= visible.length - 1} aria-label="پست بعدی" title="پست بعدی (←)">←</button>
              <span className="hidden text-[12px] text-[var(--faint)] md:inline">· {fa(coded)} پست تمام شده</span>
              <button type="button" onClick={toggleDone} aria-pressed={Boolean(st?.is_coded)} title="(M)"
                className={`done-btn ms-auto ${st?.is_coded ? 'done-on' : ''}`}>
                {st?.is_coded ? '✓ تمام شد' : 'علامت: تمام شد'}
              </button>
              {st?.is_coded && idx < visible.length - 1 && (
                <button type="button" className="btn" onClick={() => step(1)}>بعدی ←</button>
              )}
            </footer>
          </main>

          {/* Codebook column (left side in RTL) */}
          <aside className={`side side-codes ${panel === 'codes' ? 'side-open' : ''}`} aria-label="کدنامه">
            <Codebook studio={studio} confirm={setConfirmReq} onJump={(sid, hl) => go(sid, { hl })} focusCodeId={focusCode} setFocusCodeId={setFocusCode} />
          </aside>
          {panel && <button type="button" aria-label="بستن" className="scrim" onClick={() => setPanel(null)} />}
        </div>
      )}

      {confirmReq && <ConfirmDialog req={confirmReq} onClose={() => setConfirmReq(null)} />}
      {help && <ShortcutsDialog onClose={() => setHelp(false)} />}
    </div>
  );
}

// Dims every highlight except the focused code's ones.
function FocusStyle({ codeId, ws }: { codeId: number | null; ws: { highlights: { id: number; code_id: number }[] } }) {
  if (!codeId) return null;
  const ids = ws.highlights.filter(h => h.code_id === codeId).map(h => `[data-hl="${h.id}"]`);
  const keep = ids.length ? `:not(${ids.join(',')})` : '';
  return <style>{`.focusing .hl${keep}{background:transparent!important;box-shadow:none!important;opacity:.55}.focusing .hl-tag{opacity:.35}`}</style>;
}
