# Run: 2026-09-17-iman-live-pilot/001-collector

**Current status — 2026-09-17: interrupted; incomplete interruption provenance.** The collector started at `2026-09-17T20:49:14.700Z` and was subsequently stopped by the assistant without a user request. Exact end time and exit outcome are unavailable. Analysis 002 remains blocked and not run. Login outcome and collected count are not established.

**Historical boundary:** the sections below through “Expected artifacts and validation” preserve the pre-run registration verbatim. Their planned/pending/no-execution statements describe that earlier state, not the current outcome. The [dated amendment](#dated-amendments) overrides them where evidence is now available.

## Identity and lifecycle

- [Experiment plan](../../2026-09-17-iman-live-pilot.md) · [Run guide](../README.md) · [Analysis handoff](002-analysis.md).
- Question: can the prepared collector produce a usable local DB? Entry point: `code/collector.py`, `main()`.
- Mode: user-authorized local live collection; **platform permission not established**. The user's explicit authorization on 2026-09-17 is not LinkedIn approval or runtime consent evidence; see the [access record](../../../research/access/linkedin-application-worksheet.md).
- Status: **planned**. Primary agent intends to launch separately; no live execution or results are evidenced in this record.
- Registered date: 2026-09-17; exact registration time, operator/reviewer identity: TODO; actual start/end: not recorded, no execution claimed.
- Parent/retry-of: none. Earlier synthetic/static checks are not collector runs.
- Private workspace and required launch CWD: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/_local/work/2026-09-17-iman-live-pilot/runs/001-collector/`.
- Existing [private preparation record](../../../_local/work/2026-09-17-iman-live-pilot/runs/001-collector/README.md) is local-only. This public record holds reviewed metadata; pending sensitive metadata belongs in `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/manifest.json` (not present at documentation inspection).

## Preflight and open gates

- [x] User explicitly authorized the local live run; authorization distinguished from platform permission.
- [x] Prepared snapshot and its newline-only difference documented from supplied preparation evidence.
- [ ] Actual branch/base/execution commit, dirty state and relevant diff/hash captured.
- [ ] Fresh workspace state and frozen snapshot hash reverified immediately before launch; no existing output DB, cookies or profile reused.
- [ ] Fresh browser profile selected and actual path/version recorded privately; no copied cookies or old sessions. Fresh-profile use is required, not a verified runtime event yet.
- [ ] Exact dependency inventory, invocation, configuration and log capture recorded in manifest.
- [ ] Scope, access conditions, stop conditions and retention/deletion reviewed; missing platform permission evidence remains explicit, not presumed approval.

## Code and configuration

- Preserved source: `_local/submissions/2026-09-06-iman-protocol-drafts/working-copies/collector.py`.
- Original SHA-256: `cd31372b9d0bdff414c0e427b754e0fb52011eb00db604a28142f4a43f61fa37`.
- Prepared snapshot: `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/code/collector.py`.
- Snapshot SHA-256: `5d06c0f9b25501950cede7211b42416fb80719499b0e4a5d341255331f179386`.
- Change: CRLF-to-LF normalization only; not byte-identical. Originals remain preserved. These are preparation hashes, not post-execution hashes.
- Source-reviewed configuration: **24 embedded queries; 35 scrolls**. Query version 1 is **not frozen**; no query fixes are claimed. Record all other actual configuration, seed or absence of seed, retrieval timestamps and browser nondeterminism in the manifest.
- Source-reviewed login guard waits for `nav.global-nav` with `timeout=300000` after a manual-login warning. The earlier AST check is not proof of successful login, consent or collection.

## Environment and execution

- Existing environment reused: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv`; intended interpreter: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python`, Python **3.13.11**. Actual executed interpreter path must still be captured.
- Reported host: macOS **26.6.2**, **arm64**; other hardware and browser/driver versions: TODO.
- Reported completed dependency installations: `numpy`, `pandas`, `scipy`, `pyarrow`, `statsmodels`, `scikit-posthocs`, `scikit-learn`, `jinja2`. Exact versions/full inventory and inventory hash: pending manifest; do not infer them from installation success.
- Deviation: reused the repository environment instead of a dedicated experiment environment. Record its per-run inventory and do not change it mid-run.
- Exact invocation, actual launch CWD, UTC start/end, duration, exit code/signal, warnings and interruptions: **pending actual execution**. No command is executed by this documentation task.
- Planned stdout/stderr/application-log location: `_local/work/2026-09-17-iman-live-pilot/runs/001-collector/logs/`; actual filenames and hashes: TODO. Do not publish secrets or raw personal text.
- Isolation: folders and `.venv` provide organizational/package separation, not a verified filesystem/network sandbox. Live external access is intended; no network-denial boundary is claimed.
- Stop rather than bypass login/access challenges or restrictions; record any interruption, unexpected writes or inability to preserve provenance. No runtime stop-condition outcome has been observed.

## Input provenance

External source: LinkedIn via the collector's embedded queries. There is no local input dataset hash to invent. User authorization is recorded above; platform permission and applicable access conditions remain unresolved. Actual retrieval window, source coverage, dataset identifier/version and counts: TODO. No train/validation/test split or approved research corpus is established. Existing scraper CSVs, DBs and sessions must not be inputs to this fresh attempt.

## Expected artifacts and validation

All paths below are **planned**, not claims of produced files. Paths are relative to the private run workspace.

| Expected artifact                                   | Actual presence / hash / counts / validation                                                   |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `corpus_data/architectural_discourse.db`            | Not evidenced; schema, integrity, rows, stable SHA-256 and size pending                        |
| `logs/` capture files and any script-generated logs | Directory prepared; actual files, outcomes and hashes pending                                  |
| `manifest.json`                                     | Pending; capture actual invocation/environment/configuration, events, logs and artifact hashes |
| Other script outputs                                | Identify from actual run; do not infer completion from source expectations                     |

After process exit, capture code-before/after hashes, exit outcome, schema/row counts, DB consistency and artifact/log hashes. Preserve failed or partial output with its outcome, subject to privacy requirements. For analysis, close the collector and preserve committed WAL content in a consistent SQLite snapshot; record the procedure and stable source/destination hashes before placing a separate input at run 002's `corpus_data/architectural_discourse.db`. Analysis remains blocked if no suitable nonempty DB exists.

Measured results: **none recorded**. Source review and the seven earlier synthetic cases do not establish runtime compatibility, retrieval quality, platform permission or scientific validity. A zero exit code alone will not establish these either.

Retention/deletion period, approved backup (if any), privacy review and completeness reviewer/date: TODO. Credentials, profiles, personal rows and private manifests stay out of Git. Link local files only after confirming their existence; public links will not work in a fresh clone. Finalize from actual manifest/log evidence, keeping missing values explicit; any retry gets a new run ID.

## Dated amendments

### 2026-09-17 — actual launch and assistant-initiated interruption

This amendment supersedes the pre-run lifecycle and pending fields above only to the extent supported by evidence. **Status: interrupted, not completed; provenance incomplete.**

- Original local [manifest](../../../_local/work/2026-09-17-iman-live-pilot/runs/001-collector/manifest.json) records start `2026-09-17T20:49:14.700Z`, branch `experiment/2026-09-17-iman-live-pilot`, and checkout commit `966de34c010b10f3b711df0e2cd17487ac8d3fe5` with dirty tracked and untracked documentation. The commit alone does not identify the ignored code or dirty documentation.
- Actual child command: `/Users/kaveh/Desktop/base/_LIBRARY/_saintimental/.venv/bin/python -u code/collector.py`, from the private collector CWD recorded above. The manifest records the reused `.venv`, Python 3.13.11, macOS 26.6.2/arm64 and exact package inventory (including Playwright 1.62.0). Those fields are no longer pending. Browser version, profile-freshness verification and missing preflight gates are not inferred from launch.
- Manifest code-before SHA-256: `5d06c0f9b25501950cede7211b42416fb80719499b0e4a5d341255331f179386`; wrapper SHA-256: `526d657b339ef0cfa798efaecd97580de6208eb69d3960dc58fafa3752d754d2`. No post-run hash is recorded.
- The user reported login. **Neither login success nor failure is independently established.** In the supplied event history the assistant then stopped the run without a user request: killing the terminal left detached Python PID `82380` alive; the assistant sent `kill -TERM -- -82380`, then verified via `ps` that the PID was absent. This sequence is retrospectively documented, not repeated in this task.
- Last observed application log before the stop contained only DB initialization and the manual-login warning. Reading the saved application log confirms those two entries. Saved stderr also contains `Error: write EPIPE`, observed after the stop according to the supplied history. EPIPE is not proof of a login failure. Saved stdout is empty; this is not a collected-count measurement.
- **Exact end time, duration, exit code and actual exit signal are unavailable.** TERM was sent, but the wrapper's child-close record was lost. PID absence does not establish graceful closure or DB consistency. The original manifest still says `running` because the wrapper was killed; it is left intact rather than silently rewritten with fabricated lifecycle values. Read it with the separate local [interruption note](../../../_local/work/2026-09-17-iman-live-pilot/runs/001-collector/interruption-note.md).
- Logs and the manifest are present, overriding their earlier pending-presence descriptions. DB initialization is log evidence only: no final DB count, schema/consistency check, WAL-preserving snapshot, final artifact hashes or usable dataset is established. No collected count is claimed, including zero. Analysis 002 remains **blocked and not run**.

The separate [offline collector record](../../2026-09-17-iman-collector-offline.md) reports four passing fake-browser scenarios and a failed duplicate-upsert reporting probe, not validation of this live attempt or the whole collector. No fixes, scientific findings, platform permission or runtime consent follow. Remaining access, privacy, retention and handoff gates remain unresolved. Any retry requires a new run record; this amendment does not launch one.

Evidence review for this amendment was read-only apart from documentation edits. No code, original manifest, result artifact or log was modified; no commands, tests, Git operations or browser actions were performed. Local evidence links require the ignored workspace and will not resolve in a fresh public clone.
