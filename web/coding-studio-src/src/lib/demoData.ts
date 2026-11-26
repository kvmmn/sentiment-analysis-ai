// Placeholder content for demo mode only. These are NOT posts from the study sample and must not be cited.
export const DEMO_CODERS = [
  { id: 1, name: 'کدگذار ۱', name_en: 'Coder 1' },
  { id: 2, name: 'کدگذار ۲', name_en: 'Coder 2' },
  { id: 3, name: 'کدگذار ۳', name_en: 'Coder 3' },
];

const p = (sample_id: string, author_name: string, author_type: string, headline: string, posted_at: string, post_text: string, extra: Record<string, unknown> = {}) => ({
  sample_id, source_post_id: `demo-${sample_id}`, posted_at, post_text, text_chars: post_text.length,
  author_type, author_name, author_headline: headline, post_url: 'https://www.linkedin.com/',
  reactions: 40 + sample_id.charCodeAt(2) * 3, comments: 6 + sample_id.charCodeAt(2) % 9, shares: sample_id.charCodeAt(2) % 5,
  has_external_link: false, external_url_count: 0, newsletter_title: null, newsletter_url: null, ...extra,
});

export const DEMO_POSTS = [
  p('D01', 'Demo Author A', 'profile', 'Placeholder headline · Operations lead', '2026-01-12',
    'This is demo text, not a real post. Our team started using an AI assistant for weekly reports last month. It saves time, but I worry about who checks the numbers.\n\nThe tool writes a first draft in minutes. We still spend an hour verifying it. Is that really faster?\n\nCurious how other teams handle review and accountability.'),
  p('D02', 'Demo Company B', 'company', 'Placeholder company page', '2026-01-19',
    'Demo text. We are excited to announce a new training programme on responsible AI for all employees!\n\nEvery person will learn when to rely on automated suggestions and when to escalate. Transparency is at the heart of how we build trust.\n\nRead the full announcement in our newsletter.',
    { has_external_link: true, external_url_count: 1, newsletter_title: 'Demo newsletter', newsletter_url: 'https://example.com/' }),
  p('D03', 'Demo Author C', 'profile', 'Placeholder headline · Researcher', '2026-02-02',
    'Demo text. Unpopular opinion: most "AI strategy" decks I see are just a list of tools.\n\nNobody asks what problem we are solving. Nobody measures whether the work got better. We measure adoption, which is the easiest number to move.\n\nStart with the problem. Then decide if a model helps.'),
  p('D04', 'Demo Author D', 'profile', 'Placeholder headline · Teacher', '2026-02-14',
    'Demo text. My students now ask the chatbot before they ask me. At first that hurt a little.\n\nThen I noticed the questions they bring to class are deeper. They have already covered the basics. I think my job is changing, not disappearing.',
    { has_external_link: true, external_url_count: 1 }),
  p('D05', 'Demo Author E', 'profile', 'Placeholder headline · Designer', '2026-03-01',
    'Demo text. Three months without generative tools in my design process. Here is what I learned.\n\nI was slower. I was also more confident in every decision, because I could explain each one. Clients noticed the difference.\n\nI will use the tools again, but on my terms.'),
  p('D06', 'Demo Company F', 'company', 'Placeholder company page', '2026-03-09',
    'Demo text. Customer support response times dropped by a lot after we added automated triage. Our agents now focus on the hard cases.\n\nWe did not reduce headcount. We changed what people spend their day on.'),
];

export const DEMO_EXT = [
  { id: 901, sample_id: 'D02', source_kind: 'newsletter', original_url: 'https://example.com/demo-article', resolved_url: 'https://example.com/demo-article', domain: 'example.com', title: 'Demo article (placeholder)',
    extracted_text: 'This is placeholder article text for demo mode. The programme has three modules: understanding automated suggestions, checking outputs, and knowing when to escalate.\n\nManagers will receive extra guidance on accountability. Participation is required for all staff by the end of the year.',
    extracted_chars: 290, fetch_status: 'extracted', http_status: 200 },
  { id: 902, sample_id: 'D04', source_kind: 'link', original_url: 'https://example.org/blocked', resolved_url: null, domain: 'example.org', title: null,
    extracted_text: null, extracted_chars: null, fetch_status: 'login_required', http_status: 403 },
];

export function demoSeed() {
  return {
    seq: 100,
    themes: [
      { id: '11', coder_id: 1, name: 'اعتماد و پاسخ‌گویی', sort_order: 0 },
      { id: '12', coder_id: 1, name: 'تغییر نقش کار', sort_order: 1 },
    ],
    codes: [
      { id: '21', coder_id: 1, label: 'verification-burden', color_idx: 3, theme_id: '11', created_at: '2026-11-01T10:00:00Z' },
      { id: '22', coder_id: 1, label: 'accountability', color_idx: 1, theme_id: '11', created_at: '2026-11-01T10:01:00Z' },
      { id: '23', coder_id: 1, label: 'role-shift', color_idx: 2, theme_id: '12', created_at: '2026-11-01T10:02:00Z' },
      { id: '24', coder_id: 1, label: 'corporate-optimism', color_idx: 5, theme_id: null, created_at: '2026-11-01T10:03:00Z' },
    ],
    highlights: [
      { id: '31', coder_id: 1, sample_id: 'D01', source: 'post', external_source_id: null, paragraph_idx: 0, start_offset: 125, end_offset: 162, quote: 'I worry about who checks the numbers.', code_id: '22', created_at: '2026-11-01T10:05:00Z' },
      { id: '32', coder_id: 1, sample_id: 'D01', source: 'post', external_source_id: null, paragraph_idx: 1, start_offset: 42, end_offset: 78, quote: 'We still spend an hour verifying it.', code_id: '21', created_at: '2026-11-01T10:06:00Z' },
      { id: '33', coder_id: 1, sample_id: 'D04', source: 'post', external_source_id: null, paragraph_idx: 1, start_offset: 99, end_offset: 144, quote: 'I think my job is changing, not disappearing.', code_id: '23', created_at: '2026-11-01T10:07:00Z' },
    ],
    status: [
      { coder_id: 1, sample_id: 'D01', is_coded: true, link_reviewed: false, coder_notes: 'یادداشت نمونه: لحن مردد، نه منفی.', updated_at: '2026-11-01T10:08:00Z' },
    ],
  };
}
