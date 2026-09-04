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

**Status at that stage:** no app submission, terms acceptance, credentials, OAuth test, approved API product, or corpus collection was recorded. The later Products-page evidence in step 9 supersedes the app-creation and Client ID status.

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

## 8. Choose the name Saintiment

Kaveh chose **Saintiment** as the project and LinkedIn app display name on 2026-08-28. This supersedes **Sentiment AI** and the earlier app-name suggestion **GenAI Architecture Discourse Research**. The current README, privacy policy, writing outlines, asset guide, and contributor instructions were aligned with the new name. Historical entries, original image prompts, and the original research sketch retain their earlier wording.

The supplied form screenshot still displays the earlier app name and the validation message “You must provide a name for your app.” It does not show Saintiment saved or establish why the error occurred. Guidance was to enter `Saintiment` in the App name field manually. No browser actions or successful registration are claimed.

The folder `_saintimental`, repository `kvmmn/sentiment-analysis-ai`, policy URL, Telegram group **Sentiment Analysis AI**, and existing text-free logo remain unchanged. This is a naming decision, not a change to the research scope or evidence of trademark/domain availability.

Local verification passed: current document headings and the policy use Saintiment, relative Markdown links resolve, and the original research sketch and current logo remain byte-identical to their prior committed versions. Earlier publication hashes below describe the initial policy, before this naming update.

## 9. Inspect the created app's Products page

Kaveh supplied a two-page PDF of the Products tab, printed on 2026-08-28 at 15:34. Both pages were read and visually inspected. The header confirms the created **Saintiment** standalone app, a Client ID, creation date, and the chosen logo. The page lists 13 available products with Request access labels, but no approved product or successful OAuth/data request.

The [setup notes](notes.md) record the product groups and verified guidance. A useful new constraint emerged: Community Management's documented initial Development Tier route requires a new app without other API products. Accordingly, do not automatically request OIDC or Share on LinkedIn just because they are listed. OIDC can test sign-in, not retrieve a research corpus.

The immediate recommendation is to inspect Settings and, if needed, verify the app's association with its Page through an authorized super admin. The PDF cannot establish why the request labels appear gray. Research access remains a separate eligibility/application question.

The raw developer-console PDF was left unchanged and excluded from public Git history, together with temporary page renders. Only the summary and public documentation links are shared. No browser actions, product requests, authorization, or API calls were performed during this review. The README, privacy-policy app description, and asset status now reflect confirmed app creation.

## 10. Confirm Page-association verification

Kaveh reports completing verification himself as the Page admin. His Settings screenshot shows **Chaharsotoon Engineers — Verified: Aug 28, 2026**, app name **Saintiment**, the selected logo, and the correct GitHub privacy-policy URL. The app-to-Page association and saved URL are now confirmed. This does not prove product approval, an OAuth test, research eligibility, or substantive review of the policy.

The next suggested step is to inspect the Auth tab's OAuth settings and scopes without sharing secrets or tokens and without changing configuration yet. Product selection remains open. The screenshot itself was not uploaded to GitHub, and no browser action or API call was performed by the assistant.

## 11. Inspect OAuth configuration and prioritize access eligibility

Two Auth screenshots supplied by Kaveh show the Client ID and masked Primary Client Secret field, no authorized redirect URLs, and **No permissions added**. The displayed token lifetime is two months (5,184,000 seconds); it is not evidence of token issuance. No plaintext secret was visible. The screenshots and credential values were not copied into the repository.

The app's registration and Page verification have not provisioned the research permissions. The recommended next step is to inspect the official DSA research-access form without submitting it. The public form URL still requires sign-in, so its questions remain unverified. The original plan's OAuth implementation/test is deferred until the relevant permission route is established; an identity-only test would not validate access to the required discourse data.

The [setup notes](notes.md) link the official documentation rechecked for this decision and preserve the unresolved EU systemic-risk eligibility requirement. No product was requested, secret rotated, redirect set, token generated, or API tested. This is a recommended sequence, not a confirmed eligibility decision or a claim that an application was submitted.

## 12. Read the actual research application

Kaveh provided the three-page research contact-form PDF, printed at 15:46 on 2026-08-28. All pages were extracted and visually inspected. Unlike the earlier public sign-in page, this shows the actual Article 40(12) application questions. The closed dropdown choices and conditional behavior remain unknown.

