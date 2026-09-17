# Run 009 — analysis guard synthetic tests

Status: **passed 8/8; no live data or collection**. Local date 2026-09-18.

- Single invocation of AST-extracted `execute_inferential_tests` from the 008 derivative, using synthetic DataFrames in a `TemporaryDirectory`. Never imports or executes the real pipeline or preparation helper. No network.
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/009-analysis-guard-tests/`. Single `invocation.json` metadata/results file with exclusive reservation; any further execution needs a new run ID.
- Commands, CWD, record policy and individual case verdicts are in the private invocation record. All 8 synthetic cases passed: all-unclassified, singleton contingency, identical-value groups, etc. Tables and LaTeX retained even when tests skipped.
- Valid 2×2 path exercised. Dunn prerequisites (unavailable/nonsignificant) handled. No expected-count validation claims.
- Arrows confirm the status JSON schema that 008 produced. Classification/scoring copies were verified unchanged. No stakeholder inference or platform permission follows from synthetic tests.
- Private invocation hash: `126de3b23c1ea66770d8d26d4e5fce499d4bbf41219c3ee9f8d5b3f3a3600578`.
- No raw data output, network calls or live collection. Organizational isolation is not a security sandbox.
