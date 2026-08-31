# Keyword Literature Strings — Copy-Paste Protocol

Status: **working retrieval protocol v0**, 2026-08-31. Copy-paste strings for literature databases. **Query version 1 is NOT frozen.** Live hit counts were **not** run on 2026-08-31.

**Instrument:** literature retrieval only — not discourse harvest, not sentiment coding.

Host decisions: [keyword-systems.md](keyword-systems.md). Warrants: [references.md](references.md).

---

## Primary RQ1 strings (architecture + GenAI)

### S-A1 — Scopus (primary)

Paste exactly:

```text
TITLE-ABS-KEY( ( architect OR architectural OR "architecture firm" OR "architecture student" OR "architectural education" OR "architectural design" OR "design studio" OR "architectural practice" OR "architecture practice" OR archviz ) AND ( "generative AI" OR GenAI OR "generative artificial intelligence" OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "DALL-E 2" OR "DALL-E 3" OR "Stable Diffusion" OR "text-to-image" OR "text to image" OR "large language model" OR "large language models" OR LLM ) ) AND NOT TITLE-ABS-KEY( "software architect" OR "software architecture" OR "solutions architect" OR "enterprise architecture" OR "cloud architect" OR "computer architecture" OR "IT architect" OR "data architect" OR "network architect" OR "security architect" OR "systems architect" )
```

**Scopus syntax notes (2026):**

- Place **`AND NOT` at the end** of the query.
- **Always parenthesize** boolean groups (2026 precedence change).

