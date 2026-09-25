# Saintiment

A collaborative research and development project working toward two intended outputs: a scientific article and a master's final thesis. Both will draw on shared research, code, data documentation, and experiment records.

Kaveh intends to use this research as part of his master's dissertation at **Arden University**, but that integration is not yet finalized. This is an intention, not a claim of university approval, sponsorship, or responsibility for the research.

Shared project reference: [kvmmn/sentiment-analysis-ai](https://github.com/kvmmn/sentiment-analysis-ai).

Project and LinkedIn app display name: **Saintiment**, chosen by Kaveh on 2026-08-28. This replaces the earlier project name **Sentiment AI** and proposed app name **GenAI Architecture Discourse Research**. The repository URL and local folder name remain unchanged.

## Team

- [Iman Sheikhansari](https://www.linkedin.com/in/imansheikhansari/)
- [Morteza Hazbei](https://www.linkedin.com/in/morteza-hazbei/)
- [Kaveh Momeni](https://linkedin.com/in/kvmmn)

Roles and publication authorship are not yet specified. This list does not establish author order or thesis authorship.

Project and privacy contact: Kaveh Momeni — [kaveh.momeni@gmail.com](mailto:kaveh.momeni@gmail.com) is his confirmed primary, long-term contact; [25199053@ardenuniversity.ac.uk](mailto:25199053@ardenuniversity.ac.uk) remains an additional contact. Kaveh supplied both for publication. Other members' email addresses will be added when provided and authorized. An email address does not establish institutional sponsorship or an approved research affiliation.

## Communication

The Telegram group **Sentiment Analysis AI** is the team's main communication channel for now.

## Start Here

**[Project map and filing rules](docs/project-map.md)** · **[Research index](research/README.md)** · **[Code index](src/README.md)** · **[Experiment workflow](experiments/README.md)** · **[Per-invocation run guide](experiments/runs/README.md)** · **[Live-pilot plan](experiments/2026-09-17-iman-live-pilot.md)** · **[📊 2026-09-25 Meeting Guide](docs/team-meeting-guide-2026-09-25.html)** · **[📘 Full Technical Benchmark](docs/team-meeting-analysis-2026-09-25.html)** · **[🎓 Thesis Methodology Draft](docs/kaveh-independent-methodology.md)**

Looking for Iman’s code? Open the [code index](src/README.md#imans-submission-local-only). The complete source package now lives in `_local/submissions/2026-09-06-iman-protocol-drafts/`, not the historical archive. Baseline extracts remain local-only and must not be run in place; separate pilot snapshots are prepared.

## Current Status — 25 September 2026 (Run 013 Pilot & Team Meeting Preparation)

- **Pilot dataset analysis:** evaluated 1,076 raw posts from verified Run 013 snapshot (`data/linkedin_genai_architecture_discourse_2026-09-20_run013.db`, SHA-256 `f0ea0952ed5ed806...`).
- **Independent analytical pipeline:** implemented in [`src/analysis/kaveh_analytical_pipeline.py`](src/analysis/kaveh_analytical_pipeline.py) with 7/7 passing unit tests (`src/analysis/tests/test_kaveh_pipeline.py`). Features Clause-Level Context-Window ABSA (±5 tokens), a 2D continuous Discursive Stance framework (Human Agency $\times$ Discourse Valence), and Multi-Signal Stakeholder Inference.
- **Empirical findings:**
  - **H1 (Bimodality):** Naive whole-post lexicons produce an artificial bimodal artifact ($BC = 0.586$) from zero-inflation; context-window ABSA demonstrates unimodality ($BC = 0.450 < 0.555$) centered around pragmatic caution.
  - **H2 (Creativity vs. Judgment):** Validated with strong significance ($p = 1.48 \times 10^{-7}$, Mann-Whitney $U = 42,018.0$); Creativity/Ideation polarity is positive (+0.219), whereas Cognitive Judgment/Oversight is negative/critical (-0.001).
  - **Stakeholder Inference:** Recovered 68.2% (734/1,076) of posts across four cohorts using credential heuristics and textual cues, bypassing empty raw headline metadata.
  - **Deskilling vs. Offloading:** Validated that architects express concern over *Cognitive Offloading* (delegating critical thinking) rather than manual deskilling.
- **Meeting materials:** produced minimalist, self-contained interactive meeting guide in Persian with Rubik typography and live in-browser editing: [`docs/team-meeting-guide-2026-09-25.html`](docs/team-meeting-guide-2026-09-25.html), backed by 5 high-resolution figures in [`docs/figures_pilot_2026-09-25/`](docs/figures_pilot_2026-09-25/).

## Historical Status — 18 September 2026 (local; executions 17 September UTC)

- **Study:** sentiment about GenAI and skills in architectural discourse. Questions and methods remain provisional; see [research notes](research/notes.md).
- **Working retrieval frame:** Domain ∧ Technology ∧ Labor/Competency, adopted for review on 10 September. Query version 1 is **not frozen**. The August two-layer catalog is a historical alternative, not the current sampling instruction.
- **Latest team record:** [Kaveh’s sent 15 September feedback](research/team/team-feedback-to-team-2026-09-15-FA.md), including its Google Doc source. Proposed fixes are not yet implemented results. Morteza’s keyword check remains unconfirmed.
- **Engineering:** [005](experiments/runs/2026-09-17-iman-live-pilot/005-collector-readiness.md) stopped on its watchdog; [007 resume](experiments/runs/2026-09-17-iman-live-pilot/007-collector-resume.md) completed with **1,237 DB/CSV rows and unique stored IDs**, net +56. [002 analysis](experiments/runs/2026-09-17-iman-live-pilot/002-analysis.md) failed on an empty contingency table; the separate [008 guarded analysis](experiments/runs/2026-09-17-iman-live-pilot/008-analysis-guarded.md) completed, preserving 1,237 enriched rows and producing descriptive/status outputs. [009 synthetic guards](experiments/runs/2026-09-17-iman-live-pilot/009-analysis-guard-tests.md) passed 8/8; no live collection. Baselines remain intact; no new dependencies.
- **Data limitation:** all 1,237 author headlines are empty and all rows classify as `Unclassified`; stakeholder inference is impossible. The analysis guard skips unsupported tests, **not repairs missing fields**. A source-level newline/whitespace extraction defect was reproduced by an isolated synthetic Node expression, not a full DOM test. No metadata collector fix, checkpoint implementation or further live run was completed; earlier proposals remain proposals. No scientific findings or access approval follow. Raw data, private scripts and profiles remain ignored/local-only; Git synchronization is pending.
- **Earlier evidence:** 001's assistant-initiated interruption and incomplete provenance remain historical. The separate [offline test](experiments/2026-09-17-iman-collector-offline.md) passed four fake-browser scenarios but failed the duplicate-upsert reporting probe; it did not run real DOM JavaScript or validate the whole collector.
- **Access:** LinkedIn DSA case Open on the last receipt (28 August); no substantive response or research/API approval recorded. The submitted three months concerns expected storage, not an approved retention exception or collection window. App creation and Page verification are confirmed; last Auth evidence shows no permissions or redirect URLs. Kaveh operates LinkedIn manually. See [application record](research/access/linkedin-application-worksheet.md).
- **Outputs:** article and thesis remain outlines. Dataset selection, models, university requirements and publication venue remain open.
- **Organization:** files grouped by purpose on 17 September; see the [old → new location map](docs/project-map.md#relocations--17-september-2026). No research scripts were run during reorganization.

## Project Guide

| Location                                                       | Purpose                                                                              |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [Project map](docs/project-map.md)                             | Where files belong, stable IDs, source-to-result traceability, relocation map        |
| [Research](research/README.md)                                 | Questions, keyword work, access/privacy evidence, team correspondence and references |
| [Code](src/README.md)                                          | Shared implementations and links to preserved local submissions, with status labels  |
| [Experiments](experiments/README.md)                           | Plans and run records, provenance template, one branch per experiment                |
| [Data](data/README.md)                                         | Public-safe dataset metadata; private versioned inputs and outputs                   |
| [Article](writing/article.md) / [Thesis](writing/thesis.md)    | Separate outputs using shared research and experiment evidence                       |
| [Local workspace](_local/README.md)                            | Private submissions, historical reports, editable work and helper scripts            |
| [Assets](assets/README.md)                                     | Public logo and its provenance                                                       |
| [Project log](research/project-log.md)                         | Dated decisions, actions, verification and unresolved issues                         |
| [Working principles](AGENTS.md) / [Privacy policy](PRIVACY.md) | Collaboration rules and preparation-stage public notice                              |

## Next Steps

1. Complete Morteza’s keyword check and agree the four pre-run fixes in the [sent letter](research/team/team-feedback-to-team-2026-09-15-FA.md): OR parentheses; Adaptation + downskilling; education/H4; three-pillar labels. Do not silently freeze query version 1.
2. Review the [current run queue](experiments/runs/README.md) and [pilot results](experiments/2026-09-17-iman-live-pilot.md). Before any recollection, prepare a separate tested collector derivative for missing metadata; preserve baselines and earlier failures. Guarded analysis completion does not restore stakeholder data or validate the whole pipeline.
3. Keep the letter's proposed 2–3-vector study pilot distinct from the current 24-query source-reviewed engineering configuration. No query fixes or platform permission are implied. Await a substantive LinkedIn response or establish another permitted source before treating research access as granted; legacy output is not an approved corpus.
4. Refine protocol, annotation, evaluation and research questions with the team. Record verified literature in [references](research/references.md).
5. Confirm university and publication requirements; develop article and thesis from shared evidence, not planned results.

## Working Format

Use plain Markdown and keep the structure small. Add tools and dependencies only when needed. Maintain one shared evidence base for both writing outputs; use relative links to reference it.

GitHub is the shared reference for publishable project work. Keep completed changes committed and synchronized, and report any sync failure. No background synchronization service is configured.

Local dataset contents and common credential files are excluded by `.gitignore`. Review files before sharing or committing: ignore rules do not detect every secret or protect already tracked files. Personal research data and credentials do not belong in this public repository.
