# Run: <experiment-id>/<run-id>

## Identity and lifecycle

- Experiment plan: TODO relative link
- Question and script/entrypoint: TODO
- Mode: TODO offline synthetic / permitted dataset analysis / separately permitted live collection
- Status: planned / blocked / running / completed / failed / interrupted / cancelled (choose one)
- Registered date: TODO; actual UTC start/end: not started
- Operator/reviewer: TODO (do not infer)
- Parent/upstream run or retry-of: TODO or none
- Workspace and exact CWD: `_local/work/<experiment-id>/runs/<run-id>/`
- Public record is authoritative for reviewed metadata; sensitive details: TODO local manifest path, if needed

## Preflight — required before running

- [ ] Question, access mode, permitted scope and stop conditions reviewed; evidence/reference recorded.
- [ ] Experiment branch, actual commit and dirty diff/hash recorded.
- [ ] New workspace; no prior output DB/log/profile accidentally reused.
- [ ] Source and frozen code snapshot hashes verified; changes documented.
- [ ] Environment, exact dependencies and configuration recorded; no guessed versions.
- [ ] Input provenance/permission, schema, version/split and hashes recorded.
- [ ] Isolation boundary and its limitations stated; offline test cannot enter live collection flow.
- [ ] Expected artifacts, log capture, validation and retention plan recorded.

## Code and configuration

| File | Preserved source / adopted path | Source SHA-256 | Run snapshot path | Snapshot SHA-256 | Changes |
| ---- | ------------------------------- | -------------- | ----------------- | ---------------- | ------- |
| TODO | TODO                            | TODO           | TODO              | TODO             | TODO    |

- Branch / base commit / actual execution commit: TODO
- Dirty state and local code/config patch manifest: TODO
- Configuration: TODO all relevant embedded constants, queries/taxonomies and options; reference snapshot hash
- Seed/nondeterminism: TODO; record absence of seed explicitly
- Protocol/query/codebook versions and review status: TODO

## Environment and execution

- Interpreter absolute path and version: TODO
- OS/version/architecture and relevant hardware: TODO
- Environment path/identity: TODO
- Exact package versions and inventory/lockfile path + SHA-256: TODO
- Browser/driver version if relevant: TODO or not applicable
- Exact invocation (redacted if necessary): TODO, not executed
- Exact CWD: TODO
- Isolation: TODO package isolation, filesystem and network controls actually verified; limitations
- stdout / stderr / application log paths: TODO
- Start/end UTC, duration, exit code/signal: not started
- Events, warnings, exceptions and deviations: none observed; not started

## Input provenance

| Dataset ID/version/split | Origin or upstream experiment/run | Permission evidence | Workspace input path | SHA-256 before / after | Schema and row count |
| ------------------------ | --------------------------------- | ------------------- | -------------------- | ---------------------- | -------------------- |
| TODO                     | TODO                              | TODO                | TODO                 | TODO                   | TODO                 |

For collection, document the external source, access conditions, query version and actual retrieval window rather than inventing an input-file hash. For SQLite handoff record the closed/consistent snapshot procedure and verify source/destination hashes. No personal rows or session data in this table.

## Artifacts and validation

| Expected artifact | Actual path  | SHA-256      | Size / rows  | Validation outcome |
| ----------------- | ------------ | ------------ | ------------ | ------------------ |
| TODO              | not produced | not produced | not measured | not run            |

- Code hashes after run versus before: TODO
- Output/schema/row-count and input-immutability checks: TODO
- Failure/partial-output details: TODO or none, with evidence
- Measured results: none; not executed
- Scientific interpretation and limitations: TODO; no findings from a planned run
- Retention/deletion/approved backup and visibility: TODO; private artifacts never committed
- Completeness review: TODO missing evidence and reasons; reviewer/date only if confirmed
- Next attempt/follow-up: TODO

## Dated amendments

None. Preserve closed records; append corrections with date, reason and evidence instead of replacing an earlier outcome.
