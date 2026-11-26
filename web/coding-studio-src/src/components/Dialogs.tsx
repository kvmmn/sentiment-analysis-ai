import { useEffect, useRef, type ReactNode } from 'react';
import type { ConfirmReq } from './Codebook';

function Modal({ onClose, children, label }: { onClose: () => void; children: ReactNode; label: string }) {
  const box = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    box.current?.querySelector<HTMLElement>('[data-autofocus]')?.focus();
    const fn = (e: KeyboardEvent) => { if (e.key === 'Escape') { e.stopPropagation(); onClose(); } };
    window.addEventListener('keydown', fn, true);
    return () => { window.removeEventListener('keydown', fn, true); prev?.focus?.(); };
  }, [onClose]);
  return (
    <div className="fixed inset-0 z-[90] grid place-items-center bg-black/35 p-4" onMouseDown={onClose}>
      <div ref={box} role="dialog" aria-modal="true" aria-label={label} onMouseDown={e => e.stopPropagation()}
        className="w-full max-w-[420px] rounded-[8px] border border-[var(--line)] bg-[var(--card)] p-5 shadow-2xl">
        {children}
      </div>
    </div>
  );
}

export function ConfirmDialog({ req, onClose }: { req: ConfirmReq; onClose: () => void }) {
  return (
    <Modal onClose={onClose} label={req.title}>
      <h2 className="mb-2 text-[16px] font-bold">{req.title}</h2>
      <p className="mb-5 text-[13.5px] leading-7 text-[var(--muted)]">{req.body}</p>
      <div className="flex justify-end gap-2">
        <button type="button" className="btn-ghost" onClick={onClose}>انصراف</button>
        <button type="button" data-autofocus className={req.danger ? 'btn-danger' : 'btn'} onClick={() => { req.run(); onClose(); }}>{req.confirm}</button>
      </div>
    </Modal>
  );
}

const KEYS: [string, string][] = [
  ['انتخاب متن یا زدن روی جمله', 'باز کردن انتخاب کد'],
  ['۱ تا ۶', 'افزودن یکی از کدهای اخیر (در خانهٔ کد)'],
  ['Backspace', 'برداشتن آخرین کدِ عبارت (وقتی خانهٔ کد خالی است)'],
  ['↑ ↓ و Enter', 'انتخاب از پیشنهادها؛ Enter خالی می‌بندد'],
  ['L', 'نمایش یا پنهان کردن نام کدها در متن'],
  ['Esc', 'بستن پنجره'],
  ['← / →', 'پست بعدی / قبلی'],
  ['M', 'علامت «تمام شد» برای این پست'],
  ['Ctrl / ⌘ + Z', 'بازگردانی آخرین کار'],
  ['/', 'جست‌وجو در کدنامه'],
  ['?', 'همین راهنما'],
];

export function ShortcutsDialog({ onClose }: { onClose: () => void }) {
  return (
    <Modal onClose={onClose} label="میان‌برها">
      <h2 className="mb-3 text-[16px] font-bold">میان‌برهای صفحه‌کلید</h2>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-[13px]">
        {KEYS.map(([k, v]) => (<div key={k} className="contents"><dt><kbd className="kbd">{k}</kbd></dt><dd className="text-[var(--muted)]">{v}</dd></div>))}
      </dl>
      <div className="mt-5 flex justify-end"><button type="button" data-autofocus className="btn" onClick={onClose}>باشه</button></div>
    </Modal>
  );
}
