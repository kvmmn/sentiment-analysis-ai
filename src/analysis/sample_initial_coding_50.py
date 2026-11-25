"""Stratified random sampling (n = 50) from the 395 curated `keep` posts
for preliminary initial coding across Morteza, Iman, and Kaveh.

Methodology:
1. Load `status == "keep"` decisions from the team swipe snapshot and join
   with `master_posts` in the three-layer SQLite archive.
2. Apply pre-sampling eligibility filters:
   - Exclude posts with insufficient prose (< 15 words or < 100 chars after
     stripping hashtags and URLs).
   - Deduplicate exact normalized `post_text`, keeping the lowest
     `source_post_id`.
3. Draw n = 50 posts using 2D proportional stratified random sampling across
   (reviewer_set x primary_family) via Hamilton (Largest Remainder) quotas
   with fixed SEED = 20261125 and strict author uniqueness (max 1 post per
   normalized author_name across the sample).
4. Shuffle selected posts with SEED + 1 for blind presentation order (S01..S50)
   and export a 5-sheet XLSX workbook, blind CSV, and full provenance manifest.

Usage:
    python3 src/analysis/sample_initial_coding_50.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data/local/linkedin-apify-2026-10-17"
DECISIONS_PATH = DATA_DIR / "saintiment_swipe_decisions_2026-11-25.json"
SQLITE_PATH = DATA_DIR / "apify_three_layer_2026-10-18.db"
OUT_DIR = DATA_DIR / "coding_sample_50_2026-11-25"

XLSX_PATH = OUT_DIR / "saintiment_initial_coding_50_2026-11-25.xlsx"
CSV_PATH = OUT_DIR / "initial_coding_50_blind.csv"
MANIFEST_PATH = OUT_DIR / "initial_coding_50_manifest.json"

SEED = 20261125
SAMPLE_SIZE = 50
MIN_PROSE_WORDS = 15
MIN_PROSE_CHARS = 100

CODER_TABS = ["Morteza", "Iman", "Kaveh"]
BLIND_COLS = [
    "sample_id",
    "source_post_id",
    "posted_at",
    "author_name",
    "author_headline",
    "author_type",
    "post_url",
    "post_text",
    "initial_codes",
    "primary_theme",
    "stance_sentiment",
    "stakeholder_role",
    "relevance_flag",
    "coder_notes",
]
MASTER_COLS = [
    "sample_id",
    "source_post_id",
    "reviewer_set",
    "primary_family",
    "matched_families",
    "matched_query_codes",
    "text_chars",
    "reactions",
    "comments",
    "shares",
    "posted_at",
    "author_type",
    "post_url",
]

HASHTAG_RE = re.compile(r"#\S+")
URL_RE = re.compile(r"https?://\S+")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_prose(text: str) -> tuple[int, int]:
    """Return (prose_word_count, prose_char_count) after removing hashtags and URLs."""
    no_tags = HASHTAG_RE.sub(" ", text or "")
    no_urls = URL_RE.sub(" ", no_tags)
    collapsed = " ".join(no_urls.split())
    words = len(collapsed.split()) if collapsed else 0
    return words, len(collapsed)


def normalize_text(text: str) -> str:
    return " ".join((text or "").lower().split())


def normalize_author(name: str) -> str:
    return " ".join((name or "").lower().split())


def primary_family_of(matched_families: str | None) -> str:
    parts = [p.strip() for p in (matched_families or "").split(",") if p.strip()]
    return parts[0] if parts else "unknown"


def hamilton_apportionment(counts: dict[tuple[str, str], int], target: int) -> dict[tuple[str, str], int]:
    """Allocate integer quotas summing to `target` using Largest Remainder Method."""
    total = sum(counts.values())
    if total == 0:
        raise ValueError("Cannot apportion across zero eligible posts.")
    raw = {k: (v * target) / total for k, v in counts.items()}
    quotas = {k: math.floor(val) for k, val in raw.items()}
    remainder = target - sum(quotas.values())
    ranked = sorted(
        counts.keys(),
        key=lambda k: (raw[k] - quotas[k], counts[k], k),
        reverse=True,
    )
    for k in ranked[:remainder]:
        quotas[k] += 1
    return quotas


def percentile_stats(values: list[int]) -> dict[str, float]:
    s = sorted(values)
    n = len(s)
    if n == 0:
        return {"min": 0, "q1": 0, "median": 0, "q3": 0, "iqr": 0, "max": 0}

    def pct(p: float) -> float:
        idx = (n - 1) * p
        lo = math.floor(idx)
        hi = math.ceil(idx)
        if lo == hi:
            return float(s[lo])
        return s[lo] + (s[hi] - s[lo]) * (idx - lo)

    q1 = pct(0.25)
    med = pct(0.50)
    q3 = pct(0.75)
    return {
        "min": float(s[0]),
        "q1": round(q1, 1),
        "median": round(med, 1),
        "q3": round(q3, 1),
        "iqr": round(q3 - q1, 1),
        "max": float(s[-1]),
    }


def distribution_summary(rows: list[dict]) -> dict:
    n = len(rows)

    def dist(key_fn) -> dict[str, dict[str, float | int]]:
        c = Counter(key_fn(r) for r in rows)
        return {
            k: {"count": v, "pct": round((v / n) * 100, 2) if n else 0.0}
            for k, v in sorted(c.items())
        }

    return {
        "n": n,
        "reviewer_set": dist(lambda r: r["reviewer_set"]),
        "primary_family": dist(lambda r: r["primary_family"]),
        "author_type": dist(lambda r: r["author_type"] or "unknown"),
        "year": dist(lambda r: (r["posted_at"] or "")[:4] or "unknown"),
        "text_chars": percentile_stats([int(r["text_chars"] or 0) for r in rows]),
    }


def load_kept_posts() -> list[dict]:
    dec_data = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    kept_decisions = {
        str(pid): info
        for pid, info in dec_data["decisions"].items()
        if info.get("status") == "keep"
    }
    if len(kept_decisions) != 395:
        raise RuntimeError(f"Expected 395 kept posts, found {len(kept_decisions)}")

    conn = sqlite3.connect(str(SQLITE_PATH))
    conn.row_factory = sqlite3.Row
    db_rows = conn.execute(
        """
        SELECT source_post_id, post_type, post_url, posted_at, post_text, text_chars,
               author_type, author_name, author_headline,
               reactions, comments, shares,
               matched_query_codes, matched_families
        FROM master_posts
        """
    ).fetchall()
    conn.close()

    by_id = {str(r["source_post_id"]): dict(r) for r in db_rows}
    missing = [pid for pid in kept_decisions if pid not in by_id]
    if missing:
        raise RuntimeError(f"Missing {len(missing)} kept IDs in SQLite: {missing[:5]}")

    merged = []
    for pid in sorted(kept_decisions.keys()):
        row = dict(by_id[pid])
        row["source_post_id"] = pid
        row["reviewer_set"] = kept_decisions[pid]["set_name"]
        row["primary_family"] = primary_family_of(row.get("matched_families"))
        merged.append(row)
    return merged


def filter_eligible(posts: list[dict]) -> tuple[list[dict], list[dict]]:
    excluded: list[dict] = []
    prose_passed: list[dict] = []

    for p in posts:
        words, chars = strip_prose(p.get("post_text") or "")
        if words < MIN_PROSE_WORDS or chars < MIN_PROSE_CHARS:
            excluded.append({
                "source_post_id": p["source_post_id"],
                "reviewer_set": p["reviewer_set"],
                "text_chars": int(p.get("text_chars") or 0),
                "prose_words": words,
                "prose_chars": chars,
                "reason": "insufficient_prose",
            })
        else:
            prose_passed.append(p)

    seen_texts: dict[str, str] = {}
    eligible: list[dict] = []
    for p in sorted(prose_passed, key=lambda x: x["source_post_id"]):
        norm = normalize_text(p.get("post_text") or "")
        if norm in seen_texts:
            excluded.append({
                "source_post_id": p["source_post_id"],
                "reviewer_set": p["reviewer_set"],
                "text_chars": int(p.get("text_chars") or 0),
                "duplicate_of": seen_texts[norm],
                "reason": "exact_duplicate_text",
            })
        else:
            seen_texts[norm] = p["source_post_id"]
            eligible.append(p)

    return eligible, excluded


def sample_stratified(eligible: list[dict]) -> tuple[list[dict], dict[tuple[str, str], int], dict[tuple[str, str], int]]:
    strata: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for p in eligible:
        strata[(p["reviewer_set"], p["primary_family"])].append(p)

    counts = {k: len(v) for k, v in strata.items()}
    quotas = hamilton_apportionment(counts, SAMPLE_SIZE)

    rng = random.Random(SEED)
    used_authors: set[str] = set()
    selected: list[dict] = []
    realized: dict[tuple[str, str], int] = {}

    for key in sorted(strata.keys()):
        pool = sorted(strata[key], key=lambda p: p["source_post_id"])
        rng.shuffle(pool)
        quota = quotas[key]
        taken = 0
        for p in pool:
            if taken >= quota:
                break
            author_key = normalize_author(p.get("author_name") or "")
            if author_key and author_key in used_authors:
                continue
            if author_key:
                used_authors.add(author_key)
            selected.append(p)
            taken += 1
        if taken < quota:
            raise RuntimeError(
                f"Stratum {key} could only fill {taken}/{quota} posts under strict author uniqueness."
            )
        realized[key] = taken

    blind_rng = random.Random(SEED + 1)
    blind_order = list(selected)
    blind_rng.shuffle(blind_order)
    for idx, p in enumerate(blind_order, start=1):
        p["sample_id"] = f"S{idx:02d}"

    return blind_order, quotas, realized


def style_sheet(ws, headers: list[str], col_widths: dict[str, int], wrap_cols: set[str]) -> None:
    ws.freeze_panes = "A2"
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=10)
    header_align = Alignment(vertical="center", horizontal="left", wrap_text=True)

    for col_idx, name in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align
        letter = cell.column_letter
        ws.column_dimensions[letter].width = col_widths.get(name, 18)

    ws.row_dimensions[1].height = 26
    body_font = Font(size=10)
    for row_idx in range(2, ws.max_row + 1):
        for col_idx, name in enumerate(headers, start=1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = body_font
            cell.alignment = Alignment(
                vertical="top",
                horizontal="left",
                wrap_text=(name in wrap_cols),
            )


def write_workbook(sample: list[dict], eligible_summary: dict, sample_summary: dict, excluded: list[dict]) -> None:
    wb = Workbook()
    readme_ws = wb.active
    readme_ws.title = "README_Protocol"

    readme_rows = [
        ["Saintiment — Preliminary Initial Coding Sample (n = 50)", ""],
        ["Purpose", "Independent blind initial coding (open coding) across Morteza, Iman, and Kaveh prior to the Nov 26 team meeting."],
        ["Sampling Frame", "395 team-curated `keep` posts from the 48-query three-layer Apify corpus (run X2gdX05u8rP41b4rG)."],
        ["Pre-Sampling Filtering", f"{len(excluded)} posts excluded before sampling ({sum(1 for e in excluded if e['reason']=='insufficient_prose')} insufficient prose, {sum(1 for e in excluded if e['reason']=='exact_duplicate_text')} exact duplicate text). Eligible frame: {eligible_summary['n']} posts."],
        ["Sampling Design", f"2D proportional stratified random sample (reviewer_set x primary_family) using Hamilton quotas, SEED={SEED}, max 1 post per author, shuffled in blind order S01..S50."],
        ["Instructions for Coders", ""],
        ["1. Independence", "Work ONLY in your own tab (Morteza / Iman / Kaveh). Do not inspect other tabs or Master_Metadata before finishing your 50 codes."],
        ["2. Columns to Fill", "Fill `initial_codes` (comma-separated descriptive/in-vivo codes), `primary_theme`, `stance_sentiment` (-1 / 0 / +1 or Mixed), `stakeholder_role` (Academic / Practitioner / Student / Industry Leader / Other), `relevance_flag` (Yes / Borderline / No), and optional `coder_notes`."],
        ["3. Blindness", "Coder tabs intentionally omit `reviewer_set`, `matched_families`, and `matched_query_codes` to reduce framing bias."],
        ["Sample Size", f"{sample_summary['n']} unique posts by {sample_summary['n']} unique authors (median {sample_summary['text_chars']['median']} chars)."],
    ]
    for r in readme_rows:
        readme_ws.append(r)
    readme_ws.column_dimensions["A"].width = 28
    readme_ws.column_dimensions["B"].width = 96
    readme_ws["A1"].font = Font(bold=True, size=13)
    for row in readme_ws.iter_rows(min_row=2, max_row=len(readme_rows)):
        row[0].font = Font(bold=True, size=10)
        row[0].alignment = Alignment(vertical="top", wrap_text=True)
        row[1].alignment = Alignment(vertical="top", wrap_text=True)

    blind_widths = {
        "sample_id": 11,
        "source_post_id": 22,
        "posted_at": 14,
        "author_name": 24,
        "author_headline": 36,
        "author_type": 13,
        "post_url": 34,
        "post_text": 72,
        "initial_codes": 28,
        "primary_theme": 22,
        "stance_sentiment": 16,
        "stakeholder_role": 20,
        "relevance_flag": 15,
        "coder_notes": 30,
    }
    blind_wrap = {"author_headline", "post_text", "initial_codes", "primary_theme", "coder_notes"}

    for tab in CODER_TABS:
        ws = wb.create_sheet(title=tab)
        ws.append(BLIND_COLS)
        for p in sample:
            ws.append([
                p["sample_id"],
                p["source_post_id"],
                (p.get("posted_at") or "")[:10],
                p.get("author_name") or "",
                p.get("author_headline") or "",
                p.get("author_type") or "",
                p.get("post_url") or "",
                p.get("post_text") or "",
                "",
                "",
                "",
                "",
                "",
                "",
            ])
        style_sheet(ws, BLIND_COLS, blind_widths, blind_wrap)

    meta_ws = wb.create_sheet(title="Master_Metadata")
    meta_ws.append(MASTER_COLS)
    for p in sample:
        meta_ws.append([
            p["sample_id"],
            p["source_post_id"],
            p["reviewer_set"],
            p["primary_family"],
            p.get("matched_families") or "",
            p.get("matched_query_codes") or "",
            int(p.get("text_chars") or 0),
            int(p.get("reactions") or 0),
            int(p.get("comments") or 0),
            int(p.get("shares") or 0),
            (p.get("posted_at") or "")[:10],
            p.get("author_type") or "",
            p.get("post_url") or "",
        ])
    meta_widths = {
        "sample_id": 11,
        "source_post_id": 22,
        "reviewer_set": 14,
        "primary_family": 22,
        "matched_families": 26,
        "matched_query_codes": 24,
        "text_chars": 12,
        "reactions": 11,
        "comments": 11,
        "shares": 10,
        "posted_at": 14,
        "author_type": 13,
        "post_url": 34,
    }
    style_sheet(meta_ws, MASTER_COLS, meta_widths, {"matched_families", "matched_query_codes"})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wb.save(str(XLSX_PATH))


def write_blind_csv(sample: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(BLIND_COLS)
        for p in sample:
            writer.writerow([
                p["sample_id"],
                p["source_post_id"],
                (p.get("posted_at") or "")[:10],
                p.get("author_name") or "",
                p.get("author_headline") or "",
                p.get("author_type") or "",
                p.get("post_url") or "",
                p.get("post_text") or "",
                "",
                "",
                "",
                "",
                "",
                "",
            ])


def main() -> None:
    kept_posts = load_kept_posts()
    eligible, excluded = filter_eligible(kept_posts)
    sample, quotas, realized = sample_stratified(eligible)

    eligible_summary = distribution_summary(eligible)
    sample_summary = distribution_summary(sample)

    write_workbook(sample, eligible_summary, sample_summary, excluded)
    write_blind_csv(sample)

    strata_table = [
        {
            "reviewer_set": k[0],
            "primary_family": k[1],
            "eligible_count": sum(
                1 for p in eligible if p["reviewer_set"] == k[0] and p["primary_family"] == k[1]
            ),
            "quota": quotas[k],
            "realized": realized[k],
        }
        for k in sorted(quotas.keys())
    ]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "blind_order_seed": SEED + 1,
        "sample_size": len(sample),
        "eligibility_rules": {
            "min_prose_words": MIN_PROSE_WORDS,
            "min_prose_chars": MIN_PROSE_CHARS,
            "exact_normalized_text_dedup": True,
            "max_posts_per_author": 1,
        },
        "inputs": {
            "decisions_path": str(DECISIONS_PATH.relative_to(ROOT)),
            "decisions_sha256": sha256_file(DECISIONS_PATH),
            "sqlite_path": str(SQLITE_PATH.relative_to(ROOT)),
            "sqlite_sha256": sha256_file(SQLITE_PATH),
        },
        "outputs": {
            "xlsx_path": str(XLSX_PATH.relative_to(ROOT)),
            "xlsx_sha256": sha256_file(XLSX_PATH),
            "csv_path": str(CSV_PATH.relative_to(ROOT)),
            "csv_sha256": sha256_file(CSV_PATH),
        },
        "counts": {
            "curated_keep_total": len(kept_posts),
            "excluded_total": len(excluded),
            "excluded_insufficient_prose": sum(1 for e in excluded if e["reason"] == "insufficient_prose"),
            "excluded_exact_duplicate_text": sum(1 for e in excluded if e["reason"] == "exact_duplicate_text"),
            "eligible_frame_total": len(eligible),
            "sample_total": len(sample),
        },
        "excluded_posts": excluded,
        "strata_quotas": strata_table,
        "representativeness": {
            "eligible_frame": eligible_summary,
            "sample": sample_summary,
        },
        "sample_posts": [
            {
                "sample_id": p["sample_id"],
                "source_post_id": p["source_post_id"],
                "reviewer_set": p["reviewer_set"],
                "primary_family": p["primary_family"],
                "author_type": p.get("author_type") or "",
                "posted_at": (p.get("posted_at") or "")[:10],
                "text_chars": int(p.get("text_chars") or 0),
            }
            for p in sample
        ],
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Curated keep total: {len(kept_posts)}")
    print(
        f"Excluded: {len(excluded)} "
        f"(insufficient_prose={manifest['counts']['excluded_insufficient_prose']}, "
        f"exact_duplicate_text={manifest['counts']['excluded_exact_duplicate_text']})"
    )
    print(f"Eligible frame: {len(eligible)}")
    print(f"Sample size: {len(sample)}")
    print("\n12-Stratum Quotas:")
    for row in strata_table:
        print(f"  {row['reviewer_set']:7s} x {row['primary_family']:22s}: eligible={row['eligible_count']:3d} -> quota={row['quota']:2d} (realized={row['realized']:2d})")
    print("\nBalance (Eligible Frame vs. Sample):")
    for dim in ["reviewer_set", "primary_family", "author_type", "year"]:
        print(f"  [{dim}]")
        e_dim = eligible_summary[dim]
        s_dim = sample_summary[dim]
        for k in sorted(set(e_dim) | set(s_dim)):
            ec = e_dim.get(k, {"count": 0, "pct": 0.0})
            sc = s_dim.get(k, {"count": 0, "pct": 0.0})
            diff = sc["pct"] - ec["pct"]
            print(f"    {k:24s}: frame={ec['count']:3d} ({ec['pct']:5.2f}%) | sample={sc['count']:2d} ({sc['pct']:5.2f}%) | delta={diff:+5.2f} pp")
    print(f"  [text_chars] frame={eligible_summary['text_chars']} | sample={sample_summary['text_chars']}")
    print(f"\nWrote XLSX: {XLSX_PATH}")
    print(f"Wrote CSV : {CSV_PATH}")
    print(f"Wrote JSON: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
