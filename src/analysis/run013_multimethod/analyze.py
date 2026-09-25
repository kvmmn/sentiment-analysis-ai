"""Stage 2 — statistical analysis of Run 013 on the stage-1 features.

Design principles
  * One analytic sample, defined by a transparent flow (duplicates, language,
    length, domain relevance); sensitivity analyses on the wider sample.
  * Every sentiment claim is tested under three independent measures
    (RoBERTa classifier, VADER, Kaveh's domain lexicon). A finding counts as
    robust only if its direction holds under all three.
  * Effect sizes and bootstrap intervals, not p-values alone; Benjamini–Hochberg
    correction across the hypothesis family.
  * Posts by the same author are not independent: engagement models use
    author-clustered errors, and H2 is re-run with one post per author.

Writes aggregate results only (no text, no names) to docs/analysis_run013/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from aspects import ASPECTS  # noqa: E402

ROOT = HERE.parents[2]
FEAT = ROOT / "_local" / "work" / "run013-multimethod"
OUT = ROOT / "docs" / "analysis_run013"
OUT.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(20260925)
METHODS = ["roberta", "vader", "lexicon"]
# "building" is left out on purpose: as a verb ("building AI agents") it pulled software posts in.
BUILT = (r"\barchitects?\b|\barchitectural\b|\bbuildings\b|built environment|building (design|performance|code|physics)|"
         r"\baec\b|\bbim\b|\brevit\b|\brhino\b|grasshopper|design studio|\burban|\bconstruction\b|floor ?plans?|"
         r"interior design|landscape architect|facade|façade|daylight")
SOFTWARE = (r"(enterprise|software|system|systems|data|cloud|solution|solutions|agentic|ai|llm|model|technical|security|"
            r"network|integration|platform|application|information) architect|agentic|\bagents\b|enterprise ai")


# ------------------------------------------------------------------ helpers
def boot_ci(x, fn=np.mean, n=4000):
    x = np.asarray(x, float)
    if len(x) < 3:
        return [np.nan, np.nan]
    b = [fn(RNG.choice(x, len(x))) for _ in range(n)]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def cliffs_delta(a, b):
    a, b = np.asarray(a), np.asarray(b)
    gt = (a[:, None] > b[None, :]).sum()
    lt = (a[:, None] < b[None, :]).sum()
    return float((gt - lt) / (len(a) * len(b)))


def sarle_bc(x):
    x = np.asarray(x, float)
    n = len(x)
    g, k = stats.skew(x), stats.kurtosis(x)
    return float((g ** 2 + 1) / (k + 3 * (n - 1) ** 2 / ((n - 2) * (n - 3))))


def r(x, nd=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), nd)


# ------------------------------------------------------------------ load
def load():
    posts = pd.read_pickle(FEAT / "posts.pkl")
    sents = pd.read_pickle(FEAT / "sentences.pkl")
    asp = pd.read_pickle(FEAT / "sentence_aspects.pkl")
    zs = pd.read_pickle(FEAT / "zeroshot.pkl")
    import kaveh_analytical_pipeline as legacy
    sents["lexicon"] = sents["sentence"].map(legacy.score_clause_valence)
    sents = sents.merge(asp, on=["post_uid", "sent_idx"])
    posts = posts.merge(zs, on="post_uid")
    dm = pd.read_pickle(FEAT / "dmode_ml.pkl")
    posts = posts.merge(dm, on="post_uid")
    posts["dmode_softmax"] = posts["dmode"]
    posts["dmode"], posts["dmode_conf"] = posts["dmode_ml"], posts["dmode_ml_conf"]
    low = posts["text"].str.lower()
    posts["built_terms"] = low.str.contains(BUILT, regex=True)
    posts["software_arch"] = low.str.contains(SOFTWARE, regex=True)
    # Domain screening in three layers. The NLI relevance label alone let software/enterprise
    # "architecture" through (~40% of its positives), so the main sample uses the embedding margin
    # between built-environment and software/business prototypes (be_margin.npy, see features notes).
    posts["be_margin"] = np.load(FEAT / "be_margin.npy")
    lexical = posts["built_terms"] & ~posts["software_arch"]
    posts["domain_extended"] = (posts["be_margin"] > 0.05) | ((posts["be_margin"] > 0) & lexical)
    posts["domain_core"] = posts["domain_extended"] & (posts["relevance_p_relevant"] >= 0.5)
    lex_post = sents.groupby("post_uid")["lexicon"].apply(lambda v: v[v != 0].mean() if (v != 0).any() else 0.0)
    posts["lexicon_post"] = posts["post_uid"].map(lex_post).fillna(0.0)
    for a in ASPECTS:
        hit = sents[sents[a]]
        posts[f"has_{a}"] = posts["post_uid"].isin(hit["post_uid"])
        for m in METHODS:
            posts[f"{a}_{m}"] = posts["post_uid"].map(hit.groupby("post_uid")[m].mean())
    return posts, sents


def sample_flow(posts):
    steps = [("collected", posts.index == posts.index)]
    keep = ~posts["is_duplicate"]
    steps.append(("after_duplicates", keep.copy()))
    keep &= posts["lang"].eq("en")
    steps.append(("after_english_only", keep.copy()))
    keep &= ~posts["too_short"]
    steps.append(("after_min_length_80", keep.copy()))
    english = keep.copy()
    core = keep & posts["domain_core"]
    keep &= posts["domain_extended"]
    steps.append(("after_domain_relevance", keep.copy()))
    flow = {k: int(v.sum()) for k, v in steps}
    flow["domain_strict_nli_agrees"] = int(core.sum())
    return flow, keep, english, core


# ------------------------------------------------------------------ analyses
def h1_distribution(df):
    out = {}
    from sklearn.mixture import GaussianMixture
    import diptest
    for m in METHODS:
        x = df[f"{m}_post"].dropna().values
        dip, p = diptest.diptest(x)
        bic = [GaussianMixture(k, random_state=0).fit(x[:, None]).bic(x[:, None]) for k in (1, 2, 3)]
        out[m] = dict(n=len(x), mean=r(x.mean()), median=r(np.median(x)), bc=r(sarle_bc(x)),
                      dip=r(dip), dip_p=r(p), near_neutral_share=r((np.abs(x) < 0.05).mean()),
                      gmm_bic_1_2_3=[r(b, 1) for b in bic], best_k=int(np.argmin(bic) + 1),
                      hist=np.histogram(x, bins=np.linspace(-1, 1, 21))[0].tolist())
    return out


def aspect_profile(df):
    rows = []
    for a in ASPECTS:
        for m in METHODS:
            v = df[f"{a}_{m}"].dropna()
            rows.append(dict(aspect=a, method=m, n=int(len(v)), prevalence=r(df[f"has_{a}"].mean()),
                             mean=r(v.mean()), ci=[r(c) for c in boot_ci(v)], zero_share=r((v == 0).mean())))
    return rows


def compare_aspects(df, a, b):
    res = {}
    for m in METHODS:
        both = df[df[f"{a}_{m}"].notna() & df[f"{b}_{m}"].notna()]
        only_a = df[df[f"{a}_{m}"].notna() & df[f"{b}_{m}"].isna()][f"{a}_{m}"]
        only_b = df[df[f"{b}_{m}"].notna() & df[f"{a}_{m}"].isna()][f"{b}_{m}"]
        d = both[f"{a}_{m}"] - both[f"{b}_{m}"]
        w = stats.wilcoxon(d) if len(d) >= 10 and (d != 0).any() else None
        u = stats.mannwhitneyu(only_a, only_b) if min(len(only_a), len(only_b)) >= 10 else None
        res[m] = dict(
            paired_n=int(len(d)), paired_mean_diff=r(d.mean()), paired_ci=[r(c) for c in boot_ci(d)],
            wilcoxon_p=r(w.pvalue, 6) if w else None,
            indep_n=[int(len(only_a)), int(len(only_b))], indep_means=[r(only_a.mean()), r(only_b.mean())],
            mwu_p=r(u.pvalue, 6) if u else None,
            cliffs_delta=r(cliffs_delta(only_a, only_b)) if u else None)
    dirs = [np.sign(res[m]["paired_mean_diff"] or 0) for m in METHODS]
    res["robust_direction"] = bool(len(set(dirs)) == 1 and dirs[0] != 0)
    return res


def query_adjusted(df, a, b):
    """Between-post contrast a vs b with search-query fixed effects and author-clustered SE."""
    import statsmodels.formula.api as smf
    out = {}
    for m in METHODS:
        x = df[df[f"{a}_{m}"].notna() ^ df[f"{b}_{m}"].notna()].copy()
        x["y"] = x[f"{a}_{m}"].fillna(x[f"{b}_{m}"])
        x["is_a"] = x[f"{a}_{m}"].notna().astype(int)
        x["q"] = x["search_query"].where(x["search_query"].map(x["search_query"].value_counts()) >= 5, "other")
        fit = lambda f: smf.ols(f, data=x).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(x["author_name"].fillna("?"))[0]})
        raw, adj = fit("y ~ is_a"), fit("y ~ is_a + C(q)")
        out[m] = dict(n=int(len(x)), diff_raw=r(raw.params["is_a"]), diff_adj=r(adj.params["is_a"]),
                      ci_adj=[r(c) for c in adj.conf_int().loc["is_a"]], p_adj=r(adj.pvalues["is_a"], 5),
                      share_explained_by_query=r(1 - adj.params["is_a"] / raw.params["is_a"]) if raw.params["is_a"] else None)
    return out


def frame_effect(df):
    """Does the search query (sampling frame) shape measured sentiment?"""
    g = df.groupby("search_query")
    rows = []
    for q, sub in g:
        if len(sub) < 15:
            continue
        v = sub["roberta_post"]
        rows.append(dict(query=q.replace('"', ""), n=int(len(sub)), mean=r(v.mean()),
                         ci=[r(c) for c in boot_ci(v)], vader_mean=r(sub["vader_post"].mean())))
    groups = [sub["roberta_post"].values for _, sub in g if len(sub) >= 15]
    h, p = stats.kruskal(*groups)
    n = sum(len(x) for x in groups)
    return dict(kruskal_h=r(h), p=r(p, 8), epsilon_sq=r(h / (n - 1)),
                by_query=sorted(rows, key=lambda d: d["mean"]))


def framework_on_run013(df):
    """Iman's epistemic stance and the deskilling-mode variable, applied to raw Run 013 text."""
    out = {}
    for col in ("stance", "dmode"):
        vc = df[col].value_counts()
        out[col] = dict(counts={k: int(v) for k, v in vc.items()},
                        mean_conf=r(df[f"{col}_conf"].mean()),
                        low_conf_share=r((df[f"{col}_conf"] < 0.5).mean()),
                        sentiment_by_class={k: dict(n=int(len(s)), mean=r(s["roberta_post"].mean()),
                                                    ci=[r(c) for c in boot_ci(s["roberta_post"])])
                                            for k, s in df.groupby(col)})
    ct = pd.crosstab(df["dmode"], df["stance"])
    out["dmode_x_stance"] = {i: {c: int(ct.loc[i, c]) for c in ct.columns} for i in ct.index}
    out["aspect_prevalence_by_dmode"] = {
        k: {a: r(s[f"has_{a}"].mean(), 3) for a in ASPECTS} for k, s in df.groupby("dmode")}
    return out


