# Keyword Discourse Catalog — EN / FA / DE

Status: **sourced retrieval catalog**, 2026-08-31. Terms for **permitted** discourse retrieval when platform access exists. This is **not a harvest plan**, **not a collection licence**, and **not** the sentiment coding lexicon.

**Critical rule:** **Sentiment lemmas belong in DO-NOT-RETRIEVE** — use [keyword-lexicon.md](keyword-lexicon.md) for post-sample coding only.

Host decisions: [keyword-systems.md](keyword-systems.md). Scope and storage: [keywords-search-storage.md](keywords-search-storage.md).

---

## Layer model (discourse)

| Layer | EN role | Retrieval |
| --- | --- | --- |
| **A** | Architecture object **AND** GenAI | Required for neutral discovery |
| **B** | Deskilling, authorship, judgment, labour, professional identity | Second filter only — **must not select RQ1 sample** |

Construction/AEC adjacent terms and teammate hashtags (`constructionAI`, `GenAIandBuiltEnvironment`) stay **adjacent-AEC**, not Saintiment primary architecture frame.

---

## English (EN)

### Layer A — architecture + GenAI

Use pairs from [keyword-lexicon.md](keyword-lexicon.md) §1 and §2. Core lemmas:

- architect, architectural, architectural design, architecture firm, architecture student, architectural education, design studio, architectural practice, architecture practice, archviz
- generative AI, GenAI, Midjourney, ChatGPT, DALL-E, Stable Diffusion, text-to-image, AI rendering, LLM

**archviz** stays **EN** — do not invent FA/DE calques.

### Layer B — inside Layer A only

Deskilling, de-skilling, skill loss, upskilling, reskilling, authorship, professional judgment, creativity, design thinking, critical thinking, Urheberrecht (when DE cross-pass), competency / ARB outcomes language.

Professional warrants: RIBA AI Report 2025; AIA AI Firm Toolkit; ARB competency outcomes; BAK KI FAQ; Braverman / SBTC as **Layer 2 labour lemmas only**.

### Hashtags (EN) — high noise

| Tag / pattern | Status |
| --- | --- |
| architecture + GenAI combined hashtags | High noise — pilot before scale |
| `#constructionAI` | Adjacent-AEC (teammate); not primary architecture |
| `#GenAIandBuiltEnvironment` | Adjacent-AEC; **no scholarly hit** (see [keyword-source-identification.md](keyword-source-identification.md)) |
| `#GenerativeAI`, `#GenAi` | Broad GenAI noise |

### Exclusions (EN)

Always exclude IT-architecture false positives:

- software architect, software architecture, solutions architect, enterprise architecture, cloud architect, computer architecture, IT architect, data architect, network architect, security architect, systems architect

Also exclude:

- Generic AI with **no architecture object**
- BIM-only posts with **no GenAI** cue
- Job ads / promotional templates (low-authenticity screen per teammate description)

---

## Persian / Farsi (FA) — sourced lemmas

**Separate pass** — require explicit `language: fa` in storage schema. Do **not** mix with EN hits.

| Lemma (transliteration) | Source | Layer | Notes |
| --- | --- | --- | --- |
| memar / memari | Farhangestan | A | Architecture / architect |
| mohandes-e memar | IRCEO (1374 Law) | A | Licensed architect engineer |
| reshte-ye memari | IRCEO | A | Architecture discipline |
| daftar-e mohandesi-ye tarrahi-ye sakhteman | 1374 Law / IRCEO | A | Architectural design office |
| hush-e masnui-ye movalled | Honar-ha-ye Ziba + IRCEO | A | **Preferred GenAI lemma** |
| prompt-nevisi + ChatGPT | IRCEO | A | Prompt-writing with ChatGPT |
| nevisandegi | IRCEO / discourse | B | Writing / authorship |
| tafakkur-e naqqadane | Architecture education discourse | B | Critical thinking |
| ostudiyo | Studio (design studio context) | A | Weak alone — pair with memari |
| ettelaat-e sakhteman | BIM wording A | A | Keep **both** BIM Persian wordings |
| ettelaat-e sakht | BIM wording B | A | Variant — do not collapse without team decision |

### FA — NOT approved / GAP

| Item | Status |
| --- | --- |
| hushvare / humas for GenAI | **NOT approved** (Mehr 1405) — do not retrieve |
| maharat-zedayi as architecture-journal jargon | **GAP** — dictionary-only; **do not retrieve** as architecture jargon |
| deskilling lemma | **GAP** |
| hashtag set | **GAP** — do not invent |
| validated FA architecture sentiment dictionary | **GAP** |
| ISO 6707 FA | **GAP** |
| UNESCO FA architecture terms | **GAP** |

---

## German (DE) — sourced lemmas

**Separate pass** — require explicit `language: de`.

| Lemma | Source | Layer | Notes |
| --- | --- | --- | --- |
| Künstliche Intelligenz | Standard | A | AI |
| generative KI | Standard / BAK | A | GenAI |
| KI-Bildgeneratoren | BAK/AKNW | A | Image generators |
| Prompts | BAK | A | Prompt engineering |
| Architekturbüro | Professional | A | Architecture office |
| Architektinnen und Architekten | Professional | A | Gender-inclusive profession |
| Architektenschaft | Professional | A | Profession collective |
| Planende | BAK | A | Planning professionals |
| Entwerfen | Design process | A | Designing |
| Gebäudevisualisierungen | BAK/AKNW | A | Building visualizations |
| Bauwerksinformationsmodellierung | DIN EN ISO 19650 | A | BIM — preferred DE BIM term |
| Deskilling (loanword) | Layer 2 | B | English loan in DE discourse |
| Dequalifizierung | Duden | B | Deskilling |
| Kompetenzverlust | Duden | B | Skill loss |
| Urheberrecht | Legal | B | Copyright |
| Autorschaft | Legal/professional | B | Authorship |
| Verantwortung | Professional ethics | B | Responsibility |
| Berufsbild | Professional identity | B | Professional profile |

### DE — warnings

| Item | Rule |
| --- | --- |
| **Architektur** alone | Hits IT / software architecture — always pair with GenAI + exclusion set |
| **archviz** | Stay **EN**; no FA/DE calque |
| Deskilling lemmas | **Layer 2 only** — inside Layer A, never as sample selector |
| Hashtag set | **GAP** — do not invent |
| validated DE architecture sentiment dictionary | **GAP** |

---

## DO-NOT-RETRIEVE (all languages)

Sentiment and stance coding terms — for annotation after sampling only:

- excited, terrified, hype, threat, fear, optimism, positive sentiment, negative sentiment, stance markers, emotion lexicons

Full English tables remain in [keyword-lexicon.md](keyword-lexicon.md); do not add to platform query strings.

---

## Warrants (professional — not retrieval strings)

| Source | Use in project |
| --- | --- |
| RIBA AI Report 2025 | Professional judgment, human creativity framing |
| AIA AI Firm Toolkit | Firm governance of GenAI |
| ARB competency outcomes | Regulatory skill expectations |
| BAK KI FAQ | German chamber AI guidance |
| Braverman / SBTC | Layer 2 labour-market vocabulary only |

---

## Gaps summary

- Larbi (2026) methods unread — no import of their discourse lemmas
- Teammate LinkedIn 71/6173 unpublished
- FA deskilling, FA/DE hashtags, ISO 6707 FA/DE, UNESCO FA
- No live platform query tests on 2026-08-31
- No validated FA/DE sentiment dictionaries for architecture discourse
