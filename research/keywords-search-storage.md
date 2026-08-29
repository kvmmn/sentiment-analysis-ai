# Keywords, Search Scope, and Storage

Status: **working proposal for team review**, drafted 2026-08-29. This answers the Telegram-group questions about search terms, search limits, and how to store posts and comments. It is not a finalized protocol, a literature-validated lexicon, or permission to collect.

**Printable lexicon:** [keyword-lexicon.pdf](keyword-lexicon.pdf) — minimal black-on-white PDF (one category per page; essential terms highlighted). Regenerate with `python3 scripts/generate_keyword_lexicon_pdf.py` after `pip install reportlab`.

No corpus has been collected. Do not start harvesting from LinkedIn, X, or other platforms on the basis of this list. The [LinkedIn case](linkedin-application-worksheet.md) is still **Open**; ordinary visibility of a post is not a licence to retain it.

Related records: [research notes](notes.md), [access review](linkedin-data-access-review.md), [privacy policy](../PRIVACY.md), [data guide](../data/README.md).

## Answers for the group

**What are the keywords?** Use two layers. Layer A finds architecture + generative-AI discussion without requiring the word *deskilling*. Layer B then searches skill, labour, and method terms inside that discussion. Searching only for deskilling would measure concern that the query itself selected. The inventory below is a seed lexicon, not a claim that every term will retrieve relevant items.

**How far should we search?** Decide limits *before* collection: one permitted source at a time; English first; a time window starting with the public generative-AI discourse (proposed: 30 November 2022 onward); posts as the primary unit, with comments stored as related records; a small relevance pilot before any large pull. Geography, Persian/German, and later platforms remain open. Exact LinkedIn query syntax, historical depth, and comment access are still unverified.

**How should we store posts and comments?** Local, access-limited files in `data/` (already gitignored), one JSONL record per item, with a batch manifest. Keep posts, comments, and replies as separate records linked by IDs. Do not put raw text in GitHub or Telegram. Retention must follow the *permitted* source terms, not only the three-month storage answer on the LinkedIn form.

## Search design

These rules come from the existing research questions and the [pipeline notes](linkedin-data-access-review.md). They are design constraints, not implemented filters.

1. **Require architectural context.** Alone, *architecture*, *BIM*, *rendering*, and *GenAI* retrieve software-architecture, construction-software marketing, and general AI chatter.
2. **Keep a neutral discovery set.** Layer A must be runnable without Layer B so RQ1 is not pre-loaded with anxiety language.
3. **Do not search sentiment words.** *Excited*, *terrified*, *hype*, and *threat* belong in later coding, not in the retrieval query.
4. **Record the query with every item.** Retrieval bias is part of the method. A later reader must see which string produced the hit.
5. **Treat languages as separate passes.** Mixing English, Persian, and German hits without a language field makes RQ4 and prevalence claims uninterpretable.
6. **Exclude by documented rules**, not by deleting inconvenient posts. Software-architect hits are expected; log them as `exclude`.

### Proposed query logic

Write queries as: **(architecture context) AND (generative-AI cue) AND optional (skill cue) AND NOT (exclusion)**.

Until a platform's operators are known, treat the boolean sketches below as planning language, not copy-paste search boxes. LinkedIn, X, ResearchGate, and YouTube do not share one syntax.

## Keyword inventory

Terms are seeds for team editing. Tool names are included because practitioners often name products instead of saying *generative AI*. Inclusion of a product is not an endorsement or a claim that the product caused deskilling.

**Use codes**

| Code | Meaning |
| --- | --- |
| A | Architecture / built-environment context |
| G | Generative AI, models, or architecture-facing AI tools |
| S | Skill, labour, profession, deskilling |
| K | Soft skills, creativity, judgment |
| H | Hard / technical / environmental skills |
| R | Representation, drawing, digital, computational |
| W | Stakeholder / role vocabulary |
| X | Exclusion / false-positive control |
| EN / FA / DE | English / Persian / German |

