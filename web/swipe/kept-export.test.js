import assert from 'node:assert/strict';
import { test } from 'node:test';
import {
  collectKeys,
  keptExportPayload,
  KEEPER_FIELD_NAMES,
  parseKeptBy,
  stripKeeperFields,
} from './kept-export.js';

test('parseKeptBy accepts the three reviewers or all', () => {
  assert.equal(parseKeptBy(undefined), null);
  assert.equal(parseKeptBy('all'), null);
  assert.equal(parseKeptBy('1'), 1);
  assert.equal(parseKeptBy('2'), 2);
  assert.equal(parseKeptBy('3'), 3);
  assert.equal(parseKeptBy('4'), undefined);
  assert.equal(parseKeptBy('kaveh'), undefined);
});

test('stripKeeperFields keeps post fields and drops who-kept columns', () => {
  const stripped = stripKeeperFields({
    source_post_id: 'abc',
    post_text: 'hello',
    author_name: 'Ada',
    reactions: 3,
    kept_by: 3,
    kept_by_name: 'کاوه',
    kept_by_name_en: 'Kaveh',
    reviewer_id: 3,
    decided_by: 3,
    set: 3,
    set_name: 'Kaveh',
    position: 12,
    decision: 'keep',
  });
  assert.deepEqual(stripped, {
    source_post_id: 'abc',
    post_text: 'hello',
    author_name: 'Ada',
    reactions: 3,
  });
  assert.equal('kept_by' in stripped, false);
  assert.equal('position' in stripped, false);
});

test('keptExportPayload JSON has no who-selected keys', () => {
  const payload = keptExportPayload(
    [
      {
        source_post_id: '1',
        post_type: 'post',
        post_url: 'https://example.com/p',
        posted_at: '2026-01-01',
        post_text: 'text',
        text_chars: 4,
        author_type: 'profile',
        author_name: 'Ada',
        author_headline: 'Architect',
        author_url: 'https://example.com/ada',
        reactions: 1,
        comments: 0,
        shares: 0,
        media: null,
        matched_query_count: 1,
        matched_query_codes: 'Q01',
        matched_families: 'direct',
        kept_by: 1,
        kept_by_name: 'مرتضی',
        kept_by_name_en: 'Morteza',
        reviewer_id: 1,
        decided_by: 1,
      },
    ],
    { exportedAt: '2026-11-12T00:00:00.000Z' }
  );
  assert.equal(payload.summary.kept_posts, 1);
  assert.equal(payload.posts[0].source_post_id, '1');
  const keys = collectKeys(payload);
  for (const name of KEEPER_FIELD_NAMES) {
    assert.equal(keys.has(name), false, `export leaked ${name}`);
  }
});
