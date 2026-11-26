import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { initTheme } from './components/ThemeToggle';

initTheme();
// Fonts load after first paint; system fonts are the fallback when the host blocks Google Fonts.
const font = document.createElement('link');
font.rel = 'stylesheet';
font.href = 'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=JetBrains+Mono:wght@400;500&display=swap';
document.head.appendChild(font);
createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
