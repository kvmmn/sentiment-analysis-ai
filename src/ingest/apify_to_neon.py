"""Load an Apify `harvestapi/linkedin-post-search` JSONL export into Postgres (Neon).

Usage:
    DATABASE_URL=... python apify_to_neon.py RUN_ID DATASET_ID ITEMS.jsonl QUERIES.json

Idempotent: re-running the same inputs does not create duplicate rows.
The connection string is read from the environment only; never commit it.
Requires: psycopg[binary] (v3).
"""
import json
import os
import sys

import psycopg

SOURCE = "apify"
TOOL = "harvestapi/linkedin-post-search"


def dumps(obj):
    # Postgres jsonb/text cannot hold NUL; some LinkedIn payloads contain it. Dropped and counted.
    text = json.dumps(obj, ensure_ascii=False)
    return text.replace("\\u0000", "")


def clean(value):
    return value.replace("\x00", "") if isinstance(value, str) else value


def media_of(item):
    keys = ("postImages", "postVideo", "article", "document", "poll", "repost")
    media = {k: item[k] for k in keys if item.get(k)}
    return dumps(media) if media else None


def main(run_id, dataset_id, items_path, queries_path):
    items = [json.loads(line) for line in open(items_path, encoding="utf-8")]
    queries = json.load(open(queries_path, encoding="utf-8"))
    query_set = f"{run_id}-subqueries"

    with psycopg.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO runs (run_id, source, tool, input, external_ref, notes) "
            "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (run_id) DO NOTHING",
            (
                run_id,
                SOURCE,
                TOOL,
                json.dumps({"query_set": query_set, "n_queries": len(queries)}),
                f"apify-dataset:{dataset_id}",
                "Cost not recorded here (pay-per-result, about USD 0.002/post); "
                "start time not recorded.",
            ),
        )

        query_ids = {}
        for q in queries:
            cur.execute(
                "INSERT INTO queries (query_set, query_text) VALUES (%s, %s) "
                "ON CONFLICT (query_set, query_text) DO UPDATE SET query_text = EXCLUDED.query_text "
                "RETURNING query_id",
                (query_set, q),
            )
            query_ids[q] = cur.fetchone()[0]

        for item in items:
            qid = query_ids[item["query"]["search"]]
            cur.execute(
                "INSERT INTO raw_items (run_id, source_item_id, payload) VALUES (%s, %s, %s) "
                "ON CONFLICT (run_id, source_item_id) DO UPDATE SET payload = EXCLUDED.payload "
                "RETURNING id",
                (run_id, f"{item['id']}#{qid}", dumps(item)),
            )
            raw_id = cur.fetchone()[0]

            author = item.get("author") or {}
            engagement = item.get("engagement") or {}
            posted_at = (item.get("postedAt") or {}).get("date")
            # `likes` already equals the sum of all reaction types in this actor's output.
            cur.execute(
                "INSERT INTO master_posts (source, source_post_id, post_url, posted_at, post_text, "
                "author_name, author_url, author_headline, reactions, comments, shares, media, "
                "first_raw_item_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT (source, source_post_id) DO UPDATE SET source_post_id = EXCLUDED.source_post_id "
                "RETURNING id",
                (
                    SOURCE,
                    item["id"],
                    clean(item.get("linkedinUrl")),
                    posted_at,
                    clean(item.get("content")),
                    clean(author.get("name")),
                    clean(author.get("linkedinUrl")),
                    clean(author.get("info")),
                    engagement.get("likes"),
                    engagement.get("comments"),
                    engagement.get("shares"),
                    media_of(item),
                    raw_id,
                ),
            )
            post_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO post_query_hits (post_id, query_id, run_id) VALUES (%s, %s, %s) "
                "ON CONFLICT DO NOTHING",
                (post_id, qid, run_id),
            )
        conn.commit()


if __name__ == "__main__":
    main(*sys.argv[1:5])
