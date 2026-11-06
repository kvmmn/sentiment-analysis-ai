"""Seed the shared team Swipe Review database on Neon (`_saintiment_swipe_team_db`).

Splits the 1,858 unique Apify posts into three non-overlapping review sets
(1. Morteza, 2. Iman, 3. Kaveh) with a fixed-seed shuffle, so the split is
reproducible and each set gets a similar mix of queries and dates.

Usage:
    python3 src/ingest/build_team_swipe_db.py            # create + seed (refuses if decisions exist)
    python3 src/ingest/build_team_swipe_db.py --force    # wipe decisions and reseed
    python3 src/ingest/build_team_swipe_db.py --print-url  # print the team DB URL for Vercel's DATABASE_URL

Reads DATABASE_URL (any database on the same Neon server) from the environment or .env.
Requires: psycopg[binary] (v3). Post text stays in Neon; nothing is written to git.
"""
import argparse
import os
import random
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_curated_db import SOURCE_SQLITE, load_env, make_db_url  # noqa: E402

TEAM_DB = "_saintiment_swipe_team_db"
SEED = 20261106
REVIEWERS = [(1, "مرتضی", "Morteza"), (2, "ایمان", "Iman"), (3, "کاوه", "Kaveh")]

POST_COLS = [
    "source_post_id", "post_type", "post_url", "posted_at", "post_text", "text_chars",
    "author_type", "author_name", "author_headline", "author_url",
    "reactions", "comments", "shares", "media",
    "matched_query_count", "matched_query_codes", "matched_families",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS reviewers (
    id SMALLINT PRIMARY KEY,
    name TEXT NOT NULL,
    name_en TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS posts (
    source_post_id TEXT PRIMARY KEY,
    reviewer_id SMALLINT NOT NULL REFERENCES reviewers(id),
    position INTEGER NOT NULL,
    post_type TEXT,
    post_url TEXT,
    posted_at TEXT,
    post_text TEXT,
    text_chars INTEGER,
    author_type TEXT,
    author_name TEXT,
    author_headline TEXT,
    author_url TEXT,
    reactions INTEGER,
    comments INTEGER,
    shares INTEGER,
    media TEXT,
    matched_query_count INTEGER,
    matched_query_codes TEXT,
    matched_families TEXT,
    UNIQUE (reviewer_id, position)
);
CREATE TABLE IF NOT EXISTS decisions (
    source_post_id TEXT PRIMARY KEY REFERENCES posts(source_post_id) ON DELETE CASCADE,
    reviewer_id SMALLINT NOT NULL REFERENCES reviewers(id),
    status TEXT NOT NULL CHECK (status IN ('keep', 'reject')),
    decided_by SMALLINT REFERENCES reviewers(id),
    decided_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS posts_reviewer_pos ON posts (reviewer_id, position);
CREATE INDEX IF NOT EXISTS decisions_reviewer ON decisions (reviewer_id);
"""


def clean(value):
    return value.replace("\x00", "") if isinstance(value, str) else value


def load_posts():
    if not SOURCE_SQLITE.exists():
        raise SystemExit(
            f"Source SQLite DB not found at {SOURCE_SQLITE}. "
            "Run `python3 src/ingest/download_three_layer_db.py` first."
        )
    conn = sqlite3.connect(str(SOURCE_SQLITE))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(f"SELECT {', '.join(POST_COLS)} FROM master_posts").fetchall()
    conn.close()
    return [{k: clean(r[k]) for k in POST_COLS} for r in rows]


def split_posts(posts):
    """Fixed-seed shuffle, then round-robin into the three sets."""
    ordered = sorted(posts, key=lambda p: str(p["source_post_id"]))
    random.Random(SEED).shuffle(ordered)
    out = []
    counters = {rid: 0 for rid, _, _ in REVIEWERS}
    for i, p in enumerate(ordered):
        rid = REVIEWERS[i % len(REVIEWERS)][0]
        counters[rid] += 1
        out.append({**p, "source_post_id": str(p["source_post_id"]), "reviewer_id": rid, "position": counters[rid]})
    return out


def ensure_database(base_url):
    import psycopg

    with psycopg.connect(make_db_url(base_url, "neondb"), autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEAM_DB,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{TEAM_DB}"')
            print(f"Created Neon database {TEAM_DB}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="Delete existing decisions and reseed posts.")
    ap.add_argument("--print-url", action="store_true", help="Print the team DB connection URL and exit.")
    args = ap.parse_args()

    load_env()
    base_url = os.environ.get("DATABASE_URL")
    if not base_url:
        raise SystemExit("DATABASE_URL not found in environment or .env file.")
    team_url = make_db_url(base_url, TEAM_DB)
    if args.print_url:
        print(team_url)
        return

    import psycopg

    posts = split_posts(load_posts())
    ensure_database(base_url)

    with psycopg.connect(team_url) as conn, conn.cursor() as cur:
        cur.execute(SCHEMA)
        cur.execute("SELECT count(*) FROM decisions")
        n_dec = cur.fetchone()[0]
        if n_dec and not args.force:
            raise SystemExit(
                f"{n_dec} decisions already saved in {TEAM_DB}; refusing to reseed. "
                "Use --force only if you really want to wipe them."
            )
        cur.execute("DELETE FROM decisions")
        cur.execute("DELETE FROM posts")
        cur.executemany(
            "INSERT INTO reviewers (id, name, name_en) VALUES (%s, %s, %s) "
            "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, name_en = EXCLUDED.name_en",
            REVIEWERS,
        )
        cols = ["reviewer_id", "position"] + POST_COLS
        cur.executemany(
            f"INSERT INTO posts ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})",
            [tuple(p[c] for c in cols) for p in posts],
        )
        cur.execute("SELECT reviewer_id, count(*) FROM posts GROUP BY reviewer_id ORDER BY reviewer_id")
        counts = cur.fetchall()
        conn.commit()

    print(f"Seeded {len(posts)} posts into {TEAM_DB}:")
    names = {rid: f"{rid}. {en}" for rid, _, en in REVIEWERS}
    for rid, n in counts:
        print(f"  {names[rid]}: {n}")


if __name__ == "__main__":
    main()
