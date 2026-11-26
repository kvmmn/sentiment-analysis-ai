import { useEffect, useMemo, useState } from 'react';
import type { Code } from '@/lib/types';
import type { Studio } from '@/lib/useStudio';
import { COLOR_IDS, colorVar, fa } from '@/lib/text';

export interface ConfirmReq { title: string; body: string; confirm: string; danger?: boolean; run: () => void }

interface Props {
  studio: Studio;
  confirm: (r: ConfirmReq) => void;
  onJump: (sampleId: string, hlId: number) => void;
  focusCodeId: number | null;
  setFocusCodeId: (id: number | null) => void;
}

export function Codebook({ studio, confirm, onJump, focusCodeId, setFocusCodeId }: Props) {
  const { ws, derived } = studio;
  const [q, setQ] = useState('');
  const [openId, setOpenId] = useState<number | null>(null);
  const [newCode, setNewCode] = useState('');
  const [newTheme, setNewTheme] = useState('');

  const groups = useMemo(() => {
    const query = q.trim().toLowerCase();
    const codes = ws!.codes.filter(c => !query || c.label.toLowerCase().includes(query));
    const byTheme = [...ws!.themes].sort((a, b) => a.sort_order - b.sort_order || a.id - b.id).map(t => ({ id: t.id as number | null, name: t.name, codes: codes.filter(c => c.theme_id === t.id) }));
    const none = { id: null, name: 'بدون تم', codes: codes.filter(c => c.theme_id === null || !ws!.themes.some(t => t.id === c.theme_id)) };
    return [none, ...byTheme].map(g => ({ ...g, codes: [...g.codes].sort((a, b) => a.label.localeCompare(b.label)) }));
  }, [ws, q]);

  const total = ws!.codes.length;
  const segs = ws!.highlights.length;

  const addCode = async () => {
    const label = newCode.trim();
    if (!label) return;
    const c = await studio.createCode(label);
    if (c) { setNewCode(''); setOpenId(c.id); }
  };

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="border-b border-[var(--line)] px-4 pb-3 pt-4">
        <div className="mb-2 flex items-baseline justify-between">
          <h2 className="text-[15px] font-bold">کدنامه</h2>
          <span className="text-[12px] text-[var(--muted)]">{fa(total)} کد · {fa(segs)} قطعه</span>
        </div>
        <input value={q} onChange={e => setQ(e.target.value)} placeholder="جست‌وجوی کد…" aria-label="جست‌وجوی کد" className="field w-full" dir="auto" />
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto px-2 py-2">
        {groups.map(g => (g.codes.length > 0 || g.id !== null) && (
          <section key={String(g.id)} className="mb-3">
            <div className="group flex items-center justify-between px-2 py-1">
              <h3 className="text-[11.5px] font-bold tracking-wide text-[var(--muted)]">{g.name} <span className="font-normal text-[var(--faint)]">· {fa(g.codes.length)}</span></h3>
              {g.id !== null && (
                <button type="button" className="text-[11.5px] text-[var(--faint)] opacity-0 hover:text-[var(--danger)] focus:opacity-100 group-hover:opacity-100"
                  onClick={() => {
                    const id = g.id!;
                    if (g.codes.length) confirm({ title: `حذف تم «${g.name}»`, body: `${fa(g.codes.length)} کد زیر این تم هست. کدها حذف نمی‌شوند و «بدون تم» می‌شوند.`, confirm: 'حذف تم', danger: true, run: () => studio.deleteTheme(id) });
                    else studio.deleteTheme(id);
                  }}>حذف تم</button>
              )}
            </div>
            {g.codes.length === 0 && <p className="px-2 text-[12px] text-[var(--faint)]">کدی اینجا نیست. از ویرایش کد، تمش را عوض کنید.</p>}
            <ul>
              {g.codes.map(c => (
                <CodeRow key={c.id} code={c} studio={studio} confirm={confirm} onJump={onJump}
                  open={openId === c.id} toggle={() => setOpenId(openId === c.id ? null : c.id)}
                  focused={focusCodeId === c.id} setFocus={() => setFocusCodeId(focusCodeId === c.id ? null : c.id)}
                  count={derived!.countByCode.get(c.id) || 0} />
              ))}
            </ul>
          </section>
        ))}
        {total === 0 && <p className="px-3 py-6 text-[13px] leading-7 text-[var(--muted)]">هنوز کدی نساخته‌اید. بخشی از متن را انتخاب کنید و نام کد را بنویسید، یا از پایین همین ستون کد بسازید.</p>}
      </div>

      <div className="grid gap-2 border-t border-[var(--line)] p-3">
        <div className="flex gap-2">
          <input value={newCode} onChange={e => setNewCode(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addCode(); } }} placeholder="کد تازه…" aria-label="کد تازه" maxLength={120} dir="auto" className="field min-w-0 flex-1" />
          <button type="button" className="btn" onClick={addCode}>+ کد</button>
        </div>
        <div className="flex gap-2">
          <input value={newTheme} onChange={e => setNewTheme(e.target.value)} onKeyDown={async e => { if (e.key === 'Enter') { e.preventDefault(); if (await studio.createTheme(newTheme)) setNewTheme(''); } }} placeholder="تم تازه…" aria-label="تم تازه" maxLength={120} dir="auto" className="field min-w-0 flex-1" />
          <button type="button" className="btn-ghost" onClick={async () => { if (await studio.createTheme(newTheme)) setNewTheme(''); }}>+ تم</button>
        </div>
      </div>
    </div>
  );
}

