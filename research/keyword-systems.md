# Keyword Systems — Evaluation Map

Status: **working evaluation map**, 2026-08-31. This document records how Saintiment separates retrieval instruments, sampling layers, and coding lexicons. It is not permission to collect, not a frozen query version, and not a literature review.

## Purpose

Saintiment needs three keyword systems that must never be mixed:

| Instrument | Role | Primary file |
| --- | --- | --- |
| **Literature retrieval** | Find peer-reviewed and grey literature on GenAI in architectural discourse | [keyword-literature-strings.md](keyword-literature-strings.md) |
| **Discourse-retrieval catalog** | Platform search terms for permitted social/professional discourse (when access exists) | [keyword-discourse-catalog.md](keyword-discourse-catalog.md) |
| **Sentiment / stance coding lexicon** | Label emotions and stances *after* sampling | [keyword-lexicon.md](keyword-lexicon.md) (English tables preserved) |

Cross-links: [keyword-source-identification.md](keyword-source-identification.md) (teammate strings vs published analogues), [keywords-search-storage.md](keywords-search-storage.md) (scope and storage — still not a collection licence), [references.md](references.md) (verified bibliographic records).

---

## Host decisions (2026-08-31)

### 1. Three instruments, never mixed

Literature strings, discourse catalog, and sentiment/stance coding lexicon serve different stages. Do not paste discourse hashtags into Scopus, do not retrieve on sentiment lemmas, and do not treat literature `S-RW1` strings as the RQ1 primary sample frame.

### 2. Two layers — deskilling must not select the sample

| Layer | Content | Sampling role |
| --- | --- | --- |
| **Layer A** | Architecture discourse **and** GenAI | Defines the RQ1 sampling frame (neutral discovery) |
| **Layer B** | Skill, deskilling, authorship, judgment, labour | Second filter for RQ2–RQ4 and subgroup analysis |

**Rule:** Layer B must not be required at retrieval for RQ1. Requiring *deskilling* in Layer A would pre-select concern language and bias sentiment estimates.

Layer B labour lemmas (e.g. deskilling, dequalification) may inform coding and secondary filters only after Layer A establishes the architectural GenAI discourse set.

### 3. Construction / AEC / built environment — related work only

Strings for construction, AEC, AECO, built environment, BIM-only sociotechnical lifecycle talk belong in **related-work retrieval** (`S-RW1` and discourse adjacent-AEC terms), not in the primary RQ1 architecture frame. Saintiment's primary object is **architectural discourse**, not general construction-industry GenAI marketing.

### 4. Teammate 71 opinions / 6173 words — not published

Do **not** cite **71 opinions / 6173 words** as a published sample until a PDF is in hand and methods are verified. On 2026-08-31, an exact dual match of the teammates' Scopus four-block query **plus** the claimed LinkedIn *n* was **not** identified in open full text.

### 5. Verified analogue — Ghimire, Kim and Acharya (2024)

The only verified LinkedIn discourse study in this comparison set:

