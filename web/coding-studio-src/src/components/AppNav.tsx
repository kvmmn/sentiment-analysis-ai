// Links to the other screens of the team app (swipe screening and kept posts), as in v1,
// plus the compare page, which gets its own distinct style (CompareLink).
export const COMPARE_URL = '/code/compare';

export function CompareIcon({ size = 15 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <rect x="3" y="4" width="5" height="16" rx="1" /><rect x="9.5" y="4" width="5" height="16" rx="1" /><rect x="16" y="4" width="5" height="16" rx="1" />
    </svg>
  );
}

export function CompareLink({ post, label = 'مقایسهٔ کدگذارها', compact = false, className = '' }: { post?: string | null; label?: string; compact?: boolean; className?: string }) {
  const href = post ? `${COMPARE_URL}#${encodeURIComponent(post)}` : COMPARE_URL;
  return (
    <a href={href} className={`compare-link ${className}`} title="همهٔ کدگذارها کنار هم، پست به پست" aria-label={label}>
      <CompareIcon /><span className={compact ? 'max-sm:hidden' : ''}>{label}</span>
    </a>
  );
}

export function AppNav({ className = '' }: { className?: string }) {
  return (
    <nav aria-label="بخش‌های پروژه" className={`items-center gap-1 text-[12.5px] ${className}`}>
      <a href="/" className="rounded-[4px] px-2 py-1 text-[var(--muted)] hover:bg-[var(--sunk)] hover:text-[var(--ink)]">غربالگری</a>
      <a href="/kept" className="rounded-[4px] px-2 py-1 text-[var(--muted)] hover:bg-[var(--sunk)] hover:text-[var(--ink)]">منتخب‌ها</a>
      <a href="/code/" aria-current="page" className="rounded-[4px] px-2 py-1 font-semibold text-[var(--ink)]">کدگذاری</a>
    </nav>
  );
}
