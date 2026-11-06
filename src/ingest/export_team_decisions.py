"""Export all team Swipe Review decisions from Neon (`_saintiment_swipe_team_db`)
into the decisions-file format that `build_curated_db.py` already reads.

Usage:
    python3 src/ingest/export_team_decisions.py [--out PATH]
    python3 src/ingest/build_curated_db.py data/local/linkedin-apify-2026-10-17/saintiment_swipe_decisions.json --push-neon
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_curated_db import DATA_DIR, load_env, make_db_url  # noqa: E402
from build_team_swipe_db import TEAM_DB  # noqa: E402

LIVE_DECISIONS_JSON = DATA_DIR / "saintiment_swipe_decisions.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=LIVE_DECISIONS_JSON)
    args = ap.parse_args()

    load_env()
    if "DATABASE_URL" not in os.environ:
        raise SystemExit("DATABASE_URL not found in environment or .env file.")

    import psycopg

    with psycopg.connect(make_db_url(os.environ["DATABASE_URL"], TEAM_DB)) as conn, conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM posts")
        total = cur.fetchone()[0]
        cur.execute(
            "SELECT d.source_post_id, d.status, d.updated_at, d.reviewer_id, d.decided_by, r.name_en "
            "FROM decisions d JOIN reviewers r ON r.id = d.reviewer_id ORDER BY d.source_post_id"
        )
        rows = cur.fetchall()
        cur.execute(
            "SELECT r.id, r.name_en, count(p.*), count(d.*) FROM reviewers r "
            "LEFT JOIN posts p ON p.reviewer_id = r.id "
            "LEFT JOIN decisions d ON d.source_post_id = p.source_post_id "
            "GROUP BY r.id, r.name_en ORDER BY r.id"
        )
        per_set = cur.fetchall()

    decisions = {
        pid: {
            "status": status,
            "timestamp": ts.isoformat(),
            "set": rid,
            "set_name": name,
            "decided_by": by,
        }
        for pid, status, ts, rid, by, name in rows
    }
    kept = sum(1 for d in decisions.values() if d["status"] == "keep")
    out = {
        "project": "Saintiment",
        "source": f"neon:{TEAM_DB}",
        "source_run_id": "X2gdX05u8rP41b4rG",
        "source_dataset_id": "WUsK3RRYo7nKEOUbA",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "summary": {"total_posts": total, "kept": kept, "rejected": len(decisions) - kept},
        "sets": [{"id": i, "name": n, "total": t, "reviewed": r} for i, n, t, r in per_set],
        "decisions": decisions,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(decisions)} decisions ({kept} keep) to {args.out}")
    for i, n, t, r in per_set:
        print(f"  {i}. {n}: {r}/{t} reviewed")


if __name__ == "__main__":
    main()
