"""Stage 1 — model-based features for Run 013 (cached, row-level, private output).

Produces, per post and per sentence:
  * analytic-sample flags (duplicate, language, length, domain relevance)
  * sentence segmentation
  * sentence embeddings (all-mpnet-base-v2)
  * two independent sentiment measures: VADER compound and a RoBERTa classifier
    (cardiffnlp/twitter-roberta-base-sentiment-latest, score = P(pos) - P(neg))
  * zero-shot NLI labels (MoritzLaurer/deberta-v3-base-zeroshot-v2.0) for
    domain relevance, epistemic stance (Iman's codebook) and deskilling mode
    (codebook v0.1). These are provisional until checked against human coding.

Row-level outputs contain post text and author names, so they are written to
_local/ (git-ignored). Only aggregate results leave that folder (see analyze.py).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "linkedin_genai_architecture_discourse_2026-09-20_run013.csv"
OUT = ROOT / "_local" / "work" / "run013-multimethod"
OUT.mkdir(parents=True, exist_ok=True)

DEVICE = "mps" if __import__("torch").backends.mps.is_available() else "cpu"
# base rather than large: ~4x faster on Apple MPS (14 vs 56 min for the post-level labels);
# accuracy is checked against human coding in the validation step, not assumed.
NLI_MODEL = "MoritzLaurer/deberta-v3-base-zeroshot-v2.0"

# --------------------------------------------------------------------------- labels
RELEVANCE = {
    "relevant": "This text is about architecture, architects, building design or the built environment.",
    "off_domain": "This text is about business, software or AI in general, not about architecture or buildings.",
}
STANCE = {  # Iman's Epistemic Stance codes; hypotheses paraphrase his definitions
    "Solutionist Hype": "This text enthusiastically celebrates AI's speed and novelty without questioning or verifying it.",
    "Pragmatic Implementation": "This text describes a practical, concrete workflow for using AI tools in design work.",
    "Critical Skepticism": "This text critically questions AI's limitations, risks, errors or liability.",
    "Defensive Augmentation": "This text insists that AI is only an assistant and that human judgment must remain in control.",
}
DMODE = {  # codebook v0.1, operationalising Iman's and Morteza's observation
    "D0 Not addressed": "This text does not discuss professional skills or the loss of skills.",
    "D1 Experiential report": "The author describes a first-hand experience of skills being lost or weakened because of AI.",
    "D2 Prospective warning": "This text warns that AI may erode, weaken or replace architects' skills in the future.",
    "D3 Prescriptive upskilling": "This text urges architects or students to learn new skills in order to keep up with AI.",
    "D4 Reassurance": "This text reassures that AI will not replace architects or their core skills.",
}

SENT_SPLIT = re.compile(r"(?<=[.!?…])\s+(?=[A-Z0-9\"“'(#@🚀-🫶])|\n+")


def load_posts() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    df["text"] = (df["content_cleaned"].fillna("")
                  .str.replace(r"…\s*more$", "", regex=True)
                  .str.replace(r"\s+", " ", regex=True).str.strip())
    from langdetect import DetectorFactory, detect
    DetectorFactory.seed = 0

    def lang(s: str) -> str:
        try:
            return detect(s) if len(s) >= 20 else "short"
        except Exception:
            return "unknown"

    df["lang"] = df["text"].map(lang)
    df["is_duplicate"] = df.duplicated("text", keep="first")
    df["too_short"] = df["text"].str.len() < 80
    return df


def split_sentences(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for uid, text in zip(df["post_uid"], df["text"]):
        parts = [p.strip() for p in SENT_SPLIT.split(text) if p and len(p.strip()) >= 3]
        for i, s in enumerate(parts):
            rows.append((uid, i, s))
    return pd.DataFrame(rows, columns=["post_uid", "sent_idx", "sentence"])


def roberta_sentiment(texts: list[str]) -> np.ndarray:
    from transformers import pipeline
    clf = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                   device=DEVICE, top_k=None, truncation=True, max_length=256)
    out = np.zeros(len(texts))
    for i, res in enumerate(clf(texts, batch_size=64)):
        p = {r["label"].lower(): r["score"] for r in res}
        out[i] = p.get("positive", 0) - p.get("negative", 0)
    return out


def zero_shot(texts: list[str], labels: dict[str, str], prefix: str) -> pd.DataFrame:
    from transformers import pipeline
    zs = pipeline("zero-shot-classification", model=NLI_MODEL, device=DEVICE)
    names, hyps = list(labels), list(labels.values())
    probs = np.zeros((len(texts), len(names)))
    step = 128
    for start in range(0, len(texts), step):
        chunk = texts[start:start + step]
        for i, res in enumerate(zs(chunk, candidate_labels=hyps, hypothesis_template="{}",
                                   multi_label=False, batch_size=16), start=start):
            for lab, sc in zip(res["labels"], res["scores"]):
                probs[i, hyps.index(lab)] = sc
        print(f"  {prefix}: {min(start + step, len(texts))}/{len(texts)}", flush=True)
    out = pd.DataFrame(probs, columns=[f"{prefix}_p_{n}" for n in names])
    out[prefix] = [names[j] for j in probs.argmax(1)]
    out[f"{prefix}_conf"] = probs.max(1)
    return out


def main(stages: set[str]) -> None:
    posts_path, sents_path = OUT / "posts.pkl", OUT / "sentences.pkl"
    if "prep" in stages or not posts_path.exists():
        posts = load_posts()
        sents = split_sentences(posts)
        posts.to_pickle(posts_path)
        sents.to_pickle(sents_path)
        print("prep:", len(posts), "posts,", len(sents), "sentences")
    posts, sents = pd.read_pickle(posts_path), pd.read_pickle(sents_path)

    if "embed" in stages:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", device=DEVICE)
        np.save(OUT / "emb_sentences.npy", m.encode(sents["sentence"].tolist(), batch_size=64,
                                                     normalize_embeddings=True, show_progress_bar=False))
        np.save(OUT / "emb_posts.npy", m.encode(posts["text"].tolist(), batch_size=32,
                                                 normalize_embeddings=True, show_progress_bar=False))
        print("embed: done")

    if "sentiment" in stages:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        va = SentimentIntensityAnalyzer()
        sents["vader"] = [va.polarity_scores(s)["compound"] for s in sents["sentence"]]
        sents["roberta"] = roberta_sentiment(sents["sentence"].tolist())
        posts["vader_post"] = [va.polarity_scores(t)["compound"] for t in posts["text"]]
        posts["roberta_post"] = roberta_sentiment(posts["text"].tolist())
        sents.to_pickle(sents_path)
        posts.to_pickle(posts_path)
        print("sentiment: done")

    if "zeroshot" in stages:
        texts = [t if t else "(empty post)" for t in posts["text"].str.slice(0, 1000)]
        parts = [zero_shot(texts, RELEVANCE, "relevance"),
                 zero_shot(texts, STANCE, "stance"),
                 zero_shot(texts, DMODE, "dmode")]
        z = pd.concat(parts, axis=1)
        z.insert(0, "post_uid", posts["post_uid"].values)
        z.to_pickle(OUT / "zeroshot.pkl")
        print("zeroshot: done")

    if "dmode_ml" in stages:
        # Independent entailment per mode (multi-label). A post gets the strongest mode if its
        # entailment >= 0.5, otherwise D0. Softmax over five modes (the zeroshot stage) let
        # "not addressed" absorb almost everything, so this is the version used for analysis.
        from transformers import pipeline
        zs = pipeline("zero-shot-classification", model=NLI_MODEL, device=DEVICE)
        modes = {k: v for k, v in DMODE.items() if not k.startswith("D0")}
        texts = [t if t else "(empty post)" for t in posts["text"].str.slice(0, 1000)]
        P = np.zeros((len(texts), len(modes)))
        hyps = list(modes.values())
        for start in range(0, len(texts), 128):
            for i, res in enumerate(zs(texts[start:start + 128], candidate_labels=hyps, hypothesis_template="{}",
                                       multi_label=True, batch_size=16), start=start):
                for lab, sc in zip(res["labels"], res["scores"]):
                    P[i, hyps.index(lab)] = sc
            print(f"  dmode_ml: {min(start + 128, len(texts))}/{len(texts)}", flush=True)
        out = pd.DataFrame(P, columns=[f"dmode_ml_p_{k}" for k in modes])
        best = P.argmax(1)
        out["dmode_ml"] = [list(modes)[b] if P[i, b] >= 0.5 else "D0 Not addressed" for i, b in enumerate(best)]
        out["dmode_ml_conf"] = P.max(1)
        out.insert(0, "post_uid", posts["post_uid"].values)
        out.to_pickle(OUT / "dmode_ml.pkl")
        print("dmode_ml: done")

    if "aspects" in stages:
        s2 = detect_aspects(sents)
        s2.to_pickle(OUT / "sentence_aspects.pkl")
        print("aspects: done")


ASPECT_HYPOTHESIS = {
    "RQ1_Deskilling": "This sentence is about architects or designers losing skills, jobs or expertise because of AI or automation.",
    "RQ2a_Creativity": "This sentence is about creativity, design ideas, originality or aesthetics.",
    "RQ2b_CognitiveJudgment": "This sentence is about human judgment, critical thinking, verification or responsibility for decisions.",
    "RQ3a_TechnicalEnvironmental": "This sentence is about building performance, sustainability, energy, structure or code compliance.",
    "RQ3b_RepresentationBIM": "This sentence is about architectural drawings, rendering, visualization, BIM or 3D modelling.",
}


def detect_aspects(sents: pd.DataFrame) -> pd.DataFrame:
    """Retrieve candidates (keyword OR embedding similarity >= 0.40), then verify with NLI."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import kaveh_analytical_pipeline as legacy
    from aspects import ASPECTS, PROTOTYPES
    from sentence_transformers import SentenceTransformer
    from transformers import pipeline

    emb = np.load(OUT / "emb_sentences.npy")
    st = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", device=DEVICE)
    zs = pipeline("zero-shot-classification", model=NLI_MODEL, device=DEVICE)
    low = sents["sentence"].str.lower()
    out = sents[["post_uid", "sent_idx"]].copy()
    for a in ASPECTS:
        pat = re.compile("|".join(r"\b" + re.escape(w) for w in legacy.ASPECT_ONTOLOGY[a]))
        kw = low.str.contains(pat)
        sim = (emb @ st.encode(PROTOTYPES[a], normalize_embeddings=True).T).max(1)
        cand = kw | (sim >= 0.40)
        p = np.zeros(len(sents))
        idx = np.where(cand)[0]
        texts = sents["sentence"].iloc[idx].str.slice(0, 600).tolist()
        for j, res in zip(idx, zs(texts, candidate_labels=[ASPECT_HYPOTHESIS[a]], hypothesis_template="{}",
                                  multi_label=True, batch_size=32)):
            p[j] = res["scores"][0]
        out[f"{a}_kw"], out[f"{a}_sim"], out[f"{a}_cand"], out[f"{a}_nli"] = kw.values, sim, cand.values, p
        out[a] = p >= 0.5
        print(f"  {a}: keyword {kw.sum()}, candidates {cand.sum()}, verified {out[a].sum()}", flush=True)
    return out


if __name__ == "__main__":
    main(set(sys.argv[1:]) or {"prep", "embed", "sentiment", "zeroshot"})

# Note: be_margin.npy (built-environment minus software/business prototype similarity of each
# post embedding) was computed with the prototypes listed in analyze.py's docstring companion,
# domain_prototypes.py; rerun `python domain_prototypes.py` after re-embedding.
