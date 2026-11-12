# Literature strings

Generated 2026-11-12 from [`keyword-literature-strings.md`](keyword-literature-strings.md). Copy-paste strings and the tables already in that file. No string was added. Live hit counts were not run in the source.

## Paste strings

### S-A1 — Scopus (primary)

```text
TITLE-ABS-KEY( ( architect OR architectural OR "architecture firm" OR "architecture student" OR "architectural education" OR "architectural design" OR "design studio" OR "architectural practice" OR "architecture practice" OR archviz ) AND ( "generative AI" OR GenAI OR "generative artificial intelligence" OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "DALL-E 2" OR "DALL-E 3" OR "Stable Diffusion" OR "text-to-image" OR "text to image" OR "large language model" OR "large language models" OR LLM ) ) AND NOT TITLE-ABS-KEY( "software architect" OR "software architecture" OR "solutions architect" OR "enterprise architecture" OR "cloud architect" OR "computer architecture" OR "IT architect" OR "data architect" OR "network architect" OR "security architect" OR "systems architect" )
```

### W-A1 — Web of Science (primary)

```text
TS=( ( architect OR architectural OR "architecture firm" OR "architecture student" OR "architectural education" OR "architectural design" OR "design studio" OR "architectural practice" OR "architecture practice" OR archviz ) AND ( "generative AI" OR GenAI OR "generative artificial intelligence" OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "DALL-E 2" OR "DALL-E 3" OR "Stable Diffusion" OR "text-to-image" OR "text to image" OR "large language model" OR "large language models" OR LLM ) ) NOT TS=( "software architect" OR "software architecture" OR "solutions architect" OR "enterprise architecture" OR "cloud architect" OR "computer architecture" OR "IT architect" OR "data architect" OR "network architect" OR "security architect" OR "systems architect" )
```

### I-A1 — IEEE Xplore (25-term limit per clause; not primary architecture database)

```text
("architectural design" OR "architectural education" OR architect OR archviz) AND ("generative AI" OR GenAI OR Midjourney OR ChatGPT OR "Stable Diffusion" OR "text-to-image") NOT ("software architect" OR "software architecture" OR "computer architecture" OR "enterprise architecture")
```

### G-A1a — core architecture + GenAI

```text
(architect OR architectural OR "architectural design" OR archviz) ("generative AI" OR GenAI OR Midjourney OR ChatGPT) -"software architect" -"software architecture" -"enterprise architecture"
```

### G-A1b — education + studio

```text
("architecture student" OR "design studio" OR "architectural education") (GenAI OR "generative AI" OR "Stable Diffusion" OR "text-to-image")
```

### G-A1c — practice

```text
("architecture firm" OR "architectural practice" OR "architecture practice") ("generative AI" OR ChatGPT OR Midjourney OR "AI rendering")
```

### S-RW1 — Scopus

```text
TITLE-ABS-KEY( ("built environment" OR AEC OR AECO OR construction OR "construction industry" OR BIM OR sociotechnical OR "socio-technical") AND ("generative AI" OR GenAI OR ChatGPT OR LLM) )
```

### Layer B — post-retrieval or secondary filter (literature)

```text
AND ( deskilling OR de-skilling OR dequalification OR "skill loss" OR authorship OR "professional judgment" OR Urheberrecht OR "critical thinking" )
```

## Related-work published strings

| String ID | Published string | Label |
| --- | --- | --- |
| RW-GH-1 | `"Generative AI AND Construction"` | **RELATED-WORK only** |
| RW-GH-2 | `"Generative AI"` | **RELATED-WORK only** (over-broad alone; Ghimire paired with construction context) |
| RW-GH-3 | `"Large Language Models AND Construction"` | **RELATED-WORK only** |

## Scopus ASJC subject areas

| ASJC code | Subject area |
| --- | --- |
| 2216 | Architecture |
| 3304 | Education |
| 3322 | Urban Studies |
| 1709 | Human–Computer Interaction |
| ENGI | Engineering — **one member of the union only** |

## Too-narrow variants

| Variant | Pattern | Label |
| --- | --- | --- |
| Deskilling in A | Add deskilling/de-skilling to Layer A AND | **TOO-NARROW for RQ1 primary** |
| Deskilling AND into A | Require deskilling terms inside Layer A boolean | **TOO-NARROW for RQ1 primary** |
| Sentiment in title | `TITLE(sentiment*)` or require sentiment in TITLE | **TOO-NARROW for RQ1 primary** |
| Engineering limit | `LIMIT-TO Engineering` on Scopus (sole filter) | **TOO-NARROW / wrong subject scope** |
| Education ∧ creativity | AND education AND creativity at retrieval (Stanimirovic 2026 pattern) | **A+B-soft sensitivity only** |
