"""Export `master_posts` from Postgres (Neon) to a CSV that Google Sheets can import.

Usage:
    DATABASE_URL=... python export_master_csv.py OUT.csv

One row per unique post. `query_hits` is the number of sub-queries that returned the post and
`queries` lists their ids. Output contains author names and headlines: keep it private and out of Git.
Google Sheets limits: 10 million cells per spreadsheet, 50,000 characters per cell.
"""
import csv
import os
import sys

import psycopg

SQL = """
SELECT p.source, p.source_post_id, p.post_url, p.posted_at, p.author_name, p.author_url,
       p.author_headline, p.reactions, p.comments, p.shares, p.post_text,
       count(h.query_id) AS query_hits,
       string_agg(DISTINCT h.query_id::text, ',' ORDER BY h.query_id::text) AS queries
FROM master_posts p
LEFT JOIN post_query_hits h ON h.post_id = p.id
GROUP BY p.id
ORDER BY p.posted_at DESC
"""


def main(out_path):
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute(SQL)
        header = [d.name for d in cur.description]
        rows = cur.fetchall()
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main(sys.argv[1])