def topics(df, emb):
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics import silhouette_score
    X = emb
    scores = {}
    for k in range(6, 13):
        lab = KMeans(k, n_init=10, random_state=0).fit_predict(X)
        scores[k] = silhouette_score(X, lab, metric="cosine")
    k = max(scores, key=scores.get)
    lab = KMeans(k, n_init=10, random_state=0).fit_predict(X)
    docs = df["text"].groupby(lab).apply(" ".join)
    cv = CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=3,
                         token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z-]{2,}\b")
    tf = cv.fit_transform(docs).toarray().astype(float)
    tf = tf / tf.sum(1, keepdims=True)
    idf = np.log(1 + tf.shape[0] / (tf > 0).sum(0))  # class-based TF-IDF
    ctf = tf * idf
    terms = np.array(cv.get_feature_names_out())
    generic = {"ai", "architecture", "architects", "architect", "design", "generative", "new", "just", "like"}
    rows = []
    for t in range(k):
        sub = df[lab == t]
        top = [w for w in terms[np.argsort(-ctf[t])] if w not in generic][:8]
        rows.append(dict(topic=int(t), n=int(len(sub)), terms=top,
                         sentiment=r(sub["roberta_post"].mean()), sentiment_ci=[r(c) for c in boot_ci(sub["roberta_post"])],
                         aspects={a: r(sub[f"has_{a}"].mean(), 3) for a in ASPECTS},
                         top_stance=sub["stance"].mode().iat[0], top_dmode=sub["dmode"].mode().iat[0]))
    return dict(k=k, silhouette={str(kk): r(v) for kk, v in scores.items()}, topics=sorted(rows, key=lambda d: -d["n"])), lab


