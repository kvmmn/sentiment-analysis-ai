// Shared shape of the kept-posts download. The file must not name who kept a post.
export const KEPT_POST_FIELDS = [
  'source_post_id',
  'post_type',
  'post_url',
  'posted_at',
  'post_text',
  'text_chars',
  'author_type',
  'author_name',
  'author_headline',
  'author_url',
  'reactions',
  'comments',
  'shares',
  'media',
  'matched_query_count',
  'matched_query_codes',
  'matched_families',
];

export const KEEPER_FIELD_NAMES = new Set([
  'kept_by',
  'kept_by_name',
  'kept_by_name_en',
  'reviewer_id',
  'decided_by',
  'decided_by_name',
  'set',
  'set_name',
  'keeper',
  'who',
  'who_kept',
]);

export function parseKeptBy(value) {
  if (value == null || value === '' || value === 'all') return null;
  const n = Number(value);
  if (n === 1 || n === 2 || n === 3) return n;
  return undefined;
}

export function stripKeeperFields(row) {
  const out = {};
  for (const key of KEPT_POST_FIELDS) {
    if (Object.prototype.hasOwnProperty.call(row, key)) out[key] = row[key];
  }
  return out;
}

export function keptExportPayload(rows, { exportedAt = new Date() } = {}) {
  const posts = (rows || []).map(stripKeeperFields);
  return {
    project: 'Saintiment',
    source: 'neon:_saintiment_swipe_team_db',
    source_run_id: 'X2gdX05u8rP41b4rG',
    source_dataset_id: 'WUsK3RRYo7nKEOUbA',
    exported_at: exportedAt instanceof Date ? exportedAt.toISOString() : String(exportedAt),
    summary: { kept_posts: posts.length },
    posts,
  };
}

export function collectKeys(value, acc = new Set()) {
  if (Array.isArray(value)) {
    for (const item of value) collectKeys(item, acc);
  } else if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      acc.add(key);
      collectKeys(child, acc);
    }
  }
  return acc;
}
