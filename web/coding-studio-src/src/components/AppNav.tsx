// Links to the other screens of the team app (swipe screening and kept posts), as in v1,
// plus the compare page, which gets its own distinct style (CompareLink).
export const COMPARE_URL = '/code/compare';
export const CODES_URL = '/code/codes';

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

export function MapIcon({ size = 15 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="6" cy="6" r="2.5" /><circle cx="18" cy="6" r="2.5" /><circle cx="12" cy="18" r="2.5" /><path d="M8 7.5l3 8M16 7.5l-3 8M8.5 6h7" />
    </svg>
  );
}

// The coder's code map: all their codes on one page, apart from the post texts.
export function CodesLink({ coderId, label = 'نقشهٔ کدها', compact = false, className = '' }: { coderId?: number | null; label?: string; compact?: boolean; className?: string }) {
  const href = coderId ? `${CODES_URL}#c=${coderId}` : CODES_URL;
  return (
    <a href={href} className={`compare-link ${className}`} title="همهٔ کدهای این کدگذار با متن کامل، جدا از پست‌ها" aria-label={label}>
      <MapIcon /><span className={compact ? 'max-sm:hidden' : ''}>{label}</span>
    </a>
  );
}
