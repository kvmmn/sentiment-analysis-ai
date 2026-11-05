"""Shared keep/reject marks for the Swipe Review of the 2026-10-18 three-layer corpus.

The post corpus stays in Neon database `_saintiment_apify_three_layer_db`.
Each swipe is an annotation, not a rewrite of `master_posts`:

- `curation_decisions` is the current mark (keep or reject) for one post.
- `curation_decision_events` is the append-only history of those marks.
- `master_posts_marked` joins every post to its current mark.

Usage:
    python src/ingest/swipe_store.py status
    python src/ingest/swipe_store.py export-decisions
    python src/ingest/swipe_store.py export-marked

`DATABASE_URL` is read from the environment or `.env`. It is never printed.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sqlite3
import tempfile
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ROOT / "data/local/linkedin-apify-2026-10-17/swipe"
CORPUS_DB = "_saintiment_apify_three_layer_db"
SOURCE_RUN_ID = "X2gdX05u8rP41b4rG"
SOURCE_DATASET_ID = "WUsK3RRYo7nKEOUbA"
POST_ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,200}$")
STATUSES = {"keep", "reject"}

SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS curation_decisions (
        source_post_id TEXT PRIMARY KEY,
        status TEXT NOT NULL CHECK (status IN ('keep', 'reject')),
        reviewer TEXT NOT NULL DEFAULT '',
        note TEXT NOT NULL DEFAULT '',
        decided_at TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS curation_decision_events (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        source_post_id TEXT NOT NULL,
        status TEXT CHECK (status IS NULL OR status IN ('keep', 'reject')),
        reviewer TEXT NOT NULL DEFAULT '',
        note TEXT NOT NULL DEFAULT '',
        decided_at TIMESTAMPTZ NOT NULL,
        action TEXT NOT NULL CHECK (action IN ('set', 'clear')),
        recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS curation_decision_events_post_idx
        ON curation_decision_events (source_post_id, id)
    """,
    """
    CREATE OR REPLACE VIEW master_posts_marked AS
    SELECT
        m.*,
        d.status AS curation_status,
        d.reviewer AS curation_reviewer,
        d.note AS curation_note,
        d.decided_at AS curation_decided_at
    FROM master_posts m
    LEFT JOIN curation_decisions d ON d.source_post_id = m.source_post_id
    """,
)

MARKED_FIELDS = (
    "source_post_id",
    "posted_at",
    "post_type",
    "post_url",
    "author_type",
    "author_name",
    "author_headline",
    "author_url",
    "reactions",
    "comments",
    "shares",
    "text_chars",
    "matched_query_count",
    "matched_query_codes",
    "matched_families",
    "curation_status",
    "curation_reviewer",
    "curation_note",
    "curation_decided_at",
    "post_text",
)


class DecisionError(ValueError):
    """The swipe payload cannot be stored."""


def load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def make_db_url(base_url: str, db_name: str) -> str:
    parsed = urllib.parse.urlsplit(base_url)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, f"/{db_name}", parsed.query, parsed.fragment))


def corpus_db_url() -> str:
    load_env()
    if "DATABASE_URL" not in os.environ:
        raise SystemExit("DATABASE_URL not found in the environment or .env file.")
    return make_db_url(os.environ["DATABASE_URL"], CORPUS_DB)


def connect():
    import psycopg

    return psycopg.connect(corpus_db_url())


def ensure_schema(conn) -> None:
    with conn.cursor() as cur:
        for statement in SCHEMA_STATEMENTS:
            cur.execute(statement)
    conn.commit()


