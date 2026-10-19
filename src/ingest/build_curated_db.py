"""Build a new curated SQLite database (and optionally a new Neon Postgres database)
from the interactive Swipe Review decisions file exported by `docs/swipe-review.html`.

Usage:
    .venv/bin/python src/ingest/build_curated_db.py path/to/saintiment_swipe_decisions.json [--push-neon]
"""
import argparse
import csv
import json
import os
import sqlite3
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data/local/linkedin-apify-2026-10-17"
SOURCE_SQLITE = DATA_DIR / "apify_three_layer_2026-10-18.db"
CURATED_SQLITE = DATA_DIR / "apify_curated_2026-10-19.db"
CURATED_CSV = DATA_DIR / "apify_curated_2026-10-19.csv"
CURATED_JSON = DATA_DIR / "apify_curated_2026-10-19.json"
NEON_CURATED_DB = "_saintiment_apify_curated_db"


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


def parse_decisions(input_path: Path) -> dict[str, dict]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and "decisions" in raw and isinstance(raw["decisions"], dict):
        return raw["decisions"]
    if isinstance(raw, list):
        # Exported array of kept posts
        out = {}
        for row in raw:
            pid = str(row.get("source_post_id") or row.get("id") or "")
            if pid:
                out[pid] = {
                    "status": "keep",
                    "timestamp": row.get("curated_at") or datetime.now(timezone.utc).isoformat(),
                }
        return out
    if isinstance(raw, dict):
        return raw
    raise ValueError(f"Unsupported JSON structure in {input_path}")