**Do not add:** `LIMIT-TO Engineering` on this primary string. See [Subject areas](#subject-areas-scopus-asjc) below.

### W-A1 — Web of Science (primary)

Same logic as S-A1 with WoS field tags:

```text
TS=( ( architect OR architectural OR "architecture firm" OR "architecture student" OR "architectural education" OR "architectural design" OR "design studio" OR "architectural practice" OR "architecture practice" OR archviz ) AND ( "generative AI" OR GenAI OR "generative artificial intelligence" OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "DALL-E 2" OR "DALL-E 3" OR "Stable Diffusion" OR "text-to-image" OR "text to image" OR "large language model" OR "large language models" OR LLM ) ) NOT TS=( "software architect" OR "software architecture" OR "solutions architect" OR "enterprise architecture" OR "cloud architect" OR "computer architecture" OR "IT architect" OR "data architect" OR "network architect" OR "security architect" OR "systems architect" )
```

---

## Supplement strings (not primary architecture DB)

### I-A1 — IEEE Xplore (25-term limit per clause; not primary architecture database)

```text
("architectural design" OR "architectural education" OR architect OR archviz) AND ("generative AI" OR GenAI OR Midjourney OR ChatGPT OR "Stable Diffusion" OR "text-to-image") NOT ("software architect" OR "software architecture" OR "computer architecture" OR "enterprise architecture")
```

**Limitation:** IEEE clause term caps require shorter strings than S-A1. Treat as **supplement**, not primary frame.

### G-A1a–c — Google Scholar (supplements; do not paste S-A1 wholesale)

Scholar does not accept one Scopus-length string reliably. Use **several short queries**, **uppercase OR**, and **minus exclusions**:

**G-A1a — core architecture + GenAI**

```text
(architect OR architectural OR "architectural design" OR archviz) ("generative AI" OR GenAI OR Midjourney OR ChatGPT) -"software architect" -"software architecture" -"enterprise architecture"
```

**G-A1b — education + studio**

```text
("architecture student" OR "design studio" OR "architectural education") (GenAI OR "generative AI" OR "Stable Diffusion" OR "text-to-image")
```

**G-A1c — practice**

```text
("architecture firm" OR "architectural practice" OR "architecture practice") ("generative AI" OR ChatGPT OR Midjourney OR "AI rendering")
```

Record which G-A1 variant produced each hit (PRISMA-S reporting).

---

## Related-work only — S-RW1 (construction / AEC / sociotechnical)

**Not RQ1 primary.** Use for adjacent literature and sensitivity comparisons (teammate four-block, Memon et al. 2025 AECO, etc.). **Do not move these strings into S-A1 / W-A1 (Layer A).**

### S-RW1 — Scopus

```text
TITLE-ABS-KEY( ("built environment" OR AEC OR AECO OR construction OR "construction industry" OR BIM OR sociotechnical OR "socio-technical") AND ("generative AI" OR GenAI OR ChatGPT OR LLM) )
```

### Ghimire 2024 — published construction strings (related-work only)

Source: Ghimire, Kim and Acharya (2024), [arXiv:2310.04427](https://arxiv.org/abs/2310.04427) / *Buildings* 14(1):220, [doi:10.3390/buildings14010220](https://doi.org/10.3390/buildings14010220). Verified LinkedIn discourse study (32 opinions / 63,778 words). These are **construction-industry retrieval strings from that paper** — label **RELATED-WORK**, not Layer A:

| String ID | Published string | Label |
| --- | --- | --- |
| RW-GH-1 | `"Generative AI AND Construction"` | **RELATED-WORK only** |
| RW-GH-2 | `"Generative AI"` | **RELATED-WORK only** (over-broad alone; Ghimire paired with construction context) |
| RW-GH-3 | `"Large Language Models AND Construction"` | **RELATED-WORK only** |

Use for comparator / related-work passes alongside `S-RW1`. **Do not** fold into `S-A1` or `W-A1`.

### Van Tam 2025 — Boolean not recovered

Van Tam et al. (2025), *Building and Environment* 284:113526 — construction / built-environment GenAI review. **Boolean search string was not recovered** (full text blocked on 2026-08-31). **Do not invent it.** Mark TODO until PDF access.

---

## Subject areas (Scopus ASJC)

**Do not `LIMIT-TO Engineering` alone** on primary RQ1 strings — drops architectural and design literature outside Engineering.

If a subject-area refine is required, use a **union**, with Engineering only as one member — **never the sole filter**:

| ASJC code | Subject area |
| --- | --- |
| 2216 | Architecture |
| 3304 | Education |
| 3322 | Urban Studies |
| 1709 | Human–Computer Interaction |
| ENGI | Engineering — **one member of the union only** |

Example refine intent (adapt syntax to Scopus UI at run time): union of 2216 + 3304 + 3322 + 1709 + ENGI. **Not** Engineering alone.

---

## Too-narrow — sensitivity only (not primary RQ1)

Use only in **successive-fractions** or sensitivity passes (Booth 2008; see [keyword-systems.md](keyword-systems.md)):

| Variant | Pattern | Label |
| --- | --- | --- |
| Deskilling in A | Add deskilling/de-skilling to Layer A AND | **TOO-NARROW for RQ1 primary** |
| Deskilling AND into A | Require deskilling terms inside Layer A boolean | **TOO-NARROW for RQ1 primary** |
| Sentiment in title | `TITLE(sentiment*)` or require sentiment in TITLE | **TOO-NARROW for RQ1 primary** |
| Engineering limit | `LIMIT-TO Engineering` on Scopus (sole filter) | **TOO-NARROW / wrong subject scope** |
| Education ∧ creativity | AND education AND creativity at retrieval (Stanimirovic 2026 pattern) | **A+B-soft sensitivity only** |

`TITLE(sentiment*)` and deskilling-AND-into-A remain **too-narrow for RQ1** — keep labelled here; do not adopt as primary sample frame.

---

## Layer B — post-retrieval or secondary filter (literature)

For skill/deskilling/authorship/judgement sub-questions, apply **after** Layer A hits are identified — mirror discourse Layer B in [keyword-discourse-catalog.md](keyword-discourse-catalog.md).

Example secondary AND (not for RQ1 sample definition):

```text
AND ( deskilling OR de-skilling OR dequalification OR "skill loss" OR authorship OR "professional judgment" OR Urheberrecht OR "critical thinking" )
```

---

## Execution checklist (when team runs searches)

- [ ] Record database, date, string ID (S-A1, W-A1, …), and result count
- [ ] Export RIS/BibTeX with query note in research log
- [ ] Do **not** report counts from this file without a dated run
- [ ] Peer-review strategy with PRESS (McGowan et al. 2016) before locking any version
- [ ] Document deviations in [project-log.md](project-log.md)

---

## Gaps

- Live Scopus / WoS / IEEE / Scholar counts: **not run** (2026-08-31)
- Yiannoudes (2025) full string: **upon request** — not invented here
- Van Tam (2025) Boolean: **not recovered** — full text blocked; do not invent
- WoS `W-RW1` mirror of S-RW1: TODO if team adopts WoS for related-work pass
