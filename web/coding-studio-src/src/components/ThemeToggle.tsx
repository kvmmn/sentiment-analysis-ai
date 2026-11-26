import { useEffect, useState } from 'react';
import { safeStorage } from '@/lib/text';

const KEY = 'saintiment_theme';
export function initTheme() {
  const saved = safeStorage()?.getItem(KEY);
  const dark = saved === 'dark'; // light unless the user picked dark
  document.documentElement.classList.toggle('dark', dark);
}

export function ThemeToggle() {
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'));
  useEffect(() => { document.documentElement.classList.toggle('dark', dark); }, [dark]);
  return (
    <button type="button" className="icon" aria-label="حالت روشن/تیره" title="حالت روشن/تیره"
      onClick={() => { const d = !dark; setDark(d); safeStorage()?.setItem(KEY, d ? 'dark' : 'light'); }}>
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor" /></svg>
    </button>
  );
}
