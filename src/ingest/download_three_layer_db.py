"""Download the standalone 2026-10-18 three-layer Apify database from Neon into local SQLite, CSV, JSON, and JSONL files.

Usage:
    python3 src/ingest/download_three_layer_db.py
"""
import csv
import json
import os
import sqlite3
import urllib.parse
from pathlib import Path

import psycopg

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data/local/linkedin-apify-2026-10-17"
RAW_DIR = OUT_DIR / "apify_raw"
DB_NAME = "_saintiment_apify_three_layer_db"


def load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def make_db_url(base_url: str, db_name: str) -> str:
    parsed = urllib.parse.urlsplit(base_url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, f"/{db_name}", parsed.query, parsed.fragment))


def main():
    load_env()
    if "DATABASE_URL" not in os.environ:
        raise SystemExit("DATABASE_URL not found in environment or .env file.")

    db_url = make_db_url(os.environ["DATABASE_URL"], DB_NAME)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    sqlite_path = OUT_DIR / "apify_three_layer_2026-10-18.db"
    csv_path = OUT_DIR / "apify_three_layer_2026-10-18.csv"
    json_path = OUT_DIR / "apify_three_layer_2026-10-18.json"
    jsonl_path = RAW_DIR / "WUsK3RRYo7nKEOUbA.jsonl"

    print(f"Connecting to Neon database: {DB_NAME} ...")
    with psycopg.connect(db_url) as pg_conn, pg_conn.cursor() as pg_cur:
        pg_cur.execute("SELECT * FROM queries ORDER BY query_id")
        queries = pg_cur.fetchall()

        pg_cur.execute("SELECT id, run_id, source_item_id, source_post_id, query_id, query_code, payload::text FROM raw_items ORDER BY id")
        raw_items = pg_cur.fetchall()

        pg_cur.execute(
            """
            SELECT
                id, source, source_post_id, entity_id, share_urn, post_type, post_url, share_url,
                posted_at::text, posted_timestamp_ms, post_text, text_chars,
                author_id, author_type, author_name, author_public_id, author_universal_name,
                author_url, author_headline, author_website, author_urn,
                reactions, comments, shares, reactions_breakdown::text, content_attributes::text,
                newsletter_title, newsletter_url, repost_id, media::text,
                first_raw_item_id, matched_query_count, matched_query_codes, matched_families
            FROM master_posts
            ORDER BY id
            """
        )
        master_cols = [d.name for d in pg_cur.description]
        master_posts = pg_cur.fetchall()

        pg_cur.execute("SELECT post_id, query_id, query_code, query_family, run_id FROM post_query_hits")
        hits = pg_cur.fetchall()

    # 1. Write JSONL
    with jsonl_path.open("w", encoding="utf-8") as f:
        for r in raw_items:
            f.write(r[6] + "\n")
    print(f"Saved raw JSONL ({len(raw_items)} items): {jsonl_path}")

    # 2. Write CSV & JSON of unique master_posts
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(master_cols)
        w.writerows(master_posts)
    print(f"Saved master_posts CSV ({len(master_posts)} unique posts): {csv_path}")

    json_records = [dict(zip(master_cols, row)) for row in master_posts]
    json_path.write_text(json.dumps(json_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved master_posts JSON ({len(json_records)} unique posts): {json_path}")

    # 3. Write SQLite DB
    if sqlite_path.exists():
        sqlite_path.unlink()
    sconn = sqlite3.connect(str(sqlite_path))
    scur = sconn.cursor()
    scur.executescript(
        """
        CREATE TABLE queries (
            query_id INTEGER PRIMARY KEY,
            query_code TEXT UNIQUE NOT NULL,
            query_family TEXT NOT NULL,
            operators INTEGER NOT NULL,
            layers INTEGER NOT NULL,
            query_text TEXT UNIQUE NOT NULL,
            raw_hits_count INTEGER DEFAULT 0
        );
        CREATE TABLE raw_items (
            id INTEGER PRIMARY KEY,
            run_id TEXT NOT NULL,
            source_item_id TEXT UNIQUE NOT NULL,
            source_post_id TEXT NOT NULL,
            query_id INTEGER NOT NULL,
            query_code TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        CREATE TABLE master_posts (
            id INTEGER PRIMARY KEY,
            source TEXT, source_post_id TEXT UNIQUE, entity_id TEXT, share_urn TEXT,
            post_type TEXT, post_url TEXT, share_url TEXT, posted_at TEXT, posted_timestamp_ms INTEGER,
            post_text TEXT, text_chars INTEGER, author_id TEXT, author_type TEXT, author_name TEXT,
            author_public_id TEXT, author_universal_name TEXT, author_url TEXT, author_headline TEXT,
            author_website TEXT, author_urn TEXT, reactions INTEGER, comments INTEGER, shares INTEGER,
            reactions_breakdown TEXT, content_attributes TEXT, newsletter_title TEXT, newsletter_url TEXT,
            repost_id TEXT, media TEXT, first_raw_item_id INTEGER, matched_query_count INTEGER,
            matched_query_codes TEXT, matched_families TEXT
        );
        CREATE TABLE post_query_hits (
            post_id INTEGER, query_id INTEGER, query_code TEXT, query_family TEXT, run_id TEXT,
            PRIMARY KEY (post_id, query_id, run_id)
        );
        """
    )
    scur.executemany("INSERT INTO queries VALUES (?,?,?,?,?,?,?)", queries)
    scur.executemany("INSERT INTO raw_items VALUES (?,?,?,?,?,?,?)", raw_items)
    scur.executemany("INSERT INTO master_posts VALUES (" + ",".join(["?"] * 34) + ")", master_posts)
    scur.executemany("INSERT INTO post_query_hits VALUES (?,?,?,?,?)", hits)
    sconn.commit()
    sconn.close()
    print(f"Saved SQLite DB: {sqlite_path}")


if __name__ == "__main__":
    main()
