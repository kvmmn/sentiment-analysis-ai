# Initial Coding Sample (`n = 50`) — Methodology & Provenance (2026-11-25)

**Status:** completed  
**Date:** 2026-11-25  
**Purpose:** Draw a reproducible, representative sample of **50 posts** from the team-curated corpus (`N = 395` `keep` posts) for independent blind initial coding (open coding and codebook calibration across Morteza, Iman, and Kaveh prior to the 2026-11-26 team meeting). This record serves as shared methodological evidence for both the scientific article and master's thesis.

> [!NOTE]
> This public record contains aggregate counts, methodological rules, and cryptographic hashes only. No post texts, author names, URLs, or personal records are stored in git.

---

## 1. Sampling Frame & Pre-Sampling Eligibility Filtering

- **Source corpus:** 1,858 unique LinkedIn posts from the 48-query three-layer Apify run (`X2gdX05u8rP41b4rG`, dataset `WUsK3RRYo7nKEOUbA`, 2026-10-18).
- **Curated baseline (`N = 395`):** Union of `status == "keep"` decisions exported from Neon (`_saintiment_swipe_team_db`) on 2026-11-25 (`Morteza: 103`, `Iman: 169`, `Kaveh: 123` out of `620 / 619 / 619` reviewed).
- **Pre-sampling eligibility rules** (applied sequentially before sampling to prevent uncodable fragments or duplicate reposts from consuming 10% of a 50-post calibration sample):
  1. **Substantive prose threshold (`insufficient_prose`):** Strip hashtags (`#\S+`) and URLs (`https?://\S+`), collapse whitespace, and require at least **15 words** AND **100 characters** of remaining prose. Excluded **11** posts (`insufficient_prose`).
  2. **Exact-text deduplication (`exact_duplicate_text`):** Normalize remaining post texts (`" ".join(text.lower().split())`) and retain only the lowest `source_post_id` for identical copies. Excluded **5** duplicate posts.
- **Eligible sampling frame:** **`379` unique posts** (`395 - 16 = 379`).

---

## 2. Sampling Design (`2D Proportional Stratified Random Sample`)

- **Target sample size:** `n = 50` (shared across all three coders to enable 3-way Inter-Annotator Agreement and open-code triangulation).
- **Stratification variables (`12` cells):**
  1. **Reviewer screening set (`reviewer_set`):** `Morteza`, `Iman`, `Kaveh` — preserves exact proportionality across the three screening partitions.
  2. **Primary analytical query family (`primary_family`):** first family listed in `matched_families` (`cognition`, `process`, `direct`, `technical_and_pedagogy`) — ensures theoretical coverage across all four discourse pillars.
- **Apportionment:** Integer cell quotas computed via the **Largest Remainder Method (Hamilton apportionment)** so stratum quotas sum strictly to `50`.
- **Within-stratum selection & independence constraints:**
  - Deterministic PRNG (`SEED = 20261125`) over `source_post_id`-sorted pools.
  - **Strict author uniqueness:** maximum **1 post per normalized `author_name`** across all 50 sampled posts to avoid single-voice clustering.
- **Blind presentation order:** Selected 50 posts shuffled with `random.Random(20261126)` (`SEED + 1`) and assigned canonical IDs `S01`–`S50`. Coder tabs (`Morteza`, `Iman`, `Kaveh`) omit `reviewer_set`, `matched_families`, and `matched_query_codes` to prevent framing bias.

---

## 3. Verified Quotas & Representativeness Balance

### 3.1 12-Stratum Quotas (`Eligible Frame` → `Sample`)

| Reviewer Set | Primary Family | Eligible Posts | Hamilton Quota | Realized |
| --- | --- | ---: | ---: | ---: |
| Iman | `cognition` | 75 | 10 | 10 |
| Iman | `direct` | 30 | 4 | 4 |
| Iman | `process` | 42 | 6 | 6 |
| Iman | `technical_and_pedagogy` | 14 | 2 | 2 |
| Kaveh | `cognition` | 58 | 8 | 8 |
| Kaveh | `direct` | 17 | 2 | 2 |
| Kaveh | `process` | 26 | 3 | 3 |
| Kaveh | `technical_and_pedagogy` | 15 | 2 | 2 |
| Morteza | `cognition` | 55 | 7 | 7 |
| Morteza | `direct` | 18 | 2 | 2 |
| Morteza | `process` | 20 | 3 | 3 |
| Morteza | `technical_and_pedagogy` | 9 | 1 | 1 |
| **Total** | **All 12 strata** | **379** | **50** | **50** |