The [application worksheet](linkedin-application-worksheet.md) records the questions, known answers, missing facts, declaration, and source hash. Two key answers have a **250-character** limit. No supervisor-specific field is visible, although organization, department, role, and organizational profile information are requested. Existing email and company-Page details must not be mistaken for research sponsorship.

The recommendation is to clarify institutional/independent status and research eligibility before drafting submission-ready answers. No funding source, security implementation, storage location, GDPR responsibility, or systemic-risk objective was invented. Existing API/publication intentions are recorded as intentions. No form was submitted. The original account-page PDF and its renders remain local and excluded from Git; only the worksheet and summary are published.

## 13. Clarify the contact email and organization distinction

Kaveh confirmed Gmail as his primary, long-term email, mentioned an additional company-domain mailbox address, and stated that he does not have admin access for the university. He described the app/project as registered under the company, consistent with the verified Page association. This does not yet establish who formally conducts, funds, or takes responsibility for the research.

The recommendation is to use Gmail in **Email Contact**, rather than choose a domain for its appearance. No same-domain or academic-domain requirement was found in the supplied form or reviewed public researcher guidance. Additional evidence could still be requested by LinkedIn. The university address remains an additional published contact; the newly mentioned company address itself was not added to public records.

The worksheet now distinguishes contact email, the verified app publisher, and actual research affiliation. No Page reassociation, change to the live form, or claim of academic sponsorship was made. The open question is the company's actual role in the research, beyond publishing the app.

## 14. Confirm Chaharsotoon's limited role

Kaveh clarified that Chaharsotoon provides **only its LinkedIn Page** for the app association, rather than conducting or funding the research. The worksheet now records this distinction. The existing verified app association is unchanged; Chaharsotoon should not be named as the research organization solely because it is the app publisher.

Gmail remains the recommended application contact. The remaining affiliation question is whether this research is formally part of Kaveh's Arden studies or currently an independent group effort. Other funding sources, commercial-purpose details, and data-protection responsibility are not inferred from the company's limited role. No form fields or account settings were changed.

## 15. Record intended Arden dissertation use

Kaveh clarified that he wants this research to form part of his dissertation at Arden University, but that this is not yet finalized. The README, thesis outline, and application worksheet now distinguish this intention from institutional approval, sponsorship, or responsibility. The research remains a collaborative project; no new research purpose or eligibility claim was inferred.

The worksheet also refines the earlier organization question: the form's organization fields appear under About You/Research Team, so an applicant's actual student affiliation can be described separately from the project's approval status. Confirm the exact current degree/program and department before specifying the role. Gmail remains the primary contact, and the app's existing company-Page association stays unchanged. No form was submitted.

## 16. Recover existing academic context

After Kaveh pointed out that his academic background had already been discussed, the assistant checked existing local academic records. The Assignment Brain README explicitly identifies his studies as **MSc Data Science at Arden University Berlin**. The application worksheet now records this context instead of asking him to repeat it. Private academic records and the student identifier were not copied into this project.

The role can be described as master's student; the official department name and the form's available role choices remain unverified. This does not change the unfinalized status of Saintiment's dissertation integration, imply university approval, or establish research-access eligibility. No form was submitted. Future clarification should first use the available project and academic context.

## 17. Prepare the first form fields

On 2026-08-28, the official Arden Berlin campus page was checked for its address and linked in the application worksheet and references. The recommended first step is to enter known identity and student-affiliation details, inspect the Job Title choices, and leave the Article 40(12) eligibility answer unresolved. LinkedIn's current researcher-access guidance was rechecked: an academic project alone does not establish the required systemic-risk fit. Do not submit while that and the research/privacy answers remain unresolved. No live fields were entered, saved, or submitted by the assistant.

## 18. Select the academic email for this application

Kaveh agreed to use **25199053@ardenuniversity.ac.uk** in the research form's Email Contact field, matching his Arden student affiliation. This supersedes the earlier Gmail recommendation for this application only. **kaveh.momeni@gmail.com** remains his primary, permanent project contact; the README and privacy-policy contact listings remain unchanged. The choice does not assert a LinkedIn domain requirement, university approval, or a change to the app's Chaharsotoon Page association. The worksheet was updated; no live form entry or submission was performed or confirmed.

## 19. Clarify the Article 40(12) planning question

