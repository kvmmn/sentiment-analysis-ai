# References

Shared source records for the [article](../writing/article.md) and [thesis](../writing/thesis.md). The sources below support data-access planning; they are not a literature review or evidence of findings about architectural deskilling.

## LinkedIn Data Access Review Sources

Reviewed on 2026-08-28 for the [access review](linkedin-data-access-review.md). Reading status: relevant sections reviewed, except the application form, where only the sign-in requirement was visible. Publication dates are not recorded unless confirmed in the review. Vendor documentation establishes advertised capabilities only.

| ID | Publisher and source | Relevance / limitation |
| --- | --- | --- |
| LI-01 | LinkedIn — [Data access for researchers](https://www.linkedin.com/help/linkedin/answer/a1645616) | Research-program entry points and eligibility |
| LI-02 | LinkedIn — [Research Tools Program terms](https://www.linkedin.com/legal/l/research-api-terms) | Research-use, retention, and publication conditions; requires institutional interpretation |
| LI-03 | European Commission — [DSA researcher FAQ](https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en) | Distinction between Articles 40(12) and 40(4) |
| LI-04 | European Commission — [DSA Data Access Portal: About](https://data-access.dsa.ec.europa.eu/public/about) | Vetted-access application mechanism |
| LI-05 | LinkedIn — [Research application form](https://www.linkedin.com/help/linkedin/ask/DSA) | Official destination; full fields not inspected |
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
