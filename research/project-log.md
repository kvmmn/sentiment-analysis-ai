# Project Log

This is the shared record of actions, decisions, rationale, and open questions. All entries below concern work discussed on 2026-08-28. It summarizes the project conversation and file/tool checks; it is not a verbatim transcript or evidence that planned actions occurred. Keep earlier decisions visible when a later decision supersedes them.

## 1. Establish a minimal academic project

**Request:** support development, a scientific article, and a master's thesis, aiming for both outputs while recognizing that scope may change.

**Decision:** use the display name **Sentiment AI**, preserve the folder name `_saintimental`, and write project documentation in English. Start with plain Markdown and empty implementation space rather than choosing software or research methods prematurely.

**Completed:** README, contributor principles, ignore rules, research notes/references, data and experiment guides, separate article/thesis outlines, and `src/.gitkeep`. Shared research and experiment records support both outputs. No application code, dependencies, or experiment results were introduced.

**Initially deferred:** Git initialization, infrastructure, datasets, models, university requirements, and publication venue. Git synchronization was subsequently authorized in step 7; the other research choices remain open.

## 2. Record the collaboration

Kaveh supplied the GitHub repository `kvmmn/sentiment-analysis-ai`, the three team members and their LinkedIn profiles, and the Telegram group **Sentiment Analysis AI** as the main communication channel for now. These are recorded in the [README](../README.md).

No individual research roles, author order, student/thesis authorship, or institutional supervision were inferred. Public project documents belong in GitHub; a Telegram conversation does not replace the shared evidence record.

## 3. Preserve the first research sketch

Kaveh provided the first scratch document and asked for it to be restored in the proper project location. It was preserved as [initial-scratch.md](initial-scratch.md), with a separate organized summary in [notes.md](notes.md).

**Proposed direction:** sentiment about generative AI and deskilling in architectural discourse. The sketch distinguishes soft skills, hard skills, and stakeholder groups. It names LinkedIn, X, ResearchGate, podcasts, and YouTube as candidate sources.

**Interpretation:** these are questions about discourse and perceptions, not established evidence that GenAI causes deskilling. Source choices, sampling, keywords, labels, and methods are still proposals. The preserved original is not silently rewritten when the working interpretation develops.

## 4. Review the proposed LinkedIn pipeline

The team message proposed: create a developer app; configure OAuth and obtain credentials; send a test request; then apply for academic research access with institution/supervisor, research questions, required data, and privacy information.

Kaveh asked for a broad review before implementation. The [LinkedIn access review](linkedin-data-access-review.md) compares ordinary APIs, Research Tools/DSA routes, member and Page portability, own-data exports and participant contributions, institutional collaborations, existing datasets, manual collection, commercial scraping tools, and workflow tools. Sources are indexed in [references](references.md).

**Result:** app creation and OAuth do not establish broad post-search access or permission to build a research corpus. Eligibility, permitted use, retention, publication, and AI-training restrictions depend on the route. Vendor capability claims do not establish permission, coverage, or scientific validity. No scraper was run or purchased, and no suitable licensed corpus was verified.

**Reason for not building immediately:** a technically successful request could still provide the wrong sample or data the study cannot retain or use. Research eligibility and source permissions must inform the pipeline design. The question of model training versus applying existing models remains particularly relevant.

## 5. Start app registration, then switch to manual guidance

Kaveh chose to follow the group's developer-app sequence step by step after the review. A signed-in browser reached the app-creation form, and **GenAI Architecture Discourse Research** was entered as an unsaved app name. The form showed a required Page and logo, plus a privacy-policy URL field. No description field was present in that inspected form.

Kaveh manually selected **Chaharsotoon Engineers**, Page ID `17919559`. The form warned that this association cannot be changed after saving. This is a Page association, not a claim of academic affiliation or sponsorship.

Kaveh then instructed the assistant to stop operating Chrome and guide him in the conversation. That preference is recorded in [AGENTS.md](../AGENTS.md). Do not assume subsequent form actions happened without his confirmation.

**Last confirmed status:** no app submission, terms acceptance, credentials, OAuth test, approved API product, or corpus collection is recorded.

## 6. Simplify the visual identity

