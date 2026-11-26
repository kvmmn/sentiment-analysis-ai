import { memo, type ReactNode } from 'react';
import type { Code, Highlight } from '@/lib/types';
import { colorVar, splitSentences } from '@/lib/text';

interface Props {
  pIdx: number;
  text: string;
  hls: Highlight[];
  codeById: Map<number, Code>;
  draft: { start: number; end: number } | null;
  activeHlIds: Set<number>;
  showTags: boolean;
  onSentence: (pIdx: number, start: number, end: number, el: HTMLElement) => void;
  onHighlight: (hlId: number, el: HTMLElement) => void;
}

function ParagraphImpl({ pIdx, text, hls, codeById, draft, activeHlIds, showTags, onSentence, onHighlight }: Props) {
  const sentences = splitSentences(text);
  const cuts = new Set([0, text.length]);
  for (const s of sentences) { cuts.add(s.start); cuts.add(s.end); }
  for (const h of hls) { cuts.add(Math.max(0, h.start_offset)); cuts.add(Math.min(text.length, h.end_offset)); }
  if (draft) { cuts.add(Math.max(0, draft.start)); cuts.add(Math.min(text.length, draft.end)); }
  const pts = [...cuts].filter(x => x >= 0 && x <= text.length).sort((a, b) => a - b);

  const out: ReactNode[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1];
    if (a === b) continue;
    const chunk = text.slice(a, b);
    const covering = hls
      .filter(h => h.start_offset <= a && h.end_offset >= b)
      .sort((x, y) => (x.end_offset - x.start_offset) - (y.end_offset - y.start_offset));
    const inDraft = draft && draft.start <= a && draft.end >= b;
    const sent = sentences.find(s => s.start <= a && s.end >= b);

    if (covering.length) {
      const top = covering[0];
      const col = colorVar(codeById.get(top.code_id)?.color_idx);
      // one band per code in the underline, so a passage with several codes shows every colour
      const fgs = [...new Set(covering.map(h => colorVar(codeById.get(h.code_id)?.color_idx).fg))];
      const step = 100 / fgs.length;
      const bands = fgs.map((f, k) => `${f} ${k * step}% ${(k + 1) * step}%`).join(', ');
      const active = covering.some(h => activeHlIds.has(h.id));
      out.push(
        <span key={a} data-hl={top.id} title={covering.map(h => codeById.get(h.code_id)?.label).filter(Boolean).join(' · ')}
          className={`hl cursor-pointer ${active ? 'hl-active' : ''}`}
          style={{ backgroundColor: col.bg, backgroundImage: `linear-gradient(to right, ${bands})`, backgroundSize: `100% ${fgs.length > 1 ? 3 : 2}px`, backgroundPosition: 'bottom', backgroundRepeat: 'no-repeat' }}
          onClick={e => { if (window.getSelection()?.isCollapsed !== false) onHighlight(top.id, e.currentTarget); }}>
          {chunk}
        </span>,
      );
      const ending = covering.filter(h => h.end_offset === b);
      if (showTags && ending.length) {
        // Small superscript labels in each code's colour; one group per passage end.
        out.push(
          <sup key={`t${b}`} data-skip contentEditable={false} className="hl-tags">
            {ending.map(h => {
              const code = codeById.get(h.code_id);
              return (
                <button key={h.id} type="button" className="hl-tag" style={{ color: colorVar(code?.color_idx).fg }}
                  onClick={e => onHighlight(h.id, e.currentTarget)} aria-label={`ویرایش کدهای این عبارت: ${code?.label ?? ''}`}>
                  {code?.label ?? '…'}
                </button>
              );
            })}
          </sup>,
        );
      }
    } else if (inDraft) {
      out.push(<span key={a} className="hl-draft">{chunk}</span>);
    } else if (sent) {
      out.push(
        <span key={a} className="sent"
          onClick={e => { if (window.getSelection()?.isCollapsed !== false) onSentence(pIdx, sent.start, sent.end, e.currentTarget); }}>
          {chunk}
        </span>,
      );
    } else {
      out.push(chunk);
    }
  }
  return <p data-pidx={pIdx} dir="auto" className="prose-p">{out}</p>;
}

export const Paragraph = memo(ParagraphImpl);
