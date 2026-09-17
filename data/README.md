# Data

No approved research dataset has been established. Historic exploratory LinkedIn data exists locally under `src/linkedin-scraper/` and is git-ignored; it is not an approved research corpus. See the [legacy scraper guide](../src/linkedin-scraper/README.md). This directory is reserved for local data; its contents are ignored by version control except for this guide.

## Planned storage convention

- Dataset versions: `data/local/<dataset-id>/<version>/`, with separate `raw/` and `derived/` subdirectories. Preserve original inputs; record transformations and exact versions separately.
- Per-experiment outputs: `data/local/experiments/<id>/`, linked from the corresponding [experiment record](../experiments/README.md).
- These are planned paths, not directories or datasets created by this documentation change. Legacy scraper runtime artifacts remain beside the script as a documented exception; no data is moved here.

The earlier raw-layout proposal (`data/local/raw/{platform}/{batch_id}/`), item schema, and retention discussion remain in [keywords-search-storage.md](../research/keywords/keywords-search-storage.md). Use the versioned convention above for new plans; neither document authorizes collection or establishes a retention entitlement. See the [project migration map](../docs/project-map.md) for relocated files.

Record each dataset below when selected. Keep only non-sensitive metadata here. Confirm permitted access, use, and sharing before acquiring data. Never place credentials or personal records in this document.

## Dataset Template

```text
Dataset name / ID: TODO
Origin / provider: TODO
Source URL: TODO
License and access conditions: TODO
Permitted use and redistribution: TODO
Version / release / retrieval date: TODO
Local raw/derived artifact paths: TODO (data/local/<dataset-id>/<version>/)
Acquisition steps (without credentials): TODO
Source/input SHA-256 and artifact paths: TODO
Derived/output SHA-256 and artifact paths: TODO
Processing code commit, source-file SHA-256, and experiment record: TODO
Environment/interpreter and exact dependency versions: TODO
Contents and labels: TODO
Privacy or ethical considerations: TODO
Preprocessing and split definitions: TODO
Known limitations: TODO
```

Reference the dataset ID and exact version in [experiment records](../experiments/README.md). Document transformations separately from original data so results can be reproduced.
