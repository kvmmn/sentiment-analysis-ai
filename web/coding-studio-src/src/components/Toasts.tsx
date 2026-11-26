import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from 'react';

export interface ToastOpts { action?: { label: string; run: () => void }; error?: boolean; ms?: number }
interface Toast extends ToastOpts { id: number; msg: string }
type Show = (msg: string, opts?: ToastOpts) => void;

const Ctx = createContext<Show>(() => {});
export const useToast = () => useContext(Ctx);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<Toast[]>([]);
  const seq = useRef(0);
  const dismiss = useCallback((id: number) => setItems(xs => xs.filter(x => x.id !== id)), []);
  const show = useCallback<Show>((msg, opts = {}) => {
    const id = ++seq.current;
    setItems(xs => [...xs.slice(-2), { id, msg, ...opts }]);
    setTimeout(() => dismiss(id), opts.ms ?? (opts.action ? 6000 : opts.error ? 5000 : 2600));
  }, [dismiss]);

  return (
    <Ctx.Provider value={show}>
      {children}
      <div className="pointer-events-none fixed inset-x-0 bottom-20 z-[80] flex flex-col items-center gap-2 px-3 lg:bottom-6" role="status" aria-live="polite">
        {items.map(t => (
          <div key={t.id} className={`toast pointer-events-auto flex max-w-md items-center gap-3 rounded-[6px] px-4 py-2.5 text-[13px] shadow-lg ${t.error ? 'bg-[var(--danger)] text-white' : 'bg-[var(--ink)] text-[var(--paper)]'}`}>
            <span>{t.msg}</span>
            {t.action && (
              <button type="button" className="font-bold underline underline-offset-4" onClick={() => { t.action!.run(); dismiss(t.id); }}>
                {t.action.label}
              </button>
            )}
          </div>
        ))}
      </div>
    </Ctx.Provider>
  );
}
