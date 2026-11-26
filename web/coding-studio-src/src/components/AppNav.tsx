// Links to the other screens of the team app (swipe screening and kept posts), as in v1.
export function AppNav({ className = '' }: { className?: string }) {
  return (
    <nav aria-label="بخش‌های پروژه" className={`items-center gap-1 text-[12.5px] ${className}`}>
      <a href="/" className="rounded-[4px] px-2 py-1 text-[var(--muted)] hover:bg-[var(--sunk)] hover:text-[var(--ink)]">غربالگری</a>
      <a href="/kept" className="rounded-[4px] px-2 py-1 text-[var(--muted)] hover:bg-[var(--sunk)] hover:text-[var(--ink)]">منتخب‌ها</a>
      <a href="/code/" aria-current="page" className="rounded-[4px] px-2 py-1 font-semibold text-[var(--ink)]">کدگذاری</a>
    </nav>
  );
}