RQ tags are *intended use*, not evidence that the term measures that question.

### Layer A — architecture context (EN)

| Term | Notes |
| --- | --- |
| architect | High-value; still collides with *software architect* |
| architects | Plural professional talk |
| architectural | Safer than bare *architecture* |
| architectural design | |
| architectural practice | |
| architectural education | RQ4 / schools |
| architectural discourse | Rare in posts; useful in papers |
| architecture firm | |
| architecture studio | Also art-studio noise |
| architecture school | |
| architecture student | RQ4 |
| architecture office | |
| licensed architect | |
| registered architect | |
| architect of record | |
| junior architect | Labour / pipeline |
| intern architect | |
| associate architect | |
| principal architect | RQ4 |
| design principal | |
| starchitect | Rhetorical; small volume |
| AIA | US professional body; acronym collisions |
| RIBA | UK; also the institute's own content |
| RAIA / Australian Institute of Architects | Regional |
| NAAB | Education accreditation |
| built environment | Broader than architecture |
| building design | Construction-industry bleed |
| urban design | Planning bleed |
| urbanism | |
| landscape architecture | Keep only if the team includes it |
| interior architecture | Same |
| schematic design | Practice-stage language |
| design development | |
| construction documentation | |
| construction administration | |
| design studio | Education |
| studio culture | |
| design crit | |
| design jury | |
| Part 1 architect | UK pathway |
| Part 2 architect | |
| Part 3 architect | |
| architectural visualization | Also *archviz* |
| archviz | Common hashtag |
| architectural rendering | |
| facade / façade | Weak alone |
| building envelope | Technical discourse |
| massing | |
| floor plan | Weak alone |
| concept design | |
| conceptual design | Overlaps RQ2a |

### Layer A — generative AI and named tools (EN)

| Term | Notes |
| --- | --- |
| generative AI | Preferred phrase |
| GenAI | |
| gen AI | Spacing variant |
| generative artificial intelligence | Formal |
| AI-generated | Hyphen variants |
| AI generated | |
| text-to-image | |
| text to image | |
| image generation | Broad |
| AI rendering | Architecture-relevant |
| AI visualization / visualisation | |
| AI-assisted design | |
| AI-aided design | |
| AI design | Very broad |
| large language model | |
| LLM | Acronym collisions |
| prompt | Weak alone |
| prompting | |
| prompt engineering | |
| ChatGPT | High volume; needs architecture AND |
| GPT | Too short alone |
| OpenAI | |
| Claude | Name collisions |
| Gemini | Name collisions |
| Copilot | Software and Microsoft bleed |
| Midjourney | Strong architecture-visual hit rate expected |
| DALL-E / DALL·E / Dall-E | Spelling variants |
| Stable Diffusion | |
| Flux | Name collisions |
| Adobe Firefly | |
| Leonardo AI | |
| Ideogram | |
| ComfyUI | Practitioner/tooling talk |
| diffusion model | |
| LookX | Architecture-facing tool; verify current name before use |
| Veras | |
| Finch / Finch3D | Name collisions |
| TestFit | |
| Spacemaker | Now often discussed as Autodesk Forma |
| Autodesk Forma | |
| Forma | Weak alone |
| Maket / Maket.ai | |
| Hypar | |
| Snaptrude | |
| Visoid | |
| Runway | Video/tooling bleed |
| Sora | Video; optional |
| Revit AI | Pair with Revit |
| Rhino AI | |
| Grasshopper AI | |
| generative design | **Older CAD/optimization sense**; tag separately from GenAI |

### Layer B — deskilling, labour, profession (EN)

Use only *with* Layer A, or as a second filter on an already retrieved architecture+GenAI set.

