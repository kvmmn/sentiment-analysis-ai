import { useMemo, useState } from 'react';
import type { Workspace } from '@/lib/types';
import { fa } from '@/lib/text';

export type Filter = 'all' | 'uncoded' | 'coded' | 'link' | 'notes';
const FILTERS: [Filter, string][] = [['all', 'همه'], ['uncoded', 'مانده'], ['coded', 'تمام‌شده'], ['link', 'لینک‌دار'], ['notes', 'یادداشت‌دار']];

export function matches(ws: Workspace, sid: string, f: Filter) {
  const st = ws.status[sid];
  const p = ws.posts.find(x => x.sample_id === sid);
  if (f === 'uncoded') return !st?.is_coded;
  if (f === 'coded') return Boolean(st?.is_coded);
  if (f === 'link') return Boolean(p?.has_external_link) || ws.ext.some(e => e.sample_id === sid);
  if (f === 'notes') return Boolean(st?.coder_notes?.trim());
  return true;
}

interface Props { ws: Workspace; current: string | null; onPick: (sid: string) => void; filter: Filter; setFilter: (f: Filter) => void }

export function PostList({ ws, current, onPick, filter, setFilter }: Props) {
  const [q, setQ] = useState('');
  const coded = ws.posts.filter(p => ws.status[p.sample_id]?.is_coded).length;
  const segCount = useMemo(() => {
    const m = new Map<string, number>();
    for (const h of ws.highlights) m.set(h.sample_id, (m.get(h.sample_id) || 0) + 1);
    return m;
  }, [ws.highlights]);
  const list = useMemo(() => {
    const query = q.trim().toLowerCase();
    return ws.posts.filter(p => matches(ws, p.sample_id, filter) && (!query || `${p.sample_id} ${p.author_name} ${p.post_text}`.toLowerCase().includes(query)));
  }, [ws, filter, q]);
  const pct = ws.posts.length ? Math.round((coded / ws.posts.length) * 100) : 0;

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-[var(--line)] px-4 pb-3 pt-4">
        <div className="mb-1.5 flex items-baseline justify-between">
          <h2 className="text-[15px] font-bold">پست‌ها</h2>
          <span className="text-[12px] text-[var(--muted)]">{fa(coded)} از {fa(ws.posts.length)} · {fa(pct)}٪</span>
        </div>
        <div className="mb-3 h-[3px] overflow-hidden rounded-full bg-[var(--line)]"><i className="block h-full bg-[var(--ok)] transition-all" style={{ width: `${pct}%` }} /></div>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="جست‌وجو در متن، نویسنده یا شناسه…" aria-label="جست‌وجوی پست" className="field mb-2 w-full" dir="auto" />
        <div className="flex flex-wrap gap-1" role="group" aria-label="فیلتر">
          {FILTERS.map(([k, l]) => (
            <button key={k} type="button" aria-pressed={filter === k} onClick={() => setFilter(k)}
              className={`chip ${filter === k ? 'chip-on' : ''}`}>{l}</button>
          ))}
        </div>
      </div>
      <ul className="min-h-0 flex-1 overflow-y-auto py-1" aria-label="فهرست پست‌ها">
        {list.map(p => {
          const st = ws.status[p.sample_id];
          const n = segCount.get(p.sample_id) || 0;
          const on = p.sample_id === current;
          return (
            <li key={p.sample_id}>
              <button type="button" onClick={() => onPick(p.sample_id)} aria-current={on ? 'true' : undefined}
                className={`post-item grid w-full gap-0.5 px-4 py-2.5 text-start ${on ? 'post-item-on' : ''}`}>
                <span className="flex items-center gap-2">
                  <span className="sid">{p.sample_id}</span>
                  <span className="ltr min-w-0 flex-1 truncate text-[13px] font-semibold" dir="auto">{p.author_name || '—'}</span>
                  {(p.has_external_link) && <span title="لینک بیرونی" className="text-[11px] text-[var(--warn)]">⧉</span>}
                  {st?.coder_notes?.trim() && <span title="یادداشت دارد" className="text-[11px] text-[var(--muted)]">✎</span>}
                  {n > 0 && <span className="text-[11px] tabular-nums text-[var(--muted)]">{fa(n)}</span>}
                  <span className={`h-2 w-2 flex-none rounded-full ${st?.is_coded ? 'bg-[var(--ok)]' : n ? 'border border-[var(--ok)]' : 'border border-[var(--faint)]'}`} title={st?.is_coded ? 'تمام‌شده' : 'مانده'} />
                </span>
                <span className="ltr line-clamp-1 text-[12px] text-[var(--muted)]" dir="auto">{p.post_text.slice(0, 140)}</span>
              </button>
            </li>
          );
        })}
        {!list.length && (
          <li className="px-4 py-6 text-[13px] text-[var(--muted)]">
            پستی با این فیلتر نیست.{' '}
            <button type="button" className="link" onClick={() => { setFilter('all'); setQ(''); }}>نمایش همه</button>
          </li>
        )}
      </ul>
    </div>
  );
}
