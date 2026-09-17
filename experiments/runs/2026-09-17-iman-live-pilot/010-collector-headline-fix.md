# Run 010 — headline extraction fix and synthetic test

Status: **3/3 synthetic tests passed; no live collection**. Local date 2026-09-18.

- Question: does the one-expression fix in `BROWSER_PARSER_JS` recover headline extraction, where the original collapsed `fullCard` before splitting lines?
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/010-collector-headline-fix/`.
- Snapshot SHA-256: `a874e7cf93d7747ab9df9bb6c6e38c05a1f581c945543739a25d18dbd13bc673` (005).
- Derivative SHA-256: `5f44a98f2b91910116fddebb55159e7270737ee744bfc0affc655bf16724411e`.
- Harness SHA-256: `766855bcd74140fc085713565ed0299667f3a389f19384590e2474f11474d751`.
- Single change: split `card.innerText` on newlines **before** cleaning each line instead of after.
- Three tests executed:
  1. Node.js `cleanStr` unit on `"Synthetic Author\nArchitect"`—baseline 1 line, fixed 3 lines with headline.
  2. Playwright headless synthetic DOM with `<br>`-separated author/headline—original empty headline, fixed `"Architect"`.
  3. End-to-end SQLite persistence via AST-extracted `DatabaseManager` + CSV export—verified `"Architect"` in both.
- Synthetic DOM only; real LinkedIn `innerText` rendering may differ. Existing 1,237 collected rows cannot be retroactively repaired. No checkpoint/scheduling implementation, no live collection, no network.
- Exact invocation metadata, test results, and exit code are in private `invocation.json`. No analysis execution.
- Original 005 and submitted baseline unchanged.
