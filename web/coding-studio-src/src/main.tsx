import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { initTheme } from './components/ThemeToggle';

initTheme();
// Shared self-hosted fonts (web/coding/public/fonts), the same on every page of the app.
// Only on the deployed app; the claude.ai artifact preview falls back to system fonts.
if (location.pathname.startsWith('/code')) {
  for (const f of ['estedad-arabic-wght-normal', 'estedad-latin-wght-normal', 'source-serif-4-latin-opsz-normal']) {
    const pre = document.createElement('link');
    Object.assign(pre, { rel: 'preload', as: 'font', type: 'font/woff2', crossOrigin: 'anonymous', href: `/code/fonts/${f}.woff2` });
    document.head.appendChild(pre);
  }
  const font = document.createElement('link');
  font.rel = 'stylesheet';
  font.href = '/code/fonts/fonts.css';
  document.head.appendChild(font);
}
createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