interface RowProps {
  code: Code; studio: Studio; confirm: (r: ConfirmReq) => void; onJump: (sid: string, hlId: number) => void;
  open: boolean; toggle: () => void; count: number; focused: boolean; setFocus: () => void;
}

function CodeRow({ code, studio, confirm, onJump, open, toggle, count, focused, setFocus }: RowProps) {
  const { ws } = studio;
  const col = colorVar(code.color_idx);
  const [label, setLabel] = useState(code.label);
  const [target, setTarget] = useState<string>('');
  useEffect(() => { setLabel(code.label); }, [code.label, open]);

  const quotes = useMemo(() => (open ? ws!.highlights.filter(h => h.code_id === code.id).sort((a, b) => a.sample_id.localeCompare(b.sample_id)) : []), [open, ws, code.id]);
  const others = ws!.codes.filter(c => c.id !== code.id).sort((a, b) => a.label.localeCompare(b.label));

  const askMerge = (targetId: number) => {
    const t = ws!.codes.find(c => c.id === targetId);
    if (!t) return;
    confirm({
      title: 'ادغام کدها',
      body: `${fa(count)} قطعه از «${code.label}» به «${t.label}» منتقل می‌شود و «${code.label}» حذف می‌شود. این کار بازگشت‌پذیر نیست.`,
      confirm: 'ادغام کن', danger: true,
      run: () => studio.mergeCode(code.id, targetId),
    });
  };

  const saveLabel = () => {
    const clean = label.trim().slice(0, 120);
    if (!clean || clean === code.label) { setLabel(code.label); return; }
    const dup = ws!.codes.find(c => c.id !== code.id && c.label.toLowerCase() === clean.toLowerCase());
    if (dup) { setLabel(code.label); askMerge(dup.id); return; }
    studio.updateCode(code.id, { label: clean });
  };

  return (
    <li className={`rounded-[5px] ${open ? 'bg-[var(--card)] ring-1 ring-[var(--line)]' : ''}`}>
      <div className="flex items-center gap-1">
        <button type="button" onClick={toggle} aria-expanded={open}
          className="flex min-w-0 flex-1 items-center gap-2 rounded-[5px] px-2 py-1.5 text-start hover:bg-[var(--sunk)]">
          <span className="h-2.5 w-2.5 flex-none rounded-full" style={{ background: col.fg }} />
          <span className="ltr min-w-0 flex-1 truncate font-mono text-[12.5px]" dir="ltr">{code.label}</span>
          <span className="text-[11.5px] tabular-nums text-[var(--muted)]">{fa(count)}</span>
        </button>
        <button type="button" onClick={setFocus} aria-pressed={focused} title="فقط همین کد را در متن پررنگ کن"
          className={`icon ${focused ? 'text-[var(--accent)]' : 'text-[var(--faint)]'}`}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="3" /><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /></svg>
        </button>
      </div>

      {open && (
        <div className="grid gap-3 px-2 pb-3 pt-1 text-[12.5px]">
          <label className="grid gap-1">
            <span className="text-[var(--muted)]">نام</span>
            <input value={label} onChange={e => setLabel(e.target.value)} onBlur={saveLabel}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); (e.target as HTMLInputElement).blur(); } if (e.key === 'Escape') { setLabel(code.label); } }}
              maxLength={120} dir="auto" className="field ltr font-mono" />
          </label>
          <div className="grid gap-1">
            <span className="text-[var(--muted)]">رنگ</span>
            <div className="flex gap-1.5" role="radiogroup" aria-label="رنگ کد">
              {COLOR_IDS.map(i => (
                <button key={i} type="button" role="radio" aria-checked={code.color_idx === i} aria-label={`رنگ ${i}`}
                  onClick={() => code.color_idx !== i && studio.updateCode(code.id, { color_idx: i }, { quiet: true })}
                  className={`h-7 w-7 rounded-full transition ${code.color_idx === i ? 'ring-2 ring-[var(--ink)] ring-offset-2 ring-offset-[var(--card)]' : ''}`}
                  style={{ background: colorVar(i).fg }} />
              ))}
            </div>
          </div>
          <label className="grid gap-1">
            <span className="text-[var(--muted)]">تم</span>
            <select value={code.theme_id ?? ''} onChange={e => studio.updateCode(code.id, { theme_id: e.target.value ? Number(e.target.value) : null }, { quiet: true })} className="field">
              <option value="">بدون تم</option>
              {ws!.themes.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
            </select>
          </label>

          <div className="grid gap-1">
            <span className="text-[var(--muted)]">نقل‌قول‌ها ({fa(quotes.length)})</span>
            {quotes.length ? (
              <ul className="grid max-h-56 gap-0.5 overflow-y-auto rounded-[4px] bg-[var(--paper)] p-1">
                {quotes.map(h => (
                  <li key={h.id}>
                    <button type="button" onClick={() => onJump(h.sample_id, h.id)} className="flex w-full gap-2 rounded-[3px] px-1.5 py-1 text-start hover:bg-[var(--sunk)]">
                      <span className="sid flex-none">{h.sample_id}</span>
                      <span className="ltr line-clamp-2 text-[12px] text-[var(--muted)]" dir="auto">{h.quote}</span>
                    </button>
                  </li>
                ))}
              </ul>
            ) : <span className="text-[var(--faint)]">هنوز به هیچ متنی اعمال نشده.</span>}
          </div>

          {others.length > 0 && (
            <div className="flex items-center gap-2">
              <select value={target} onChange={e => setTarget(e.target.value)} className="field min-w-0 flex-1" aria-label="ادغام با">
                <option value="">ادغام با کد دیگر…</option>
                {others.map(o => <option key={o.id} value={o.id}>{o.label}</option>)}
              </select>
              <button type="button" className="btn-ghost" disabled={!target} onClick={() => { askMerge(Number(target)); setTarget(''); }}>ادغام</button>
            </div>
          )}
          <div className="flex justify-end">
            <button type="button" className="font-semibold text-[var(--danger)] hover:underline"
              onClick={() => confirm({
                title: `حذف کد «${code.label}»`,
                body: count ? `${fa(count)} قطعهٔ کدگذاری‌شده هم حذف می‌شود. بلافاصله بعدش می‌توانید بازگردانی کنید.` : 'این کد به هیچ متنی اعمال نشده.',
                confirm: 'حذف کد', danger: true, run: () => studio.deleteCode(code.id),
              })}>حذف کد</button>
          </div>
        </div>
      )}
    </li>
  );
}
