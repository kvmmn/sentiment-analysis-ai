# Keyword Source Identification — Teammates vs Published Analogues

Status: **identification record**, 2026-08-31. Compares teammate-described retrieval strings and sample claims with verified and closest published analogues. No corpus was scraped or collected for this record.

**Do not cite 71 opinions / 6173 words as published** until methods and counts are verified against a paper's full text. Teammate 71/6173 remains **unverified**.

**Record integrity:** **Both** Ghimire et al. (2024) **and** Larbi et al. (2026) stay in this file. Do not omit Larbi in later memos or summaries.

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
- **71/6173 must not be cited as published** — not confirmed against Larbi (2026) PDF or any other full text in hand.
- `#GenAIandBuiltEnvironment`: **no scholarly hit** found in identification pass.
- OpenAlex search for **6173 words** as a LinkedIn sample descriptor: **0** matching works.

---

## Ghimire, Kim and Acharya (2024) — verified related-work analogue

| Field | Record |
| --- | --- |
| Citation | Ghimire, S.; Kim, S.; Acharya, M. Generative AI in Construction: Exploring the Potentials and Limitations of ChatGPT. *Buildings* **2024**, *14*(1), 220. |
| DOI | [10.3390/buildings14010220](https://doi.org/10.3390/buildings14010220) |
| arXiv | [2310.04427](https://arxiv.org/abs/2310.04427) |
| PDF access | **In hand** via arXiv on research pass (MDPI publisher PDF returned HTTP 403 on same pass) |
| Platform | **LinkedIn — CONFIRMED** |
| Sample | **32 opinions / 63,778 words — CONFIRMED** |
| Population | Construction professionals |
| Published retrieval strings | `"Generative AI AND Construction"`; `"Generative AI"`; `"Large Language Models AND Construction"` (see [keyword-literature-strings.md](keyword-literature-strings.md) RW-GH-1–3) |
| Hashtags | `#generativai` (**misspelled**, confirmed in PDF); `#construction`; `#generativeai`; `#aec` |
| Window | To 20 Aug 2023 |

**Status:** Methods **CONFIRMED** from arXiv full text. Only **verified** LinkedIn *n* in this comparison set.

**Saintiment stance:** **Related-work analogue only** — construction-industry object. **Not** Saintiment Layer A (architectural discourse). Do not move Ghimire strings into S-A1 / W-A1.

---

## Larbi et al. (2026) — closest closed-OA built-environment + sentiment candidate

| Field | Record |
| --- | --- |
| Citation | Larbi, D.; et al. Title maps GenAI + built environment + sentiments + socioeconomic implications. *Technological Forecasting and Social Change* **2026**, *228*, 124689. |
| DOI | [10.1016/j.techfore.2026.124689](https://doi.org/10.1016/j.techfore.2026.124689) |
| Access | **Closed OA** — PDF **not in hand** on 2026-08-31 research pass |
| Sample | **71 opinions / 6173 words — UNVERIFIED** against this PDF (coincidence with teammate claim only; **not confirmed**) |
| Author post | Circumstantial **76% of 71** positive — **not** evidence of sample size or methods |
| Relation | Cites Ghimire (2024) |

**Status:** Remains the **closest closed-OA built-environment + sentiment candidate** in this identification set. Methods and sample counts **UNVERIFIED** until PDF access. **Keep in record** — do not drop when Ghimire is updated.

**Saintiment stance:** Even if 71/6173 were verified in Larbi, object is built environment + sentiment, not architectural discourse (Layer A). **Still do not cite 71/6173 as published** until verified against full text.

---

## Van Tam (2025) — adjacent review, not the 71-*n* paper

| Field | Record |
| --- | --- |
| Citation | Van Tam, et al. *Building and Environment* **2025**, *284*, 113526 |
| Access | **Exists; closed** on research pass |
| Topic | Construction / built environment GenAI review |
| Boolean string | **Not recovered** — full text blocked; do not invent |
| 71/6173 | **This paper is NOT the 71-*n* paper** |

---

## Xiong et al. (2026) — survey, not LinkedIn

| Field | Record |
| --- | --- |
| Venue | *Automation in Engineering Informatics* (AEI) **71**, 104392 |
| Sample | **n = 162** survey — **not** LinkedIn discourse |
| Note | Volume **71** is a bibliographic coincidence, not evidence for 71 opinions |

---

## Object difference table

| Dimension | Teammates (described) | Ghimire 2024 (confirmed) | Larbi 2026 (candidate) | Saintiment primary frame |
| --- | --- | --- | --- | --- |
| **Discourse object** | Construction / built environment | Construction professionals | Built environment + sentiments (title) | **Architectural discourse** |
| **Platform** | LinkedIn | LinkedIn (**confirmed**) | Unknown (PDF unread) | TBD — access not granted |
| **Sample size** | 71 opinions (unverified pub.) | **32 opinions** (**confirmed**) | 71/6173 (**unverified**) | **None collected** |
| **Word count** | 6173 words (unverified pub.) | **63,778 words** (**confirmed**) | Unverified | **None collected** |
| **GenAI scope** | GenAI in construction / BE | ChatGPT / GenAI construction | GenAI + BE + sentiment (title) | GenAI in **architecture** practice/education |
| **Literature filter** | Scopus 4-block + LIMIT-TO Engineering | Three construction strings (RW-GH) | Unknown | **S-A1 / W-A1** — no Engineering limit |
| **Deskilling / skills** | Not specified in excerpt | Limitations focus | Socioeconomic (title) | Layer B filter — not retrieval |
| **Hashtags** | GenAIandBuiltEnvironment, constructionAI, etc. | `#generativai` (misspelled), `#generativeai #aec` | Unknown | EN high-noise; FA/DE GAP |
| **PDF / methods** | Unpublished team description | arXiv PDF; methods **confirmed** | Closed OA; PDF unread; **keep in record** | Project record only |
| **Saintiment role** | Unpublished comparator | **Related-work only** — not Layer A | Closest BE+sentiment candidate | Layer A = S-A1 / W-A1 |

---

## Hashtag and metadata checks

| Query / tag | Scholarly hit | Notes |
| --- | --- | --- |
| `#GenAIandBuiltEnvironment` | **None** | No scholarly hit in identification pass |
| OpenAlex "6173 words" LinkedIn | **0 works** | Does not corroborate teammate count as published |
| `#generativai` (Ghimire) | In Ghimire 2024 PDF | **Misspelled** hashtag; confirmed |
| `#generativeai #aec` (Ghimire) | In Ghimire 2024 PDF | Verified construction discourse |

---

## Implications for Saintiment

1. **Do not cite 71/6173 as published.** Teammate claim unverified; Larbi PDF unread; Van Tam is **not** the 71-*n* paper.
2. **Ghimire 2024** — methods confirmed (LinkedIn; 32 / 63,778); **related-work analogue only**, not Layer A.
3. **Larbi 2026** — **retain** as closest closed-OA built-environment + sentiment candidate; 71/6173 **unverified** against PDF.
4. **Van Tam 2025** — exists, closed; Boolean not recovered; **not** the 71-*n* source.
5. **Teammate Scopus four-block + Engineering limit** informs related-work sensitivity, not primary RQ1 retrieval.
6. **Volume 71** in Xiong et al. (2026) AEI is unrelated to opinion counts.

---

## Gaps

- Larbi (2026) PDF unread — 71/6173 still **unverified** against that paper
- Teammate four-block Scopus string not deposited as a reproducible appendix
- Van Tam (2025) Boolean not recovered (full text blocked)
- MDPI Ghimire PDF HTTP 403 on research pass (methods read from arXiv instead)
- No independent replication of teammate LinkedIn sift; no scrape