Kaveh asked whether to answer Yes or No to the exact question about planning research under Article 40(12). LinkedIn's official researcher guidance was rechecked on 2026-08-28. The question concerns intended research under that framework, not prior university or LinkedIn approval. For the unchanged study, the assistant recommends No if a binary answer is needed and pausing submission: the current sentiment/GenAI/architectural-deskilling purpose has not established the required EU systemic-risk contribution. This is a provisional assessment, not a categorical exclusion of the topic or a user-selected answer.

Yes should follow a genuine research plan satisfying the relevant purpose and conditions, not a fabricated justification for access. LinkedIn's guidance says other public-data research projects are not currently supported, so No must not be presented as an alternative general academic API route. The live form's response to either option is unverified. No form was changed or submitted.

## 20. Draft the remaining form guidance

Kaveh asked to continue through the rest of the form. The worksheet now includes conditional guidance for the remaining team, funding, research, and privacy questions and a provisional 237-character research summary. The summary explicitly leaves timeline and data scope unresolved and is not a complete proposal for submission. No durations, funding sources, commercial-purpose declarations, storage locations, implemented security controls, or responsible persons were invented. API access and publication remain known intentions. No user selection, form entry, or submission is implied by this preparation.

## 21. Record the submitted case and correct the duration interpretation

Kaveh reported selecting three months because a selection was required and submitting the form. His one-page case-details PDF, printed on 2026-08-28 at 16:19, was extracted and visually reviewed. It confirms a DSA Researcher Access (Beta) case with status **Open**, the submitted answers, and an automated acknowledgement. It is not a human eligibility decision or API approval. The raw PDF, case number, and account-specific case URL remain local and are excluded from public Git; the original PDF is unchanged.

The receipt shows **3 Months** under expected data **storage**, not collection. The assistant's initial response to the upload incorrectly described this as a collection duration; the receipt corrects that interpretation. The earlier blank-form PDF does contain a separate collection-duration field, but no value for it appears in this case receipt. Do not infer a three-month collection window, a fixed deletion date, or permission to retain personal data for three months from this selection. Kaveh's report also corrects the practical suggestion to leave the relevant duration selection blank.

The submitted answers include Article 40(12): No; Arden student affiliation and email; API and publication: Yes; self-funded with no external funding; commercial purpose: No; storage country: Germany; external access beyond the identified researchers: No; and no previous applications. These are evidenced declarations, not independent verification of infrastructure or all eligibility conditions. The submitted proposal is the earlier 237-character summary with timeline and data scope still unfinalized. The application record now replaces obsolete preparation-only status with the receipt evidence and remaining follow-up needs. Form submission with No produced a case; it does not establish an alternative access entitlement. No follow-up message, closure, browser action, or automated monitoring was performed by the assistant.

## 22. Draft keywords, search limits, and storage

Kaveh asked to work on the Telegram-group questions: which keywords to search, how far to search, and how to store posts and comments. A working proposal is in [keywords-search-storage.md](keywords-search-storage.md).

**Decision recorded as a draft, not a team vote:** use two query layers (architecture + GenAI discovery, then skill terms) so deskilling language does not select the sample; keep English, Persian, and German lists separate; propose a first time window from 30 November 2022; store one JSONL record per item under gitignored `data/local/`. Sentiment words are for later coding, not retrieval.

**Not decided:** which terms to keep, whether Persian or German runs proceed, first permitted platform, comment depth, and the retention clock if LinkedIn access is offered (form: three months in Germany; Research Tools default for personal data can be 24 hours).

**Reason for not collecting:** the LinkedIn case remains Open; this lexicon is not a harvest plan. No scraper, API call, or dataset file was added.

## 23. Organize the full keyword catalog

Kaveh asked for a complete, categorized, sorted keyword list aimed at the project questions. The seed tables in the earlier search note were replaced by [keyword-lexicon.md](keyword-lexicon.md): a core set plus full English sections for architecture, GenAI, RQ1–RQ4, exclusions, and optional Persian/German/hashtag lists. Terms are sorted inside each category. This remains a working catalog, not a validated retrieval study or a collection licence.

## 24. Keyword-systems expansion — three instruments, two layers

On 2026-08-31 the project recorded a keyword-systems expansion **on this repository only** (no social corpus scraped, no live database counts run, no new dependencies).

**Decisions:**

