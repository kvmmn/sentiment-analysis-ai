"""Serve Swipe Review and write each keep/reject mark into the shared Neon corpus.

Usage:
    python src/ingest/swipe_review_server.py
    python src/ingest/swipe_review_server.py --port 8765

Open http://127.0.0.1:8765/ . The page loads the 1,858 three-layer posts from
`_saintiment_apify_three_layer_db` and upserts every swipe into
`curation_decisions`. Downloads from that page are generated from the same
database, so another person running this server sees and can export the same marks.

Binds to 127.0.0.1. Post text is personal data and is not committed to git.
`DATABASE_URL` is read from the environment or `.env` and is never printed.
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from swipe_store import (
    DecisionError,
    apply_decision,
    connect,
    decisions_csv,
    decisions_manifest,
    ensure_schema,
    fetch_api_posts,
    fetch_events,
    fetch_marked_posts,
    fetch_queries,
    list_decisions,
    marked_csv,
    marked_sqlite_bytes,
    parse_decision_request,
    progress_summary,
)

MAX_BODY = 32_768


def _html_path():
    from pathlib import Path

    return Path(__file__).resolve().parents[2] / "docs" / "swipe-review.html"


class SwipeHandler(BaseHTTPRequestHandler):
    server_version = "SaintimentSwipe/1.0"

    def log_message(self, fmt: str, *args) -> None:
        # Request lines only. Do not log bodies; they can contain post text or names.
        super().log_message(fmt, *args)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/", "/swipe-review.html"):
            self._send_bytes(_html_path().read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/api/swipe/health":
            self._send_json({"ok": True, "service": "saintiment-swipe"})
            return
        if path == "/api/swipe/posts":
            self._with_store(self._posts)
            return
        if path == "/api/swipe/decisions":
            self._with_store(self._decisions)
            return
        if path == "/api/swipe/export/decisions.json":
            self._with_store(self._export_decisions_json)
            return
        if path == "/api/swipe/export/decisions.csv":
            self._with_store(self._export_decisions_csv)
            return
        if path == "/api/swipe/export/marked.csv":
            self._with_store(self._export_marked_csv)
            return
        if path == "/api/swipe/export/marked.sqlite":
            self._with_store(self._export_marked_sqlite)
            return
        self._send_json({"error": "not found"}, status=404)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/api/swipe/decisions":
            self._send_json({"error": "not found"}, status=404)
            return
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > MAX_BODY:
            self._send_json({"error": "invalid body"}, status=400)
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            item = parse_decision_request(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, DecisionError) as exc:
            self._send_json({"error": str(exc)}, status=400)
            return
        self._with_store(lambda conn: self._write_decision(conn, item))

    def _with_store(self, action) -> None:
        try:
            with connect() as conn:
                ensure_schema(conn)
                action(conn)
        except DecisionError as exc:
            self._send_json({"error": str(exc)}, status=400)
        except Exception as exc:  # database or network failure; no credentials in the message we return
            self._send_json({"error": "database unavailable", "detail": exc.__class__.__name__}, status=503)

    def _posts(self, conn) -> None:
        posts = fetch_api_posts(conn)
        self._send_json({"count": len(posts), "posts": posts})

    def _decisions(self, conn) -> None:
        self._send_json({"summary": progress_summary(conn), "decisions": list_decisions(conn)})

    def _write_decision(self, conn, item: dict) -> None:
        result = apply_decision(conn, item)
        result["summary"] = progress_summary(conn)
        self._send_json(result)

    def _export_decisions_json(self, conn) -> None:
        body = json.dumps(decisions_manifest(conn), ensure_ascii=False, indent=2).encode("utf-8")
        self._send_bytes(body, "application/json; charset=utf-8", "saintiment_swipe_decisions.json")

    def _export_decisions_csv(self, conn) -> None:
        body = ("\ufeff" + decisions_csv(list_decisions(conn))).encode("utf-8")
        self._send_bytes(body, "text/csv; charset=utf-8", "saintiment_swipe_decisions.csv")

    def _export_marked_csv(self, conn) -> None:
        body = ("\ufeff" + marked_csv(fetch_marked_posts(conn))).encode("utf-8")
        self._send_bytes(body, "text/csv; charset=utf-8", "saintiment_swipe_marked.csv")

    def _export_marked_sqlite(self, conn) -> None:
        blob = marked_sqlite_bytes(
            fetch_marked_posts(conn),
            list_decisions(conn),
            fetch_events(conn),
            fetch_queries(conn),
        )
        self._send_bytes(blob, "application/vnd.sqlite3", "saintiment_swipe_marked.sqlite")

    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send_bytes(body, "application/json; charset=utf-8", status=status)

    def _send_bytes(self, body: bytes, content_type: str, download_name: str | None = None, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if download_name:
            self.send_header("Content-Disposition", f'attachment; filename="{download_name}"')
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve Saintiment swipe review against the shared Neon corpus.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with connect() as conn:
        ensure_schema(conn)
        summary = progress_summary(conn)
    httpd = ThreadingHTTPServer((args.host, args.port), SwipeHandler)
    print(f"Saintiment swipe review: http://{args.host}:{args.port}/")
    print(
        "Corpus {corpus} — {unreviewed} unreviewed, {kept} keep, {rejected} reject.".format(
            corpus=summary["corpus_database"],
            **summary,
        )
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
