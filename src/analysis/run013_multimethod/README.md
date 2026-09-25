# Run 013 multi-method analysis

Second-generation analysis of the Run 013 corpus (2026-09-25). It supersedes the single-lexicon
results of `kaveh_analytical_pipeline.py` for the meeting guide, and reuses that pipeline's aspect
ontology and domain lexicon as one of three sentiment measures.

## What it does

| Stage | Script | Output (private, `_local/work/run013-multimethod/`) |
|---|---|---|
| Language, duplicates, length flags; sentence split | `features.py prep` | `posts.pkl`, `sentences.pkl` |
| Sentence and post embeddings (all-mpnet-base-v2) | `features.py embed` | `emb_*.npy` |
| Sentiment: RoBERTa (cardiffnlp) and VADER | `features.py sentiment` | columns in the pickles |
| Zero-shot NLI: domain relevance, epistemic stance, deskilling mode | `features.py zeroshot` | `zeroshot.pkl` |
| Deskilling mode, multi-label | `features.py dmode_ml` | `dmode_ml.pkl` |
| Aspect detection: keyword or embedding candidates, NLI verification | `features.py aspects` | `sentence_aspects.pkl` |
| Built-environment vs software/business margin | `domain_prototypes.py` | `be_margin.npy` |
| Statistics and validation sample | `analyze.py` | `docs/analysis_run013/results.json` (aggregate only), `validation_sample_for_coding.csv` |

Row-level outputs contain post text and author names and stay in `_local/`. Only aggregates are
written to `docs/`.

## Run

```bash
python3 -m venv _local/venv-analysis
_local/venv-analysis/bin/pip install -r src/analysis/run013_multimethod/requirements.txt
export HF_HUB_OFFLINE=1   # after models are cached; online hub calls stalled on this machine
_local/venv-analysis/bin/python src/analysis/run013_multimethod/features.py prep embed sentiment zeroshot dmode_ml aspects
_local/venv-analysis/bin/python src/analysis/run013_multimethod/domain_prototypes.py
_local/venv-analysis/bin/python src/analysis/run013_multimethod/analyze.py
```

Zero-shot stages use `deberta-v3-base-zeroshot-v2.0` (about 15 min on Apple MPS; the large model
took about 4x longer). Labels are provisional until compared with human coding of the validation sample.

## Known limits

- The deskilling-mode variable failed a validity spot-check with zero-shot NLI; use human coding.
- Domain screening thresholds (`be_margin > 0.05`, or `> 0` with explicit built-environment terms)
  were set by manual inspection of borderline posts.
- Judgment (n=37) and deskilling (n=16) aspects are small in the domain sample.