def utc_iso(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return str(value)


def parse_timestamp(value) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value or "").strip()
        if not text:
            return datetime.now(timezone.utc)
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_decision_request(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise DecisionError("body must be a JSON object")
    source_post_id = str(payload.get("source_post_id") or "").strip()
    if not POST_ID_RE.fullmatch(source_post_id):
        raise DecisionError("invalid source_post_id")
    raw_status = payload.get("status")
    if raw_status is None or raw_status == "":
        status = None
    else:
        status = str(raw_status).strip().lower()
        if status not in STATUSES:
            raise DecisionError("status must be keep, reject, or null")
    reviewer = str(payload.get("reviewer") or "").replace("\x00", "").strip()
    if len(reviewer) > 80:
        raise DecisionError("reviewer is too long")
    note = str(payload.get("note") or "").replace("\x00", "").strip()
    if len(note) > 500:
        raise DecisionError("note is too long")
    try:
        decided_at = parse_timestamp(payload.get("decided_at") or payload.get("timestamp"))
    except ValueError as exc:
        raise DecisionError("invalid decided_at") from exc
    return {
        "source_post_id": source_post_id,
        "status": status,
        "reviewer": reviewer,
        "note": note,
        "decided_at": decided_at,
    }


def decision_public(row) -> dict | None:
    if row is None:
        return None
    source_post_id, status, reviewer, note, decided_at = row
    return {
        "source_post_id": source_post_id,
        "status": status,
        "timestamp": utc_iso(decided_at),
        "reviewer": reviewer or "",
        "note": note or "",
    }


def fetch_decision(cur, source_post_id: str) -> dict | None:
    cur.execute(
        """
        SELECT source_post_id, status, reviewer, note, decided_at
        FROM curation_decisions
        WHERE source_post_id = %s
        """,
        (source_post_id,),
    )
    return decision_public(cur.fetchone())


def post_exists(cur, source_post_id: str) -> bool:
    cur.execute("SELECT 1 FROM master_posts WHERE source_post_id = %s", (source_post_id,))
    return cur.fetchone() is not None


def apply_decision(conn, item: dict) -> dict:
    """Insert, replace, or clear one mark. An older timestamp does not overwrite a newer one."""
    with conn.cursor() as cur:
        if item["status"] is None:
            cur.execute(
                """
                DELETE FROM curation_decisions
                WHERE source_post_id = %s AND decided_at <= %s
                RETURNING source_post_id
                """,
                (item["source_post_id"], item["decided_at"]),
            )
            deleted = cur.fetchone()
            if deleted:
                _insert_event(cur, item, "clear")
                conn.commit()
                return {"applied": True, "decision": None}
            current = fetch_decision(cur, item["source_post_id"])
            conn.commit()
            return {"applied": current is None, "decision": current}

        if not post_exists(cur, item["source_post_id"]):
            conn.rollback()
            raise DecisionError("source_post_id is not in master_posts")

        cur.execute(
            """
            INSERT INTO curation_decisions (source_post_id, status, reviewer, note, decided_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (source_post_id) DO UPDATE SET
                status = EXCLUDED.status,
                reviewer = EXCLUDED.reviewer,
                note = EXCLUDED.note,
                decided_at = EXCLUDED.decided_at,
                updated_at = now()
            WHERE curation_decisions.decided_at <= EXCLUDED.decided_at
            RETURNING source_post_id
            """,
            (
                item["source_post_id"],
                item["status"],
                item["reviewer"],
                item["note"],
                item["decided_at"],
            ),
        )
        written = cur.fetchone()
        if written:
            _insert_event(cur, item, "set")
            conn.commit()
            return {
                "applied": True,
                "decision": {
                    "source_post_id": item["source_post_id"],
                    "status": item["status"],
                    "timestamp": utc_iso(item["decided_at"]),
                    "reviewer": item["reviewer"],
                    "note": item["note"],
                },
            }
        current = fetch_decision(cur, item["source_post_id"])
        conn.commit()
        return {"applied": False, "decision": current}


def _insert_event(cur, item: dict, action: str) -> None:
    cur.execute(
        """
        INSERT INTO curation_decision_events
            (source_post_id, status, reviewer, note, decided_at, action)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            item["source_post_id"],
            item["status"],
            item["reviewer"],
            item["note"],
            item["decided_at"],
            action,
        ),
    )


def list_decisions(conn) -> dict[str, dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT source_post_id, status, reviewer, note, decided_at
            FROM curation_decisions
            ORDER BY decided_at, source_post_id
            """
        )
        rows = cur.fetchall()
    decisions = {}
    for row in rows:
        public = decision_public(row)
        decisions[public["source_post_id"]] = {
            "status": public["status"],
            "timestamp": public["timestamp"],
            "reviewer": public["reviewer"],
            "note": public["note"],
        }
    return decisions


def progress_summary(conn) -> dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                COUNT(*) AS total_posts,
                COUNT(*) FILTER (WHERE curation_status = 'keep') AS kept,
                COUNT(*) FILTER (WHERE curation_status = 'reject') AS rejected,
                COUNT(*) FILTER (WHERE curation_status IS NULL) AS unreviewed
            FROM master_posts_marked
            """
        )
        total_posts, kept, rejected, unreviewed = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM curation_decision_events")
        events = cur.fetchone()[0]
    return {
        "corpus_database": CORPUS_DB,
        "source_run_id": SOURCE_RUN_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "total_posts": int(total_posts),
        "kept": int(kept),
        "rejected": int(rejected),
        "unreviewed": int(unreviewed),
        "events": int(events),
    }


def decisions_manifest(conn) -> dict:
    summary = progress_summary(conn)
    return {
        "project": "Saintiment",
        "source_run_id": SOURCE_RUN_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "corpus_database": CORPUS_DB,
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "summary": {
            "total_posts": summary["total_posts"],
            "kept": summary["kept"],
            "rejected": summary["rejected"],
            "unreviewed": summary["unreviewed"],
        },
        "decisions": list_decisions(conn),
    }


def decisions_csv(decisions: dict[str, dict]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["source_post_id", "status", "decided_at", "reviewer", "note"])
    for source_post_id, item in decisions.items():
        writer.writerow([
            source_post_id,
            item.get("status", ""),
            item.get("timestamp", ""),
            item.get("reviewer", ""),
            item.get("note", ""),
        ])
    return buffer.getvalue()


def _text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return utc_iso(value)
    return str(value)


def fetch_marked_posts(conn) -> list[dict]:
    columns = """
        source_post_id, posted_at, post_type, post_url, author_type, author_name,
        author_headline, author_url, author_public_id, reactions, comments, shares,
        text_chars, matched_query_count, matched_query_codes, matched_families,
        media::text, curation_status, curation_reviewer, curation_note,
        curation_decided_at, post_text
    """
    with conn.cursor() as cur:
        cur.execute(f"SELECT {columns} FROM master_posts_marked ORDER BY id")
        names = [d.name for d in cur.description]
        return [dict(zip(names, row)) for row in cur.fetchall()]


def fetch_api_posts(conn) -> list[dict]:
    posts = []
    for row in fetch_marked_posts(conn):
        posts.append({
            "source_post_id": row["source_post_id"],
            "posted_at": _text(row["posted_at"]),
            "post_type": row["post_type"] or "post",
            "author_type": row["author_type"] or "profile",
            "author_name": row["author_name"] or "",
            "author_headline": row["author_headline"] or "",
            "author_url": row["author_url"] or "",
            "author_public_id": row["author_public_id"] or "",
            "post_url": row["post_url"] or "",
            "reactions": row["reactions"] or 0,
            "comments": row["comments"] or 0,
            "shares": row["shares"] or 0,
            "text_chars": row["text_chars"] or 0,
            "matched_query_count": row["matched_query_count"] or 0,
            "matched_query_codes": row["matched_query_codes"] or "",
            "matched_families": row["matched_families"] or "",
            "media": row["media"],
            "post_text": row["post_text"] or "",
            "curation_status": row["curation_status"] or "",
            "curation_reviewer": row["curation_reviewer"] or "",
            "curation_decided_at": _text(row["curation_decided_at"]),
        })
    return posts


def fetch_queries(conn) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT query_id, query_code, query_family, operators, layers, query_text, raw_hits_count
            FROM queries
            ORDER BY query_id
            """
        )
        return cur.fetchall()


