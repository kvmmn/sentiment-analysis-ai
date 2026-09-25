# Analysis Pipeline Component (`src/analysis`)

**Status:** Verified independent implementation (2026-09-25)  
**Author/Lead:** Kaveh Momeni (for Master's Thesis at Arden University and shared scientific article)  
**Test Suite:** `src/analysis/tests/test_kaveh_pipeline.py` (7/7 passing unit tests)

## Overview

This component implements Kaveh's independent analytical pipeline for analyzing architectural discourse on generative AI from social media (specifically LinkedIn corpora). It was developed and empirically validated on the Run 013 dataset (1,076 posts).

## Key Modules

1. **`kaveh_analytical_pipeline.py`**:
   - **Clause-Level Context-Window ABSA:** Evaluates sentiment within a ±5-token sliding window around aspect anchors across five architectural dimensions (Ideation/Aesthetics, Technical/BIM, Labor/Agency, Pedagogy/Education, Ethical/Legal). Handles intensifiers, diminishers, and negation flipping.
   - **2D Continuous Discursive Stance:** Models stance across two continuous axes:
     - *Human Agency / Sovereignty Axis* ($-1.0$ automated substitution to $+1.0$ autonomous human steering).
     - *Discourse Valence Axis* ($-1.0$ dystopian/critical to $+1.0$ utopian/optimistic).
   - **Multi-Signal Stakeholder Inference:** Combines credential markers (Dr., AIA, Prof.), first-person organizational cues, and query intent to classify posts into four cohorts (Practitioners, Academics, Students, Industry Leaders) overcoming empty headline metadata.
   - **Inferential Statistical Testing:** Calculates Sarle's Bimodality Coefficient ($BC$), Mann-Whitney $U$, Kruskal-Wallis, and ANOVA with rigorous non-parametric guards.

2. **`tests/test_kaveh_pipeline.py`**:
   - Unit test suite verifying clause-level valence scoring, negation flipping, intensifier multipliers, window isolation, 2D stance mapping, stakeholder inference heuristics, and Sarle's bimodality coefficient.

## Usage

```bash
# Run unit tests
.venv/bin/python -m unittest src/analysis/tests/test_kaveh_pipeline.py

# Execute pipeline on a dataset
.venv/bin/python src/analysis/kaveh_analytical_pipeline.py
```