1. **Three instruments never mixed:** literature retrieval ([keyword-literature-strings.md](keyword-literature-strings.md)), discourse-retrieval catalog ([keyword-discourse-catalog.md](keyword-discourse-catalog.md)), sentiment/stance coding lexicon ([keyword-lexicon.md](keyword-lexicon.md) English tables preserved).
2. **Two layers:** Layer A = architecture AND GenAI (RQ1 sampling frame); Layer B = skill/deskilling/authorship/judgment as second filter. Deskilling must **not** select the sample.
3. Construction/AEC/built environment/sociotechnical strings = **related-work only** (`S-RW1`), not primary RQ1.
4. **Do not cite 71 opinions / 6173 words as published** until a PDF is verified. Exact dual match of teammates' Scopus four-block plus LinkedIn _n_ was **not** identified in open full text on 2026-08-31.
5. **Verified analogue:** Ghimire, Kim and Acharya (2024) _Buildings_ 14(1):220 — 32 opinions / 63,778 words, construction professionals, LinkedIn (KS-01).
6. **Closest unread:** Larbi et al. (2026) TFSC 228:124689 — closed OA; 71/6173 unverified; author 76% positive is not a sample-size claim (KS-02).
7. Primary literature strings: **S-A1** (Scopus), **W-A1** (WoS); no LIMIT-TO Engineering; I-A1 (IEEE) and G-A1a–c (Scholar) are supplements.
8. EN/FA/DE lists separate; GAPs marked; no invented translations or hashtags.
9. Query version 1 is **NOT frozen**.

**New files:** [keyword-systems.md](keyword-systems.md), [keyword-source-identification.md](keyword-source-identification.md), [keyword-literature-strings.md](keyword-literature-strings.md), [keyword-discourse-catalog.md](keyword-discourse-catalog.md).

**Updated:** README current status, keyword-lexicon top map (pointers only), keywords-search-storage pointer, references KS-\* records, notes methodology pointer, article Related Work pointer. [initial-scratch.md](initial-scratch.md) bytes preserved.

**Verification:** Remote `main` fetched before branch; secret-pattern scan before commit; PR against `main`; no force push.

## 25. Public HTML keyword catalog (2026-08-31)

Added a static browser catalog at [docs/index.html](../docs/index.html) (with [docs/.nojekyll](../docs/.nojekyll) for GitHub Pages). The page presents current EN/FA/DE keywords and English coding lists from the existing markdown sources for team review before the next decision. Query version 1 remains **not frozen**. No collection authorised. The 71-comments figure is **not cited** as a published fact.

## 26. Catalog HTML simplified for teammate reading (2026-08-31)

Replaced the public [docs/index.html](../docs/index.html) layout with a quieter single-column page (cream paper, no color legend, no duplicate EN discourse block). Visible sections show search / screen / do-not-search lemmas once; full IT exclusions, construction/AEC strings, Scopus S-A1, and lexicon §1–7 / §10 remain in closed `<details>`. **Lemmas unchanged** — keyword markdown sources not edited.

## 27. Catalog HTML English UI (2026-08-31)

Public [docs/index.html](../docs/index.html) interface copy is English-only LTR; Persian and German keyword chips unchanged.

## Current handoff and open items

- Publication and anonymous policy-URL verification are complete; see the checks below.
- The submitted application uses the Arden email; retain Gmail as the permanent project contact.
- The case is Open in the supplied receipt with an automated acknowledgement. Await a substantive support response through the same case and academic mailbox; no response deadline, access grant, or authorization test is confirmed. Read the application record before preparing any reply.
- Team: review the [keyword systems map](keyword-systems.md), [literature strings](keyword-literature-strings.md), [discourse catalog](keyword-discourse-catalog.md), and [keyword lexicon](keyword-lexicon.md); confirm institution/supervisor, study responsibility and legal basis, research eligibility, allowed data/fields, sampling and analysis versus training, retention, processors, and publication conditions before collection.
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

## 24. Integrate team scraper and run first controlled test (2026-09-03)

**Context:** a team member contributed a Playwright-based LinkedIn post scraper in `linkedin-scraper/` (scraper.py, keywords.txt, linkedin_posts.csv with 67 posts from a prior run). The LinkedIn DSA Researcher Access case remains Open; this is a pre-API-access exploration.

**Completed:**

