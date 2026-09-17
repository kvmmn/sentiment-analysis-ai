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

**[Project map and filing rules](docs/project-map.md)** · **[Research index](research/README.md)** · **[Code index](src/README.md)** · **[Experiment workflow](experiments/README.md)**

Looking for Iman’s code? Open the [code index](src/README.md#imans-submission-local-only). The complete source package now lives in `_local/submissions/2026-09-06-iman-protocol-drafts/`, not the historical archive. It is local-only and unrun; the index links directly to both Python extracts.

## Current Status — 17 September 2026

- **Study:** sentiment about GenAI and skills in architectural discourse. Questions and methods remain provisional; see [research notes](research/notes.md).
- **Working retrieval frame:** Domain ∧ Technology ∧ Labor/Competency, adopted for review on 10 September. Query version 1 is **not frozen**. The August two-layer catalog is a historical alternative, not the current sampling instruction.
- **Latest team record:** [Kaveh’s sent 15 September feedback](research/team/team-feedback-to-team-2026-09-15-FA.md), including its Google Doc source. Proposed fixes are not yet implemented results. Morteza’s keyword check remains unconfirmed.
- **Code and data:** earlier September scraper engineering tests occurred. Outputs remain private and are not an approved research corpus. No completed formal experiment record or established research findings exist.
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
2. For a code test, start at the [code index](src/README.md) and [experiment workflow](experiments/README.md). Prepare a separate offline synthetic check before considering live collection. Preserve submission originals and record exact source hashes and changes.
3. A proposed 2–3-vector pilot needs an experiment branch, a plan and permitted inputs/access. The old scraper output is not an approved corpus. Await a substantive LinkedIn response or establish another permitted source.
4. Refine protocol, annotation, evaluation and research questions with the team. Record verified literature in [references](research/references.md).
5. Confirm university and publication requirements; develop article and thesis from shared evidence, not planned results.

## Working Format

Use plain Markdown and keep the structure small. Add tools and dependencies only when needed. Maintain one shared evidence base for both writing outputs; use relative links to reference it.

GitHub is the shared reference for publishable project work. Keep completed changes committed and synchronized, and report any sync failure. No background synchronization service is configured.

Local dataset contents and common credential files are excluded by `.gitignore`. Review files before sharing or committing: ignore rules do not detect every secret or protect already tracked files. Personal research data and credentials do not belong in this public repository.
