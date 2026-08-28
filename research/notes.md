# Research Notes

Status: initial research direction proposed, not a finalized study design. No data have been collected or findings established in this project.

Source: [initial scratch document](initial-scratch.md), supplied by Kaveh Momeni on 2026-08-28 and preserved unchanged. Supplying the document does not establish its authorship. The working summary below lightly edits wording for clarity; the original remains the source for the initial ideas.

## Problem

Working title from the scratch document: **Sentiment Analysis of GenAI Applications in Architectural Discourse: Deskilling**.

The proposed study examines sentiment about generative AI (GenAI) and deskilling in architectural discourse, with questions about soft skills, hard skills, and differences between stakeholder groups.

This is a proposed investigation of discourse and perceptions. It does not establish that GenAI causes deskilling or directly measure changes in skills.

## Research Questions

These questions are provisional. The skill groupings and terms come from the scratch document and require clarification and literature support.

| ID | Working question |
| --- | --- |
| RQ1 | What are the overarching sentiments in discussions of GenAI and deskilling in architectural discourse? |
| RQ2 | What sentiments concern soft skills in architectural discourse around the emergence of GenAI? |
| RQ2a | What sentiments concern creativity and design thinking? |
| RQ2b | What sentiments concern cognitive skills and judgment? |
| RQ3 | What sentiments concern hard skills in architectural discourse around the emergence of GenAI? |
| RQ3a | What sentiments concern technical skills, including environmental design skills? |
| RQ3b | What sentiments concern representation, including digital and computational skills? |
| RQ4 | Does sentiment about deskilling differ between practitioners, academics, students, and industry leaders? |

## Methodology Ideas

The scratch document lists LinkedIn, X, ResearchGate, podcasts, and YouTube as candidate search areas. These are not confirmed datasets or approved collection methods.

The data-gathering and keyword-search sections are blank in the original. Collection procedures, search terms, sampling, labeling, models, and evaluation are still TODO. No research-corpus collection has been initiated.

### LinkedIn Access Review — 2026-08-28

The team proposed investigating LinkedIn's official research-access route. The initial focus was reviewing methods, tools, and access conditions before implementation. See the [LinkedIn data access review](linkedin-data-access-review.md) for verified documentation, route comparisons, unresolved permissions, and recommendations. At the time of that review, no app or pipeline had been created. Later app creation is recorded below; it does not establish research eligibility or approve collection.

### Developer Setup Progress — 2026-08-28

After the review, Kaveh requested following the group's proposed developer-app route step by step. The signed-in Chrome session reached the [Create an app form](https://www.linkedin.com/developers/apps/new). The proposed name, **GenAI Architecture Discourse Research**, was entered as an unsaved draft.

The live form requires a LinkedIn Page association and an app logo. It warns that the Page association cannot be changed after saving; a personal member profile cannot substitute for the Page. The privacy-policy URL is displayed without a required marker.

Kaveh manually selected **Chaharsotoon Engineers** as the app's LinkedIn Page; the form confirmed the selection and linked to company ID `17919559`. This records the app association only, not university affiliation or research sponsorship. Three [Sentiment AI logo candidates](../assets/README.md) were generated. The current project asset is the minimal symbol without text. At this draft-form stage, no terms acceptance, app submission, credentials, logo upload, or data collection had been confirmed.

Kaveh subsequently requested guidance in the conversation only, without further Chrome operation. He performs the remaining LinkedIn form actions manually.

### Privacy Policy and Shared Repository — 2026-08-28

Kaveh requested a concise privacy policy hosted in GitHub, a substantive requirements review, and GitHub as the shared reference for ongoing work. The repository was verified public and initially empty. See the [privacy-policy review](privacy-policy-review.md) for the distinction between ordinary API, research, and Lead Gen obligations, and the [policy](../PRIVACY.md) for the preparation-stage notice. Its future-research provisions do not assert granted access or a finalized study protocol.

Kaveh supplied his Gmail and Arden University email addresses for publication as contact channels. Other team emails remain pending. These addresses do not establish institutional approval or determine who will be the research data controller.

The [project log](project-log.md) records the chronological decisions, rationale, progress, and outstanding work across the project.

### Created App: Products PDF Review — 2026-08-28

Source: Kaveh's local `List_Products_AppDetail_Developers_LinkedIn.pdf`, two pages, printed at 15:34 on 2026-08-28. Both pages were extracted and visually inspected. The original PDF and temporary renders are kept local and ignored by Git; the public summary omits developer identifiers. A Client ID is not a Client Secret, but neither identifier is needed in this public record.

Source SHA-256: `3e9739e527353cd026e36ffbd72d22808996ce392307fddde6181ca24db44b12`.

**Observed:** the app header shows **Saintiment**, the selected symbol, a Client ID, creation date 28 August 2026, and type **Standalone app**. This confirms app creation and logo use. The Products tab lists 13 products with **Request access** labels under **Available products**. No approved product is shown. The PDF does not reveal Page-association verification, granted OAuth scopes, redirect settings, token validity, or successful data access. Gray printed labels do not establish the live controls' enabled state or its cause.

