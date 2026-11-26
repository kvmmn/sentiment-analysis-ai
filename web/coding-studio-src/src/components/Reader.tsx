import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import type { Post, Source } from '@/lib/types';
import type { Studio } from '@/lib/useStudio';
import { FETCH_LABEL, colorVar, fa, offsetIn, splitParagraphs } from '@/lib/text';
import { Paragraph } from './Paragraph';
import { CodePicker } from './CodePicker';
import type { CodeRef } from '@/lib/useStudio';
import { useToast } from './Toasts';

// A passage being coded. It can carry several codes: one highlight row per code, all with the same range.
export interface Draft { source: Source; pIdx: number; start: number; end: number; quote: string; extId: number | null; anchor: DOMRect }

interface Props {
  studio: Studio;
  post: Post;
  draft: Draft | null;
  setDraft: (d: Draft | null) => void;
  flashHlId: number | null;
  sourceTab: Source;
  setSourceTab: (s: Source) => void;
  showTags: boolean;
}


export function Reader({ studio, post, draft, setDraft, flashHlId, sourceTab, setSourceTab, showTags }: Props) {
  const toast = useToast();
  const { ws, derived } = studio;
  const wrap = useRef<HTMLDivElement>(null);
  const pop = useRef<HTMLDivElement>(null);
  const lastPointer = useRef<'mouse' | 'touch'>('mouse');
  const [popPos, setPopPos] = useState<{ top?: number; bottom?: number; left: number } | null>(null);
  const [narrow, setNarrow] = useState(() => window.matchMedia('(max-width: 639px)').matches);

  useEffect(() => {
    const mq = window.matchMedia('(max-width: 639px)');
    const fn = () => setNarrow(mq.matches);
    mq.addEventListener('change', fn);
    return () => mq.removeEventListener('change', fn);
  }, []);

  const exts = useMemo(() => ws!.ext.filter(e => e.sample_id === post.sample_id), [ws, post.sample_id]);
  const extracted = exts.find(e => e.fetch_status === 'extracted' && e.extracted_text);
  const firstExt = extracted || exts[0] || null;
  const source: Source = sourceTab === 'external' && extracted ? 'external' : 'post';
  const paragraphs = useMemo(() => splitParagraphs(source === 'external' ? extracted!.extracted_text : post.post_text), [source, extracted, post.post_text]);
  const status = ws!.status[post.sample_id];
  const postHls = useMemo(() => ws!.highlights.filter(h => h.sample_id === post.sample_id), [ws, post.sample_id]);
  const hlsByP = useMemo(() => {
    const m = new Map<number, typeof postHls>();
    for (const h of postHls) if (h.source === source) m.set(h.paragraph_idx, [...(m.get(h.paragraph_idx) || []), h]);
    return m;
  }, [postHls, source]);

  // ---- open the picker
  const openNew = useCallback((pIdx: number, start: number, end: number, rect: DOMRect) => {
    const text = paragraphs[pIdx] || '';
    setDraft({ source, pIdx, start, end, quote: text.slice(start, end), extId: source === 'external' ? extracted?.id ?? null : null, anchor: rect });
  }, [paragraphs, source, extracted, setDraft]);

  const onSentence = useCallback((pIdx: number, start: number, end: number, el: HTMLElement) => openNew(pIdx, start, end, el.getBoundingClientRect()), [openNew]);
  const openFor = useCallback((hlId: number, el: HTMLElement) => {
    const h = ws!.highlights.find(x => x.id === hlId);
    if (!h || h.paragraph_idx < 0) return;
    setDraft({ source: h.source, pIdx: h.paragraph_idx, start: h.start_offset, end: h.end_offset, quote: h.quote, extId: h.external_source_id, anchor: el.getBoundingClientRect() });
  }, [ws, setDraft]);
  const onHighlight = openFor;

  const capture = useCallback(() => {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.rangeCount || !wrap.current) return;
    const r = sel.getRangeAt(0);
    const pOf = (n: Node) => ((n.nodeType === 1 ? n as Element : n.parentElement)?.closest('[data-pidx]') as HTMLElement | null);
    const pa = pOf(r.startContainer), pb = pOf(r.endContainer);
    if (!pa && !pb) return;
    if (!wrap.current.contains(pa || pb)) return;
    if (!pa || pa !== pb) { toast('انتخاب را داخل یک پاراگراف نگه دارید'); return; }
    const pIdx = Number(pa.dataset.pidx);
    const text = paragraphs[pIdx] || '';
    let s = offsetIn(pa, r.startContainer, r.startOffset);
    let e = offsetIn(pa, r.endContainer, r.endOffset);
    if (s > e) [s, e] = [e, s];
    while (s < e && /\s/.test(text[s])) s++;
    while (e > s && /\s/.test(text[e - 1])) e--;
    if (e - s < 2) return;
    const rect = r.getBoundingClientRect();
    sel.removeAllRanges();
    openNew(pIdx, s, e, rect);
  }, [paragraphs, openNew, toast]);

  useEffect(() => {
    let t: number | undefined;
    const onSel = () => {
      if (lastPointer.current !== 'touch') return;
      clearTimeout(t);
      t = window.setTimeout(capture, 650);
    };
    document.addEventListener('selectionchange', onSel);
    return () => { document.removeEventListener('selectionchange', onSel); clearTimeout(t); };
  }, [capture]);

  // Close on outside press
  useEffect(() => {
    if (!draft) return;
    const fn = (e: PointerEvent) => {
      const t = e.target as Element;
      if (pop.current?.contains(t) || t.closest?.('[data-pidx]')) return;
      setDraft(null);
    };
    document.addEventListener('pointerdown', fn);
    return () => document.removeEventListener('pointerdown', fn);
  }, [draft, setDraft]);

  useLayoutEffect(() => {
    if (!draft || !wrap.current || narrow) { setPopPos(null); return; }
    const w = wrap.current.getBoundingClientRect();
    const a = draft.anchor;
    const width = Math.min(300, w.width - 16);
    const left = Math.max(8, Math.min(w.width - width - 8, a.left - w.left + a.width / 2 - width / 2));
    const scroller = document.getElementById('reader-scroll')?.getBoundingClientRect();
    const roomAbove = a.top - (scroller?.top ?? 0);
    // Sit above the passage (anchored by its bottom edge, so it grows upward) to keep the following lines
    // readable; near the top edge fall back to below.
    if (roomAbove > 150) setPopPos({ bottom: w.bottom - a.top + 6, left });
    else setPopPos({ top: a.bottom - w.top + 6, left });
  }, [draft, narrow]);

  useEffect(() => {
    if (!flashHlId) return;
    wrap.current?.querySelector(`[data-hl="${flashHlId}"]`)?.scrollIntoView({ block: 'center', behavior: 'smooth' });
  }, [flashHlId, source]);

  const sameRange = (h: { source: string; paragraph_idx: number; start_offset: number; end_offset: number }, d: Draft) =>
    h.source === d.source && h.paragraph_idx === d.pIdx && h.start_offset === d.start && h.end_offset === d.end;
  const rangeHls = draft ? postHls.filter(h => sameRange(h, draft)) : [];
  const applied = new Set(rangeHls.map(h => h.code_id));
  const activeIds = useMemo(() => new Set([...rangeHls.map(h => h.id), ...(flashHlId ? [flashHlId] : [])]),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [rangeHls.map(h => h.id).join(','), flashHlId]);
  const pickerCodes = derived!.recent.map(id => derived!.codeById.get(id)!).filter(Boolean);

  const toggle = (ref: CodeRef, on: boolean) => {
    if (!draft) return;
    const d = draft;
    const id = 'id' in ref ? ref.id : studio.findByLabel(ref.label)?.id;
    const mine = id === undefined ? [] : rangeHls.filter(h => h.code_id === id);
    if (mine.some(h => h.id < 0)) return; // still saving
    if (on) {
      if (mine.length) return;
      studio.addHighlight({ sample_id: post.sample_id, source: d.source, external_source_id: d.extId, paragraph_idx: d.pIdx, start_offset: d.start, end_offset: d.end, quote: d.quote }, id === undefined ? ref : { id });
    } else {
      for (const h of mine) studio.deleteHighlight(h.id);
    }
  };

  const picker = draft && (
    <CodePicker
      key={`${draft.source}-${draft.pIdx}-${draft.start}-${draft.end}`}
      codes={pickerCodes}
      counts={derived!.countByCode}
      applied={applied}
      focusToken={draft.anchor}
      dropUp={narrow || popPos?.bottom !== undefined}
      onClose={() => setDraft(null)}
      onToggle={toggle}
    />
  );

  const groups = useMemo(() => {
    const m = new Map<string, typeof postHls>();
    const sorted = [...postHls].sort((a, b) => (a.source === b.source ? a.paragraph_idx - b.paragraph_idx || a.start_offset - b.start_offset || a.id - b.id : a.source === 'post' ? -1 : 1));
    for (const h of sorted) {
      const key = h.paragraph_idx < 0 ? `m${h.id}` : `${h.source}|${h.paragraph_idx}|${h.start_offset}|${h.end_offset}`;
      m.set(key, [...(m.get(key) || []), h]);
    }
    return [...m.entries()].map(([key, hls]) => ({ key, hls }));
  }, [postHls]);

  // ---- manual code for links that could not be extracted
  const [mQuote, setMQuote] = useState('');
  const [mCode, setMCode] = useState('');
  const addManual = () => {
    const quote = mQuote.trim(), label = mCode.trim();
    if (!quote || !label) { toast('نقل‌قول و نام کد هر دو لازم است', { error: true }); return; }
    studio.addHighlight({ sample_id: post.sample_id, source: 'external', external_source_id: exts[0]?.id ?? null, paragraph_idx: -1, start_offset: 0, end_offset: 0, quote }, { label });
    setMQuote(''); setMCode('');
  };

  // ---- notes (memo), saved after a pause and on blur
  const [notes, setNotes] = useState(status?.coder_notes || '');
  const savedNotes = useRef(status?.coder_notes || '');
  const [notesState, setNotesState] = useState<'idle' | 'dirty' | 'saved'>('idle');
  const notesRef = useRef(notes);
  notesRef.current = notes;
  const setStatusRef = useRef(studio.setStatus);
  setStatusRef.current = studio.setStatus;
  // Reader is keyed by post, so this runs when leaving a post: save a memo typed just before switching.
  useEffect(() => {
    const sid = post.sample_id;
    return () => { if (notesRef.current !== savedNotes.current) setStatusRef.current(sid, { coder_notes: notesRef.current }); };
  }, [post.sample_id]);
  const flushNotes = useCallback(async (value: string) => {
    if (value === savedNotes.current) return;
    const ok = await studio.setStatus(post.sample_id, { coder_notes: value });
    if (ok) { savedNotes.current = value; setNotesState('saved'); }
  }, [studio, post.sample_id]);
  useEffect(() => {
    if (notesState !== 'dirty') return;
    const t = setTimeout(() => flushNotes(notes), 900);
    return () => clearTimeout(t);
  }, [notes, notesState, flushNotes]);

  const metrics = [
    ['واکنش', post.reactions], ['نظر', post.comments], ['اشتراک', post.shares],
  ].filter(([, v]) => v !== null && v !== undefined) as [string, number][];

  return (
    <article className="mx-auto w-full max-w-[760px] px-4 pb-10 pt-5 sm:px-8">
      {/* Meta */}
      <header className="mb-5 grid gap-1.5">
        <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1">
          <span className="sid">{post.sample_id}</span>
          <h2 className="ltr text-[17px] font-bold leading-snug" dir="auto">{post.author_name || 'Unknown'}</h2>
          <span className="tag">{post.author_type === 'company' ? 'صفحهٔ شرکت' : post.author_type === 'profile' ? 'فرد' : post.author_type || '—'}</span>
          {post.has_external_link && <span className="tag tag-warn">لینک بیرونی</span>}
        </div>
        {post.author_headline && <p className="ltr text-[13px] text-[var(--muted)]" dir="auto">{post.author_headline}</p>}
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-[12.5px] text-[var(--muted)]">
          {post.posted_at && <span className="ltr tabular-nums">{post.posted_at}</span>}
          {metrics.map(([k, v]) => <span key={k}>{fa(v)} {k}</span>)}
          {post.post_url && <a href={post.post_url} target="_blank" rel="noopener noreferrer" className="link">LinkedIn ↗</a>}
        </div>
      </header>

      {/* External link */}
      {(post.has_external_link || exts.length > 0) && (
        <section className="mb-5 rounded-[6px] border border-[var(--line)] bg-[var(--card)] p-3 text-[13px]">
          <div className="flex flex-wrap items-center justify-between gap-2">
            {extracted ? (
              <div className="seg" role="tablist" aria-label="منبع متن">
                <button type="button" role="tab" aria-selected={source === 'post'} className={source === 'post' ? 'on' : ''} onClick={() => { setDraft(null); setSourceTab('post'); }}>متن پست</button>
                <button type="button" role="tab" aria-selected={source === 'external'} className={source === 'external' ? 'on' : ''} onClick={() => { setDraft(null); setSourceTab('external'); }}>مقالهٔ استخراج‌شده</button>
              </div>
            ) : <span className="font-semibold">لینک بیرونی</span>}
            <div className="flex items-center gap-3">
              <a className="link" href={firstExt?.resolved_url || firstExt?.original_url || post.newsletter_url || post.post_url || '#'} target="_blank" rel="noopener noreferrer">لینک اصلی ↗</a>
              <label className="flex cursor-pointer items-center gap-1.5">
                <input type="checkbox" className="accent-[var(--accent)]" checked={Boolean(status?.link_reviewed)} onChange={e => studio.setStatus(post.sample_id, { link_reviewed: e.target.checked })} />
                <span>لینک بررسی شد</span>
              </label>
            </div>
          </div>
          <p className="mt-2 text-[12.5px] text-[var(--muted)]">
            {firstExt ? <><b className="ltr text-[var(--ink)]">{firstExt.domain || 'link'}</b>{firstExt.title && <> — <span className="ltr" dir="auto">{firstExt.title}</span></>} · {FETCH_LABEL[firstExt.fetch_status] || firstExt.fetch_status}</> : (post.newsletter_title || 'لینک بیرونی پیوست است')}
          </p>
          {!extracted && (
            <div className="mt-3 grid gap-2 border-t border-dashed border-[var(--line)] pt-3">
              <p className="text-[12.5px] text-[var(--muted)]">متن لینک در دسترس نبود. اگر نکتهٔ مهمی در آن دیدید، اینجا ثبتش کنید:</p>
              <div className="flex flex-wrap gap-2">
                <input value={mQuote} onChange={e => setMQuote(e.target.value)} dir="auto" maxLength={2000} placeholder="نقل‌قول یا نکتهٔ کلیدی…" aria-label="نقل‌قول از لینک" className="field min-w-[180px] flex-[2]" />
                <input value={mCode} onChange={e => setMCode(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addManual(); } }} dir="auto" maxLength={120} list="code-labels" placeholder="کد…" aria-label="کد" className="field min-w-[120px] flex-1" />
                <datalist id="code-labels">{ws!.codes.map(c => <option key={c.id} value={c.label} />)}</datalist>
                <button type="button" className="btn" onClick={addManual}>ثبت</button>
              </div>
            </div>
          )}
        </section>
      )}

      {/* Prose */}
      <div
        ref={wrap}
        className="relative"
        onPointerDown={e => { lastPointer.current = e.pointerType === 'touch' ? 'touch' : 'mouse'; }}
        onMouseUp={() => { if (lastPointer.current === 'mouse') setTimeout(capture, 0); }}
      >
        <p className="mb-3 text-[12px] text-[var(--faint)]">روی یک جمله بزنید یا بخشی از متن را انتخاب کنید. روی هایلایت بزنید تا کدش را عوض یا حذف کنید.</p>
        <div className={`prose-body ${source === 'external' ? 'is-ext' : ''}`}>
          {paragraphs.length ? paragraphs.map((t, i) => (
            <Paragraph key={`${source}-${i}`} pIdx={i} text={t} hls={hlsByP.get(i) || []} codeById={derived!.codeById}
              draft={draft && draft.pIdx === i && draft.source === source && !rangeHls.length ? draft : null}
              activeHlIds={activeIds} showTags={showTags}
              onSentence={onSentence} onHighlight={onHighlight} />
          )) : <p className="text-[var(--muted)]">این پست متنی ندارد.</p>}
        </div>
        {picker && !narrow && popPos && (
          <div ref={pop} role="dialog" aria-label="انتخاب کد" className="pop absolute z-40 w-[300px] max-w-[calc(100%-16px)]" style={{ top: popPos.top, bottom: popPos.bottom, left: popPos.left }}>
            {picker}
          </div>
        )}
      </div>
      {picker && narrow && (
        <div ref={pop} role="dialog" aria-label="انتخاب کد" className="sheet fixed inset-x-0 bottom-0 z-[60] pb-[env(safe-area-inset-bottom)]">
          {picker}
        </div>
      )}

      {/* Segments on this post */}
      <section className="mt-8 border-t border-[var(--line)] pt-4">
        <div className="mb-2 flex items-baseline justify-between text-[12.5px] text-[var(--muted)]">
          <h3 className="font-semibold text-[var(--ink)]">قطعه‌های کدگذاری‌شدهٔ این پست</h3>
          <span>{fa(groups.length)} عبارت · {fa(postHls.length)} کد</span>
        </div>
        {groups.length ? (
          <ul className="grid gap-1">
            {groups.map(g => (
              <li key={g.key} className="flex items-start gap-2 rounded-[4px] px-2 py-1.5 hover:bg-[var(--sunk)]">
                <div className="flex min-w-0 flex-1 flex-col gap-1">
                  <div className="flex flex-wrap items-center gap-1">
                    {g.hls.map(h => {
                      const code = derived!.codeById.get(h.code_id);
                      const c = colorVar(code?.color_idx);
                      return (
                        <span key={h.id} className="ltr inline-flex items-center rounded-[3px] font-mono text-[11.5px]" style={{ background: c.bg, color: c.fg }}>
                          <span className="ps-1.5">{code?.label}</span>
                          <button type="button" className="px-1.5 opacity-60 hover:opacity-100" onClick={() => studio.deleteHighlight(h.id)} aria-label={`برداشتن ${code?.label ?? ''}`} title="برداشتن این کد">×</button>
                        </span>
                      );
                    })}
                    {g.hls[0].source === 'external' && <span className="text-[11px] text-[var(--muted)]">[لینک]</span>}
                  </div>
                  <button type="button" className="text-start disabled:opacity-100" disabled={g.hls[0].paragraph_idx < 0} title="نمایش و ویرایش در متن"
                    onClick={() => {
                      const h = g.hls[0];
                      if (h.source !== source) setSourceTab(h.source);
                      setTimeout(() => {
                        const el = wrap.current?.querySelector(`[data-hl="${h.id}"]`) as HTMLElement | null;
                        if (el) { el.scrollIntoView({ block: 'center', behavior: 'smooth' }); openFor(h.id, el); }
                      }, 60);
                    }}>
                    <span className="ltr line-clamp-2 text-[13px] text-[var(--muted)]" dir="auto">“{g.hls[0].quote}”</span>
                  </button>
                </div>
                {g.hls.length > 1 && <span className="mt-0.5 text-[11px] text-[var(--faint)]">{fa(g.hls.length)} کد</span>}
              </li>
            ))}
          </ul>
        ) : <p className="text-[12.5px] text-[var(--faint)]">هنوز چیزی در این پست کدگذاری نشده.</p>}
      </section>

      {/* Memo */}
      <section className="mt-6">
        <label htmlFor="memo" className="mb-1.5 flex items-baseline justify-between text-[12.5px]">
          <span className="font-semibold">یادداشت تحلیلی (memo)</span>
          <span className="text-[var(--faint)]">{notesState === 'dirty' ? 'در حال نوشتن…' : notesState === 'saved' ? 'ذخیره شد' : 'فقط برای همین کدگذار'}</span>
        </label>
        <textarea id="memo" value={notes} dir="auto" maxLength={4000} rows={3}
          onChange={e => { setNotes(e.target.value); setNotesState('dirty'); }}
          onBlur={() => flushNotes(notes)}
          placeholder="برداشت، تردید یا ایده‌ای دربارهٔ این پست…"
          className="field w-full resize-y leading-7" />
      </section>
    </article>
  );
}