| Term | RQ | Notes |
| --- | --- | --- |
| deskilling | RQ1, RQ4 | Core; spelling *de-skilling*, *de skilling* |
| skill loss | RQ1 | |
| skill erosion | RQ1 | |
| skill atrophy | RQ1 | |
| losing skills | RQ1 | |
| lost skills | RQ1 | |
| dumbing down | RQ1 | Informal |
| replace architects | RQ1, RQ4 | |
| replacing architects | RQ1 | |
| architect replacement | RQ1 | |
| automate architecture | RQ1 | |
| automated design | RQ1, RQ3 | |
| automation of design | RQ1 | |
| job displacement | RQ1, RQ4 | |
| job loss | RQ4 | Very broad |
| junior pipeline | RQ4 | |
| training pipeline | RQ4 | |
| apprenticeship | RQ4 | |
| fewer juniors | RQ4 | |
| craft | RQ2, RQ3 | Ambiguous |
| craftsmanship | RQ2, RQ3 | |
| tacit knowledge | RQ2b | |
| professional expertise | RQ2b | |
| commoditization / commodification | RQ1 | |
| obsolescence | RQ1 | |
| obsolete skills | RQ1 | |
| reskilling | RQ1 | Opposite pole; keep |
| upskilling | RQ1 | |
| skill shift | RQ1 | |
| skill transformation | RQ1 | |
| new skills | RQ1 | Weak |
| future of the profession | RQ1, RQ4 | |
| future of architecture | RQ1 | Grandiose; noisy |
| future of architects | RQ1 | |
| AI will replace | RQ1 | Stance cue in text, not a retrieval-only term |
| human in the loop | RQ2b | |
| cheaper design | RQ1 | |
| faster cheaper | RQ1 | |

### Layer B — soft skills and judgment (EN)

| Term | RQ | Notes |
| --- | --- | --- |
| soft skills | RQ2 | |
| creativity | RQ2a | Very common; needs Layer A+G |
| creative thinking | RQ2a | |
| design thinking | RQ2a | Management-speak bleed |
| originality | RQ2a | |
| authorship | RQ2a | |
| authorial | RQ2a | |
| imagination | RQ2a | |
| artistic | RQ2a | |
| aesthetic | RQ2a | |
| taste | RQ2a, RQ2b | |
| conceptual thinking | RQ2a | |
| idea generation | RQ2a | |
| storytelling | RQ2 | |
| narrative | RQ2 | Weak |
| client communication | RQ2 | |
| presentation skills | RQ2 | |
| collaboration | RQ2 | Weak |
| empathy | RQ2 | |
| judgment / judgement | RQ2b | Both spellings |
| professional judgment | RQ2b | |
| design judgment | RQ2b | |
| critical thinking | RQ2b | |
| critical judgment | RQ2b | |
| decision-making | RQ2b | |
| design intuition | RQ2b | |
| intuition | RQ2b | Weak |
| expertise | RQ2b | |
| cognitive skills | RQ2b | Rare in posts |
| spatial reasoning | RQ2b | |
| discernment | RQ2b | |
| problem-solving | RQ2b | Weak |

### Layer B — hard / technical / environmental (EN)

| Term | RQ | Notes |
| --- | --- | --- |
| hard skills | RQ3 | |
| technical skills | RQ3, RQ3a | |
| technical knowledge | RQ3a | |
| environmental design | RQ3a | |
| environmental performance | RQ3a | |
| building performance | RQ3a | |
| building science | RQ3a | |
| energy modeling / modelling | RQ3a | |
| daylighting | RQ3a | |
| thermal comfort | RQ3a | |
| passive design | RQ3a | |
| sustainability | RQ3a | Very broad |
| carbon | RQ3a | Weak alone |
| life-cycle / LCA | RQ3a | |
| building codes | RQ3a | |
| building regulations | RQ3a | |
| zoning | RQ3a | Planning bleed |
| code compliance | RQ3a | |
| fire safety | RQ3a | |
| accessibility | RQ3a | Broad |
| structural design | RQ3a | Engineering bleed |
| MEP | RQ3a | |
| detailing | RQ3, RQ3b | |
| construction detailing | RQ3a | |
| construction knowledge | RQ3a | |
| buildability | RQ3a | |
| materials knowledge | RQ3a | |
| specification / specifications | RQ3a | |
| technical drawing | RQ3b | |
| working drawings | RQ3b | |

