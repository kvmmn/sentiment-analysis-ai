# Keyword Discourse Catalog — EN / FA / DE

Status: **sourced retrieval catalog**, 2026-08-31. Terms for **permitted** discourse retrieval when platform access exists. This is **not a harvest plan**, **not a collection licence**, and **not** the sentiment coding lexicon.

**Critical rule:** **Sentiment lemmas belong in DO-NOT-RETRIEVE** — use [keyword-lexicon.md](keyword-lexicon.md) for post-sample coding only.

Host decisions: [keyword-systems.md](keyword-systems.md) (includes **lexicon draft conflict** ruling). Scope and storage: [keywords-search-storage.md](keywords-search-storage.md).

**Lexicon note:** Two **03 lexicon drafts** existed and were **not silently merged**; host rulings below.

---

## Draft conflict — two 03 lexicon drafts (not silently merged)

Two **03 lexicon drafts** proposed FA/DE/EN discourse lemmas. They **conflicted** and were **not silently merged**; the **later conservative pass is not automatic truth**. Host rulings (2026-08-31) are recorded in [keyword-systems.md](keyword-systems.md#lexicon-draft-conflict--two-03-drafts-2026-08-31).

### Host ruling details (03 conflict)

- **`دفتر مهندسی`** is the **INBR** legal office term; do **not** invent **`دفتر معماری`** as Nezam terminology.
- **BIM (FA):** keep **both** INSO 23198-1 **`مدلسازی اطلاعات ساخت`** and INSO 12690-1 **`مدل سازی اطلاعات ساختمان`**; **not Layer A**.
- **`هوش مصنوعی مولد`** is sourced to https://jfaup.ut.ac.ir/p_generative-ai and IRCEO LMS course **1180313** syllabus (**`آشنایی با هوش مصنوعی مولد`** — https://lmsiriceo.ir/course/show/470/d98d61b1b9f19d88849096542a221190); **not** Farhangestan-approved; **not** an invented calque.

Summary:

| Ruling | Outcome |
| --- | --- |
| FA `هوش مصنوعی مولد` | **KEEP** — sourced journal/CPD use; not Farhangestan-approved; not invented calque |
| FA legal office | **دفتر مهندسی** (INBR) — not `دفتر معماری` |
| FA BIM (both INSO) | **Not Layer A** |
| DE `Dequalifizierung`, `Architektur`+KI | Layer B / pairing rules per host |
| EN `archviz`, `AI rendering`, skill terms | DISCOURSE-NOT-CONTROLLED or Layer B rules per host |
| FA `دانشجوی معماری` | Optional collocation — not required Layer A |
| FA `مهارت‌زدایی` | **GAP** (Braverman) — English `deskilling` in mixed FA scholarly queries |

---

## Layer model (discourse)

| Layer | EN role | Retrieval |
| --- | --- | --- |
| **A** | Architecture object **AND** GenAI | Required for neutral discovery |
| **B** | Deskilling, authorship, judgment, labour, professional identity | Second filter only — **must not select RQ1 sample** |

Construction/AEC adjacent terms and teammate hashtags (`constructionAI`, `GenAIandBuiltEnvironment`) stay **adjacent-AEC**, not Saintiment primary architecture frame.

---

## English (EN)

### Layer A — architecture + GenAI (controlled core)

Use pairs from [keyword-lexicon.md](keyword-lexicon.md) §1 and §2. Core lemmas:

- architect, architectural, architectural design, architecture firm, architecture student, architectural education, design studio, architectural practice, architecture practice
- generative AI, GenAI, Midjourney, ChatGPT, DALL-E, Stable Diffusion, text-to-image, LLM

### DISCOURSE-NOT-CONTROLLED — optional Layer A recall

High-recall platform terms; expand where useful:

| Term | Layer | Notes |
| --- | --- | --- |
| archviz | A (optional) | EN only — no FA/DE calque |
| AI rendering | A (optional) | Pair with architecture object |
| architectural visualization | A (optional) | US spelling variant |
| architectural visualisation | A (optional) | UK spelling variant |

### Not Layer A — optional Layer B only

Use **only if a sourced paper** employs the term in architectural GenAI discourse:

- design thinking
- computational design
- hand drawing

### Layer B — inside Layer A only

Deskilling, de-skilling, upskilling, reskilling, authorship, professional judgment, creativity, critical thinking, Urheberrecht (when DE cross-pass), competency / ARB outcomes language.

| Term | Layer | Notes |
| --- | --- | --- |
| skill loss | B | Plain-language variant — **not** Braverman's technical lemma |
| industry leader | — | **GAP** as controlled retrieval vocab — **code role after retrieval** (RQ4) |

Professional warrants: RIBA AI Report 2025; AIA AI Firm Toolkit; ARB competency outcomes; BAK KI FAQ; Braverman / SBTC as **Layer 2 labour lemmas only** (do not equate `skill loss` with Braverman deskilling).

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

| Lemma (Persian) | Transliteration | Source | Layer | Notes |
| --- | --- | --- | --- | --- |
| معمار / معماری | memar / memari | Farhangestan | A | Architecture / architect |
| مهندس معمار | mohandes-e memar | IRCEO (1374 Law) | A | Licensed architect engineer |
| رشته معمار | reshte-ye memari | IRCEO | A | Architecture discipline |
| دفتر مهندسی | daftar-e mohandesi | INBR | A | **INBR legal office term** — do **not** invent `دفتر معماری` as Nezam terminology |
| هوش مصنوعی مولد | hush-e masnui-ye movalled | Honar-ha-ye Ziba; IRCEO LMS 1180313 | A | Sourced — https://jfaup.ut.ac.ir/p_generative-ai ; syllabus `آشنایی با هوش مصنوعی مولد` — **not** Farhangestan-approved; **not** invented calque |
| پرامپت‌نویسی + ChatGPT | prompt-nevisi | IRCEO | A | Prompt-writing with ChatGPT |
| نویسندگی | nevisandegi | IRCEO / discourse | B | Writing / authorship |
| تفکر نقادانه | tafakkur-e naqqadane | Architecture education | B | Critical thinking |
| استودیو | ostudiyo | Studio context | A | Weak alone — pair with memari |
| دانشجوی معماری | daneshjoo-ye memari | Discourse collocation | A (optional) | **Not** Academy controlled vocab — do **not** require in Layer A |

### FA — GenAI lemma sources (`هوش مصنوعی مولد`)

Re-verified 2026-08-31. **Sourced professional/journal use** — do **not** claim Farhangestan or Academy *approval*:

- Honar-ha-ye Ziba (*Me'mari va Shahrsazi*): generative-AI policy page — heading and body use `هوش مصنوعی مولد` — https://jfaup.ut.ac.ir/p_generative-ai
- IRCEO LMS course 1180313 syllabus: `آشنایی با هوش مصنوعی مولد` — https://lmsiriceo.ir/course/show/470/d98d61b1b9f19d88849096542a221190 (same syllabus on Nezam Qom news 1796)

Later conservative pass marked **GAP** because it required Academy/INSO/Nezam *lemma* registration and missed journal/CPD *use*. **Host:** keep as sourced; conservative GAP rejected for this lemma.

### FA — BIM (both INSO wordings; not Layer A)

Keep **both** standards; neither is Layer A:

| Lemma (Persian) | Standard | Layer | Notes |
| --- | --- | --- | --- |
| مدلسازی اطلاعات ساخت | **INSO 23198-1** | — | **Not Layer A** |
| مدل سازی اطلاعات ساختمان | **INSO 12690-1** | — | **Not Layer A** — keep **both** wordings |

### FA — NOT approved / GAP

| Item | Status |
| --- | --- |
| hushvare / humas for GenAI | **NOT approved** (Mehr 1405) — do not retrieve |
| مهارت‌زدایی | **GAP** as Braverman deskilling equivalent — use **English** `deskilling` in mixed FA scholarly queries |
| deskilling (FA lemma) | **GAP** |
| hashtag set | **GAP** — do not invent |
| validated FA architecture sentiment dictionary | **GAP** |
| ISO 6707 FA | **GAP** |
| UNESCO FA architecture terms | **GAP** |
| `دفتر معماری` as Nezam terminology | **Do not invent** — use `دفتر مهندسی` (INBR) |

---

## German (DE) — sourced lemmas

**Separate pass** — require explicit `language: de`.

| Lemma | Source | Layer | Notes |
| --- | --- | --- | --- |
| Künstliche Intelligenz | Standard | A | AI |
| generative KI | Standard / BAK | A | GenAI |
| KI-Bildgeneratoren | BAK/AKNW | A | Image generators |
| Prompts | BAK | A | Prompt engineering |
| ChatGPT | Duden | A | Proper noun in Duden |
| Architekturbüro | Professional | A | Architecture office |
| Architektinnen und Architekten | Professional | A | Gender-inclusive profession |
| Architektenschaft | Professional | A | Profession collective |
| Planende | BAK | A | Planning professionals |
| Entwerfen | Design process | A | Designing |
| Gebäudevisualisierungen | BAK/AKNW | A | Building visualizations |
| Bauwerksinformationsmodellierung | DIN EN ISO 19650 | — | BIM — **not Layer A** unless paired with GenAI |

### DE — Layer B only

| Lemma | Source | Notes |
| --- | --- | --- |
| Deskilling (loanword) | Discourse | English loan |
| Dequalifizierung | Duden | **Layer B only** — host ruling |
| Kompetenzverlust | Duden | Skill loss |
| Urheberrecht | Legal | Copyright |
| Autorschaft | Legal/professional | Authorship |
| Verantwortung | Professional ethics | Responsibility |
| Berufsbild | Professional identity | Professional profile |

### DE — warnings

| Item | Rule |
| --- | --- |
| **Architektur** alone | Hits IT / software architecture — always **AND** with **KI** or **`Architekt*`** + exclusion set |
| **archviz** | Stay **EN**; no FA/DE calque |
| Dequalifizierung / deskilling lemmas | **Layer B only** — never sample selector |
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

- Two 03 drafts recorded; conflicts resolved per host — not silent merge
- Larbi (2026) methods unread — no import of their discourse lemmas
- Teammate LinkedIn 71/6173 unpublished
- FA `مهارت‌زدایی`, FA/DE hashtags, ISO 6707 FA/DE, UNESCO FA
- EN `industry leader` as controlled retrieval vocab
- No live platform query tests on 2026-08-31
- No validated FA/DE sentiment dictionaries for architecture discourse
