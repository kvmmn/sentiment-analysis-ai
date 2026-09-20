# Run 012 — headline fix collector (rate-limited)

Status: **completed but rate-limited; headline fix not verified on real LinkedIn**. Local date 2026-09-18.

- Fixed collector with the headline extraction fix from Run 010 (split `card.innerText` before `cleanStr`). Fresh database, fresh browser session. All 24 queries, 35 scrolls each.
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/012-collector-headline-fix/`.
- Code SHA-256: `5f44a98f2b91910116fddebb55159e7270737ee744bfc0affc655bf16724411e` (identical to 010 fixed derivative, unchanged before/after).
- Invocation: experiment `run-once.cjs 012-collector-headline-fix collector.py`, 2-hour watchdog.
- Start `2026-09-18T12:42:??.???Z`; end `2026-09-18T13:53:??.???Z`; duration ~71 minutes; exit **0**; watchdog not triggered.

## Results

| Metric                 | Run 012 (fixed) | Run 011 (original) |
| ---------------------- | --------------- | ------------------ |
| DB rows                | **257**         | 1,043              |
| Unique IDs             | 257             | 1,043              |
| SQLite quick_check     | ok              | ok                 |
| Headlines populated    | **0**           | 0                  |
| Author names populated | 22 (9%)         | 186 (18%)          |
| Queries with results   | **5 of 24**     | ~20 of 24          |

## Rate limit discovered

After run 012 completed, a diagnostic browser inspection of the same session revealed:

> _"Our systems have detected unusual search traffic coming from your account. To protect member privacy and system security, search activity on your account has been paused. Try again later."_

LinkedIn blocked search on this account after three back-to-back collection runs (011 at ~09:41 UTC, then 012 at ~12:42 UTC). The first 5 queries returned 257 posts; queries 6–24 returned zero because search was paused mid-run.

## Why the headline fix couldn't be verified

The headline fix (split `card.innerText` before `cleanStr`) passed 3/3 synthetic tests in Run 010. But on real LinkedIn:

1. **Rate limiting** prevented inspecting the actual DOM during collection
2. **Author name extraction** is a prerequisite — the headline lookup finds the author name first, then takes the next line. Only 22 names were found (vs 186 in run 011), suggesting the extraction was already degraded before the headline step
3. Real LinkedIn DOM uses different HTML structure than the synthetic `<br>`-separated test

## Next steps

1. **Wait for rate limit cooldown** — at least several hours, possibly until tomorrow
2. **Add longer inter-query delays** — current 4–8 seconds may need 30–60 seconds
3. **Test on a single query first** — verify the fix works before running all 24
4. **Investigate author name extraction separately** — it's failing independently of the headline fix