def engagement(df):
    import statsmodels.formula.api as smf
    d = df.copy()
    d["log_len"] = np.log1p(d["char_length"])
    for a in ASPECTS:
        d[f"asp_{a}"] = d[f"has_{a}"].astype(int)
    d["video"] = d["media_category"].eq("video").astype(int)
    d["author"] = d["author_name"].fillna("unknown")
    f = ("reaction_count ~ roberta_post + C(stance, Treatment('Pragmatic Implementation')) + "
         + " + ".join(f"asp_{a}" for a in ASPECTS) + " + log_len + video")
    m = smf.negativebinomial(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d["author"])[0]},
                                            disp=0, maxiter=200)
    ci = m.conf_int()
    rows = []
    for k in m.params.index:
        if k in ("Intercept", "alpha"):
            continue
        rows.append(dict(term=k.replace("C(stance, Treatment('Pragmatic Implementation'))[T.", "stance: ").rstrip("]"),
                         irr=r(np.exp(m.params[k]), 3), ci=[r(np.exp(ci.loc[k, 0]), 3), r(np.exp(ci.loc[k, 1]), 3)],
                         p=r(m.pvalues[k], 4)))
    return dict(n=int(m.nobs), alpha=r(m.params.get("alpha")), pseudo_r2=r(m.prsquared), terms=rows,
                note="Negative binomial; author-clustered SE; comments/reposts not usable in Run 013 (all zero).")


