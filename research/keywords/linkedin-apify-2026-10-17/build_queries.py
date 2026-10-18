#!/usr/bin/env python3
"""Build the optimized 2026-10-17 Apify LinkedIn query list (v2 — strengthened).

Each executable query has at most five AND/OR operators. That ceiling is the
2026-10-07 observation: LinkedIn content search returned no posts at six or
more operators and returned posts at five or fewer.

Preserves the 17 October team structure (Domain/Tools ∧ AI ∧ Skill/Cognition/Process
plus Tier 2 two-layer Option A) while incorporating high-signal terms from the
project lexicon, Morteza's Sep 8 feedback, Kaveh's Sep 15 audit, Run 013 empirical
findings (Sep 25), and the Oct 7 Apify pilot.

This script is the source of the strings in queries.json. It does not call
Apify.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "queries.json"

OPERATOR_CEILING = 5

# Terms confirmed from the 17 October group list + targeted strengtheners from
# project documents (Core Lexicon, Sep 8 team consensus, Sep 15 letter, Sep 25
# empirical pilot, and Oct 7 Apify run).
KEYWORDS = {
    "domain_and_tools": [
        "architect",
        "architects",
        "architecture",
        "architectural",
        '"architectural design"',
        '"computational design"',
        "BIM",
        "Revit",
        "Rhino",
        "Grasshopper",
        "Parametric",
        '"generative design"',
        "Rendering",
        "archviz",
        '"architectural education"',
        '"architecture students"',
    ],
    "ai": [
        "AI",
        "GenAI",
        '"generative AI"',
        '"artificial intelligence"',
        "Midjourney",
        "ChatGPT",
        "Copilot",
        '"Stable Diffusion"',
        "DALL-E",
        '"AI rendering"',
    ],
    "skill_direct": [
        "skill",
        "skills",
        "upskilling",
        "deskilling",
        "reskilling",
        "downskilling",
        '"skill loss"',
        "expertise",
    ],
    "skill_cognition": [
        "creativity",
        '"design thinking"',
        '"critical thinking"',
        "judgment",
        "intuition",
        "authorship",
        '"cognitive offloading"',
        "overreliance",
    ],
    "skill_process": [
        "workflow",
        "automation",
        "replace",
        "replacement",
        "augmentation",
        '"human-in-the-loop"',
        '"role of the architect"',
    ],
    "skill_technical_and_pedagogy": [
        '"technical skills"',
        '"environmental design"',
        '"building performance"',
        '"energy modeling"',
        "curriculum",
        "learning",
    ],
}

# Parents from Iman's uploaded suggestion. Several exceed the operator ceiling
# and are kept as the received sketch, not as the Apify input.
RECEIVED_PARENTS = [
    '(architect OR architecture) AND (AI OR GenAI OR "generative AI") AND (skill OR skills OR upskilling OR deskilling)',
    '(architect OR architecture) AND (AI OR GenAI OR "generative AI") AND (creativity OR "critical thinking" OR judgment)',
    '(architect OR architecture) AND (AI OR GenAI OR "generative AI") AND (workflow OR automation OR replace)',
    '(architect OR architecture) AND (Midjourney OR ChatGPT OR Copilot) AND (skill OR skills OR creativity OR judgment)',
    '(architect OR architecture) AND (Midjourney OR ChatGPT OR Copilot) AND (workflow OR automation OR replace)',
    '(BIM OR Revit OR Grasshopper OR Rhino) AND (AI OR GenAI OR Midjourney OR ChatGPT) AND (skill OR skills OR workflow OR automation)',
    '(BIM OR Revit OR Grasshopper OR Rhino) AND (AI OR GenAI OR Midjourney OR ChatGPT) AND (creativity OR judgment OR "critical thinking")',
    '(BIM OR Revit OR Grasshopper) AND (Midjourney OR ChatGPT OR Copilot)',
    '(BIM OR Revit OR Grasshopper) AND (GenAI OR "generative AI" OR AI)',
    '(architect OR architectural) AND (Rhino OR Parametric) AND (Midjourney OR ChatGPT OR GenAI OR AI)',
    '(architect OR architectural) AND ("generative design" OR Rendering) AND (Midjourney OR ChatGPT OR GenAI OR AI)',
]

POST_FILTERS = [
    "software architect",
    "software architecture",
    "enterprise architect",
    "enterprise architecture",
    "solution architect",
    "solutions architect",
    "GitHub Copilot",
    "cloud architect",
    "data architect",
    "security architect",
    "systems architect",
    "network architect",
]


def operator_count(query: str) -> int:
    return len(re.findall(r"\b(AND|OR|NOT)\b", query))


def block(terms: list[str]) -> str:
    if len(terms) == 1:
        return terms[0]
    return "(" + " OR ".join(terms) + ")"


def make(tier: str, family: str, parts: list[list[str]]) -> dict:
    query = " AND ".join(block(part) for part in parts)
    count = operator_count(query)
    if count > OPERATOR_CEILING:
        raise SystemExit(f"over ceiling ({count}): {query}")
    if len(query) > 500:
        raise SystemExit(f"over 500 chars ({len(query)}): {query}")
    return {
        "tier": tier,
        "family": family,
        "query": query,
        "operators": count,
        "layers": len(parts),
    }


def term_set(query: str) -> set[str]:
    found = set(re.findall(r'"[^"]+"|\b[A-Za-z][A-Za-z0-9.+-]*\b', query))
    found -= {"AND", "OR", "NOT"}
    return found


def build() -> dict:
    profession = ["architect", "architectural"]
    profession_plural = ["architect", "architects"]
    generic_ai = ["GenAI", '"generative AI"']
    named_ai = ["Midjourney", "ChatGPT"]

    # Core 8 x 4 = 32 grid (preserving the 17 October structure, with duplicate
    # third-leg terms de-duplicated so "skill loss", "design thinking", and
    # "augmentation" are covered without extra queries).
    skills = [
        ("direct", ["skill", "skills"]),
        ("direct", ["upskilling", "reskilling"]),
        ("direct", ["deskilling", '"skill loss"']),
        ("cognition", ["creativity", '"design thinking"']),
        ("cognition", ['"critical thinking"', "intuition"]),
        ("cognition", ["authorship", "judgment"]),
        ("process", ["workflow", "automation"]),
        ("process", ["replace", "augmentation"]),
    ]
    tool_for_skill = [
        ["BIM", "Revit"],
        ["Rhino", "Grasshopper"],
        ["Parametric", '"generative design"'],
        ["Rendering", "archviz"],
        ["BIM", "Revit"],
        ["Rhino", "Grasshopper"],
        ["Parametric", '"generative design"'],
        ["Rendering", "architecture"],
    ]

    tier1: list[dict] = []
    for (skill_family, skill_terms), tool_terms in zip(skills, tool_for_skill):
        tier1.append(make("tier1_three_layer", skill_family, [profession, generic_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [profession, named_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [tool_terms, generic_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [tool_terms, named_ai, skill_terms]))

    # Original 4 supplementary queries (AI, "artificial intelligence", Copilot)
    tier1.append(
        make(
            "tier1_three_layer",
            "direct",
            [profession, ["AI", '"artificial intelligence"'], ["skill", "skills"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "process",
            [["BIM", "Revit"], ["AI", '"artificial intelligence"'], ["workflow", "automation"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "process",
            [["BIM", "Revit"], ["Copilot", "ChatGPT"], ["workflow", "automation"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "direct",
            [["Rhino", "Grasshopper"], ["Copilot"], ["skill", "skills"]],
        )
    )

    # 12 targeted strengtheners from full repository review:
    # - Direct skill: downskilling (Morteza Sep 8 / Kaveh Sep 15) & expertise (Oct 7)
    tier1.append(
        make(
            "tier1_three_layer",
            "direct",
            [profession_plural, generic_ai, ["downskilling", "deskilling"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "direct",
            [['"architectural design"', '"computational design"'], ["GenAI", "ChatGPT"], ["skills", "expertise"]],
        )
    )

    # - Cognition & visual GenAI: cognitive offloading / overreliance (Sep 25 finding),
    #   Stable Diffusion / DALL-E (Sep 15 letter), AI rendering (Oct 7 top precision)
    tier1.append(
        make(
            "tier1_three_layer",
            "cognition",
            [profession, generic_ai, ['"cognitive offloading"', "overreliance"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "cognition",
            [profession_plural, named_ai, ['"cognitive offloading"', "overreliance"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "cognition",
            [profession, ['"Stable Diffusion"', "DALL-E"], ["creativity", "authorship"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "cognition",
            [["Rendering", "archviz"], ['"AI rendering"', "Midjourney"], ["creativity", "judgment"]],
        )
    )

    # - Process & Adaptation: human-in-the-loop, role of the architect, replacement
    tier1.append(
        make(
            "tier1_three_layer",
            "process",
            [profession_plural, generic_ai, ['"human-in-the-loop"', '"role of the architect"']],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "process",
            [['"architectural design"', "architecture"], generic_ai, ["replacement", "augmentation"]],
        )
    )

    # - Technical, environmental & pedagogy (RQ3a & RQ4 neutral education queries)
    tier1.append(
        make(
            "tier1_three_layer",
            "technical_and_pedagogy",
            [profession, generic_ai, ['"technical skills"', '"environmental design"']],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "technical_and_pedagogy",
            [["BIM", '"architectural design"'], ["AI", '"generative AI"'], ['"building performance"', '"energy modeling"']],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "technical_and_pedagogy",
            [['"architectural education"', '"architecture students"'], generic_ai, ["curriculum", "learning"]],
        )
    )
    tier1.append(
        make(
            "tier1_three_layer",
            "technical_and_pedagogy",
            [['"architectural education"', '"architecture students"'], named_ai, ["skills", '"critical thinking"']],
        )
    )

    queries = tier1
    for index, item in enumerate(queries, start=1):
        item["id"] = f"Q{index:02d}"

    # Verify no duplicate query strings
    seen = set()
    for item in queries:
        if item["query"] in seen:
            raise SystemExit(f"duplicate query: {item['query']}")
        seen.add(item["query"])

    required = set()
    for group in KEYWORDS.values():
        required.update(group)
    covered = set()
    for item in queries:
        covered |= term_set(item["query"])
    missing = sorted(required - covered)
    if missing:
        raise SystemExit(f"terms missing from executable queries: {missing}")

    return {
        "protocol_id": "linkedin-apify-2026-10-17",
        "status": "final confirmed three-layer list for the Apify round (confirmed 2026-10-18); 55 keywords across 3 layers, 48 queries; no run started in this commit",
        "actor": "harvestapi/linkedin-post-search",
        "operator_ceiling": OPERATOR_CEILING,
        "operator_ceiling_source": "research/project-log.md section 40, Apify tests on 2026-10-07",
        "keywords": KEYWORDS,
        "query_count": len(queries),
        "queries": queries,
        "searchQueries": [item["query"] for item in queries],
        "post_filters_not_in_the_query": POST_FILTERS,
        "recommended_actor_input_not_executed": {
            "maxPosts": 50,
            "postedLimitDate": "2022-11-30",
            "sortBy": "date",
            "scrapeComments": False,
            "scrapeReactions": False,
            "profileScraperMode": "short",
            "contentType": "all",
        },
    }


def main() -> None:
    payload = build()
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"three-layer queries: {payload['query_count']}")
    print(f"max operators: {max(item['operators'] for item in payload['queries'])}")



if __name__ == "__main__":
    main()
