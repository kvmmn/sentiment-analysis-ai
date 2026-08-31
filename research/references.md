# References

Shared source records for the [article](../writing/article.md) and [thesis](../writing/thesis.md). The sources below support data-access planning; they are not a literature review or evidence of findings about architectural deskilling.

## LinkedIn Data Access Review Sources

Reviewed on 2026-08-28 for the [access review](linkedin-data-access-review.md). Initially, relevant sections were reviewed except the sign-in-only application form. Its printed fields were inspected later from Kaveh's PDF, as recorded below. Publication dates are not recorded unless confirmed in the review. Vendor documentation establishes advertised capabilities only.

| ID | Publisher and source | Relevance / limitation |
| --- | --- | --- |
| LI-01 | LinkedIn — [Data access for researchers](https://www.linkedin.com/help/linkedin/answer/a1645616) | Research-program entry points and eligibility |
| LI-02 | LinkedIn — [Research Tools Program terms](https://www.linkedin.com/legal/l/research-api-terms) | Research-use, retention, and publication conditions; requires institutional interpretation |
| LI-03 | European Commission — [DSA researcher FAQ](https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en) | Distinction between Articles 40(12) and 40(4) |
| LI-04 | European Commission — [DSA Data Access Portal: About](https://data-access.dsa.ec.europa.eu/public/about) | Vetted-access application mechanism |
| LI-05 | LinkedIn — [Research application form](https://www.linkedin.com/help/linkedin/ask/DSA) | Full printed fields later inspected in Kaveh's three-page PDF; dropdown choices and conditional behavior not inspected. See the application worksheet. |
| LI-06 | LinkedIn — [Accessing LinkedIn APIs](https://www.linkedin.com/help/linkedin/answer/a526048) | Normal developer-app process |
| LI-07 | LinkedIn / Microsoft Learn — [Getting Access to LinkedIn APIs](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access) | OAuth and open/restricted permissions |
| LI-08 | LinkedIn / Microsoft Learn — [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-04) | Scoped social-content access |
| LI-09 | LinkedIn / Microsoft Learn — [Restricted uses of Marketing APIs](https://learn.microsoft.com/en-us/linkedin/marketing/restricted-use-cases?view=li-lms-2025-11) | Restrictions beyond endpoint availability |
| LI-10 | LinkedIn — [Download your data](https://www.linkedin.com/help/linkedin/answer/a1341346) | Own-account exports and categories |
| LI-11 | LinkedIn / Microsoft Learn — [Member Data Portability (Member)](https://learn.microsoft.com/en-us/linkedin/dma/member-data-portability/member-data-portability-member/?view=li-dma-data-portability-2026-05) | Eligibility, self-service access, changelogs, and snapshots |
| LI-12 | LinkedIn / Microsoft Learn — [Pages Data Portability overview](https://learn.microsoft.com/en-us/linkedin/dma/pages-data-portability/pages-data-portability-overview?view=li-dma-data-portability-2026-05) | Organisation-content access |
| LI-13 | LinkedIn — [Pages portability application review](https://www.linkedin.com/help/linkedin/answer/a6220307) | Access process and privacy-dependent omissions |
| LI-14 | LinkedIn — [DMA Portability API terms](https://www.linkedin.com/legal/l/portability-api-terms) | Separate portability agreement |
| LI-15 | LinkedIn — [Prohibited software and extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions?lang=en) | Scraping, automation, and reuse restrictions |
| LI-16 | LinkedIn — [Restricted Action Message](https://www.linkedin.com/help/linkedin/answer/a1339210/restricted-action-message?lang=en) | Systematic manual viewing is not an unrestricted alternative |
| LI-17 | LinkedIn — [Ad Library](https://www.linkedin.com/help/linkedin/answer/a1517918) | Advertising data, not general discourse |
| LI-18 | LinkedIn — [Economic Graph research](https://economicgraph.linkedin.com/research) | Background and examples of collaborations |
| LI-19 | Benjar Scraping API / Apify — [LinkedIn Post Search Scraper](https://apify.com/benjarapi/linkedin-post-search) | Advertised search; listing marked under maintenance at review |
| LI-20 | dami_studio / Apify — [LinkedIn Post Search Scraper](https://apify.com/dami_studio/linkedin-post-search-scraper) | Advertised index-based discovery; no comment bodies |
| LI-21 | Bright Data — [LinkedIn Scraper API](https://brightdata.com/products/web-scraper/linkedin) | Commercial capability claims, not independently tested |
| LI-22 | PhantomBuster — [LinkedIn commenter-export workflow](https://phantombuster.com/blog/social-selling/turn-linkedin-posts-into-lead-magnets-workflow/) | Commercial capability claims; outreach workflow not adopted |
| LI-23 | European Commission — [Data protection explained](https://commission.europa.eu/law/law-topic/data-protection/reform/what-does-general-data-protection-regulation-gdpr-govern_en) | Identifiability and pseudonymization |
| LI-24 | European Commission — [Principles of the GDPR](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en) | Research safeguards and privacy by design |

## Created-App Products Review Sources

Relevant sections checked on 2026-08-28 for the Products-page review in [notes](notes.md). LI-01 and LI-13 were also revisited. Kaveh's two-page developer-console PDF is local evidence, excluded from the public repository; its observations are separated from documentation-based guidance.

| ID | Publisher and source | Relevance / limitation |
| --- | --- | --- |
| LI-25 | LinkedIn — [Send an app verification request for a LinkedIn Page](https://www.linkedin.com/help/linkedin/answer/a1665329) | Settings, Verify, Generate URL, and Page super-admin approval; distinct from Page badge verification. |
| LI-26 | LinkedIn / Microsoft Learn — [Sign In with LinkedIn using OpenID Connect](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2) | Authentication and basic profile scopes; not a post-search product. |
| LI-27 | LinkedIn / Microsoft Learn — [Community Management overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-04) | Vetted use cases; FAQ 4's initial product restriction and FAQ 6's closed `r_member_social` permission. |

After the Auth screenshots were supplied, LI-01, LI-05, and LI-07 were rechecked on 2026-08-28. The public research form still exposed only a sign-in page; its actual questions were not inspected. The next-step recommendation in the setup notes is based on the documented permissions and eligibility requirements, not an assumed form layout.

## Research Application Form Evidence

LI-05's actual fields were subsequently inspected on 2026-08-28 from Kaveh's local `Contact_form_LinkedIn_Help.pdf`. The [worksheet](linkedin-application-worksheet.md) preserves the field inventory, print time, evidence hash, and inspection limits. LI-01, LI-02, and LI-03 were revisited to distinguish eligibility, storage requirements, and the Article 40(12)/40(4) affiliation conditions. The raw account-page PDF is not published.

## Privacy Policy and Publication Sources

Relevant sections reviewed on 2026-08-28 for the [privacy-policy review](privacy-policy-review.md). LI-02 also supports that review. These sources explain requirements and hosting behavior; they do not verify this project's legal compliance or LinkedIn acceptance.

| ID | Publisher and source | Relevance / reading notes |
| --- | --- | --- |
| PP-01 | LinkedIn — [API Terms of Use](https://www.linkedin.com/legal/l/api-terms-of-use) | §§4–5 storage, deletion, accessible privacy notice, user agreement, and consent; §7 security. Page dated 13 December 2022. |
| PP-02 | LinkedIn — [Lead Gen Forms Privacy Policy](https://www.linkedin.com/help/linkedin/answer/a420012/lead-gen-forms-privacy-policy?lang=en) | Dedicated policy URL in advertising forms; not the research-access procedure. |
| PP-03 | European Commission — [Data protection obligations](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en) | Transparency under GDPR Articles 12–14; indirect collection and rights. Applicability and institutional responsibilities require assessment. |
| PP-04 | GitHub — [Viewing and understanding files](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files) | Rendered Markdown preview; does not certify third-party acceptance of a file URL. |
| PP-05 | GitHub — [Configuring a GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | Branch-based publication as a fallback; no Pages deployment created. |
| PP-06 | GitHub — [General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) | Hosting provider's separate data processing; linked from the project policy. |
| PP-07 | LinkedIn / Microsoft Learn — [LinkedIn API Documentation](https://learn.microsoft.com/en-us/linkedin/) | Documentation index supplied in the user's pasted AI response; not itself a research-access or policy-content approval. |

Copy the template below for each actual source. Verify bibliographic details against the source; leave unknown information as TODO. Use a stable source ID when referring to a record from notes or drafts.

## Applicant affiliation source

- **AFF-01:** Arden University, [Berlin campus](https://arden.ac.uk/where-to-study/locations/berlin). Accessed 2026-08-28; campus-address section reviewed. Lists Dessauer Str. 3-5, 10963 Berlin, Germany. Supports campus contact details only, not personal enrolment, formal department name, or approval of Saintiment.

## Keyword Systems and Literature Warrants — 2026-08-31

Records support search-method design and source identification. They are **not** Saintiment experiment results. Live database counts were not run on 2026-08-31.

### Verified discourse analogue (LinkedIn)

| ID | Record | Reading status |
| --- | --- | --- |
| KS-01 | Ghimire, S.; Kim, S.; Acharya, M. Generative AI in Construction: Exploring the Potentials and Limitations of ChatGPT. *Buildings* **2024**, *14*(1), 220. DOI: [10.3390/buildings14010220](https://doi.org/10.3390/buildings14010220). arXiv: [2310.04427](https://arxiv.org/abs/2310.04427). PDF in hand via arXiv (MDPI PDF 403 on research pass). **Methods confirmed:** LinkedIn; **32 opinions / 63,778 words**; construction professionals; three published strings (RW-GH-1–3); hashtags include misspelled `#generativai`. Related-work analogue only — not Saintiment Layer A. | Read — arXiv PDF; methods confirmed |
| KS-02 | Larbi, D.; et al. GenAI, built environment, sentiments, socioeconomic implications (title-level). *Technological Forecasting and Social Change* **2026**, *228*, 124689. DOI: [10.1016/j.techfore.2026.124689](https://doi.org/10.1016/j.techfore.2026.124689). Closed OA. Closest closed-OA BE+sentiment candidate; **71/6173 unverified** against PDF; methods unread 2026-08-31; cites KS-01. Circumstantial 76% of 71 is not evidence. **Keep in record.** | Unread — closed OA |
| KS-03 | Van Tam, et al. Construction / built environment GenAI review. *Building and Environment* **2025**, *284*, 113526. Exists; closed access. **Not the 71-*n* paper.** Boolean not recovered. | Bibliographic + access note only |
| KS-04 | Xiong, et al. Survey *n* = 162 (not LinkedIn). *Automation in Engineering Informatics* (AEI) **2026**, *71*, 104392. Volume 71 is bibliographic coincidence, not opinion count. | TODO |

### Search-method warrants

| ID | Record | Relevance |
| --- | --- | --- |
| KS-10 | Page, M.J.; et al. PRISMA 2020 elaboration item 7. *BMJ* **2021**. DOI: [10.1136/bmj.n160](https://doi.org/10.1136/bmj.n160). | Document search strategy |
| KS-11 | Booth, A. (2008). Unsystematic reviews and from anecdote to metaphor. In *Cochrane Handbook* context — successive fractions for sensitivity. | String sensitivity analysis |
| KS-12 | Rethlefsen, M.L.; et al. PRISMA-S. **2021**. DOI: [10.31222/osf.io/7rgy3](https://doi.org/10.31222/osf.io/7rgy3). | Report search methods |
| KS-13 | McGowan, J.; et al. PRESS peer review of electronic search strategies. *Journal of Clinical Epidemiology* **2016**. | Peer-review search strategy |
| KS-14 | Chen, et al. *Architecture* **2026**, *6*(2), 60. No subject-area restriction at search; Stage-2 + umbrella AI too broad/narrow for Saintiment primary. | Comparator — not adopted wholesale |
| KS-15 | Stanimirovic (2026). ANDs education/creativity at retrieval — A+B-soft sensitivity only for Saintiment. | Too-narrow sensitivity |
| KS-16 | Yiannoudes (2025). Full string upon request — not recorded here. | TODO |
| KS-17 | Memon, et al. (2025) AECO focus — related-work (`S-RW1`), not primary RQ1. | Related-work scope |

### Professional / regulatory warrants (discourse Layer B context)

| ID | Record | Relevance |
| --- | --- | --- |
| KS-20 | RIBA AI Report 2025 | Professional judgment, human creativity |
| KS-21 | AIA AI Firm Toolkit | Firm GenAI guidance |
| KS-22 | ARB competency outcomes | Regulatory skill framing |
| KS-23 | BAK KI FAQ | German chamber AI guidance |
| KS-24 | Braverman; SBTC | Layer 2 labour lemmas — not retrieval |

### Persian / German source notes (discourse catalog)

| ID | Record | Relevance |
| --- | --- | --- |
| KS-30 | Farhangestan — memar / memari | FA architecture lemmas |
| KS-31 | IRCEO; 1374 Law — mohandes-e memar, reshte-ye memari, daftar-e mohandesi-ye tarrahi-ye sakhteman | FA professional terms |
| KS-32 | Honar-ha-ye Ziba (*Me'mari va Shahrsazi*) — `هوش مصنوعی مولد` on [generative-AI policy page](https://jfaup.ut.ac.ir/p_generative-ai); IRCEO LMS 1180313 `آشنایی با هوش مصنوعی مولد` — [course syllabus](https://lmsiriceo.ir/course/show/470/d98d61b1b9f19d88849096542a221190) (+ Nezam Qom news 1796). **Sourced** journal/CPD discourse; **not** Farhangestan-approved equivalent. Host ruling 2026-08-31 vs later conservative GAP. | Verified URLs on research pass |
| KS-33 | Mehr 1405 — hushvare/humas **not approved** for GenAI | FA exclusion |
| KS-34 | BAK/AKNW — Gebäudevisualisierungen, KI-Bildgeneratoren | DE visualisation / GenAI |
| KS-35 | DIN EN ISO 19650 — Bauwerksinformationsmodellierung | DE BIM term |
| KS-36 | Duden — Dequalifizierung, Kompetenzverlust | DE Layer 2 deskilling |

## Source Template

```text
Source ID: TODO
Title: TODO
Author(s): TODO
Year: TODO
Publication / publisher: TODO
DOI / URL: TODO
Accessed on: TODO
Reading status: TODO (unread / in progress / read)
Relevance to this project: TODO
Reading notes: TODO
Claims supported and page / section locations: TODO
Limitations or questions: TODO
```