### Layer B — representation and digital practice (EN)

| Term | RQ | Notes |
| --- | --- | --- |
| representation | RQ3b | Philosophical bleed |
| architectural representation | RQ3b | |
| drawing | RQ3b | Weak alone |
| hand drawing | RQ3b | |
| drafting / draughting | RQ3b | |
| CAD | RQ3b | |
| BIM | RQ3b | Huge non-GenAI corpus |
| Revit | RQ3b | |
| AutoCAD | RQ3b | |
| Rhino / Rhinoceros | RQ3b | |
| Grasshopper | RQ3b | Insect collisions if unanchored |
| SketchUp | RQ3b | |
| ArchiCAD | RQ3b | |
| Vectorworks | RQ3b | |
| Lumion | RQ3b | |
| Enscape | RQ3b | |
| V-Ray | RQ3b | |
| Twinmotion | RQ3b | |
| Unreal Engine | RQ3b | Games bleed |
| rendering | RQ3b | |
| visualization / visualisation | RQ3b | |
| 3D modeling / modelling | RQ3b | |
| computational design | RQ3b | |
| parametric design | RQ3b | Pre-GenAI tradition |
| algorithmic design | RQ3b | |
| digital skills | RQ3b | |
| scripting | RQ3b | Software bleed |
| visual programming | RQ3b | |
| digital fabrication | RQ3b | Optional scope |
| Photoshop | RQ3b | Weak |
| post-production | RQ3b | |
| collage | RQ3b | |
| diagram | RQ3b | Weak |
| section / elevation / perspective | RQ3b | Weak alone |

### Stakeholder vocabulary (EN)

For RQ4 retrieval and later coding. Do **not** infer role from a name or photo. Prefer self-identification in the text or a consented profile field.

| Term | Group hint |
| --- | --- |
| practitioner | practitioner |
| practicing / practising architect | practitioner |
| professional practice | practitioner |
| academic | academic |
| professor | academic |
| lecturer | academic |
| educator | academic |
| faculty | academic |
| architecture researcher | academic |
| student | student |
| architecture student | student |
| graduate student | student |
| intern | student / early career |
| year-out | student (UK) |
| industry leader | industry leader |
| thought leader | weak / marketing |
| principal | industry leader / practice |
| partner | practice |
| director | practice |
| practice director | practice |
| firm owner | practice |
| Dean / head of school | academic |
| developer | adjacent; usually not RQ4 as written |
| client | adjacent |
| critic | adjacent |

### Exclusion and control terms (EN)

Log matches; do not silently drop them from the raw batch if the platform returned them. Mark `relevance_status: exclude`.

| Term or pattern | Why |
| --- | --- |
| software architect | IT role |
| solutions architect / solution architect | IT role |
| enterprise architect / enterprise architecture | IT |
| cloud architect | IT |
| data architect | IT |
| information architect | UX / IT |
| security architect | IT |
| systems architect | IT |
| IT architect | IT |
| TOGAF / Zachman | Enterprise-architecture frameworks |
| computer architecture / CPU architecture / chip architecture | Hardware |
| instruction set | Hardware |
| microservices | Software |
| naval architect | Different profession |
| GitHub Copilot | Usually software engineering |

### Persian seed terms (FA) — optional second pass

Prepared because the team discusses in Persian and Iranian architectural discourse may matter. **Not selected.** Do not mix into the English corpus without a `language` field.

