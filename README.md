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

## Current Status

Initial planning stage. The [first scratch document](research/initial-scratch.md) proposes studying sentiment about GenAI and deskilling in architectural discourse, including soft skills, hard skills, and stakeholder differences. The [research notes](research/notes.md) organize this proposal; the topic and questions are not yet finalized.

Datasets, models, university requirements, and publication venue remain undecided. No experiments have been run or findings established in this project.

Current focus (2026-08-31): the [keyword systems map](research/keyword-systems.md) separates literature retrieval ([strings](research/keyword-literature-strings.md)), discourse catalog ([EN/FA/DE](research/keyword-discourse-catalog.md)), and sentiment coding ([lexicon](research/keyword-lexicon.md)). **Keyword catalog (browser):** [docs/index.html](docs/index.html) — once GitHub Pages is enabled from `/docs`, also at [https://kvmmn.github.io/sentiment-analysis-ai/](https://kvmmn.github.io/sentiment-analysis-ai/). [Source identification](research/keyword-source-identification.md) compares teammate strings with verified analogues (Ghimire 2024: 32 opinions; Larbi 2026 methods unread). Query version 1 is **not** frozen; no live database counts or social corpus were collected. Search limits and storage stay in the [scope note](research/keywords-search-storage.md) — still not a collection licence. Kaveh submitted the LinkedIn research-access form on 2026-08-28. His case receipt shows **Open** and an automated acknowledgement, not research/API approval. The [application record](research/linkedin-application-worksheet.md) captures the submitted answers, including Arden email, Article 40(12): No, and expected data storage of **3 Months in Germany**. This is a declared storage period, not an approved retention exception or a confirmed collection window. Await a substantive support response. The **Saintiment** app and verified Page association remain in place; the last Auth evidence showed **no OAuth permissions** or **redirect URLs**, with no later authorization test confirmed. Kaveh operates LinkedIn manually. See the [setup notes](research/notes.md) and [access review](research/linkedin-data-access-review.md).

Desk update (2026-09-10): the team is reviewing Iman’s draft package (study protocol, three-pillar search matrix `Domain ∧ GenAI ∧ Labor Dynamics`, annotation codebook, harvest/analysis scripts). Kaveh adopted the **three-pillar model as the working sampling frame** for the keyword-review pass; individual terms, the LinkedIn vector list, and query version 1 are still **not frozen**, and no new collection was run. Team order agreed on 8 September: keyword confirmation (Kaveh → Morteza) → pilot/collection → protocol and inclusion/exclusion rewrite. The drafts, the Telegram summary, the desk critique, and Kaveh’s feedback letter to the team live only under `_local/archive/` (git-ignored). The 4 September Playwright scrape produced an exploratory CSV in `linkedin-scraper/`; it is not an approved research corpus. See the [project log](research/project-log.md) sections 28–31.

## Project Guide

| Location | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Working principles for contributors and coding agents |
| [Privacy policy](PRIVACY.md) | Preparation-stage privacy notice for the project and proposed LinkedIn app |
| [Privacy-policy review](research/privacy-policy-review.md) | Requirements, drafting rationale, and publication status |
| [Research application record](research/linkedin-application-worksheet.md) | Submitted answers, receipt status, evidence limits, and follow-up needs |
| [Logo](assets/README.md) | Current project logo and generation record |
| [Project log](research/project-log.md) | Chronology, decisions, rationale, completed work, and open questions |
| [Local workspace](_local/README.md) | Machine-only archive and scratch (`archive/`, `scraper/`); contents git-ignored except this README |
| [Initial scratch document](research/initial-scratch.md) | Original first draft, preserved unchanged |
| [Research notes](research/notes.md) | Problem definition, questions, ideas, and decisions |
| [Keyword systems map](research/keyword-systems.md) | Host decisions: three instruments, two layers, gaps |
| [Keyword literature strings](research/keyword-literature-strings.md) | Scopus S-A1, WoS W-A1, IEEE/ Scholar supplements — copy-paste protocol |
| [Keyword discourse catalog](research/keyword-discourse-catalog.md) | Sourced EN/FA/DE discourse retrieval terms (not a harvest plan) |
| [Keyword source identification](research/keyword-source-identification.md) | Teammate strings vs Ghimire, Larbi, and adjacent papers |
| [Keyword lexicon](research/keyword-lexicon.md) | English sentiment/stance coding tables mapped to research questions |
| [Keywords, search scope, and storage](research/keywords-search-storage.md) | Search limits and local JSONL storage plan (not a collection licence) |
| [LinkedIn access review](research/linkedin-data-access-review.md) | Sourced comparison of access routes, tools, restrictions, and next steps |
| [References](research/references.md) | Shared source records and reading notes |
| [LinkedIn scraper](linkedin-scraper/README.md) | Exploratory Playwright scraper, keywords, and test-run CSV (engineering test, not a research corpus) |
| [Source code](src/) | Reserved for future implementation |
| [Data guide](data/README.md) | Dataset documentation and handling guidance |
| [Experiments](experiments/README.md) | Template for reproducible experiment records |
| [Article](writing/article.md) | Scientific article outline |
| [Thesis](writing/thesis.md) | Master's thesis outline |

## Next Steps

1. Review and refine the proposed research problem and questions with the team.
2. Confirm the keyword list on Iman’s three-pillar matrix (Kaveh, then Morteza); run a small pilot before any full harvest; freeze query version 1 only after that pass. The [keyword systems map](research/keyword-systems.md) records the earlier host evaluation.
3. Confirm university requirements and explore publication requirements.
4. Read relevant literature and record verified sources.
5. Identify suitable datasets, access conditions, and evaluation approaches.
6. Plan a first baseline experiment before choosing implementation tools. Do not collect a corpus until a source is permitted.

## Working Format

Use plain Markdown and keep the structure small. Add tools and dependencies only when needed. Maintain one shared evidence base for both writing outputs; use relative links to reference it.

GitHub is the shared reference for publishable project work. Keep completed changes committed and synchronized, and report any sync failure. No background synchronization service is configured.

Local dataset contents and common credential files are excluded by `.gitignore`. Review files before sharing or committing: ignore rules do not detect every secret or protect already tracked files. Personal research data and credentials do not belong in this public repository.
