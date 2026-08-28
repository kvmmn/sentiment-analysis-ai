# Experiments

No experiments have been run. Use a separate Markdown record for each experiment, named `YYYY-MM-DD-short-name.md`, adding a suffix if necessary to keep names unique.

Copy the template below. Fill in the question and planned configuration before running; record the actual execution and results afterward. Preserve unsuccessful runs and link follow-up records rather than silently overwriting earlier findings.

## Experiment Template

```text
# Experiment: TODO

## Status and Date
TODO: planned / running / completed / failed; date of execution.

## Question or Hypothesis
TODO: what this experiment is intended to test.

## Data
TODO: dataset ID, exact version, preprocessing, and train/validation/test splits.
Link to the dataset documentation in ../data/README.md.

## Code Version
TODO: commit ID if Git is later adopted; otherwise a preserved code snapshot
or file hashes sufficient to identify the exact implementation.

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

Both the [article](../writing/article.md) and [thesis](../writing/thesis.md) should reference these records when reporting results. Keep private data and credentials out of records and linked artifacts.
