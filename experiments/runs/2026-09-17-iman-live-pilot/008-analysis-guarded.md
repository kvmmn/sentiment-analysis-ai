# Run 008 — guarded analysis

Status: **completed engineering execution; stakeholder inference unavailable**. Local date 2026-09-18; exact lifecycle below is UTC 2026-09-17.

- Parent code: [failed analysis 002](002-analysis.md); dataset: [completed collector 007](007-collector-resume.md). Independent read-only-source SQLite backup, no split, 1,237 rows. No browser or additional collection.
- Private CWD: `_local/work/2026-09-17-iman-live-pilot/runs/008-analysis-guarded/`. Preparation, execution manifest, stdout/stderr and `validation.json` remain local-only.
- Invocation: experiment `run-once.cjs 008-analysis-guarded analysis_pipeline.py`, executing repository `.venv/bin/python -u code/analysis_pipeline.py` in that CWD. Reused Python 3.13.11 environment; full package/OS/branch/dirty-state inventory in manifest. Base commit `966de34c010b10f3b711df0e2cd17487ac8d3fe5`; experimental source uncommitted/private. One-hour watchdog, not triggered.
- Start `2026-09-17T22:54:15.663Z`; end `2026-09-17T22:54:20.167Z`; exit **0**.
- Baseline code SHA-256: `1b5d21e6445e5ffc9e4eb190657ec6b1e926c83a02af1f8e5220b9a8b03eb8ad`.
- Derivative SHA-256: `06c54dbdaba9514fb3f2afde7c4b92846c0370c0683ff8239ab217bd9800dec7`.
- Source DB SHA-256: `390beaf3026600235a42a48fcf644be3a4900f56a0eb044bf95a43e5263b4883`.
- Input backup SHA-256: `5217e0c7fd0aa4d0392e879ee4a1be063795313256c6b5f1bfe5dcce5a70cdfc` (same as 002's input).

## Changes and verification

Classification/lexical scoring remain unchanged. Added explicit skipped-test statuses for insufficient/identical Kruskal groups and empty/single-dimension contingencies; record Dunn prerequisites. Retain tables and LaTeX even when tests cannot run. Missing/empty DB now fails explicitly; input opens read-only. Computed chi-square results report expected counts without claiming assumptions validated. [Synthetic guard tests](009-analysis-guard-tests.md) passed before execution.

Validation at `2026-09-17T22:55:09.255789+00:00`: all 10 manifest-listed artifacts matched hashes; code and input DB unchanged; SQLite quick_check passed; preserved 007 DB hash unchanged. Enriched CSV and Parquet each contain 1,237 rows with matching ordered, unique IDs. Every stakeholder label is `Unclassified`.

Produced private artifacts under `corpus_data/`: enriched CSV/Parquet; `journal_tables/table1_aspect_descriptives.csv` (five aspects), empty stakeholder/stance contingency CSV, `manuscript_table1.tex`, `manuscript_table3.tex`, and `inferential_test_status.json`. Kruskal skipped (`insufficient_groups`), Dunn skipped (`prerequisite_not_met`), chi-square skipped (`empty_contingency`). No Dunn table expected or produced. Artifact hashes/sizes and logs are in the private manifest.

## Limits and next action

All 1,237 source headlines are empty; this revision does not repair them. Collector source normalizes whitespace before splitting on newlines, making next-line headline selection impossible. An isolated synthetic expression reproduced newline loss, not live DOM correctness. Source CSV also has only 189 nonempty author names, including 138 `Unknown` values; 1,099 profile URL fields are nonempty. No identities or raw text are published.

Do not use these outputs as validated sentiment measurements, stakeholder comparisons, causal findings or publication-ready tables. Review extraction with synthetic fixtures and a separately registered derivative before any recollection. No collector checkpoint or metadata fix was implemented in this task. Access, retention/deletion, scientific validation and reviewer remain unresolved. Organizational isolation is not an OS/network sandbox; private outputs are not backed up by GitHub.