| Term | Family | Notes |
| --- | --- | --- |
| معماری | A | Also metaphorical |
| معمار | A | |
| معماران | A | |
| طراحی معماری | A | |
| دفتر معماری | A | |
| آموزش معماری | A | |
| دانشجوی معماری | W | |
| آتلیه معماری | A | |
| رندر معماری | R | |
| ویژوالایز | R | Loanword |
| هوش مصنوعی مولد | G | Closest to generative AI |
| هوش مصنوعی | G | Too broad alone |
| هوش مصنوعی در معماری | G+A | Strong pair |
| طراحی با هوش مصنوعی | G | |
| رندر با هوش مصنوعی | G+R | |
| میدجرنی | G | Midjourney |
| چت‌جی‌پی‌تی / چت جی پی تی | G | ChatGPT |
| مهارت‌زدایی | S | Common academic rendering of deskilling |
| کاهش مهارت | S | |
| از دست رفتن مهارت | S | |
| زوال مهارت | S | |
| جایگزینی معمار | S | |
| بیکاری معماران | S | |
| اتوماسیون طراحی | S | |
| مهارت نرم | K | |
| خلاقیت | K | |
| تفکر طراحی | K | |
| قضاوت حرفه‌ای | K | |
| سلیقه | K | |
| مهارت سخت | H | |
| مهارت فنی | H | |
| طراحی محیطی | H | |
| دانش ساخت | H | |
| جزئیات اجرایی | H | |
| مقررات ملی ساختمان | H | Iran-specific |
| ترسیم | R | |
| دست‌رسمی / اسکیس | R | |
| نقشه‌کشی | R | |
| مدل‌سازی | R | |
| بیم / BIM | R | |
| طراحی پارامتریک | R | |
| طراحی محاسباتی | R | |
| حرفه‌مند | W | |
| حرفه‌ای | W | Weak |
| دانشگاهی / آکادمیک | W | |
| دانشجو | W | |
| مدیر دفتر | W | |
| کارفرما | W | Adjacent |

### German seed terms (DE) — optional second pass

Prepared because storage was declared in Germany and Berlin campus affiliation is on the application. **Not selected.**

| Term | Family | Notes |
| --- | --- | --- |
| Architektur | A | |
| Architekt / Architektin / Architekten | A | |
| Architekturbüro | A | |
| Architekturstudium | A, W | |
| generative KI | G | |
| Künstliche Intelligenz | G | Broad |
| KI-generiert | G | |
| Midjourney | G | Same token |
| Dequalifizierung | S | Usual German for deskilling |
| Entqualifizierung | S | Less common variant |
| Kompetenzverlust | S | |
| Kreativität | K | |
| Design Thinking | K | Loan |
| Urteilsvermögen | K | |
| fachliches Urteil | K | |
| technische Fähigkeiten | H | |
| umweltgerechtes Entwerfen | H | |
| Darstellung | R | |
| Visualisierung | R | |
| Handzeichnung | R | |
| BIM | R | |

## Example query sketches

These are planning strings. Adapt operators to the permitted interface.

**A1 — neutral discovery (preferred first pilot)**

```text
(architect OR architectural OR "architecture firm" OR "architecture student" OR archviz)
AND ("generative AI" OR GenAI OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "Stable Diffusion")
NOT ("software architect" OR "solutions architect" OR "enterprise architecture" OR "cloud architect")
```

**A2 — tool-heavy visual practice**

```text
(architect OR architectural OR archviz)
AND (Midjourney OR LookX OR Veras OR "Autodesk Forma" OR Firefly)
```

**B1 — deskilling inside the topic**

```text
A1 AND (deskilling OR "de-skilling" OR "skill loss" OR "replace architects" OR upskilling OR reskilling)
```

**B2 — soft skills**

```text
A1 AND (creativity OR "design thinking" OR authorship OR "professional judgment" OR judgement)
```

**B3 — hard / environmental**

```text
A1 AND ("technical skills" OR "environmental design" OR "building performance" OR "energy modeling" OR detailing)
```

**B4 — representation / digital**

