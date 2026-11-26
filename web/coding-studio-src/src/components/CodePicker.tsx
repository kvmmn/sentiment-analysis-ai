import { useEffect, useMemo, useRef, useState } from 'react';
import type { Code } from '@/lib/types';
import { colorVar, fa } from '@/lib/text';
import type { CodeRef } from '@/lib/useStudio';

interface Props {
  codes: Code[]; // "recently used" order
  counts: Map<number, number>;
  applied: Set<number>; // codes already on this exact passage
  quote: string;
  onToggle: (ref: CodeRef, on: boolean) => void;
  onRemoveAll?: () => void;
  onClose: () => void;
  focusToken?: unknown; // changes when the same passage is clicked again
}

type Opt = { kind: 'code'; code: Code } | { kind: 'new'; label: string };

// Multi-tag picker: every pick toggles one code on the passage and the picker stays open.
export function CodePicker({ codes, counts, applied, quote, onToggle, onRemoveAll, onClose, focusToken }: Props) {
  const [q, setQ] = useState('');
  const [active, setActive] = useState(0);
  const input = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);
  // Order is fixed at open time so rows do not jump while codes are toggled.
  const firstApplied = useRef(applied);
  const order = useRef(codes.map(c => c.id));
  const stable = useMemo(() => {
    const pos = (id: number) => { const i = order.current.indexOf(id); return i < 0 ? 1e9 + id : i; };
    return [...codes].sort((a, b) => pos(a.id) - pos(b.id));
  }, [codes]);

  useEffect(() => { input.current?.focus({ preventScroll: true }); }, [focusToken]);

  const opts = useMemo<Opt[]>(() => {
    const query = q.trim().toLowerCase();
    const list = query ? stable.filter(c => c.label.toLowerCase().includes(query)) : stable;
    const exact = query ? list.find(c => c.label.toLowerCase() === query) : undefined;
    let sorted: Code[];
    if (exact) sorted = [exact, ...list.filter(c => c !== exact)];
    else if (query) sorted = [...list].sort((a, b) => Number(!a.label.toLowerCase().startsWith(query)) - Number(!b.label.toLowerCase().startsWith(query)));
    else sorted = [...list.filter(c => firstApplied.current.has(c.id)), ...list.filter(c => !firstApplied.current.has(c.id))];
    const out: Opt[] = sorted.map(code => ({ kind: 'code', code }));
    if (query && !exact) out.push({ kind: 'new', label: q.trim() });
    return out;
  }, [q, stable]);

  useEffect(() => { setActive(0); }, [q]);
  useEffect(() => { listRef.current?.querySelector<HTMLElement>(`[data-i="${active}"]`)?.scrollIntoView({ block: 'nearest' }); }, [active]);

  const pick = (o: Opt | undefined) => {
    if (!o) return;
    if (o.kind === 'new') { onToggle({ label: o.label }, true); setQ(''); return; }
    onToggle({ id: o.code.id }, !applied.has(o.code.id));
    if (q) setQ('');
  };

  const onKey = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Escape') { e.preventDefault(); onClose(); return; }
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive(a => Math.min(opts.length - 1, a + 1)); return; }
    if (e.key === 'ArrowUp') { e.preventDefault(); setActive(a => Math.max(0, a - 1)); return; }
    if (e.key === 'Enter') {
      e.preventDefault();
      if (!q && e.shiftKey) { onClose(); return; }
      if (!q && !opts.length) return;
      pick(opts[active]);
      return;
    }
    if (!q && /^[1-9]$/.test(e.key) && !e.altKey && !e.ctrlKey && !e.metaKey) {
      const o = opts[Number(e.key) - 1];
      if (o) { e.preventDefault(); setActive(Number(e.key) - 1); pick(o); }
    }
  };

  const hint = (() => {
    const o = opts[active];
    if (!o) return codes.length ? 'کدی با این نام نیست' : 'نام اولین کد را بنویسید';
    if (o.kind === 'new') return `Enter: ساخت و افزودن «${o.label}»`;
    return applied.has(o.code.id) ? `Enter: برداشتن «${o.code.label}»` : `Enter: افزودن «${o.code.label}»`;
  })();

  return (
    <div className="flex max-h-[min(440px,72dvh)] flex-col" onMouseDown={e => e.stopPropagation()}>
      <div className="border-b border-[var(--line)] px-3 pb-2 pt-3">
        <p className="ltr mb-2 line-clamp-2 text-[12px] italic text-[var(--muted)]" dir="auto">“{quote}”</p>
        <input
          ref={input} value={q} onChange={e => setQ(e.target.value)} onKeyDown={onKey}
          dir="auto" maxLength={120}
          placeholder={codes.length ? 'جست‌وجو یا نام کد تازه…' : 'نام کد…'}
          aria-label="نام کد" role="combobox" aria-expanded="true" aria-controls="code-options"
          aria-activedescendant={opts[active] ? `opt-${active}` : undefined}
          className="w-full rounded-[4px] border border-[var(--line)] bg-[var(--paper)] px-3 py-2 text-[14px] outline-none focus:border-[var(--accent)]"
        />
        <div className="mt-1.5 flex items-baseline justify-between gap-2 text-[11.5px] text-[var(--muted)]">
          <span aria-live="polite">{hint}</span>
          <span className="whitespace-nowrap">{applied.size ? `${fa(applied.size)} کد روی این عبارت` : 'چند کد هم می‌شود'}</span>
        </div>
      </div>
      <div ref={listRef} id="code-options" role="listbox" aria-multiselectable="true" className="min-h-0 flex-1 overflow-y-auto p-1.5">
        {opts.map((o, i) => {
          const on = i === active;
          if (o.kind === 'new') {
            return (
              <button key="new" id={`opt-${i}`} data-i={i} role="option" aria-selected={false} type="button"
                onMouseEnter={() => setActive(i)} onClick={() => pick(o)}
                className={`flex w-full items-center gap-2 rounded-[4px] px-2.5 py-2 text-start text-[13px] ${on ? 'bg-[var(--sunk)]' : ''}`}>
                <span className="grid h-[18px] w-[18px] place-items-center rounded-[3px] border border-dashed border-[var(--muted)] text-[13px] leading-none">+</span>
                <span>ساخت و افزودن</span>
                <b className="ltr font-mono text-[12.5px]">{o.label}</b>
              </button>
            );
          }
          const col = colorVar(o.code.color_idx);
          const checked = applied.has(o.code.id);
          return (
            <button key={o.code.id} id={`opt-${i}`} data-i={i} role="option" aria-selected={checked} type="button"
              onMouseEnter={() => setActive(i)} onClick={() => pick(o)}
              className={`flex w-full items-center gap-2 rounded-[4px] px-2.5 py-1.5 text-start text-[13px] ${on ? 'bg-[var(--sunk)]' : ''}`}>
              <span className="grid h-[18px] w-[18px] flex-none place-items-center rounded-[3px] border-2 text-[11px] font-bold leading-none text-white"
                style={{ borderColor: col.fg, background: checked ? col.fg : 'transparent' }} aria-hidden="true">{checked ? '✓' : ''}</span>
              <span className="ltr min-w-0 flex-1 truncate font-mono text-[12.5px]" dir="ltr">{o.code.label}</span>
              <span className="text-[11px] tabular-nums text-[var(--faint)]">{fa(counts.get(o.code.id))}</span>
              {!q && i < 9 && <kbd className="kbd">{fa(i + 1)}</kbd>}
            </button>
          );
        })}
      </div>
      <div className="flex items-center justify-between gap-2 border-t border-[var(--line)] px-3 py-2 text-[12px]">
        {onRemoveAll && applied.size > 0 ? (
          <button type="button" onClick={onRemoveAll} className="font-semibold text-[var(--danger)] hover:underline">
            {applied.size > 1 ? 'برداشتن همهٔ کدها' : 'حذف این هایلایت'}
          </button>
        ) : <span className="text-[var(--faint)]">Enter افزودن/برداشتن</span>}
        <button type="button" onClick={onClose} className="btn py-1">تمام <kbd className="kbd ms-1 border-transparent bg-transparent text-inherit opacity-70">Esc</kbd></button>
      </div>
    </div>
  );
}
