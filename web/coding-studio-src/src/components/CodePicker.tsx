import { useEffect, useMemo, useRef, useState } from 'react';
import type { Code } from '@/lib/types';
import { colorVar, fa } from '@/lib/text';
import type { CodeRef } from '@/lib/useStudio';

interface Props {
  codes: Code[]; // "recently used" order
  counts: Map<number, number>;
  applied: Set<number>; // codes already on this exact passage
  onToggle: (ref: CodeRef, on: boolean) => void;
  onClose: () => void;
  focusToken?: unknown; // changes when the same passage is clicked again
  dropUp?: boolean; // suggestions open upward when the bar sits above the passage
}

const RECENT = 6;

// Compact tag bar: tags already on the passage (pinned), recent tags one tap away, and one input.
// Suggestions appear only while typing, so the text around the passage stays visible.
export function CodePicker({ codes, counts, applied, onToggle, onClose, focusToken, dropUp }: Props) {
  const [q, setQ] = useState('');
  const [active, setActive] = useState(0);
  const input = useRef<HTMLInputElement>(null);

  useEffect(() => { input.current?.focus({ preventScroll: true }); }, [focusToken]);

  // Recent row is fixed at open time so chips do not jump while toggling.
  const recentIds = useRef(codes.filter(c => !applied.has(c.id)).slice(0, RECENT).map(c => c.id));
  const byId = useMemo(() => new Map(codes.map(c => [c.id, c])), [codes]);
  const pinned = codes.filter(c => applied.has(c.id));
  const recent = recentIds.current.map(id => byId.get(id)).filter((c): c is Code => Boolean(c) && !applied.has(c!.id));

  const query = q.trim().toLowerCase();
  const matches = useMemo(() => {
    if (!query) return [];
    const list = codes.filter(c => c.label.toLowerCase().includes(query));
    return list.sort((a, b) =>
      Number(a.label.toLowerCase() !== query) - Number(b.label.toLowerCase() !== query) ||
      Number(!a.label.toLowerCase().startsWith(query)) - Number(!b.label.toLowerCase().startsWith(query))).slice(0, 6);
  }, [codes, query]);
  const exact = matches.find(c => c.label.toLowerCase() === query);
  const rows: ({ kind: 'code'; code: Code } | { kind: 'new'; label: string })[] = [
    ...matches.map(code => ({ kind: 'code' as const, code })),
    ...(query && !exact ? [{ kind: 'new' as const, label: q.trim() }] : []),
  ];
  useEffect(() => { setActive(0); }, [query]);

  const pickRow = (i: number) => {
    const r = rows[i];
    if (!r) return;
    if (r.kind === 'new') onToggle({ label: r.label }, true);
    else onToggle({ id: r.code.id }, !applied.has(r.code.id));
    setQ('');
  };

  const onKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Escape') { e.preventDefault(); onClose(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive(a => Math.min(rows.length - 1, a + 1)); return; }
    if (e.key === 'ArrowUp') { e.preventDefault(); setActive(a => Math.max(0, a - 1)); return; }
    if (e.key === 'Enter') { e.preventDefault(); if (q) pickRow(active); else onClose(); return; }
    if (!q && e.key === 'Backspace' && pinned.length) { e.preventDefault(); onToggle({ id: pinned[pinned.length - 1].id }, false); return; }
    if (!q && /^[1-6]$/.test(e.key) && !e.altKey && !e.ctrlKey && !e.metaKey) {
      const c = recent[Number(e.key) - 1];
      if (c) { e.preventDefault(); onToggle({ id: c.id }, true); }
    }
  };

  const chip = (c: Code, on: boolean, n?: number) => {
    const col = colorVar(c.color_idx);
    return (
      <button key={c.id} type="button" onClick={() => onToggle({ id: c.id }, !on)}
        title={on ? `برداشتن ${c.label}` : `افزودن ${c.label}`} aria-pressed={on}
        dir="ltr" className={`tag-chip ${on ? 'tag-chip-on' : ''}`}
        style={on ? { background: col.bg, color: col.fg, borderColor: 'transparent' } : { borderColor: 'var(--line)' }}>
        {!on && <i className="h-1.5 w-1.5 rounded-full" style={{ background: col.fg }} />}
        <span className="max-w-[130px] truncate">{c.label}</span>
        {on ? <span aria-hidden="true" className="opacity-60">×</span> : n ? <kbd className="kbd-mini">{fa(n)}</kbd> : null}
      </button>
    );
  };

  return (
    <div className="grid gap-1.5 p-1.5" onMouseDown={e => e.stopPropagation()}>
      {pinned.length > 0 && (
        <div className="flex flex-wrap items-center gap-1" aria-label="کدهای این عبارت">{pinned.map(c => chip(c, true))}</div>
      )}
      {!q && recent.length > 0 && (
        <div className="flex flex-wrap items-center gap-1" aria-label="کدهای اخیر">
          {recent.map((c, i) => chip(c, false, i + 1))}
        </div>
      )}
      <div className="relative">
        <input
          ref={input} value={q} onChange={e => setQ(e.target.value)} onKeyDown={onKey}
          dir="auto" maxLength={120}
          placeholder={pinned.length ? 'کد دیگر…' : 'نام کد…'}
          aria-label="نام کد" role="combobox" aria-expanded={rows.length > 0} aria-controls="code-options"
          aria-activedescendant={rows.length ? `opt-${active}` : undefined}
          className="h-8 w-full rounded-[4px] border border-[var(--line)] bg-[var(--paper)] pe-7 ps-2.5 text-[13px] outline-none focus:border-[var(--accent)]"
        />
        <button type="button" onClick={onClose} aria-label="بستن" title="بستن (Esc)" className="absolute inset-y-0 end-1 grid w-6 place-items-center text-[14px] text-[var(--faint)] hover:text-[var(--ink)]">×</button>
        {rows.length > 0 && (
          <div id="code-options" role="listbox" className={`pop absolute inset-x-0 z-10 p-1 ${dropUp ? 'bottom-[calc(100%+4px)]' : 'top-[calc(100%+4px)]'}`}>
            {rows.map((r, i) => (
              <button key={r.kind === 'new' ? 'new' : r.code.id} id={`opt-${i}`} role="option" type="button"
                aria-selected={r.kind === 'code' && applied.has(r.code.id)}
                onMouseEnter={() => setActive(i)} onClick={() => pickRow(i)}
                className={`flex w-full items-center gap-2 rounded-[3px] px-2 py-1 text-start text-[12.5px] ${i === active ? 'bg-[var(--sunk)]' : ''}`}>
                {r.kind === 'new' ? (
                  <><span className="text-[var(--muted)]">+ کد تازه</span><b className="ltr font-mono">{r.label}</b></>
                ) : (
                  <>
                    <i className="h-2 w-2 flex-none rounded-full" style={{ background: colorVar(r.code.color_idx).fg }} />
                    <span className="ltr min-w-0 flex-1 truncate font-mono" dir="ltr">{r.code.label}</span>
                    {applied.has(r.code.id) ? <span className="text-[11px] text-[var(--ok)]">✓</span> : <span className="text-[11px] text-[var(--faint)]">{fa(counts.get(r.code.id))}</span>}
                  </>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