### 3.2 Eligible Frame (`N = 379`) vs. Sample (`n = 50`) Balance

| Dimension | Category | Eligible Frame | Sample (`n = 50`) | Delta (pp) |
| --- | --- | ---: | ---: | ---: |
| `reviewer_set` | Iman | 161 (42.48%) | 22 (44.00%) | +1.52 |
| `reviewer_set` | Kaveh | 116 (30.61%) | 15 (30.00%) | -0.61 |
| `reviewer_set` | Morteza | 102 (26.91%) | 13 (26.00%) | -0.91 |
| `primary_family` | `cognition` | 188 (49.60%) | 25 (50.00%) | +0.40 |
| `primary_family` | `process` | 88 (23.22%) | 12 (24.00%) | +0.78 |
| `primary_family` | `direct` | 65 (17.15%) | 8 (16.00%) | -1.15 |
| `primary_family` | `technical_and_pedagogy` | 38 (10.03%) | 5 (10.00%) | -0.03 |
| `author_type` | `profile` | 318 (83.91%) | 40 (80.00%) | -3.91 |
| `author_type` | `company` | 61 (16.09%) | 10 (20.00%) | +3.91 |
| `year` | `2026` | 354 (93.40%) | 48 (96.00%) | +2.60 |
| `year` | `2025` | 23 (6.07%) | 2 (4.00%) | -2.07 |
| `year` | `2024` | 1 (0.26%) | 0 (0.00%) | -0.26 |
| `year` | `2023` | 1 (0.26%) | 0 (0.00%) | -0.26 |

- **Post length (`text_chars`):** Eligible frame median `1408.0` (Q1 `920.5`, Q3 `2052.5`, IQR `1132.0`, min `147.0`, max `3589.0`) vs. Sample median `1471.0` (Q1 `892.0`, Q3 `1991.0`, IQR `1099.0`, min `228.0`, max `2905.0`).
- **Author diversity:** `50` unique `source_post_id`s by `50` unique `author_name`s; `0` duplicate texts; `0` posts below prose threshold.

---

## 4. Provenance & Reproducibility

- **Sampling script:** [`src/analysis/sample_initial_coding_50.py`](../src/analysis/sample_initial_coding_50.py) (`SEED = 20261125`, `blind_order_seed = 20261126`).
- **Inputs (local-only, git-ignored):**
  - `data/local/linkedin-apify-2026-10-17/saintiment_swipe_decisions_2026-11-25.json` (SHA-256: `3df2effc5557862b8e9ea9f728c83586e2ca14667efb8aa06b10b5d4128d6cc5`)
  - `data/local/linkedin-apify-2026-10-17/apify_three_layer_2026-10-18.db` (SHA-256: `b1029855ed5269cff30906f5af69304ad56bcf1b82b3a3110d5e3b9df9c5dc0e`)
- **Local outputs (`data/local/linkedin-apify-2026-10-17/coding_sample_50_2026-11-25/`, git-ignored):**
  - `saintiment_initial_coding_50_2026-11-25.xlsx` (SHA-256: `6c756f785b0281dab04e7ecdac10c2d67b08b6c52466722e2377ac42627befeb`) — 5 tabs: `README_Protocol`, `Morteza`, `Iman`, `Kaveh`, `Master_Metadata`.
  - `initial_coding_50_blind.csv` (SHA-256: `ee3a68596de889ba758ef279d217334a8fbe2ef9ad143d8da9334724fbe7e662`).
  - `initial_coding_50_manifest.json` (full exclusion log, stratum quotas, balance metrics, and canonical `S01`–`S50` mapping).
