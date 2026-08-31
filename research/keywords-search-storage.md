# Keywords, Search Scope, and Storage

Status: **working proposal for team review**, drafted 2026-08-29. This answers the Telegram-group questions about search terms, search limits, and how to store posts and comments. It is not a finalized protocol, a literature-validated lexicon, or permission to collect.

No corpus has been collected. Do not start harvesting from LinkedIn, X, or other platforms on the basis of this list. The [LinkedIn case](linkedin-application-worksheet.md) is still **Open**; ordinary visibility of a post is not a licence to retain it.

Related records: [keyword systems map](keyword-systems.md), [literature strings](keyword-literature-strings.md), [discourse catalog](keyword-discourse-catalog.md), [keyword lexicon](keyword-lexicon.md), [research notes](notes.md), [access review](linkedin-data-access-review.md), [privacy policy](../PRIVACY.md), [data guide](../data/README.md).

**Still not a collection licence.** The 2026-08-31 keyword-systems expansion separates literature retrieval, discourse catalog, and coding lexicon; see [keyword-systems.md](keyword-systems.md).

## Answers for the group

**What are the keywords?** The categorized, sorted catalog is the [keyword lexicon](keyword-lexicon.md). Use two layers. Layer A finds architecture + generative-AI discussion without requiring the word *deskilling*. Layer B then searches skill, labour, and method terms inside that discussion. Searching only for deskilling would measure concern that the query itself selected.

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

## Keyword list

The full categorized list lives in the [keyword lexicon](keyword-lexicon.md). Core set, RQ sections, exclusions, Persian, German, and hashtags are there and sorted inside each category. Query sketches below still use the core set.

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

1. Team edits the [keyword lexicon](keyword-lexicon.md) (add/strike terms in a shared pass).
2. Freeze **query version 1** (A1 plus exclusions) as a short text block.
3. Run a **relevance pilot only** on a permitted source — or wait if none exists.
4. Record precision and exclusions in an [experiment file](../experiments/README.md); then revise terms. Do not grow the corpus first.