```text
A1 AND (rendering OR BIM OR Revit OR "computational design" OR "hand drawing" OR "parametric design")
```

**Hashtag-only (X / Instagram-style surfaces; high noise)**

`#architecture` `#Midjourney` `#AIarchitecture` `#ArchViz` `#GenerativeAI` `#LookX` — always combine with a human relevance pass.

## Search scope

All rows are **proposals**. The team should accept, change, or defer each line. Nothing below authorises collection.

| Dimension | Proposed first pass | Why this default | Still open |
| --- | --- | --- | --- |
| Permission | Only a source the team is allowed to use | Public appearance ≠ retain/reuse | LinkedIn case outcome; other platform terms |
| Platforms | One source per batch; do not pool yet | Different sampling frames and licences | Order after LinkedIn response; X, ResearchGate, YouTube, podcasts remain candidates |
| Time start | 2022-11-30 (ChatGPT public launch) | Marks mainstream GenAI discourse | Midjourney 2022; older *generative design* |
| Time end | Date of each permitted capture | Reproducible | Rolling vs fixed close |
| Language | English | Matches current RQs and largest overlapping professional talk | Persian, German, others |
| Geography | No country filter | Professional networks are transnational | EU-only if a regulator/API requires it |
| Unit of analysis | Post or article as primary item | RQ1–RQ3 are about statements in discourse | Thread-level vs item-level sentiment |
| Comments | Store as child records when permitted | Comments are part of the conversation | Depth (one level vs full tree); missingness |
| Podcasts / video | Transcript segments, not audio blobs | Aligns with text sentiment methods | Who transcribes; accuracy |
| Volume before coding | About 80–120 Layer-A hits | Enough to estimate precision | Exact *n* |
| Scale-up | Only after precision and permission | Avoid a large biased dump | Target corpus size |
| Duplicates | Keep first capture; mark later copies | Reposts are not independent sentiment | Quote-posts |
| Engagement counts | Store if offered; do not treat as labels | Likes ≠ sentiment | |
| RQ4 roles | Unknown unless evidenced | Prevents invented demographics | Self-report vs profile field |

### Relevance coding for the pilot

Before any large search, two readers should label a pilot sample:

- `relevant` — architecture *and* generative AI (or a named GenAI tool) in a professional/educational sense
- `borderline` — architecture-adjacent or GenAI-adjacent only
- `exclude` — software architecture, generic AI, or no architecture
- `skill_mentioned` — yes/no, independent of sentiment
- `deskilling_claim` — yes/no: the text asserts skill loss or replacement, not merely mentions AI

Disagreement rate belongs in the experiment record. Do not tune keywords until this pass exists.

## Storage

This is a handling plan for *when* a permitted intake exists. It is not a deployed database and does not change the [preparation-stage privacy policy](../PRIVACY.md).

### Rules

1. **Local only.** Raw and working files live under `data/` (gitignored except `data/README.md`). Never commit posts, comments, author names, URLs that identify a person, or exports.
2. **Not Telegram, not public GitHub issues.** Share counts, query versions, and aggregate notes. Do not paste member text into the group or into an external LLM unless a reviewed processing arrangement exists.
3. **One record per item.** Post, comment, reply, article, and transcript segment are different `item_type` values. Replies point at `parent_id`.
4. **Do not pool sources** in one file. Separate folders per `source_platform` and `batch_id`.
5. **Minimise.** Store fields needed for the questions. Do not keep messages, connection graphs, photos of people, emails, or full profile dumps “in case they help later”.
6. **Retention is source-specific.** The LinkedIn form declared **3 months** storage in **Germany**. The published Research Tools terms default to **24 hours** for individual personal data unless documentation or written agreement says otherwise. If access is offered, reconcile those clocks *before* keeping a corpus. Do not treat the form answer as a granted exception.
7. **Access.** Limit to the named researchers. Encryption at rest and a deletion calendar are required before personal data is stored; they are not claimed as already built.
8. **Analysis vs training.** Default assumption: apply or evaluate existing methods. Do not fine-tune on LinkedIn or other restricted text unless the grant explicitly allows it.