def fetch_events(conn) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, source_post_id, status, reviewer, note, decided_at, action, recorded_at
            FROM curation_decision_events
            ORDER BY id
            """
        )
        return cur.fetchall()


def marked_csv(posts: list[dict]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=MARKED_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for row in posts:
        writer.writerow({key: _text(row.get(key)) for key in MARKED_FIELDS})
    return buffer.getvalue()


def write_marked_sqlite(path: Path, posts: list[dict], decisions: dict[str, dict], events: list[tuple], queries: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE queries (
                query_id INTEGER PRIMARY KEY,
                query_code TEXT UNIQUE NOT NULL,
                query_family TEXT NOT NULL,
                operators INTEGER NOT NULL,
                layers INTEGER NOT NULL,
                query_text TEXT NOT NULL,
                raw_hits_count INTEGER DEFAULT 0
            );
            CREATE TABLE master_posts (
                source_post_id TEXT PRIMARY KEY,
                posted_at TEXT,
                post_type TEXT,
                post_url TEXT,
                author_type TEXT,
                author_name TEXT,
                author_headline TEXT,
                author_url TEXT,
                reactions INTEGER,
                comments INTEGER,
                shares INTEGER,
                text_chars INTEGER,
                matched_query_count INTEGER,
                matched_query_codes TEXT,
                matched_families TEXT,
                curation_status TEXT,
                curation_reviewer TEXT,
                curation_note TEXT,
                curation_decided_at TEXT,
                post_text TEXT
            );
            CREATE TABLE curation_decisions (
                source_post_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                decided_at TEXT,
                reviewer TEXT NOT NULL DEFAULT '',
                note TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE curation_decision_events (
                id INTEGER PRIMARY KEY,
                source_post_id TEXT NOT NULL,
                status TEXT,
                reviewer TEXT NOT NULL DEFAULT '',
                note TEXT NOT NULL DEFAULT '',
                decided_at TEXT,
                action TEXT NOT NULL,
                recorded_at TEXT
            );
            """
        )
        conn.executemany("INSERT INTO queries VALUES (?,?,?,?,?,?,?)", queries)
        conn.executemany(
            f"INSERT INTO master_posts VALUES ({','.join('?' for _ in MARKED_FIELDS)})",
            [tuple(_text(row.get(key)) for key in MARKED_FIELDS) for row in posts],
        )
        conn.executemany(
            "INSERT INTO curation_decisions VALUES (?,?,?,?,?)",
            [
                (
                    source_post_id,
                    item.get("status", ""),
                    item.get("timestamp", ""),
                    item.get("reviewer", ""),
                    item.get("note", ""),
                )
                for source_post_id, item in decisions.items()
            ],
        )
        conn.executemany(
            "INSERT INTO curation_decision_events VALUES (?,?,?,?,?,?,?,?)",
            [
                (
                    event[0],
                    event[1],
                    event[2] or "",
                    event[3] or "",
                    event[4] or "",
                    _text(event[5]),
                    event[6],
                    _text(event[7]),
                )
                for event in events
            ],
        )
        conn.commit()
    finally:
        conn.close()


