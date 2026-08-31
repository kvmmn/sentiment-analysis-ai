# Keyword Source Identification — Teammates vs Published Analogues

Status: **identification record**, 2026-08-31. Compares teammate-described retrieval strings and sample claims with verified and closest published analogues. No corpus was scraped or collected for this record.

**Do not cite 71 opinions / 6173 words as published** until a PDF is in hand and methods are verified.

Related: [keyword-systems.md](keyword-systems.md), [keyword-literature-strings.md](keyword-literature-strings.md), [keyword-discourse-catalog.md](keyword-discourse-catalog.md), [references.md](references.md).

---

## Teammates — described approach (unpublished)

As described in team discussion (not a published paper in this repository):

### Scopus four-block query (Engineering-limited)

Four AND blocks, with Scopus filters:

1. **GenAI block** — generative AI / GenAI / named tools / LLM terms
2. **Built environment / construction / AEC block**
3. **Sociotechnical / socioeconomic / lifecycle block**
4. **Impact block**

**Filters applied:** `LIMIT-TO Engineering`, Article, English.

**Saintiment stance:** this Engineering-limited, construction-centred four-block string is **related-work or sensitivity material**, not the primary RQ1 architecture frame. Primary strings are **S-A1** / **W-A1** in [keyword-literature-strings.md](keyword-literature-strings.md).

### LinkedIn discourse (claimed, unverified as publication)

| Element | Teammate description |
| --- | --- |
| Search phrases | *generative AI in construction*; *GenAI in construction*; *generative artificial intelligence in the built environment* |
| Hashtags | `GenAi`, `GenerativeAI`, `GenAIandBuiltEnvironment`, `constructionAI` |
| Claimed sample | **71 opinions / 6173 words** after sifting |
| Data basis | Public data; platform ToS; promo/low-authenticity screen |

**Verification status (2026-08-31):**

- Exact dual match of the Scopus four-block **plus** this LinkedIn *n* was **NOT** identified in open full text.
- **71/6173 must not be cited as published** until a PDF confirms methods and counts.
- `#GenAIandBuiltEnvironment`: **no scholarly hit** found in identification pass.
- OpenAlex search for **6173 words** as a LinkedIn sample descriptor: **0** matching works.

---

## Verified analogue — Ghimire, Kim and Acharya (2024)

| Field | Record |
| --- | --- |
| Citation | Ghimire, S.; Kim, S.; Acharya, M. Generative AI in Construction: Exploring the Potentials and Limitations of ChatGPT. *Buildings* **2024**, *14*(1), 220. |
| DOI | [10.3390/buildings14010220](https://doi.org/10.3390/buildings14010220) |
| OA | [MDPI 2075-5309/14/1/220](https://www.mdpi.com/2075-5309/14/1/220); [arXiv:2310.04427](https://arxiv.org/abs/2310.04427) |
| Platform | LinkedIn |
| Sample | **32 opinions / 63,778 words** |
| Population | Construction professionals |
| Keywords | *Generative AI in construction* |
| Hashtags | `#generativai #construction`; `#generativeai #aec` |
| Window | To 20 Aug 2023 |

**Status:** Only **verified** LinkedIn *n* in this comparison set (methods read from OA full text).

---

## Closest object + sentiment — Larbi et al. (2026)

| Field | Record |
| --- | --- |
| Citation | Larbi, D.; et al. (2026). Title maps GenAI + built environment + sentiments + socioeconomic implications. *Technological Forecasting and Social Change* **228**, 124689. |
| DOI | [10.1016/j.techfore.2026.124689](https://doi.org/10.1016/j.techfore.2026.124689) |
| Access | **Closed OA** — PDF not read in this project on 2026-08-31 |
| Sample | **71/6173 unverified** — coincidence with teammate claim; **not confirmed** |
| Author post | **76% positive** reported in author communication — **not** a sample-size claim |
| Relation | Cites Ghimire (2024) |

**Status:** Closest title-level match to GenAI + built environment + sentiment; **methods UNVERIFIED**.

---

## Other adjacent records

### Van Tam (2025) — construction / built environment review

| Field | Record |
| --- | --- |
| Venue | *Building and Environment* **284**, 113526 |
| Topic | Construction / built environment GenAI review |
| 71/6173 | **Not confirmed** in identification pass |

### Xiong et al. (2026) — survey, not LinkedIn

| Field | Record |
| --- | --- |
| Venue | *Automation in Engineering Informatics* (AEI) **71**, 104392 |
| Sample | **n = 162** survey — **not** LinkedIn discourse |
| Note | Volume **71** is a bibliographic coincidence, not evidence for 71 opinions |

---

## Object difference table

| Dimension | Teammates (described) | Ghimire 2024 (verified) | Larbi 2026 (unread) | Saintiment primary frame |
| --- | --- | --- | --- | --- |
| **Discourse object** | Construction / built environment | Construction professionals | Built environment + sentiments (title) | **Architectural discourse** |
| **Platform** | LinkedIn | LinkedIn | Unknown (methods unread) | TBD — access not granted |
| **Sample size** | 71 opinions (unverified pub.) | **32 opinions** (verified) | 71/6173 (unverified) | **None collected** |
| **Word count** | 6173 words (unverified pub.) | **63,778 words** (verified) | Unverified | **None collected** |
| **GenAI scope** | GenAI in construction / BE | ChatGPT / GenAI construction | GenAI + BE + sentiment (title) | GenAI in **architecture** practice/education |
| **Literature filter** | Scopus 4-block + LIMIT-TO Engineering | Not same string | Unknown | **S-A1 / W-A1** — no Engineering limit |
| **Deskilling / skills** | Not specified in excerpt | Limitations focus | Socioeconomic (title) | Layer B filter — not retrieval |
| **Hashtags** | GenAIandBuiltEnvironment, constructionAI, etc. | `#generativeai #aec` | Unknown | EN high-noise; FA/DE GAP |
| **Verification** | Unpublished team description | OA PDF + arXiv | Closed OA; PDF unread | Project record only |

---

## Hashtag and metadata checks

| Query / tag | Scholarly hit | Notes |
| --- | --- | --- |
| `#GenAIandBuiltEnvironment` | **None** | No scholarly hit in identification pass |
| OpenAlex "6173 words" LinkedIn | **0 works** | Does not corroborate teammate count as published |
| `#generativeai #aec` (Ghimire) | In Ghimire 2024 | Verified construction discourse |

---

## Implications for Saintiment

1. **Do not treat 71/6173 as a citable published sample** without Larbi PDF verification — and even then, Larbi's object is built environment, not architectural discourse.
2. **Ghimire 2024** is the defensible LinkedIn construction analogue; Saintiment's architecture focus requires **S-A1/W-A1** and the discourse catalog, not a construction-only clone.
3. **Teammate Scopus four-block + Engineering limit** informs related-work sensitivity, not primary RQ1 retrieval.
4. **Volume 71** in Xiong et al. (2026) AEI is unrelated to opinion counts.

---

## Gaps

- Larbi (2026) full text unread
- Teammate four-block Scopus string not deposited as a reproducible appendix
- Van Tam (2025) full string comparison not completed
- No independent replication of teammate LinkedIn sift on 2026-08-31
