"""Unit tests for swipe-mark validation and the downloadable marked database."""
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from swipe_store import (
    DecisionError,
    decisions_csv,
    marked_csv,
    parse_decision_request,
    write_marked_sqlite,
)


class ParseDecisionTests(unittest.TestCase):
    def test_keep_payload(self):
        item = parse_decision_request({
            "source_post_id": "7474806423776940032",
            "status": "KEEP",
            "reviewer": " Kaveh ",
            "note": " on topic ",
            "decided_at": "2026-11-05T21:00:00Z",
        })
        self.assertEqual(item["status"], "keep")
        self.assertEqual(item["reviewer"], "Kaveh")
        self.assertEqual(item["note"], "on topic")
        self.assertEqual(item["decided_at"], datetime(2026, 11, 5, 21, 0, tzinfo=timezone.utc))

    def test_clear_payload(self):
        item = parse_decision_request({"source_post_id": "abc-1", "status": None, "reviewer": "Morteza"})
        self.assertIsNone(item["status"])
        self.assertEqual(item["reviewer"], "Morteza")

    def test_rejects_bad_status_and_id(self):
        with self.assertRaises(DecisionError):
            parse_decision_request({"source_post_id": "1", "status": "maybe"})
        with self.assertRaises(DecisionError):
            parse_decision_request({"source_post_id": "has space", "status": "keep"})
        with self.assertRaises(DecisionError):
            parse_decision_request({"source_post_id": "1", "status": "keep", "note": "x" * 501})


class MarkedExportTests(unittest.TestCase):
    def test_sqlite_and_csv_keep_the_mark_on_every_post(self):
        posts = [
            {
                "source_post_id": "100",
                "posted_at": "2026-01-01",
                "post_type": "post",
                "post_url": "https://www.linkedin.com/posts/100",
                "author_type": "profile",
                "author_name": "A",
                "author_headline": "Architect",
                "author_url": "",
                "reactions": 2,
                "comments": 0,
                "shares": 0,
                "text_chars": 12,
                "matched_query_count": 1,
                "matched_query_codes": "Q01",
                "matched_families": "direct",
                "curation_status": "keep",
                "curation_reviewer": "Kaveh",
                "curation_note": "",
                "curation_decided_at": "2026-11-05T21:00:00Z",
                "post_text": "GenAI skills",
            },
            {
                "source_post_id": "200",
                "posted_at": "2026-01-02",
                "post_type": "post",
                "post_url": "",
                "author_type": "profile",
                "author_name": "B",
                "author_headline": "",
                "author_url": "",
                "reactions": 0,
                "comments": 0,
                "shares": 0,
                "text_chars": 4,
                "matched_query_count": 1,
                "matched_query_codes": "Q02",
                "matched_families": "direct",
                "curation_status": "",
                "curation_reviewer": "",
                "curation_note": "",
                "curation_decided_at": "",
                "post_text": "todo",
            },
        ]
        decisions = {
            "100": {"status": "keep", "timestamp": "2026-11-05T21:00:00Z", "reviewer": "Kaveh", "note": ""}
        }
        queries = [(1, "Q01", "direct", 5, 3, "(architect)", 50)]
        events = [(1, "100", "keep", "Kaveh", "", "2026-11-05T21:00:00Z", "set", "2026-11-05T21:00:01Z")]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "marked.sqlite"
            write_marked_sqlite(path, posts, decisions, events, queries)
            conn = sqlite3.connect(path)
            try:
                kept = conn.execute(
                    "SELECT curation_status, curation_reviewer FROM master_posts WHERE source_post_id = '100'"
                ).fetchone()
                waiting = conn.execute(
                    "SELECT curation_status FROM master_posts WHERE source_post_id = '200'"
                ).fetchone()
                decision = conn.execute("SELECT status, reviewer FROM curation_decisions").fetchone()
                event = conn.execute("SELECT action FROM curation_decision_events").fetchone()
                query = conn.execute("SELECT query_code FROM queries").fetchone()
            finally:
                conn.close()
        self.assertEqual(kept, ("keep", "Kaveh"))
        self.assertEqual(waiting, ("",))
        self.assertEqual(decision, ("keep", "Kaveh"))
        self.assertEqual(event, ("set",))
        self.assertEqual(query, ("Q01",))
        csv_text = marked_csv(posts)
        self.assertIn("curation_status", csv_text)
        self.assertIn("keep", csv_text)
        manifest_csv = decisions_csv(decisions)
        self.assertIn("100,keep,2026-11-05T21:00:00Z,Kaveh", manifest_csv)


if __name__ == "__main__":
    unittest.main()
