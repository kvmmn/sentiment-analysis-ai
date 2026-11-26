import { useCallback, useEffect, useState } from 'react';
import { ApiError, createDemoBackend, detectBackend, errorText, type Backend } from '@/lib/backend';
import type { Coder } from '@/lib/types';
import { fa, safeStorage } from '@/lib/text';
import { ToastProvider } from '@/components/Toasts';
import { Studio } from '@/components/Studio';
import { ThemeToggle } from '@/components/ThemeToggle';
import { AppNav } from '@/components/AppNav';

const LAST_CODER = 'saintiment_coding_last_coder';

function parseHash(): { coder: number | null; post: string | null } {
  const m = location.hash.match(/^#coder-(\d+)(?:\/([\w-]+))?/);
  return m ? { coder: Number(m[1]), post: m[2] || null } : { coder: null, post: null };
}

type Phase = 'boot' | 'offline' | 'login' | 'ready';

export default function App() {
  return <ToastProvider><Shell /></ToastProvider>;
}

function Shell() {
  const [phase, setPhase] = useState<Phase>('boot');
  const [backend, setBackend] = useState<Backend | null>(null);
  const [route, setRoute] = useState(parseHash);

  const boot = useCallback(async () => {
    setPhase('boot');
    const r = await detectBackend();
    if ('offline' in r) { setPhase('offline'); return; }
    setBackend(r.backend);
    setPhase(r.authed ? 'ready' : 'login');
  }, []);

  useEffect(() => { boot(); }, [boot]);
  useEffect(() => {
    const fn = () => setRoute(parseHash());
    window.addEventListener('hashchange', fn);
    return () => window.removeEventListener('hashchange', fn);
  }, []);

  const onUnauthorized = useCallback(() => setPhase('login'), []);
  const openCoder = (id: number) => { safeStorage()?.setItem(LAST_CODER, String(id)); location.hash = `coder-${id}`; };
  const back = () => { history.pushState(null, '', location.pathname + location.search); setRoute({ coder: null, post: null }); };
  const onPostChange = useCallback((sid: string) => {
    const h = `#coder-${parseHash().coder}/${sid}`;
    if (parseHash().coder && location.hash !== h) history.replaceState(null, '', h);
  }, []);

  if (phase === 'boot') return <Center><p className="animate-pulse text-[var(--muted)]">در حال اتصال…</p></Center>;
  if (phase === 'offline') {
    return (
      <Center>
        <div className="grid max-w-sm gap-3 text-center">
          <h1 className="text-[18px] font-bold">سرور پاسخ نداد</h1>
          <p className="text-[13.5px] leading-7 text-[var(--muted)]">اتصال به API کدگذاری برقرار نشد. اینترنت را بررسی کنید و دوباره تلاش کنید. در حالت نمایشی هیچ چیز در پایگاه داده ذخیره نمی‌شود.</p>
          <button type="button" className="btn" onClick={boot}>تلاش دوباره</button>
          <button type="button" className="link text-[13px]" onClick={() => { setBackend(createDemoBackend()); setPhase('ready'); }}>ادامه در حالت نمایشی</button>
        </div>
      </Center>
    );
  }
  if (phase === 'login' || !backend) return <Login backend={backend!} onDone={() => setPhase('ready')} />;
  if (route.coder) {
    return <CoderStudio key={route.coder} backend={backend} coderId={route.coder} post={route.post} onBack={back} onUnauthorized={onUnauthorized} onPostChange={onPostChange} />;
  }
  return <CoderPicker backend={backend} onPick={openCoder} onLogout={async () => { await backend.logout(); setPhase('login'); }} onUnauthorized={onUnauthorized} />;
}

function Center({ children }: { children: React.ReactNode }) {
  return <div className="grid min-h-[100dvh] place-items-center p-5">{children}</div>;
}

function Login({ backend, onDone }: { backend: Backend; onDone: () => void }) {
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  return (
    <div className="grid min-h-[100dvh] grid-rows-[1fr_auto] lg:grid-cols-[1.1fr_1fr] lg:grid-rows-1">
      <div className="hidden flex-col justify-between border-e border-[var(--line)] bg-[var(--card)] p-10 lg:flex">
        <span className="ltr font-mono text-[13px] text-[var(--muted)]">Saintiment / Coding Studio v2</span>
        <p className="max-w-md text-[26px] font-bold leading-[1.6]">متن را بخوانید، جمله را بزنید، کد بگذارید. بقیه‌اش با ما.</p>
        <span className="text-[12px] text-[var(--faint)]">کدگذاری کیفی پست‌های نمونه</span>
      </div>
      <form className="grid content-center gap-4 p-6 sm:p-12" onSubmit={async e => {
        e.preventDefault(); setBusy(true); setErr('');
        try { await backend.login(pw); setPw(''); onDone(); } catch (x) {
          setErr(x instanceof ApiError && x.code === 'wrong_password' ? 'رمز اشتباه است' : x instanceof ApiError && x.code === 'network' ? errorText(x) : 'خطای سرور؛ کمی بعد دوباره تلاش کنید');
        } finally { setBusy(false); }
      }}>
        <h1 className="text-[22px] font-bold">ورود</h1>
        <label htmlFor="pw" className="text-[13px] text-[var(--muted)]">رمز تیم (همان رمز صفحهٔ غربالگری)</label>
        <input id="pw" type="password" autoFocus required value={pw} onChange={e => setPw(e.target.value)} autoComplete="current-password" dir="ltr" className="field max-w-sm py-3 text-[16px]" aria-describedby="pw-err" />
        <button type="submit" disabled={busy} className="btn max-w-sm py-3">{busy ? 'در حال ورود…' : 'ورود'}</button>
        <p id="pw-err" role="alert" className="min-h-[1.5em] text-[13px] text-[var(--danger)]">{err}</p>
      </form>
    </div>
  );
}

function CoderPicker({ backend, onPick, onLogout, onUnauthorized }: { backend: Backend; onPick: (id: number) => void; onLogout: () => void; onUnauthorized: () => void }) {
  const [coders, setCoders] = useState<Coder[] | null>(null);
  const [err, setErr] = useState('');
  const last = Number(safeStorage()?.getItem(LAST_CODER) || 0);
  const load = useCallback(async () => {
    setErr(''); setCoders(null);
    try { setCoders(await backend.coders()); } catch (e) {
      if (e instanceof ApiError && e.code === 'unauthorized') onUnauthorized(); else setErr(errorText(e));
    }
  }, [backend, onUnauthorized]);
  useEffect(() => { load(); }, [load]);

  const exportJson = async () => {
    const data = await backend.exportAll();
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'saintiment_coding_export.json'; a.click();
  };

  return (
    <div className="min-h-[100dvh]">
      <header className="flex h-12 items-center gap-2 border-b border-[var(--line)] bg-[var(--card)] px-4">
        <span className="ltr font-mono text-[12.5px] text-[var(--muted)]">Saintiment / code</span>
        {backend.mode === 'demo' && <span className="demo-badge">حالت نمایشی</span>}
        {backend.mode === 'remote' && <AppNav className="ms-3 flex" />}
        <div className="ms-auto flex items-center gap-1">
          <ThemeToggle />
          {backend.mode === 'remote' && <button type="button" className="icon-text" onClick={onLogout}>خروج</button>}
        </div>
      </header>
      <main className="mx-auto grid max-w-5xl gap-8 px-5 py-10 lg:grid-cols-[1fr_1.4fr]">
        <section>
          <h1 className="mb-3 text-[24px] font-bold leading-snug">کدگذاری کیفی</h1>
          <p className="text-[14px] leading-8 text-[var(--muted)]">هر کدگذار کدنامه و هایلایت‌های جدای خودش را دارد. پست‌ها برای همه یکسان است و اطلاعات غربالگری در آن‌ها پنهان است.</p>
          {backend.mode === 'demo' && (
            <p className="mt-4 rounded-[6px] border border-dashed border-[var(--warn)] p-3 text-[12.5px] leading-7 text-[var(--muted)]">
              این نسخه به سرور وصل نیست. پست‌ها ساختگی‌اند (نه از نمونهٔ پژوهش) و تغییرات فقط در همین مرورگر می‌ماند. روی Vercel همین صفحه به دادهٔ واقعی وصل می‌شود.
            </p>
          )}
          <button type="button" className="link mt-6 text-[13px]" onClick={exportJson}>دانلود خروجی کامل (JSON) ↓</button>
        </section>
        <section className="grid content-start gap-3" aria-busy={!coders}>
          {err && <div className="grid gap-2"><p className="text-[var(--danger)]">{err}</p><button type="button" className="btn w-fit" onClick={load}>تلاش دوباره</button></div>}
          {!coders && !err && [0, 1, 2].map(i => <div key={i} className="h-[92px] animate-pulse rounded-[6px] bg-[var(--sunk)]" />)}
          {coders?.map(c => {
            const pct = c.total_posts ? Math.round((c.coded_count / c.total_posts) * 100) : 0;
            return (
              <button key={c.id} type="button" onClick={() => onPick(c.id)}
                className={`coder-card grid gap-2.5 rounded-[6px] border bg-[var(--card)] p-4 text-start transition ${c.id === last ? 'border-[var(--ink)]' : 'border-[var(--line)] hover:border-[var(--faint)]'}`}>
                <span className="flex items-baseline justify-between gap-2">
                  <span className="text-[17px] font-bold">{c.name}{c.id === last && <span className="ms-2 text-[11.5px] font-normal text-[var(--muted)]">آخرین بار</span>}</span>
                  <span className="text-[13px] tabular-nums text-[var(--muted)]">{fa(c.coded_count)} / {fa(c.total_posts)}</span>
                </span>
                <span className="h-[3px] overflow-hidden rounded-full bg-[var(--line)]"><i className="block h-full bg-[var(--ok)]" style={{ width: `${pct}%` }} /></span>
                <span className="text-[12.5px] text-[var(--muted)]">{fa(c.codes_count)} کد · {fa(c.highlights_count)} قطعه{c.last_activity ? ` · آخرین فعالیت ${new Date(c.last_activity).toLocaleDateString('fa-IR')}` : ''}</span>
              </button>
            );
          })}
        </section>
      </main>
    </div>
  );
}

function CoderStudio(props: { backend: Backend; coderId: number; post: string | null; onBack: () => void; onUnauthorized: () => void; onPostChange: (sid: string) => void }) {
  const [name, setName] = useState(`کدگذار ${fa(props.coderId)}`);
  useEffect(() => { props.backend.coders().then(cs => { const c = cs.find(x => x.id === props.coderId); if (c) setName(c.name); }).catch(() => {}); }, [props.backend, props.coderId]);
  return <Studio backend={props.backend} coderId={props.coderId} coderName={name} initialPost={props.post} onBack={props.onBack} onUnauthorized={props.onUnauthorized} onPostChange={props.onPostChange} />;
}