def authors(df):
    c = df["author_name"].value_counts()
    return dict(n_posts=int(len(df)), n_authors=int(c.size), max_posts_one_author=int(c.max()),
                share_top10_authors=r(c.head(10).sum() / len(df)), authors_with_1_post=int((c == 1).sum()))


def method_agreement(df, sents):
    out = {}
    pairs = [("roberta", "vader"), ("roberta", "lexicon"), ("vader", "lexicon")]
    for a, b in pairs:
        out[f"sentence_{a}_{b}"] = r(stats.spearmanr(sents[a], sents[b]).statistic, 3)
        out[f"post_{a}_{b}"] = r(stats.spearmanr(df[f"{a}_post"], df[f"{b}_post"]).statistic, 3)
    return out


def aspect_detection_report(sents):
    rows = []
    for a in ASPECTS:
        kw, cand, ver = sents[f"{a}_kw"], sents[f"{a}_cand"], sents[a]
        rows.append(dict(aspect=a, keyword=int(kw.sum()), candidates=int(cand.sum()), verified=int(ver.sum()),
                         keyword_confirmed_share=r((kw & ver).sum() / max(kw.sum(), 1), 3),
                         verified_without_keyword=int((ver & ~kw).sum())))
    return rows


def validation_sample(df, n_per=12):
    parts = []
    # stratified by provisional stance (dmode is not measurable automatically yet), topped up at random
    for k, s in df.groupby("stance"):
        parts.append(s.sample(min(n_per + 3, len(s)), random_state=1))
    rest = df[~df["post_uid"].isin(pd.concat(parts)["post_uid"])]
    parts.append(rest.sample(max(0, 60 - sum(len(p) for p in parts)), random_state=1))
    v = pd.concat(parts).sample(frac=1, random_state=2)
    cols = ["post_uid", "search_query", "author_name", "text"]
    out = v[cols].copy()
    for c in ["persona", "content_archetype", "evidence", "pillar", "epistemic_stance", "labor_implication",
              "deskilling_mode", "sentiment_-2_to_2", "aspects_present", "coder", "notes"]:
        out[c] = ""
    out.to_csv(FEAT / "validation_sample_for_coding.csv", index=False)
    v[["post_uid", "stance", "dmode", "roberta_post"] + [f"has_{a}" for a in ASPECTS]].to_csv(
        FEAT / "validation_sample_model_labels.csv", index=False)
    return int(len(out))