- **Repository preparation:** pulled 12 remote commits (keyword catalog work from 2026-08-31), created `_local/` folder for local-only work (git-ignored except README), updated `.gitignore` to protect scraper runtime artifacts (`linkedin_session/`, `linkedin_posts.db`, `scraper.log`, `debug/`).
- **Documentation:** added `linkedin-scraper/README.md` (purpose, setup, usage, security, limitations) and `requirements.txt` (playwright>=1.40.0).
- **Commit and push:** `be67e98` — 7 files, 4103 insertions. Verified sync: local and remote both at `be67e98`.
- **Environment setup:** installed Playwright 1.62.0 and Chromium 151.0.7922.34 on macOS ARM64 with Python 3.12.8.
- **Test run:** executed with `MAX_POSTS_PER_KEYWORD=5`, `MAX_SCROLLS=10` (reduced from 30/35 for quick trial). All 7 keywords processed in ~2.5 minutes. 41 new posts collected. Parameters reverted to original values after test.
- **Test documentation:** `_local/scraper-test-log.md` records configuration, environment, per-keyword results, data quality analysis, and 6 identified issues.

**Issues found in test:**

1. 🔴 Metric extraction (`reactions`, `comments`, `reposts`) returned `None` for all 41 new posts — LinkedIn DOM may have changed since the prior run (which captured metrics correctly).
2. 🔴 `posted_relative` extraction never worked — 0/168 posts have a timestamp.
3. 🔴 DB path is relative to CWD, not script location — DB was created in project root instead of `linkedin-scraper/`.
4. 🟡 `load_keywords()` log message says "Created" even when file exists.
5. 🟡 CSV keyword quoting uses triple quotes (`"""future of architects"""`).
6. 🟢 `author_headline` extraction inconsistent.

**What worked:** login flow, search URL construction, post text extraction, dedup/merge across keywords, incremental CSV export, session persistence across keywords.

**Not decided:** whether to fix the scraper issues now or wait for API access; whether the CSV data should remain in the public repository long-term.

**Open:** the 67 posts from the prior run (2026-09-02) were in the committed CSV but the DB from that run was not preserved. The test run created a fresh DB with only the 41 new posts. The combined CSV (168 rows) includes both runs with overlap handled by dedup.

**Decision (2026-09-03):** before modifying code, run a second test with longer wait times and more scrolls (`INITIAL_WAIT_MS=10000`, `SCROLL_WAIT_MS=4000`, `MAX_SCROLLS=15`) to determine whether the metric extraction failure is a timing issue or a DOM change requiring code fixes. Document both runs in `_local/scraper-test-log.md`. Only fix code if the parameter variation confirms the extraction logic itself is broken.

**Run #2 result (2026-09-03):** 47 posts collected. Metrics still 0/47 despite 2× wait times. Confirmed: **timing is not the issue — LinkedIn changed their DOM** between 2026-09-02 (when metrics worked) and 2026-09-03 (when they stopped). `posted_relative` was never working (0/168 in original run). **Decision: code fix required** — update `EXTRACT_JS` metric extraction regex and `posted_relative` header-line parsing. Parameters reverted to original after test.

**Narrative assessment (2026-09-03):** We took a teammate's LinkedIn scraper and ran two controlled experiments. The scraper itself is solid — login, search, text extraction, dedup, and CSV export all work correctly, collecting 41–47 posts across 7 keywords in ~2 minutes with zero errors. But two critical fields came back empty: engagement metrics and relative post dates. The original run from the day before had captured metrics, so we tested whether longer wait times would fix it. They didn't. This confirmed LinkedIn changed their page structure overnight, breaking the metric extraction code. The date extraction never worked at all — a pre-existing bug. The path forward is clear: inspect LinkedIn's current markup and update the JavaScript extraction function to match the new selectors, then rewrite the date parser.

**Run #3 — code fix verification (2026-09-04):** Four fixes applied after live DOM inspection. Metric extraction now uses a 3-strategy approach (aria-label → last-3-numbers → regex fallback), matching LinkedIn's 2026 DOM where engagement counts appear as unlabeled numbers at the end of post cards. `posted_relative` now matches the `2d •` / `16h •` format. DB path fixed to `Path(__file__).parent`. `load_keywords()` log corrected. **Results: reactions fill rate improved from 0% to 41%, posted_relative from 0% to 95%.** Remaining None metrics are from article posts and company pages (different DOM). All parameters reverted to original. Fixes committed in `linkedin-scraper/scraper.py`.