- **Ghimire, Kim and Acharya (2024)** *Buildings* 14(1):220, doi:[10.3390/buildings14010220](https://doi.org/10.3390/buildings14010220)
- **32 opinions / 63,778 words**; construction professionals; keywords *Generative AI in construction*; hashtags `#generativai #construction`, `#generativeai #aec`; window to 20 Aug 2023
- OA: [MDPI](https://www.mdpi.com/2075-5309/14/1/220), [arXiv:2310.04427](https://arxiv.org/abs/2310.04427)

See [keyword-source-identification.md](keyword-source-identification.md) for the object-difference table.

### 6. Closest object+sentiment paper — Larbi et al. (2026), methods unread

- **Larbi et al. (2026)** *Technological Forecasting and Social Change* 228:124689, doi:[10.1016/j.techfore.2026.124689](https://doi.org/10.1016/j.techfore.2026.124689)
- Title maps GenAI + built environment + sentiments + socioeconomic implications; **closed OA**; **71/6173 unverified**
- Author post claiming **76% positive** is **not** a sample-size claim
- Cites Ghimire (2024)

### 7. Primary literature strings — S-A1 (Scopus) and W-A1 (WoS)

- **S-A1** and **W-A1** are the primary architecture-discourse retrieval strings (copy-paste in [keyword-literature-strings.md](keyword-literature-strings.md))
- **No `LIMIT-TO Engineering`** on primary RQ1 strings
- **I-A1** (IEEE) and **G-A1a–c** (Google Scholar supplements) are secondary — IEEE is not the primary architecture database and has a 25-term clause limit
- **Live database counts were not run** on 2026-08-31

### 8. EN / FA / DE lists stay separate

English, Persian (Farsi), and German catalogues remain in separate passes with explicit language fields. Mark **GAP** where lemmas, hashtags, or validated sentiment dictionaries are missing. Do **not** invent translations or hashtags.

### 9. English lexicon tables preserved

Existing English tables in [keyword-lexicon.md](keyword-lexicon.md) are unchanged. This expansion adds **pointers only** at the top of that file.

### 10. Query version 1 is NOT frozen

Team review continues. Do not treat any string set as locked until explicitly versioned after review.

---

## Too-narrow patterns (do not use as RQ1 primary)

| Pattern | Why excluded from primary RQ1 |
| --- | --- |
| Requiring **deskilling** in Layer A | Pre-selects concern; violates neutral discovery |
| Requiring **sentiment** in title | Misses architectural GenAI discourse without affect in title |
| **`LIMIT-TO Engineering`** (Scopus) | Drops architectural and design literature outside Engineering subject area |
| **ANDing education/creativity at retrieval** | Too narrow for RQ1; usable only as A+B-soft sensitivity (cf. Stanimirovic 2026) |

---

## Literature warrants (cite as method precedents — not Saintiment results)

These sources inform search design; they are not evidence of Saintiment findings:

| Source | Relevance |
| --- | --- |
| Page et al. (2021) PRISMA elaboration item 7, doi:[10.1136/bmj.n160](https://doi.org/10.1136/bmj.n160) | Document search strategy |
| Booth (2008) successive fractions | Sensitivity analysis for string variants |
| Rethlefsen et al. (2021) PRISMA-S, doi:[10.31222/osf.io/7rgy3](https://doi.org/10.31222/osf.io/7rgy3) | Reporting search methods |
| McGowan et al. (2016) PRESS | Peer review of electronic search strategies |
| Chen et al. (2026) *Architecture* 6(2):60 | No subject-area restriction at search; their Stage-2 + umbrella AI is too broad/narrow for Saintiment |
| Stanimirovic (2026) | ANDs education/creativity at retrieval → A+B-soft sensitivity only |
| Yiannoudes (2025) | Full string upon request — do not invent |
| Memon et al. (2025) AECO | Related-work, not primary RQ1 |

Full records: [references.md](references.md).

---

## Professional warrants (discourse coding context — Layer 2)

| Source | Use |
| --- | --- |
| RIBA AI Report 2025 | Professional judgment + human creativity |
| AIA AI Firm Toolkit | Firm-level GenAI guidance |
| ARB competency outcomes | Regulatory skill framing |
| BAK KI FAQ | German chamber guidance on AI |
| Braverman / SBTC | Layer 2 labour lemmas only — not retrieval |

---

## Known gaps (2026-08-31)

- Larbi (2026) PDF unread; methods unverified
- Teammate four-block Scopus string unpublished; 71/6173 uncorroborated
- No live Scopus / WoS / IEEE / Scholar counts executed
- ISO 6707 FA/DE architecture terms not sourced here
- UNESCO FA architecture terminology not sourced here
- FA deskilling lemma — GAP
- FA/DE hashtag sets — GAP
- No validated FA/DE architecture sentiment dictionaries
- `#GenAIandBuiltEnvironment` — no scholarly hit; OpenAlex 6173 words = 0 (see source-identification note)

---

## File map

```
keyword-systems.md          ← this evaluation map (host decisions)
keyword-literature-strings.md   ← S-A1, W-A1, I-A1, S-RW1, Scholar supplements
keyword-discourse-catalog.md    ← EN/FA/DE discourse retrieval (not harvest plan)
keyword-source-identification.md ← teammate vs Ghimire vs Larbi vs Van Tam vs Xiong
keyword-lexicon.md          ← English coding tables (unchanged); sentiment NOT in retrieve
keywords-search-storage.md  ← scope, storage, layers (not collection licence)
```