| Products visible in the PDF | Relevance to the next decision |
| --- | --- |
| Sign In with LinkedIn using OpenID Connect | Could support a narrow, authorized authentication test and basic profile retrieval. It does not provide a discourse corpus. Request only if that test is needed after considering product constraints. [OIDC documentation](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2) |
| Member Data Portability API (Member); Member Data Portability API (3rd Party) | The printed descriptions distinguish access to one's own data from member-authorized third-party access. Neither description promises unrestricted public-post search. Eligibility and the special setup conditions in the [access review](linkedin-data-access-review.md) still need checking before choosing either route. |
| Pages Data Portability API | A possible route for an explicitly authorized Page sample, not platform-wide discourse. [LinkedIn's application guide](https://www.linkedin.com/help/linkedin/answer/a6220307) |
| Community Management API | A vetted product for management and analytics use cases. Its documentation says new Development Tier applications must not already have other API products; it also says `r_member_social` is closed to new requests. Do not enable another product merely to test the interface before making this choice. [Community Management overview, FAQs 4 and 6](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-04) |
| Share on LinkedIn; Advertising API; Lead Sync API; Matched Audiences API; Conversions API; Live Events; Events Management API; LinkedIn Ad Library | Their listed purposes are publishing, advertising/leads, conversions, events, or ad data. None is a reason to request access for the current general-discourse study without a matching use case. |

**Recommended next action at the PDF-review stage:** inspect **Settings** for the Page association's verification status. If unverified, use **Verify → Generate URL**, and have an authorized Page super admin approve the association. The selected company functions as the app publisher; this is not a university endorsement, blue-badge Page verification, or research-access approval. Do not share the generated verification link publicly. [Official app-verification procedure](https://www.linkedin.com/help/linkedin/answer/a1665329)

After that, choose the actual product route before requesting scopes or configuring an OAuth test. No Research Tools product appears in this PDF. LinkedIn documents a separate [research-access application](https://www.linkedin.com/help/linkedin/answer/a1645616), subject to eligibility; none of the displayed products should be treated as its substitute. The current study's eligibility remains unresolved.

### Page Association Verified — 2026-08-28

Kaveh's Settings screenshot, supplied at 15:40, shows **Chaharsotoon Engineers — Verified: Aug 28, 2026**, app name **Saintiment**, the chosen logo, and the saved URL `https://github.com/kvmmn/sentiment-analysis-ai/blob/main/PRIVACY.md`. Kaveh states that he is the Page admin and completed the approval himself. This confirms the app-to-Page association and saved privacy URL; it does not establish a substantive privacy review, product approval, or research-data access.

The next action recommended at this stage was to inspect **Auth** without sharing secrets or changing configuration. The resulting observations are recorded below. No screenshot was copied into the public repository.

### Auth Configuration Inspected — 2026-08-28

Kaveh supplied two Auth screenshots. They show a Client ID, a masked Primary Client Secret field, **No redirect URLs added**, and **No permissions added**. The displayed access-token lifetime is **2 months (5,184,000 seconds)**. This is a configured lifetime, not evidence of an issued token or a guarantee that any issued token will remain valid that long. No secret value was exposed in the screenshots, and no credential values or images are copied into this public record.

The app therefore has no displayed OAuth scopes for the proposed data test. Adding a redirect URL or generating a new secret would not grant data permissions. LinkedIn's documentation ties permissions to products/programs and requires authorization and authentication for data access. [Getting access, rechecked 2026-08-28](https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access)

**Recommended next step:** Kaveh should open the [official DSA research-access form](https://www.linkedin.com/help/linkedin/ask/DSA) while signed in, inspect the questions, and share only blank/non-sensitive form content before submitting anything. The public web check still exposes only a sign-in page, so the form's actual fields have not been verified. Do not enable an unrelated product just to obtain a token; preserve the existing product-selection options. No new secret, token, or callback configuration is needed for this inspection.

This adjusts the group's proposed order: check access eligibility before implementing the research OAuth/test request. The reason is the study's need for discourse data, not merely a working sign-in flow. LinkedIn's public-data research program requires a contribution to understanding specified systemic risks in the EU; academic status alone does not establish eligibility. The existing GenAI/architectural-deskilling questions have not yet demonstrated that fit. Do not manufacture a risk justification to match the application. [Researcher guidance, rechecked 2026-08-28](https://www.linkedin.com/help/linkedin/answer/a1645616)

## Decisions

On 2026-08-28, Kaveh chose **Saintiment** as the project and LinkedIn app display name. It supersedes **Sentiment AI** and the earlier proposed app name **GenAI Architecture Discourse Research**. This changes naming only; the research direction, repository URL, `_saintimental` folder, and Telegram group name are unchanged. See the [project log](project-log.md) for the form screenshot's observed status.

No research-design decisions have been confirmed. The questions and source areas above remain proposals for team discussion.

## Open Questions

The following are planning questions added while organizing the draft, not decisions from the original document.

- How will deskilling, soft skills, hard skills, and the proposed subcategories be defined and supported by literature?
- What will sentiment refer to: GenAI generally, its effect on a specific skill, or deskilling? How will sentiment be distinguished from agreement with a deskilling claim?
- Which source areas are feasible, and what access, privacy, ethical, and reuse requirements must be checked before collection?
- What languages, time period, search terms, sampling approach, and unit of analysis will define the dataset? Will audio or video sources require transcripts?
- How will stakeholder groups be identified from sufficient evidence, including overlapping or unknown roles?
- What labeling approach, baseline methods, and evaluation criteria will be used?