# ------------------------------------------------------------------ main
def main():
    from statsmodels.stats.multitest import multipletests
    posts, sents = load()
    flow, keep, english, core = sample_flow(posts)
    df = posts[keep].reset_index(drop=True)
    emb = np.load(FEAT / "emb_posts.npy")[keep.values]
    s_an = sents[sents["post_uid"].isin(df["post_uid"])]

    res = dict(sample_flow=flow, authors=authors(df), method_agreement=method_agreement(df, s_an),
               aspect_detection=aspect_detection_report(s_an), h1=h1_distribution(df),
               aspect_profile=aspect_profile(df))
    res["h2_creativity_vs_judgment"] = compare_aspects(df, "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    res["h3_technical_vs_representation"] = compare_aspects(df, "RQ3a_TechnicalEnvironmental", "RQ3b_RepresentationBIM")
    res["deskilling_vs_creativity"] = compare_aspects(df, "RQ1_Deskilling", "RQ2a_Creativity")
    res["h2_query_adjusted"] = query_adjusted(df, "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    # sensitivity: one post per author, and the wider English sample (off-domain included)
    one = df.drop_duplicates("author_name")
    res["h2_one_post_per_author"] = compare_aspects(one, "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    res["h2_english_all_domains"] = compare_aspects(posts[english], "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    res["h2_domain_strict"] = compare_aspects(posts[core], "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    res["h2_query_adjusted_english_all"] = query_adjusted(posts[english], "RQ2a_Creativity", "RQ2b_CognitiveJudgment")
    res["domain_by_query"] = sorted(
        [dict(query=q.replace('"', ""), n=int(len(g)), in_domain=r(g["domain_extended"].mean(), 3),
              sentiment=r(g["roberta_post"].mean(), 3), sentiment_in_domain=r(g.loc[g["domain_extended"], "roberta_post"].mean(), 3))
         for q, g in posts[english].groupby("search_query") if len(g) >= 15], key=lambda d: d["in_domain"])
    res["frame_effect_english_all"] = frame_effect(posts[english])
    res["stance_softmax_vs_dmode"] = {k: int(v) for k, v in df["dmode_softmax"].value_counts().items()}
    # BH across the confirmatory family (paired Wilcoxon, RoBERTa)
    fam = {k: res[k]["roberta"]["wilcoxon_p"] for k in
           ("h2_creativity_vs_judgment", "h3_technical_vs_representation", "deskilling_vs_creativity")}
    ok = {k: v for k, v in fam.items() if v is not None}
    if ok:
        rej, padj, _, _ = multipletests(list(ok.values()), method="fdr_bh")
        res["bh_adjusted"] = {k: dict(p=r(p, 6), p_bh=r(q, 6), reject=bool(x)) for k, p, q, x in
                              zip(ok, ok.values(), padj, rej)}
    res["frame_effect"] = frame_effect(df)
    res["framework_on_run013"] = framework_on_run013(df)
    res["topics"], lab = topics(df, emb)
    res["engagement"] = engagement(df)
    res["validation_sample_n"] = validation_sample(df)
    (OUT / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    df.assign(topic=lab).drop(columns=["text", "content_raw", "content_cleaned", "author_profile_url", "post_url"],
                              errors="ignore").to_pickle(FEAT / "analytic_sample.pkl")
    print(json.dumps({k: res[k] for k in ("sample_flow", "authors", "method_agreement")}, indent=1))


if __name__ == "__main__":
    main()