def marked_sqlite_bytes(posts: list[dict], decisions: dict[str, dict], events: list[tuple], queries: list[tuple]) -> bytes:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "saintiment_swipe_marked.sqlite"
        write_marked_sqlite(path, posts, decisions, events, queries)
        return path.read_bytes()


def clear_post_marks(conn, source_post_id: str) -> None:
    """Remove one post's current mark and history. Used to undo a connectivity probe."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM curation_decisions WHERE source_post_id = %s", (source_post_id,))
        cur.execute("DELETE FROM curation_decision_events WHERE source_post_id = %s", (source_post_id,))
    conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Read or export shared Saintiment swipe marks.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="Print how many posts are keep, reject, or still unreviewed")
    decisions_cmd = sub.add_parser("export-decisions", help="Write the decisions manifest JSON")
    decisions_cmd.add_argument("--out", type=Path, default=EXPORT_DIR / "saintiment_swipe_decisions.json")
    marked_cmd = sub.add_parser("export-marked", help="Write SQLite and CSV copies with a mark on every post")
    marked_cmd.add_argument("--out-dir", type=Path, default=EXPORT_DIR)
    args = parser.parse_args()

    with connect() as conn:
        ensure_schema(conn)
        if args.command == "status":
            print(json.dumps(progress_summary(conn), indent=2))
            return
        if args.command == "export-decisions":
            payload = decisions_manifest(conn)
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Wrote {args.out} ({payload['summary']['kept']} keep, {payload['summary']['rejected']} reject)")
            return
        posts = fetch_marked_posts(conn)
        decisions = list_decisions(conn)
        events = fetch_events(conn)
        queries = fetch_queries(conn)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path = args.out_dir / "saintiment_swipe_marked.sqlite"
    csv_path = args.out_dir / "saintiment_swipe_marked.csv"
    json_path = args.out_dir / "saintiment_swipe_decisions.json"
    write_marked_sqlite(sqlite_path, posts, decisions, events, queries)
    csv_path.write_text(marked_csv(posts), encoding="utf-8")
    json_path.write_text(
        json.dumps(decisions_manifest_from_parts(posts, decisions), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {sqlite_path}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {json_path}")


def decisions_manifest_from_parts(posts: list[dict], decisions: dict[str, dict]) -> dict:
    kept = sum(1 for item in decisions.values() if item.get("status") == "keep")
    rejected = sum(1 for item in decisions.values() if item.get("status") == "reject")
    return {
        "project": "Saintiment",
        "source_run_id": SOURCE_RUN_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "corpus_database": CORPUS_DB,
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "summary": {
            "total_posts": len(posts),
            "kept": kept,
            "rejected": rejected,
            "unreviewed": max(0, len(posts) - kept - rejected),
        },
        "decisions": decisions,
    }


if __name__ == "__main__":
    main()
