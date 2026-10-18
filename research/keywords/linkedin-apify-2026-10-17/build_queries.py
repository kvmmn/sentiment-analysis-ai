#!/usr/bin/env python3
"""Build the 2026-10-17 Apify LinkedIn query list.

Each executable query has at most five AND/OR operators. That ceiling is the
2026-10-07 observation: LinkedIn content search returned no posts at six or
more operators and returned posts at five or fewer.

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

# Terms confirmed for this round. Skill groups are the 17 October group list.
# Domain and technology terms are that list plus Iman's 17 October keyword JSON.
KEYWORDS = {
    "domain_and_tools": [
        "architect",
        "architecture",
        "architectural",
        "BIM",
        "Revit",
        "Rhino",
        "Grasshopper",
        "Parametric",
        '"generative design"',
        "Rendering",
    ],
    "ai": [
        "AI",
        "GenAI",
        '"generative AI"',
        '"artificial intelligence"',
        "Midjourney",
        "ChatGPT",
        "Copilot",
    ],
    "skill_direct": ["skill", "skills", "upskilling", "deskilling", "reskilling"],
    "skill_cognition": [
        "creativity",
        '"critical thinking"',
        "judgment",
        "intuition",
        "authorship",
    ],
    "skill_process": ["workflow", "automation", "replace"],
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
]


def operator_count(query: str) -> int:
    return len(re.findall(r"\b(AND|OR|NOT)\b", query))


def block(terms: list[str]) -> str:
    if len(terms) == 1:
        return terms[0]
    return "(" + " OR ".join(terms) + ")"


def quote_bare(query: str) -> str:
    """Wrap a query so a bare leading term is still one search string."""
    return query


def make(tier: str, family: str, parts: list[list[str]]) -> dict:
    query = " AND ".join(block(part) for part in parts)
    count = operator_count(query)
    if count > OPERATOR_CEILING:
        raise SystemExit(f"over ceiling ({count}): {query}")
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
    generic_ai = ["GenAI", '"generative AI"']
    named_ai = ["Midjourney", "ChatGPT"]
    skills = [
        ("direct", ["skill", "skills"]),
        ("direct", ["upskilling", "reskilling"]),
        ("direct", ["deskilling", "reskilling"]),
        ("cognition", ["creativity", "judgment"]),
        ("cognition", ['"critical thinking"', "intuition"]),
        ("cognition", ["authorship", "judgment"]),
        ("process", ["workflow", "automation"]),
        ("process", ["replace", "automation"]),
    ]
    tool_for_skill = [
        ["BIM", "Revit"],
        ["Rhino", "Grasshopper"],
        ["Parametric", '"generative design"'],
        ["Rendering", "architecture"],
        ["BIM", "Revit"],
        ["Rhino", "Grasshopper"],
        ["Parametric", '"generative design"'],
        ["Rendering", "architecture"],
    ]

    tier1: list[dict] = []
    for skill_family, skill_terms, tool_terms in (
        (family, skill, tool) for (family, skill), tool in zip(skills, tool_for_skill)
    ):
        tier1.append(make("tier1_three_layer", skill_family, [profession, generic_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [profession, named_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [tool_terms, generic_ai, skill_terms]))
        tier1.append(make("tier1_three_layer", skill_family, [tool_terms, named_ai, skill_terms]))

    # Terms that the covering grid above does not yet place: bare AI,
    # "artificial intelligence", and Copilot.
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

    # Two-layer option A. Five domain pairs cover all ten domain terms.
    # Four technology sides cover all seven AI terms. 5 x 4 = 20.
    # One cell is omitted: profession titles AND Copilot, the GitHub Copilot /
    # software-architect collision. Copilot stays on the tool pairs.
    domain_pairs = [
        ["architect", "architectural"],
        ["architecture", "BIM"],
        ["Revit", "Rhino"],
        ["Grasshopper", "Parametric"],
        ['"generative design"', "Rendering"],
    ]
    ai_sides = [
        ["Midjourney", "ChatGPT"],
        ["GenAI", '"generative AI"'],
        ["AI", '"artificial intelligence"'],
        ["Copilot"],
    ]
    tier2: list[dict] = []
    for domain in domain_pairs:
        for ai in ai_sides:
            if domain == ["architect", "architectural"] and ai == ["Copilot"]:
                continue
            tier2.append(make("tier2_two_layer", "option_a", [domain, ai]))

    queries = tier1 + tier2
    for index, item in enumerate(queries, start=1):
        item["id"] = f"Q{index:02d}"

    required = set()
    for group in KEYWORDS.values():
        required.update(group)
    covered = set()
    for item in queries:
        covered |= term_set(item["query"])
    missing = sorted(required - covered)
    if missing:
        raise SystemExit(f"terms missing from executable queries: {missing}")
    if len(tier2) != 19:
        raise SystemExit(f"tier 2 count is {len(tier2)}, expected 19")

    parents = [
        {"query": query, "operators": operator_count(query), "executable": operator_count(query) <= OPERATOR_CEILING}
        for query in RECEIVED_PARENTS
    ]

    return {
        "protocol_id": "linkedin-apify-2026-10-17",
        "status": "working list for this Apify round; query version 1 is not frozen; no run has been started",
        "actor": "harvestapi/linkedin-post-search",
        "operator_ceiling": OPERATOR_CEILING,
        "operator_ceiling_source": "research/project-log.md section 40, Apify tests on 2026-10-07",
        "keywords": KEYWORDS,
        "tier1_count": len(tier1),
        "tier2_count": len(tier2),
        "queries": queries,
        "searchQueries": [item["query"] for item in queries],
        "received_parents_not_all_executable": parents,
        "tier2_omitted_cell": '(architect OR architectural) AND Copilot',
        "tier2_omitted_reason": "Profession titles plus Copilot collide with GitHub Copilot and software-architect posts. Copilot remains paired with BIM, Revit, Rhino, Grasshopper, Parametric, Rendering, generative design, and architecture.",
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
    print(f"tier1 {payload['tier1_count']}  tier2 {payload['tier2_count']}  total {len(payload['queries'])}")
    print(f"max operators {max(item['operators'] for item in payload['queries'])}")


if __name__ == "__main__":
    main()