def build_local_curated_sqlite(decisions: dict[str, dict], out_sqlite: Path, out_csv: Path, out_json: Path):
    if not SOURCE_SQLITE.exists():
        raise SystemExit(
            f"Source SQLite DB not found at {SOURCE_SQLITE}. "
            "Run `.venv/bin/python src/ingest/download_three_layer_db.py` first."
        )

    keep_ids = {pid for pid, meta in decisions.items() if isinstance(meta, dict) and meta.get("status") == "keep"}
    if not keep_ids:
        raise SystemExit("No posts with status == 'keep' found in the decisions file.")

    src_conn = sqlite3.connect(str(SOURCE_SQLITE))
    src_cur = src_conn.cursor()

    src_cur.execute("SELECT * FROM runs")
    runs_rows = src_cur.fetchall()

    src_cur.execute("SELECT * FROM queries ORDER BY query_id")
    queries_rows = src_cur.fetchall()

    src_cur.execute("SELECT * FROM master_posts ORDER BY id")
    master_cols = [d[0] for d in src_cur.description]
    spid_idx = master_cols.index("source_post_id")
    id_idx = master_cols.index("id")
    all_master = src_cur.fetchall()
    kept_master = [row for row in all_master if str(row[spid_idx]) in keep_ids]
    kept_post_pk_ids = {row[id_idx] for row in kept_master}

    src_cur.execute("SELECT * FROM raw_items ORDER BY id")
    all_raw = src_cur.fetchall()
    kept_raw = [row for row in all_raw if str(row[3]) in keep_ids]

    src_cur.execute("SELECT * FROM post_query_hits")
    all_hits = src_cur.fetchall()
    kept_hits = [row for row in all_hits if row[0] in kept_post_pk_ids]
    src_conn.close()

    out_sqlite.parent.mkdir(parents=True, exist_ok=True)
    if out_sqlite.exists():
        out_sqlite.unlink()

    dst_conn = sqlite3.connect(str(out_sqlite))
    dst_cur = dst_conn.cursor()
    dst_cur.executescript(
        """
        CREATE TABLE runs (
            run_id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            tool TEXT NOT NULL,
            dataset_id TEXT NOT NULL,
            started_at TEXT,
            finished_at TEXT,
            usage_usd REAL,
            n_queries INTEGER,
            raw_item_count INTEGER,
            unique_post_count INTEGER,
            input_json TEXT
        );
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
            source TEXT NOT NULL,
            source_post_id TEXT UNIQUE NOT NULL,
            entity_id TEXT,
            share_urn TEXT,
            post_type TEXT,
            post_url TEXT,
            share_url TEXT,
            posted_at TEXT,
            posted_timestamp_ms INTEGER,
            post_text TEXT,
            text_chars INTEGER,
            author_id TEXT,
            author_type TEXT,
            author_name TEXT,
            author_public_id TEXT,
            author_universal_name TEXT,
            author_url TEXT,
            author_headline TEXT,
            author_website TEXT,
            author_urn TEXT,
            reactions INTEGER,
            comments INTEGER,
            shares INTEGER,
            reactions_breakdown TEXT,
            content_attributes TEXT,
            newsletter_title TEXT,
            newsletter_url TEXT,
            repost_id TEXT,
            media TEXT,
            first_raw_item_id INTEGER,
            matched_query_count INTEGER DEFAULT 1,
            matched_query_codes TEXT,
            matched_families TEXT
        );
        CREATE TABLE post_query_hits (
            post_id INTEGER NOT NULL,
            query_id INTEGER NOT NULL,
            query_code TEXT NOT NULL,
            query_family TEXT NOT NULL,
            run_id TEXT NOT NULL,
            PRIMARY KEY (post_id, query_id, run_id)
        );
        CREATE TABLE curation_decisions (
            source_post_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            decided_at TEXT
        );
        """
    )

    dst_cur.executemany("INSERT INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?)", runs_rows)
    dst_cur.executemany("INSERT INTO queries VALUES (?,?,?,?,?,?,?)", queries_rows)
    dst_cur.executemany("INSERT INTO raw_items VALUES (?,?,?,?,?,?,?)", kept_raw)
    dst_cur.executemany(
        "INSERT INTO master_posts VALUES (" + ",".join(["?"] * len(master_cols)) + ")",
        kept_master,
    )
    dst_cur.executemany("INSERT INTO post_query_hits VALUES (?,?,?,?,?)", kept_hits)
    decision_rows = [
        (str(pid), str(meta.get("status", "")), str(meta.get("timestamp", "")))
        for pid, meta in decisions.items()
        if isinstance(meta, dict) and meta.get("status") in ("keep", "reject")
    ]
    dst_cur.executemany("INSERT INTO curation_decisions VALUES (?,?,?)", decision_rows)
    dst_conn.commit()
    dst_conn.close()

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(master_cols)
        w.writerows(kept_master)

    json_records = [dict(zip(master_cols, row)) for row in kept_master]
    out_json.write_text(json.dumps(json_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Created new curated SQLite DB: {out_sqlite}")
    print(f"  - master_posts (kept): {len(kept_master)}")
    print(f"  - raw_items (kept):    {len(kept_raw)}")
    print(f"  - post_query_hits:     {len(kept_hits)}")
    print(f"  - curation_decisions:  {len(decision_rows)} total logged")
    print(f"Created curated CSV:  {out_csv}")
    print(f"Created curated JSON: {out_json}")
    return kept_master, master_cols, queries_rows, kept_raw, kept_hits, decision_rows


def push_to_neon(kept_master, master_cols, queries_rows, kept_raw, kept_hits, decision_rows):
    import psycopg

    load_env()
    if "DATABASE_URL" not in os.environ:
        raise SystemExit("DATABASE_URL not found in environment or .env file for --push-neon.")

    base_url = os.environ["DATABASE_URL"]
    admin_url = make_db_url(base_url, "neondb")
    with psycopg.connect(admin_url, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (NEON_CURATED_DB,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{NEON_CURATED_DB}"')
            print(f"Created Neon database: {NEON_CURATED_DB}")

    target_url = make_db_url(base_url, NEON_CURATED_DB)
    with psycopg.connect(target_url) as conn, conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS queries (
                query_id INTEGER PRIMARY KEY,
                query_code TEXT UNIQUE NOT NULL,
                query_family TEXT NOT NULL,
                operators INTEGER NOT NULL,
                layers INTEGER NOT NULL,
                query_text TEXT UNIQUE NOT NULL,
                raw_hits_count INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS raw_items (
                id INTEGER PRIMARY KEY,
                run_id TEXT NOT NULL,
                source_item_id TEXT UNIQUE NOT NULL,
                source_post_id TEXT NOT NULL,
                query_id INTEGER NOT NULL,
                query_code TEXT NOT NULL,
                payload JSONB NOT NULL
            );
            CREATE TABLE IF NOT EXISTS master_posts (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                source_post_id TEXT UNIQUE NOT NULL,
                entity_id TEXT,
                share_urn TEXT,
                post_type TEXT,
                post_url TEXT,
                share_url TEXT,
                posted_at TIMESTAMPTZ,
                posted_timestamp_ms BIGINT,
                post_text TEXT,
                text_chars INTEGER,
                author_id TEXT,
                author_type TEXT,
                author_name TEXT,
                author_public_id TEXT,
                author_universal_name TEXT,
                author_url TEXT,
                author_headline TEXT,
                author_website TEXT,
                author_urn TEXT,
                reactions INTEGER,
                comments INTEGER,
                shares INTEGER,
                reactions_breakdown JSONB,
                content_attributes JSONB,
                newsletter_title TEXT,
                newsletter_url TEXT,
                repost_id TEXT,
                media JSONB,
                first_raw_item_id INTEGER,
                matched_query_count INTEGER DEFAULT 1,
                matched_query_codes TEXT,
                matched_families TEXT
            );
            CREATE TABLE IF NOT EXISTS post_query_hits (
                post_id INTEGER NOT NULL,
                query_id INTEGER NOT NULL,
                query_code TEXT NOT NULL,
                query_family TEXT NOT NULL,
                run_id TEXT NOT NULL,
                PRIMARY KEY (post_id, query_id, run_id)
            );
            CREATE TABLE IF NOT EXISTS curation_decisions (
                source_post_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                decided_at TEXT
            );
            TRUNCATE TABLE post_query_hits, master_posts, raw_items, queries, curation_decisions;
            """
        )
        cur.executemany("INSERT INTO queries VALUES (%s,%s,%s,%s,%s,%s,%s)", queries_rows)
        cur.executemany("INSERT INTO raw_items VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb)", kept_raw)
        placeholders = ",".join(["%s"] * len(master_cols))
        cur.executemany(f"INSERT INTO master_posts VALUES ({placeholders})", kept_master)
        cur.executemany("INSERT INTO post_query_hits VALUES (%s,%s,%s,%s,%s)", kept_hits)
        cur.executemany("INSERT INTO curation_decisions VALUES (%s,%s,%s)", decision_rows)
        conn.commit()
    print(f"Synced {len(kept_master)} curated master_posts to Neon database `{NEON_CURATED_DB}`.")


def main():
    parser = argparse.ArgumentParser(description="Build curated SQLite & Neon DB from Swipe Review decisions.")
    parser.add_argument("decisions_file", type=Path, help="Path to saintiment_swipe_decisions.json")
    parser.add_argument("--out-db", type=Path, default=CURATED_SQLITE, help="Output SQLite DB path")
    parser.add_argument("--push-neon", action="store_true", help="Also push curated DB to Neon Postgres")
    args = parser.parse_args()

    decisions = parse_decisions(args.decisions_file)
    kept_master, master_cols, queries_rows, kept_raw, kept_hits, decision_rows = build_local_curated_sqlite(
        decisions, args.out_db, CURATED_CSV, CURATED_JSON
    )
    if args.push_neon:
        push_to_neon(kept_master, master_cols, queries_rows, kept_raw, kept_hits, decision_rows)


if __name__ == "__main__":
    main()
