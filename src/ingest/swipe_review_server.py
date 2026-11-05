"""Serve Swipe Review and write each keep/reject mark into the shared Neon corpus.

Usage:
    python src/ingest/swipe_review_server.py
    python src/ingest/swipe_review_server.py --phone

On this computer, open http://127.0.0.1:8765/ . With --phone, the same Wi-Fi
phone opens the address printed at startup. That address carries a one-time
key so other devices on the network do not receive the posts. The key is not
written to git and is not included in the request log.

The page loads the 1,858 three-layer posts from
`_saintiment_apify_three_layer_db` and upserts every swipe into
`curation_decisions`. Downloads from that page are generated from the same
database, so another person running this server sees and can export the same marks.

The default bind is 127.0.0.1. Post text is personal data and is not committed
to git. `DATABASE_URL` is read from the environment or `.env` and is never printed.
"""
from __future__ import annotations

import argparse
import hmac
import json
import os
import re
import secrets
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

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
COOKIE_NAME = "saintiment_swipe_access"
_KEY_IN_LOG = re.compile(r"([?&]k=)[^&\s]+")

DENIED_HTML = """<!doctype html>
<html lang="fa" dir="rtl">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Saintiment</title>
<body style="font-family:Tahoma,sans-serif;padding:24px;line-height:1.7">
<p>این آدرس پست‌ها را نشان نمی‌دهد.</p>
<p>روی کامپیوتر دستور <code>python src/ingest/swipe_review_server.py --phone</code> را اجرا کنید و همان آدرسی را که آنجا چاپ می‌شود، در گوشی باز کنید. کامپیوتر و گوشی باید روی یک وای‌فای باشند و آن پنجره باز بماند.</p>
</body>
</html>
""".encode("utf-8")


def _html_path():
    from pathlib import Path

    return Path(__file__).resolve().parents[2] / "docs" / "swipe-review.html"


def keys_match(given: str, token: str) -> bool:
    if not given or not token:
        return False
    given_b = given.encode("utf-8")
    token_b = token.encode("utf-8")
    if len(given_b) != len(token_b):
        return False
    return hmac.compare_digest(given_b, token_b)


def cookie_token(cookie_header: str) -> str:
    for part in (cookie_header or "").split(";"):
        name, sep, value = part.strip().partition("=")
        if sep and name == COOKIE_NAME:
            return value
    return ""


def access_allowed(client_ip: str, token: str, query_key: str, header_key: str, cookie_header: str) -> bool:
    """Loopback is the computer running the server. Every other device needs the key."""
    if client_ip in {"127.0.0.1", "::1"}:
        return True
    if not token:
        return False
    return any(keys_match(candidate, token) for candidate in (query_key, header_key, cookie_token(cookie_header)))


def redact_access_key(text: str) -> str:
    return _KEY_IN_LOG.sub(r"\1redacted", text)


def local_ipv4_addresses() -> list[str]:
    found: list[str] = []

    def add(ip: str) -> None:
        if ip and not ip.startswith("127.") and ip not in found:
            found.append(ip)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            add(sock.getsockname()[0])
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            add(info[4][0])
    except OSError:
        pass
    return found


class SwipeHandler(BaseHTTPRequestHandler):
    server_version = "SaintimentSwipe/1.0"
    access_token = ""

    def log_message(self, fmt: str, *args) -> None:
        # Request lines only. Do not log bodies or the phone access key.
        super().log_message(fmt, *(redact_access_key(str(arg)) for arg in args))

    def _query_key(self) -> str:
        values = parse_qs(urlparse(self.path).query).get("k", [])
        return values[0] if values else ""

    def _allowed(self) -> bool:
        return access_allowed(
            self.client_address[0],
            self.access_token,
            self._query_key(),
            self.headers.get("X-Swipe-Key", ""),
            self.headers.get("Cookie", ""),
        )

    def _cookie_headers(self) -> list[tuple[str, str]]:
        if not self.access_token:
            return []
        return [(
            "Set-Cookie",
            f"{COOKIE_NAME}={self.access_token}; Path=/; Max-Age=2592000; SameSite=Lax; HttpOnly",
        )]

    def _send_denied(self) -> None:
        self._send_bytes(DENIED_HTML, "text/html; charset=utf-8", status=401)

    def do_GET(self) -> None:
        if not self._allowed():
            self._send_denied()
            return
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
        if not self._allowed():
            self._send_denied()
            return
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
        if status != 401:
            for name, value in self._cookie_headers():
                self.send_header(name, value)
        if download_name:
            self.send_header("Content-Disposition", f'attachment; filename="{download_name}"')
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve Saintiment swipe review against the shared Neon corpus.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--phone", action="store_true", help="Also accept a phone on the same Wi-Fi")
    parser.add_argument("--token", default=os.environ.get("SWIPE_REVIEW_TOKEN", ""), help="Phone access key. Generated when omitted.")
    args = parser.parse_args()
    if args.phone and args.host == "127.0.0.1":
        args.host = "0.0.0.0"
    token = args.token
    if args.host not in {"127.0.0.1", "::1"} and not token:
        token = secrets.token_urlsafe(12)
    SwipeHandler.access_token = token
    with connect() as conn:
        ensure_schema(conn)
        summary = progress_summary(conn)
    httpd = ThreadingHTTPServer((args.host, args.port), SwipeHandler)
    print(f"On this computer: http://127.0.0.1:{args.port}/")
    if token:
        phone_urls = [f"http://{ip}:{args.port}/?k={token}" for ip in local_ipv4_addresses()]
        if phone_urls:
            print("On your phone, same Wi-Fi:")
            for url in phone_urls:
                print(url)
        else:
            print("No Wi-Fi address found. The phone cannot open this server until the computer has a network address.")
        print("Leave this window open. Do not commit or publish the phone address.")
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