The design evolved from an S/dialogue mark to an architectural academic emblem with a wordmark, then to a much simpler professional symbol. Kaveh clarified that the result should be **only a logo, without writing**.

The current [PNG](../assets/sentiment-ai-logo.png) uses two opposing geometric quotation/bracket forms on white. Its bytes match the generated minimal-symbol output. Earlier prompts remain in [the asset record](../assets/README.md); only the current PNG remains in the project folder. No new image or restoration of discarded variants was needed during the privacy-policy task.

## 7. Prepare privacy disclosures and adopt GitHub as the reference

Kaveh requested a short privacy-policy file in GitHub, permission to make the repository public if needed, a careful official-source review, and ongoing synchronization of project work. The repository was checked and was already **public and empty**, so no visibility change was needed. This request supersedes the foundation's earlier decision to defer Git.

The [privacy-policy review](privacy-policy-review.md) records why the pasted Lead Gen explanation is not the governing research-access procedure. It also distinguishes the general API policy obligation from the Research Tools exception and its continuing transparency/contact requirements.

**Drafting choice:** publish an accurate preparation-stage policy. Do not invent a university sponsor, controller, active data collection, storage implementation, or granted permissions. Do not add arbitrary platform/model/retention constraints. Existing contractual and legal requirements still apply. A public policy cannot obtain access by itself.

**Hosting choice:** use one rendered Markdown file in the public repository. No website framework, local document tooling, or GitHub Pages deployment is necessary for this first URL. LinkedIn's acceptance of that URL must still be checked by Kaveh.

Kaveh authorized publishing both `kaveh.momeni@gmail.com` and `25199053@ardenuniversity.ac.uk` as his contact addresses. The policy and README list both. Other members' emails will be added when supplied and authorized. No test email was sent, and no institutional sponsorship is inferred from the domain.

Kaveh also requested documentation of all work and the path taken. This log summarizes decisions and alternatives; topic-specific reviews hold the detailed evidence. GitHub synchronization is a working practice, not an unattended automation.

## Current handoff and open items

- Publication and anonymous policy-URL verification are complete; see the checks below.
- Kaveh: enter the privacy-policy URL and complete the LinkedIn form manually if he accepts its terms and the fixed Page association. Report the resulting screen without secrets.
- Team: confirm institution/supervisor, study responsibility and legal basis, research eligibility, allowed data/fields, sampling and analysis versus training, retention, processors, and publication conditions before collection.
- Add other members' authorized contact details and confirmed roles when available.
- Preserve undecided university/venue requirements; there are no experiments or findings to report yet.

## Publication verification

Completed on 2026-08-28:

- Initialized Git on `main`, connected the existing repository as `origin`, and fetched before publishing. The remote had no existing commits to preserve. No visibility change or force push was used.
- Reviewed and published 17 files in initial commit `7e1f28c1980d60b3ca160bbf36ea4dfca20d0950`. This included the foundation, original scratch document, research reviews, policy, current logo, and this history. Dataset contents, secrets, and operating-system files were excluded.
- Checked 14 Markdown files, 52 relative links, 10 representative ignore-rule cases, both policy contact addresses, and the current logo hash. A simple secret-pattern scan found no matches; this is not a comprehensive security audit. Staged whitespace checks passed except for the deliberately excluded, unchanged original scratch document.
- Verified the [public policy URL](https://github.com/kvmmn/sentiment-analysis-ai/blob/main/PRIVACY.md) without authentication: HTTP 200, no login redirect, and the title and both contacts present. Its raw contents exactly matched the local file. Policy SHA-256: `56233606c253df81f99f25a068a75e6ea77ac001393a52d2e3875ad2f6fe4082`.
- Verified that local `HEAD` and GitHub `main` matched the initial commit after push. This verification record is saved in a subsequent documentation commit.
- Tooling issues were resolved without weakening security: restricted network/Git metadata operations used approved escalation; an anonymous Python HTTPS check failed because of its local certificate configuration, then system curl passed with TLS verification enabled.

No LinkedIn acceptance of the policy URL, app creation, access grant, inbox-delivery test, or research collection is implied by these checks. No Chrome actions were performed during the privacy-policy/publication work.
