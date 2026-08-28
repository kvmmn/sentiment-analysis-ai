# LinkedIn Data Access Review

Reviewed: 2026-08-28. Status: documentation review and recommendations, not an approved collection protocol or a tested pipeline.

## Summary

The group's proposed research-access route exists, but academic intent alone does not establish eligibility. We should settle access and permitted research uses before building OAuth or a collector. The present research questions concern perceptions of GenAI and deskilling; their fit with the DSA research purpose has not been established.

This review covers the main access categories and representative tools, not every vendor. Official documentation supports platform claims; vendor descriptions establish only advertised capabilities. No app, access request, paid account, API request for member data, or collection job was created. University ethics and data-protection review is still needed; this document is not legal advice.

## 1. Check of the Group's Proposed Steps

| Proposed step | Assessment | Practical consequence |
| --- | --- | --- |
| Create an app using a real account | The normal developer process exists and includes a LinkedIn Page association. Product requirements differ. [App access guidance](https://www.linkedin.com/help/linkedin/answer/a526048) | Creating an app is not research approval. The original suggestion, GenAI Architecture Discourse Research, was later superseded by Kaveh's chosen display name, Saintiment. |
| Obtain credentials and configure OAuth | Correct for APIs requiring OAuth. Publicly available permissions cover authenticated-member identity and publishing, not unrestricted post collection. [API access and permissions](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access) | A valid token does not grant an unapproved scope. |
| Test an API request | Useful after a product and its scopes are granted. | A successful identity request would test authentication, not access to the discourse corpus. Test only an approved read endpoint. |
| Submit for research access | There is a dedicated [DSA research application](https://www.linkedin.com/help/linkedin/ask/DSA), linked from [LinkedIn's researcher guidance](https://www.linkedin.com/help/linkedin/answer/a1645616). | Check project eligibility and data requirements before spending time on a generic integration. The form required sign-in during review; its complete fields were not inspected. |

The group's explanation of LinkedIn's motives is not needed to establish access rights. Evaluate the actual product, scope, agreement, and permitted use.

## 2. The Research Route: Eligibility and Unresolved Capabilities

### Public data: DSA Article 40(12)

LinkedIn describes a beta program with conditions covering commercial independence, funding disclosure, security and confidentiality, and necessary, proportionate data access. It says other public-data research projects are not currently supported through this route. [LinkedIn researcher guidance](https://www.linkedin.com/help/linkedin/answer/a1645616)

The European Commission explains that Article 40(12) concerns research into systemic risks in the EU. Article 40(4) is a distinct process involving Digital Services Coordinator vetting and additional conditions, including research-organisation affiliation, for non-public access. Applications for that process are available through the DSA portal. It is not a general academic-data alternative. [Commission FAQ](https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en), [DSA portal](https://data-access.dsa.ec.europa.eu/public/about)

**Assessment for this study:** professional concern about losing architectural skills does not, by itself, demonstrate the required systemic-risk purpose. This is an assessment of the current draft, not a rejection decision. Ask whether the actual research qualifies; do not invent a platform-harm rationale to gain access. Clarify university affiliation, supervision, funding, and institutional responsibility without assuming any team member's status.

The reviewed public documentation does not establish this project's available keyword-search endpoint, historical coverage, query syntax, quotas, comment/reply depth, author-role fields, export format, or delivery schedule. A catalog of possible data is not a grant of every field. The Article 40(4) catalog must not be presented as an Article 40(12) API specification.

### Research terms that affect implementation

The published [Research Tools terms](https://www.linkedin.com/legal/l/research-api-terms) require specific review:

- Sections 3.1–3.2 restrict AI training, mixing other LinkedIn sources, publishing tools, personal-data databases, and identifiable disclosures, subject to stated exceptions.
- Section 4.1 defaults to 24-hour storage for individual personal data, including posts/comments; other research data has a one-year default. Documentation or written agreement may change this.
- Section 5.1 addresses advance courtesy copies and licensing of work products.
- Section 7.5 says developer-portal approval is not the required written permission.

Obtain institutionally reviewed clarification before training, retaining a corpus, distributing software, or sharing data. Inference, external model processing, team access, and reproducibility need explicit assessment; none is assumed approved.

## 3. Comparison of Collection Routes

The suitability judgments below are project recommendations, not guarantees of approval or legal conclusions.

| Route | Available or proposed material | Fit and limits for this project |
| --- | --- | --- |
| Official DSA public-data research access | Data approved for a qualifying project | Investigate eligibility first. Wider-discourse coverage remains unverified. |
| DSA vetted access via a regulator | Necessary approved non-public data | Consider only if a genuine systemic-risk study requires it; disproportionate for a first ingestion pilot. |
| Participant donations of their own content or account exports | Material selected and supplied by consenting contributors | Best small-pilot candidate if the team accepts a recruited sample. No developer app needed for manual exports. Recruitment, consent, selection bias, and third-party material need a protocol. |
| Member Data Portability API | A consenting member's own data | Official technical-pilot option for eligible EEA/Switzerland members. Not a search of other people's posts. A third-party participant application is a separate access/use question. |
| Pages Data Portability API | Cooperating organisations' Page content and permitted interactions | Potential route through architecture firms, schools, or professional bodies. Requires Page-admin authorization and product access; it does not cover arbitrary Pages or personal-profile discourse. |
| Marketing / Community Management APIs | Scoped member or organisation social content | Not a default academic-corpus route: permission and use restrictions apply even when endpoints return data. |
| Manual LinkedIn browsing or search-engine discovery | Candidate material visible through ordinary interfaces | Discovery is not automatic permission to retain/reuse content. Small scale is not a blanket exemption. Any approved sampling must record selection and coverage limits. |
| Commercial scraping APIs, browser extensions, or unofficial clients | Vendor-advertised posts, profiles, comments, or search outputs | Not selected. Platform authorization, provenance, member privacy, and completeness are unresolved. A vendor API key is not a LinkedIn research credential. |
| Existing corpus or licensed dataset | Publisher-provided material | Potentially useful only after verifying content rights, collection provenance, date/language coverage, relevant text, and stakeholder evidence. No suitable corpus was validated in this review. |
| Direct institutional collaboration | A specifically negotiated dataset or analysis | Worth an inquiry if a supervisor has an appropriate relationship; no open entitlement or availability is assumed. |
| Ad Library / Economic Graph outputs | Advertising material or labour-market research | Useful background or a different research design, not substitutes for ordinary architectural posts and discussions. |
| Consented surveys or interviews | New participant responses | A fallback if discourse access fails. This changes the evidence and requires team agreement and an appropriate ethics process. |

### Official alternatives: details that matter

**Account exports:** LinkedIn provides own-account downloads, including Shares and Comments categories; Articles may contain URLs rather than article bodies. Do not request a participant's entire archive by default: it may include messages, connections, and unrelated sensitive material. Prefer selected own-authored content with documented permission and minimization. [Download your data](https://www.linkedin.com/help/linkedin/answer/a1341346)

**Member portability:** the self-service product uses the designated default LinkedIn Company Page and scope `r_dma_portability_self_serve`. Its documentation limits token consent to members located in the EEA or Switzerland. Changelog events begin after consent and have a 28-day query window; snapshots can include historical member data. These are different mechanisms, not a 28-day limit on all historical content. Confirm actual eligibility rather than relying on the computer's timezone. [Member API documentation](https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-member/?view=li-dma-data-portability-2026-05)

**Page portability:** `r_dma_admin_pages_content` covers authorised organisation content and activity, including posts and comments. Member interactions remain subject to consent/privacy restrictions, so missing data is not evidence of absent discussion. [Page API overview](https://learn.microsoft.com/en-us/linkedin/dma/pages-data-portability/pages-data-portability-overview?view=li-dma-data-portability-2026-05), [application and privacy guidance](https://www.linkedin.com/help/linkedin/answer/a6220307)

**Portability is a separate agreement:** member/Page authorization and lawful processing are still required. Its terms also restrict combining the service with unofficially obtained LinkedIn content; do not plan a portability-plus-scraper workaround. Do not transfer research-program restrictions or permissions wholesale to this product. [Portability terms](https://www.linkedin.com/legal/l/portability-api-terms)

**Community Management:** the Posts API describes restricted `r_member_social` and role-scoped organisation access, not a general keyword-search corpus endpoint. Marketing terms limit member-data uses to Page/profile management and restrict export and storage. An architecture Page administrator's cooperation alone does not remove those restrictions. [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-04), [restricted uses](https://learn.microsoft.com/en-us/linkedin/marketing/restricted-use-cases?view=li-lms-2025-11)

**Adjacent sources:** the [Ad Library](https://www.linkedin.com/help/linkedin/answer/a1517918) supports advertising searches. [Economic Graph research](https://economicgraph.linkedin.com/research) shows published research and collaborations; it does not establish an open post-text API for this project.

## 4. Tools: What They Solve and What They Do Not

| Tool category / example | Documentation finding | Assessment |
| --- | --- | --- |
| Official developer portal, OAuth tooling, curl or Postman | Tools for authorized API integration and inspection | Use after the route and scopes are clear. A custom OAuth application may be unnecessary for an own-data smoke test. |
| Local CSV/JSON processing and a small Python importer | Proposed implementation approach, not installed or tested | Sufficient for an approved export pilot. Keep collection, normalization, and analysis separate. |
| Apify marketplace Actors | A [keyword-search Actor](https://apify.com/benjarapi/linkedin-post-search) advertises post extraction but was marked under maintenance. Another [search Actor](https://apify.com/dami_studio/linkedin-post-search-scraper) describes web-index discovery and explicitly excludes comment bodies. | Actor-specific validation is essential. A comment count is not comment text, and index discovery is not complete LinkedIn search. No Actor was run. |
| Bright Data | Its [LinkedIn scraper offering](https://brightdata.com/products/web-scraper/linkedin) advertises posts and profile/company-based discovery. | Commercial extraction capability advertised, not platform permission or a verified research sample. No purchase or test. |
| PhantomBuster | Its [commenter-export documentation](https://phantombuster.com/blog/social-selling/turn-linkedin-posts-into-lead-magnets-workflow/) advertises account-connected CSV output with names, profile URLs, and comments. | Lead-generation tooling is not a validated research protocol. Do not adopt its outreach workflow for this study. |
| Browser automation, unofficial libraries, scraping extensions | LinkedIn prohibits unauthorized scraping/automation and warns of account restrictions. [Platform policy](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions?lang=en) | Do not use session-cookie sharing, fake accounts, or access-control workarounds. Changing the client does not grant permission. |
| Workflow runners or AI agents | Can orchestrate tools, but do not change upstream rights or coverage | Not needed for the foundation or eligibility review. Do not add orchestration infrastructure yet. |

LinkedIn also warns against systematic manual page viewing. Search-engine visibility and buying data from an intermediary do not resolve content-use rights. Whether a particular collection is lawful requires a jurisdiction-specific assessment; a terms violation is not being equated here with a universal criminal prohibition. [Manual viewing guidance](https://www.linkedin.com/help/linkedin/answer/a1339210/restricted-action-message?lang=en), [software and reuse policy](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions?lang=en)

## 5. Research Quality and Pipeline Requirements

These are proposed design requirements, not implemented features or confirmed team decisions.

- **Define the sample:** decide public discourse versus a recruited participant/Page sample, languages, dates, and whether the unit is a post, comment, or thread. Keep different routes separately identifiable; do not pool them without methodological and contractual review.
- **Avoid keyword bias:** searching only for deskilling may select concern before measuring it. Pilot neutral GenAI-and-architecture terms alongside skill-related terms, then document relevance exclusions, including software-architecture false positives.
- **Preserve context:** separate original posts, repost commentary, comments, and replies; record incomplete threads. Do not treat reaction totals as sentiment labels or missing comments as zero comments.
- **Handle RQ4 honestly:** use permitted evidence or participant self-report for stakeholder categories; permit overlapping and unknown roles. Do not infer occupations from names/photos or silently enrich profiles from other sites.
- **Separate analysis from training:** clarify whether the goal is applying existing sentiment methods, evaluating them, or fitting/fine-tuning a model. Validate any permitted analysis against human annotation; general sentiment and agreement with a deskilling claim are different targets.
- **Check privacy before storage:** have the institution establish processing grounds, ethics requirements, access roles, retention/deletion, and any external processors. Pseudonymization is not necessarily anonymization. [Commission data-protection explanation](https://commission.europa.eu/law/law-topic/data-protection/reform/what-does-general-data-protection-regulation-gdpr-govern_en), [safeguards](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en)
- **Keep sensitive material out of public channels:** no raw corpus, identifying excerpts, secrets, tokens, or personal records in the public GitHub repo or Telegram group. Use institution-approved restricted storage if retention is permitted; `.gitignore` is not access control. Do not upload member text to an external LLM without approved processing arrangements.
- **Keep reproducibility within permission:** record permitted provenance, query/configuration versions, acquisition dates, transformations, and missingness. A permanent raw archive is not assumed. Publish only authorized code, aggregate results, and suitably non-identifying artifacts.

The eventual flow should be: approved source → permitted intake → validation/minimization → approved retention or transient processing → analysis → disclosure review. There is no unconditional raw-data database stage.

### Acceptance checks for a later pilot

1. Confirm the correct product, scopes, authorized account/Page, and allowed fields before a small read request or import.
2. Validate timestamp/timezone parsing, Unicode, missing text, duplicates, reposts, and parent relationships against legitimately supplied examples.
3. Record the distinction between zero results, incomplete pagination, access denial, deleted content, and unavailable comments.
4. Stop on insufficient authorization; respect documented quotas and retry instructions without trying to evade controls.
5. Test retention expiry/deletion across working files, logs, caches, and backups, and confirm credentials never appear in output.
6. Demonstrate the intended analysis is allowed and useful before scaling; do not promise population-representative sentiment from a convenience sample.

## 6. Recommended Next Steps

1. **Eligibility and use check first.** Prepare a short, accurate project brief for the supervisor/institution and LinkedIn. Include the existing research questions, intended sources/fields, time range, analysis-versus-training intent, funding, team access, privacy safeguards, and intended article/thesis outputs. Treat this as preparation, not a statement that every item is a verified application-form field.
2. **Ask concrete questions.** Does this study qualify? Which interface and fields would be available? Are keyword discovery, historical posts, comments/replies, and permitted stakeholder evidence supported? What retention, annotation, analysis, publication, and software-sharing permissions apply? What review timeline and limits should be expected? LinkedIn lists `LI_DSAResearcher@linkedin.com` under Article 40(4); use the Article 40(12) form for that application rather than assuming the email replaces it. [Contact guidance](https://www.linkedin.com/help/linkedin/answer/a1645616)
3. **Choose an independent pilot only with team agreement.** If preserving the current topic matters more than broad platform coverage, evaluate selected own-content donations first; eligible member portability or cooperating Page owners can be assessed afterward. This does not satisfy platform-wide sampling or guarantee sufficient architecture-related text.
4. **Build only after route selection.** Start with one approved source and a small, documented import/read test. No paid scraper, database service, application deployment, or scheduled harvesting is needed today.

Before implementation, the team needs to confirm: university/supervisor and ethics support; whether model training is intended; and whether the study requires wider public discourse or can use an explicitly recruited sample. Volume, language, dates, and budget remain open. No approval probability, delivery time, or collection price has been validated.

## Evidence and Review Limits

Primary-source links are attached to the relevant claims above and indexed in [references](references.md). Documentation was reviewed on the date at the top; URLs and terms should be checked again before applying or collecting. Vendor claims were not independently benchmarked. The sign-in-only form and granted research interface were not inspected, and no live API behavior was verified. A limited search of dataset repositories did not establish a suitable licensed corpus; this is not proof that none exists.
