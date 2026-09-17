# Experiments

No experiments have been run in this folder. Do not treat the 2026-09-03/04 LinkedIn scraper tests, Iman’s unrun `collector.py`, or the sent 15 September letter as completed experiment records.

Use one Markdown file per experiment, named `YYYY-MM-DD-short-name.md`, adding a suffix if necessary to keep names unique. Copy the template below.

## How to start a professional experiment

Keep this path small: git + this template. Do not add CI, experiment databases, or research-agent workspaces unless the team later adopts them. [OpenResearch](https://github.com/alphaXiv/OpenResearch) is only an optional later suggestion in Kaveh’s [sent letter](../research/team-feedback-to-team-2026-09-15-FA.md); it is not required here.

1. **Update `main`.** Fetch and check out the latest `origin/main` so the run is not based on a stale letter draft or an old scraper commit.
2. **New branch per experiment.** Create `experiment/YYYY-MM-DD-short-name` from that `main`. Do not mix two experimental questions on one branch. Do not commit results onto `main` until the record is filled and reviewed.
3. **Record before you run.** Copy the template into `experiments/YYYY-MM-DD-short-name.md`. Fill **Question or Hypothesis**, **Data** (planned dataset ID, version, split), and **Configuration and Execution** (method, parameters, commands) while they are still plans. Link `../data/README.md` if a dataset entry exists.
4. **Code version.** After the branch exists, record the commit that will be executed (`git rev-parse HEAD`). If you change code on the branch, record the commit you actually ran, not an earlier one. Point at files under `src/` or `linkedin-scraper/` rather than inventing a new tree.
5. **Run only what is permitted.** A query list is not a collection licence. The LinkedIn DSA case remains Open on last evidence. Exploratory scraper CSVs stay git-ignored and are not an approved research corpus.
6. **Record after you run.** Fill actual execution details, results, and limitations. Leave unmeasured values as TODO. If the run fails, keep the record with status `failed` and link a follow-up file; do not overwrite the failed record with a later success.
7. **Private data stays out.** Credentials, session files, and personal post dumps do not belong in the record or in git. Describe paths and row counts without pasting profile text.

The 2026-09-03/04 scraper sessions in `research/project-log.md` section 24 are engineering tests. If a similar run is repeated as a professional experiment, start a **new** branch and a **new** file here; do not silently replace those log notes.

Both the [article](../writing/article.md) and [thesis](../writing/thesis.md) should reference these records when reporting results.

## Experiment Template

```text
# Experiment: TODO

## Status and Date
TODO: planned / running / completed / failed; date of execution.

## Git
TODO: branch name (`experiment/YYYY-MM-DD-short-name`);
base commit of main; commit actually executed.

## Question or Hypothesis
TODO: what this experiment is intended to test.

## Data
TODO: dataset ID, exact version, preprocessing, and train/validation/test splits.
Link to the dataset documentation in ../data/README.md.
If no permitted dataset exists yet, say so; do not invent one.

## Code Version
TODO: commit ID of the code that ran, plus the files/scripts used.

## Configuration and Execution
TODO: method, parameters, random seeds, evaluation metrics, command or steps,
software versions, and relevant hardware.

## Results
TODO: actual measurements and links to supporting artifacts.
Leave unmeasured results as TODO; do not substitute expected values.

## Interpretation and Limitations
TODO: observations, uncertainty, failures, and limits on conclusions.

## Next Steps
TODO: follow-up questions or links to subsequent experiment records.
```
