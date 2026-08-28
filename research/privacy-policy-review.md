# Privacy Policy Review

Reviewed: 2026-08-28. Scope: the privacy-policy URL for the **Saintiment** application, initially proposed as **GenAI Architecture Discourse Research**, not approval to collect a corpus. This is implementation research, not a legal opinion or an institutional ethics determination.

## What the official sources establish

| Context | Finding and consequence |
| --- | --- |
| Ordinary developer application | API Terms §§5.1–5.2 require accessible, accurate privacy disclosures and appropriate member consent. They also address a user agreement, which a privacy policy does not replace. Describe actual collection, use, disclosure, storage, deletion, and withdrawal before account authorization. [API Terms](https://www.linkedin.com/legal/l/api-terms-of-use) |
| Research Tools | §1.3 removes the general privacy-policy/user-agreement obligation for that program. §3.2 still requires accessible contact mechanisms and clear information supporting individuals' rights. This exception does not waive applicable privacy law. [Research Terms](https://www.linkedin.com/legal/l/research-api-terms) |
| Lead Gen Forms | A dedicated privacy-policy page and use disclosures are required in that advertising workflow. It is not the project's proposed use case; the pasted AI response must not be treated as research-access guidance. [Lead Gen guidance](https://www.linkedin.com/help/linkedin/answer/a420012/lead-gen-forms-privacy-policy?lang=en) |
| Privacy law | Where GDPR applies, transparency includes the responsible organization, purposes, legal basis, categories, retention, and rights; indirectly obtained data also requires source information. Publishing a policy alone does not resolve notification duties or establish an exception. Jurisdiction and institutional responsibility still need confirmation. [European Commission](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/obligations_en) |

The Research Terms also restrict training AI on Research Data (§3.1(i)) and impose default storage ceilings of 24 hours for individual personal data and one year for other Research Data, subject to their documented exceptions (§4.1). The published policy must not promise longer retention or imply that generic research consent overrides these terms. See the [access review](linkedin-data-access-review.md) for the broader restrictions. Access approval and permission for a particular use are separate questions. [Research Terms](https://www.linkedin.com/legal/l/research-api-terms)

## Drafting decisions

The [policy](../PRIVACY.md) is intentionally a preparation-stage notice. It distinguishes current correspondence from future research, gives the actual app/project names, and avoids claiming an operating pipeline, approved access, a university sponsor, or implemented security controls.

It does not arbitrarily fix a platform, model, sample size, research storage period, hosting region, or blanket consent-only approach. Human annotation and computational analysis remain possible within source permissions. It does not impose a project-wide ban on model development using independently permitted data. No wording can remove restrictions already imposed by an access agreement or law.

Before research collection, confirm the controller/institution, study-specific legal basis, relevant special-category conditions if any, exact sources/fields, authorized team access, processors/locations and transfer safeguards, deletion schedule, and applicable participant/indirect-collection notices. Assess ethics and impact-assessment requirements with the responsible institution where applicable. These are operational decisions, not facts to invent for an application.

For current inquiries, the policy uses a narrow correspondence purpose and retention criteria, not indefinite research reuse. A working private contact route is necessary; a public issue tracker is unsuitable for personal-data requests. Kaveh confirmed both listed contact addresses for publication on 2026-08-28; delivery has not been tested. Other members' addresses remain unspecified. The university-domain address is not evidence of university sponsorship or a controller determination.

## Hosting and maintenance

The repository was verified through the authenticated GitHub CLI as **public and empty** on 2026-08-28. No visibility change is necessary.

The minimal approach is one root Markdown file, `PRIVACY.md`, viewed through GitHub's rendered file page. [GitHub file-view documentation](https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files) describes its Markdown preview. The intended public URL is `https://github.com/kvmmn/sentiment-analysis-ai/blob/main/PRIVACY.md`.

**Hosting assessment, not a LinkedIn guarantee:** a public rendered file can expose the complete statement over HTTPS without project-specific infrastructure. No source reviewed expressly certifies GitHub blob URLs for LinkedIn app review. Confirm anonymous access after publication, and let Kaveh enter the URL manually. If LinkedIn requires a standalone web page, GitHub Pages can publish from a branch without local dependencies; it is not enabled for this task. [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

GitHub becomes the shared reference for publishable project work. Review changes for secrets and personal data before committing; synchronize completed work and report failures. This is a contribution workflow, not a background automation. Keep restricted data outside the public repository, even if future research permissions allow storing it elsewhere.

## Verification status

- Official documentation reviewed; no LinkedIn browser actions or form submission performed in this task.
- Public contact addresses: supplied and authorized by Kaveh; inbox delivery not tested.
- Published in initial commit `7e1f28c1980d60b3ca160bbf36ea4dfca20d0950` on `main`. The [public policy page](https://github.com/kvmmn/sentiment-analysis-ai/blob/main/PRIVACY.md) returned HTTP 200 without authentication or a login redirect; both contacts were present. The public raw file matched the local policy byte for byte. No GitHub Pages site was created.
- LinkedIn acceptance and research-access approval: not verified.
