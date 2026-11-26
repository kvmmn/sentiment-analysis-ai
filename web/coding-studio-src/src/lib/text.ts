export function splitParagraphs(text: string | null | undefined): string[] {
  return String(text || '').split(/\n{2,}/).map(s => s.trim()).filter(Boolean);
}

export interface Range { start: number; end: number }

// Same sentence rule as v1, so stored offsets keep lining up.
export function splitSentences(text: string): Range[] {
  const ranges: Range[] = [];
  const re = /[^.!?\n]+[.!?]+(?:\s+|$)|[^.!?\n]+$/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text)) !== null) {
    const trimmed = m[0].trimEnd();
    if (trimmed.length > 0) ranges.push({ start: m.index, end: m.index + trimmed.length });
  }
  return ranges;
}

// Character offset of (node, offset) inside a paragraph element, ignoring label tags drawn into the text.
export function offsetIn(pEl: HTMLElement, node: Node, offset: number): number {
  const skip = (n: Node) => Boolean(n.parentElement?.closest('[data-skip]'));
  const walker = document.createTreeWalker(pEl, NodeFilter.SHOW_TEXT);
  let total = 0;
  let t: Node | null;
  if (node.nodeType !== Node.TEXT_NODE) {
    const stop = node.childNodes[offset] || null;
    while ((t = walker.nextNode())) {
      if (stop && (stop === t || stop.contains(t) || (stop.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_FOLLOWING))) break;
      if (!stop && !node.contains(t) && (node.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_FOLLOWING)) break;
      if (!skip(t)) total += t.nodeValue?.length || 0;
    }
    return total;
  }
  while ((t = walker.nextNode())) {
    if (t === node) return total + (skip(t) ? 0 : offset);
    if (!skip(t)) total += t.nodeValue?.length || 0;
  }
  return total;
}

export const fa = (n: number | null | undefined) => Number(n || 0).toLocaleString('fa-IR');

export const COLOR_IDS = [1, 2, 3, 4, 5, 6] as const;
export const colorVar = (idx: number | null | undefined) => {
  const i = COLOR_IDS.includes(Number(idx) as 1) ? Number(idx) : 1;
  return { fg: `var(--c${i})`, bg: `var(--c${i}-bg)` };
};

export const FETCH_LABEL: Record<string, string> = {
  extracted: 'متن مقاله استخراج شد',
  login_required: 'لینک نیازمند ورود در مرورگر است',
  paywalled: 'سایت محدودیت اشتراک دارد',
  pdf_or_media: 'فایل PDF یا رسانه',
  metadata_only: 'فقط عنوان صفحه در دسترس است',
  failed: 'دسترسی مستقیم ممکن نبود',
};

export function safeStorage() {
  try {
    const k = '__t';
    window.localStorage.setItem(k, '1');
    window.localStorage.removeItem(k);
    return window.localStorage;
  } catch {
    return null;
  }
}

export function download(name: string, content: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function csvCell(v: unknown) {
  const s = String(v ?? '');
  return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}