### Proposed local layout

```text
data/
  README.md                          # committed metadata only
  local/                             # gitignored
    raw/
      {platform}/
        {batch_id}/
          items.jsonl
          manifest.json
    working/
      annotations.jsonl              # labels only, still identifying if it keys to raw IDs
    derived/                         # aggregates only, after a disclosure check
```

`batch_id` format: `YYYY-MM-DD-short-name` (same idea as experiment records).

### `manifest.json` (per batch)

```text
batch_id: TODO
source_platform: linkedin | x | researchgate | youtube | podcast | donation | page_portability | other
permission_basis: pending | research_api | donation | page_portability | other
query_id / query_text / query_version: TODO
time_window_start / time_window_end: TODO
language_filter: TODO
captured_at: TODO
capturing_person: TODO
item_count: TODO
comment_count: TODO
retention_until: TODO
storage_location_country: Germany (if that remains the declaration)
limitations: TODO
```

### Item record (`items.jsonl`)

One JSON object per line. Unknown values stay `null`. Do not invent engagement numbers.

```text
record_id                 stable UUID for this stored item
dataset_version           e.g. lexicon-2026-08-29 / later corpus version
source_platform           see manifest
item_type                 post | comment | reply | article | transcript_segment
parent_id                 record_id or source id of parent; null for top-level
thread_id                 shared id for the conversation
source_item_id            platform id if provided
source_url                only if permitted to store
source_created_at         original timestamp if provided; keep timezone
captured_at               when we obtained it
query_id / query_text     which search produced this hit
language                  ISO code if known
text                      permitted body text
title                     if any
media_note                none | image | video | link | unknown  (not the media file)
engagement                likes, comments, reposts, views — null if unknown
author.source_author_id   platform id if permitted; else omit
author.display_handle     only if needed and permitted; prefer a hash for working files
author.stakeholder_label  practitioner | academic | student | industry_leader | adjacent | unknown | overlapping
author.stakeholder_evidence short quote or "self_report" / "profile_field" / "unknown"
permission_basis          copy from manifest
retention_until           date
relevance_status          unreviewed | relevant | borderline | exclude
exclude_reason            software_architecture | no_architecture | no_genai | duplicate | other
skill_mentioned           null | true | false
deskilling_claim          null | true | false
annotator_id              if labelled
annotator_notes           methodological notes, not gossip
```

Reaction totals are metadata, not sentiment labels. A missing comment thread is `unavailable`, not zero comments.

### What this project will not store in Git

- Raw JSONL, CSV exports, screenshots of posts, or author tables
- Client secrets, tokens, case numbers, or mailbox contents
- Telegram forwards of captured text

`data/README.md` should list **dataset metadata only** (name, licence, date, item counts, checksum of a local file) after a batch exists.

## Team decisions still required

- Accept, cut, or add terms; especially product names and whether landscape/interior are in scope.
- English-only first pass versus a planned Persian and/or German pass.
- Start date: ChatGPT launch vs an earlier Midjourney or generative-design window.
- First permitted source after the LinkedIn response (or a donation/Page pilot if API access is refused).
- Comment depth and whether videos need transcripts.
- Who holds the files in Germany, who can annotate, and the deletion date that matches the actual grant.
- Whether sentiment labels mean polarity toward GenAI, toward a skill effect, or agreement with a deskilling claim (still open in [notes](notes.md)).

## Next working step

1. Team edits this lexicon (add/strike terms in a shared pass).
2. Freeze **query version 1** (A1 plus exclusions) as a short text block.
3. Run a **relevance pilot only** on a permitted source — or wait if none exists.
4. Record precision and exclusions in an [experiment file](../experiments/README.md); then revise terms. Do not grow the corpus first.
