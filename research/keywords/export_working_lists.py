#!/usr/bin/env python3
"""Write JSON, Markdown, YAML, and Word copies of working lists already in the repo.

Sources are read. No term, query, or count is added. Word is a .docx zip
written with the standard library. This script does not import a YAML or
document package.
"""

from __future__ import annotations

import ast
import json
import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
KEYWORDS = Path(__file__).resolve().parent
GENERATED = "2026-11-12"


def split_row(line: str) -> list[str]:
    parts = line.strip().strip("|").split("|")
    return [part.strip() for part in parts]


def heading_level(line: str) -> int | None:
    if not line.startswith("#"):
        return None
    marks = len(line) - len(line.lstrip("#"))
    if marks == 0 or (len(line) > marks and line[marks] != " "):
        return None
    return marks


def parse_tables_and_middots(text: str) -> tuple[list[dict], list[dict]]:
    tables: list[dict] = []
    groups: list[dict] = []
    heading = ""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        level = heading_level(line)
        if level is not None:
            heading = line[level:].strip()
            index += 1
            continue
        if (
            line.startswith("|")
            and index + 1 < len(lines)
            and re.match(r"^\|\s*-+", lines[index + 1])
        ):
            columns = split_row(line)
            index += 2
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].startswith("|"):
                row = split_row(lines[index])
                if len(row) < len(columns):
                    row = row + [""] * (len(columns) - len(row))
                rows.append(row[: len(columns)])
                index += 1
            tables.append({"heading": heading, "columns": columns, "rows": rows})
            continue
        if "·" in line and not line.startswith("|") and not line.startswith("```"):
            terms = [part.strip() for part in line.split("·")]
            terms = [part for part in terms if part]
            if len(terms) >= 2 and not any("http" in part for part in terms):
                groups.append({"heading": heading, "terms": terms})
        index += 1
    return tables, groups


def parse_bullets(text: str) -> list[dict]:
    found: list[dict] = []
    heading = ""
    for line in text.splitlines():
        level = heading_level(line)
        if level is not None:
            heading = line[level:].strip()
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            found.append({"heading": heading, "text": stripped[2:].strip()})
    return found


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def to_yaml(value, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for key, item in value.items():
            key_text = yaml_quote(str(key)) if not re.fullmatch(r"[A-Za-z0-9_]+", str(key)) else str(key)
            if isinstance(item, (dict, list)) and item:
                lines.append(f"{pad}{key_text}:")
                lines.append(to_yaml(item, indent + 2))
            else:
                rendered = to_yaml(item, 0)
                lines.append(f"{pad}{key_text}: {rendered}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return "[]"
        lines = []
        for item in value:
            if isinstance(item, (dict, list)) and item:
                rendered = to_yaml(item, indent + 2)
                if isinstance(item, dict):
                    first, *rest = rendered.splitlines()
                    lines.append(f"{pad}- {first.lstrip()}")
                    lines.extend(rest)
                else:
                    lines.append(f"{pad}-")
                    lines.append(rendered)
            else:
                lines.append(f"{pad}- {to_yaml(item, 0)}")
        return "\n".join(lines)
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, str):
        return yaml_quote(value)
    raise TypeError(type(value))


def write_yaml(path: Path, value: dict) -> None:
    path.write_text(to_yaml(value) + "\n", encoding="utf-8")


def docx_paragraph(text: str, *, bold: bool = False) -> str:
    run_props = "<w:rPr><w:b/></w:rPr>" if bold else ""
    safe = escape(text)
    return (
        "<w:p>"
        f"<w:r>{run_props}<w:t xml:space=\"preserve\">{safe}</w:t></w:r>"
        "</w:p>"
    )


def write_docx(path: Path, paragraphs: list[tuple[str, bool]]) -> None:
    body = "".join(docx_paragraph(text, bold=bold) for text, bold in paragraphs)
    body += (
        "<w:sectPr>"
        "<w:pgSz w:w=\"12240\" w:h=\"15840\"/>"
        "<w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\"/>"
        "</w:sectPr>"
    )
    document = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
        f"<w:body>{body}</w:body></w:document>"
    )
    content_types = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
        "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
        "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
        "<Override PartName=\"/word/document.xml\" "
        "ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>"
        "</Types>"
    )
    rels = (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
        "<Relationship Id=\"rId1\" "
        "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" "
        "Target=\"word/document.xml\"/>"
        "</Relationships>"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("word/document.xml", document)


def write_bundle(stem: Path, payload: dict, paragraphs: list[tuple[str, bool]], markdown: str) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    stem.with_suffix(".json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_yaml(stem.with_suffix(".yaml"), payload)
    stem.with_suffix(".md").write_text(markdown, encoding="utf-8")
    write_docx(stem.with_suffix(".docx"), paragraphs)


def md_table(columns: list[str], rows: list[list[str]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in rows]
    return "\n".join([header, rule, *body])


def executed_keywords() -> None:
    source = KEYWORDS / "linkedin-apify-2026-10-17" / "queries.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    keywords = data["keywords"]
    filters = data["post_filters_not_in_the_query"]
    total = sum(len(items) for items in keywords.values())
    if total != 55:
        raise SystemExit(f"expected 55 keywords, found {total}")
    payload = {
        "generated": GENERATED,
        "source": "research/keywords/linkedin-apify-2026-10-17/queries.json",
        "note": (
            "Extract of keywords and post_filters_not_in_the_query. "
            "Not a new list. The Boolean strings stay in queries.json."
        ),
        "protocol_id": data["protocol_id"],
        "status": data["status"],
        "keyword_count": total,
        "keywords": keywords,
        "post_filters_not_in_the_query": filters,
    }
    paragraphs: list[tuple[str, bool]] = [
        ("Executed keywords, 55 terms", True),
        (payload["note"], False),
        (f"Source: {payload['source']}", False),
    ]
    lines = [
        "# Executed keywords, 55 terms",
        "",
        f"Generated {GENERATED} from [`queries.json`](queries.json). {payload['note']}",
        "",
        f"Keyword count: {total}.",
        "",
    ]
    labels = {
        "domain_and_tools": "Domain and tools",
        "ai": "AI",
        "skill_direct": "Direct skill",
        "skill_cognition": "Cognition and design",
        "skill_process": "Process, adaptation, and role",
        "skill_technical_and_pedagogy": "Technical, environmental, and pedagogy",
    }
    for key, items in keywords.items():
        title = f"{labels.get(key, key)} ({len(items)})"
        paragraphs.append((title, True))
        lines.append(f"## {title}")
        lines.append("")
        for item in items:
            paragraphs.append((item, False))
            lines.append(f"- {item}")
        lines.append("")
    paragraphs.append((f"Post-filters, not in the query ({len(filters)})", True))
    lines.append(f"## Post-filters, not in the query ({len(filters)})")
    lines.append("")
    for item in filters:
        paragraphs.append((item, False))
        lines.append(f"- {item}")
    lines.append("")
    write_bundle(
        KEYWORDS / "linkedin-apify-2026-10-17" / "keywords",
        payload,
        paragraphs,
        "\n".join(lines),
    )


def literature_strings() -> None:
    source = KEYWORDS / "keyword-literature-strings.md"
    text = source.read_text(encoding="utf-8")
    fences = []
    heading = ""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        level = heading_level(line)
        if level is not None:
            heading = line[level:].strip()
            index += 1
            continue
        if line.strip() == "```text":
            label = heading
            look = index - 1
            while look >= 0 and not lines[look].strip():
                look -= 1
            if look >= 0 and lines[look].startswith("**") and lines[look].endswith("**"):
                label = lines[look].strip("*").strip()
            index += 1
            body: list[str] = []
            while index < len(lines) and lines[index].strip() != "```":
                body.append(lines[index])
                index += 1
            fences.append({"heading": label, "text": "\n".join(body).strip()})
            index += 1
            continue
        index += 1
    tables, _groups = parse_tables_and_middots(text)
    by_heading = {table["heading"]: table for table in tables}
    published = by_heading.get("Ghimire 2024 — published construction strings (related-work only)")
    asjc = by_heading.get("Subject areas (Scopus ASJC)")
    narrow = by_heading.get("Too-narrow — sensitivity only (not primary RQ1)")
    if published is None or asjc is None or narrow is None:
        raise SystemExit(f"literature tables missing: {list(by_heading)}")
    expected_headings = [
        "S-A1 — Scopus (primary)",
        "W-A1 — Web of Science (primary)",
        "I-A1 — IEEE Xplore (25-term limit per clause; not primary architecture database)",
        "G-A1a — core architecture + GenAI",
        "G-A1b — education + studio",
        "G-A1c — practice",
        "S-RW1 — Scopus",
        "Layer B — post-retrieval or secondary filter (literature)",
    ]
    if [item["heading"] for item in fences] != expected_headings:
        raise SystemExit(f"paste headings changed: {[item['heading'] for item in fences]}")
    payload = {
        "generated": GENERATED,
        "source": "research/keywords/keyword-literature-strings.md",
        "note": (
            "Copy-paste strings and the tables already in that file. "
            "No string was added. Live hit counts were not run in the source."
        ),
        "paste_strings": fences,
        "related_work_published_strings": {
            "heading": published["heading"],
            "columns": published["columns"],
            "rows": published["rows"],
        },
        "scopus_asjc": {
            "heading": asjc["heading"],
            "columns": asjc["columns"],
            "rows": asjc["rows"],
        },
        "too_narrow_variants": {
            "heading": narrow["heading"],
            "columns": narrow["columns"],
            "rows": narrow["rows"],
        },
    }
    paragraphs: list[tuple[str, bool]] = [
        ("Literature strings", True),
        (payload["note"], False),
    ]
    lines = [
        "# Literature strings",
        "",
        f"Generated {GENERATED} from [`keyword-literature-strings.md`](keyword-literature-strings.md). {payload['note']}",
        "",
        "## Paste strings",
        "",
    ]
    paragraphs.append(("Paste strings", True))
    for item in fences:
        paragraphs.append((item["heading"], True))
        paragraphs.append((item["text"], False))
        lines.append(f"### {item['heading']}")
        lines.append("")
        lines.append("```text")
        lines.append(item["text"])
        lines.append("```")
        lines.append("")
    for block_name, block in (
        ("Related-work published strings", payload["related_work_published_strings"]),
        ("Scopus ASJC subject areas", payload["scopus_asjc"]),
        ("Too-narrow variants", payload["too_narrow_variants"]),
    ):
        paragraphs.append((block_name, True))
        lines.append(f"## {block_name}")
        lines.append("")
        lines.append(md_table(block["columns"], block["rows"]))
        lines.append("")
        for row in block["rows"]:
            paragraphs.append((" | ".join(row), False))
    write_bundle(KEYWORDS / "literature-strings", payload, paragraphs, "\n".join(lines))


def lexicon() -> None:
    source = KEYWORDS / "keyword-lexicon.md"
    text = source.read_text(encoding="utf-8")
    tables, groups = parse_tables_and_middots(text)
    term_tables = [table for table in tables if table["columns"] and table["columns"][0] in {"Term", "Block"}]
    if not any(table["columns"][0] == "Term" for table in term_tables):
        raise SystemExit("lexicon term tables not found")
    payload = {
        "generated": GENERATED,
        "source": "research/keywords/keyword-lexicon.md",
        "note": (
            "Term tables and middle-dot lists from that file, including the Counts table. "
            "Not a validated thesaurus. No term was added."
        ),
        "tables": term_tables,
        "middot_lists": groups,
    }
    paragraphs: list[tuple[str, bool]] = [("Keyword lexicon lists", True), (payload["note"], False)]
    lines = [
        "# Keyword lexicon lists",
        "",
        f"Generated {GENERATED} from [`keyword-lexicon.md`](keyword-lexicon.md). {payload['note']}",
        "",
    ]
    for group in groups:
        paragraphs.append((group["heading"], True))
        lines.append(f"## {group['heading']}")
        lines.append("")
        for term in group["terms"]:
            paragraphs.append((term, False))
            lines.append(f"- {term}")
        lines.append("")
    for table in term_tables:
        paragraphs.append((table["heading"], True))
        lines.append(f"## {table['heading']}")
        lines.append("")
        lines.append(md_table(table["columns"], table["rows"]))
        lines.append("")
        if table["columns"][0] == "Term":
            for row in table["rows"]:
                paragraphs.append((row[0], False))
    write_bundle(KEYWORDS / "lexicon", payload, paragraphs, "\n".join(lines))


def discourse() -> None:
    source = KEYWORDS / "keyword-discourse-catalog.md"
    text = source.read_text(encoding="utf-8")
    tables, _groups = parse_tables_and_middots(text)
    bullets = parse_bullets(text)
    plain_lines: list[dict] = []
    heading = ""
    for line in text.splitlines():
        level = heading_level(line)
        if level is not None:
            heading = line[level:].strip()
            continue
        stripped = line.strip()
        if (
            stripped
            and not stripped.startswith(("- ", "|", "#", ">"))
            and stripped.count(",") >= 4
            and "http" not in stripped
            and len(stripped) < 500
        ):
            plain_lines.append({"heading": heading, "text": stripped})
    if [item["text"] for item in plain_lines] != [
        "Deskilling, de-skilling, upskilling, reskilling, authorship, professional judgment, creativity, critical thinking, Urheberrecht (when DE cross-pass), competency / ARB outcomes language."
    ]:
        raise SystemExit(f"unexpected plain term lines: {plain_lines}")
    if not tables or not bullets:
        raise SystemExit("discourse lists not found")
    payload = {
        "generated": GENERATED,
        "source": "research/keywords/keyword-discourse-catalog.md",
        "note": (
            "Tables, bullet lines, and the Layer B comma list from that file. "
            "Other prose stays in the source. No lemma was added. GAP rows are copied as written."
        ),
        "tables": tables,
        "bullets": bullets,
        "plain_term_lines": plain_lines,
    }
    paragraphs: list[tuple[str, bool]] = [("Discourse catalog lists", True), (payload["note"], False)]
    lines = [
        "# Discourse catalog lists",
        "",
        f"Generated {GENERATED} from [`keyword-discourse-catalog.md`](keyword-discourse-catalog.md). {payload['note']}",
        "",
        "## Plain term lines",
        "",
    ]
    paragraphs.append(("Plain term lines", True))
    for item in plain_lines:
        paragraphs.append((item["heading"], True))
        paragraphs.append((item["text"], False))
        lines.append(f"### {item['heading']}")
        lines.append("")
        lines.append(item["text"])
        lines.append("")
    lines.extend([
        "## Bullets",
        "",
    ])
    paragraphs.append(("Bullets", True))
    current = None
    for bullet in bullets:
        if bullet["heading"] != current:
            current = bullet["heading"]
            paragraphs.append((current, True))
            lines.append(f"### {current}")
            lines.append("")
        paragraphs.append((bullet["text"], False))
        lines.append(f"- {bullet['text']}")
        lines.append("")
    lines.append("## Tables")
    lines.append("")
    paragraphs.append(("Tables", True))
    for table in tables:
        paragraphs.append((table["heading"], True))
        lines.append(f"### {table['heading']}")
        lines.append("")
        lines.append(md_table(table["columns"], table["rows"]))
        lines.append("")
    write_bundle(KEYWORDS / "discourse-terms", payload, paragraphs, "\n".join(lines))


def october_term_blocks() -> None:
    source = KEYWORDS / "linkedin-boolean-2026-10-07" / "decompose.py"
    text = source.read_text(encoding="utf-8")
    blocks = {}
    for name in ("A", "B", "C"):
        match = re.search(rf"^{name} = (\[.*\])$", text, re.M)
        if match is None:
            raise SystemExit(f"missing {name} in decompose.py")
        blocks[name] = ast.literal_eval(match.group(1))
    if (len(blocks["A"]), len(blocks["B"]), len(blocks["C"])) != (10, 5, 13):
        raise SystemExit(f"unexpected block sizes: { {k: len(v) for k, v in blocks.items()} }")
    payload = {
        "generated": GENERATED,
        "source": "research/keywords/linkedin-boolean-2026-10-07/decompose.py",
        "note": (
            "The three term lists that decompose.py multiplies into the 105 sub-queries. "
            "The sub-queries themselves stay in subqueries.json. No term was added."
        ),
        "A_domain": blocks["A"],
        "B_ai": blocks["B"],
        "C_labor": blocks["C"],
    }
    labels = (
        ("A_domain", "A — domain"),
        ("B_ai", "B — AI"),
        ("C_labor", "C — labor / competency"),
    )
    paragraphs: list[tuple[str, bool]] = [("7 October term blocks", True), (payload["note"], False)]
    lines = [
        "# 7 October term blocks",
        "",
        f"Generated {GENERATED} from [`decompose.py`](decompose.py). {payload['note']}",
        "",
    ]
    for key, title in labels:
        paragraphs.append((f"{title} ({len(payload[key])})", True))
        lines.append(f"## {title} ({len(payload[key])})")
        lines.append("")
        for item in payload[key]:
            paragraphs.append((item, False))
            lines.append(f"- {item}")
        lines.append("")
    write_bundle(
        KEYWORDS / "linkedin-boolean-2026-10-07" / "term-blocks",
        payload,
        paragraphs,
        "\n".join(lines),
    )


def legacy_scraper_keywords() -> None:
    source = ROOT / "src" / "linkedin-scraper" / "keywords.txt"
    phrases = []
    for line in source.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            phrases.append(stripped)
    if len(phrases) != 7:
        raise SystemExit(f"expected 7 legacy phrases, found {len(phrases)}")
    payload = {
        "generated": GENERATED,
        "source": "src/linkedin-scraper/keywords.txt",
        "note": (
            "One phrase per non-comment line of the legacy scraper keyword file. "
            "Historical exploratory list, not an approved collection set. No phrase was added."
        ),
        "phrases": phrases,
    }
    paragraphs: list[tuple[str, bool]] = [("Legacy scraper keywords", True), (payload["note"], False)]
    lines = [
        "# Legacy scraper keywords",
        "",
        f"Generated {GENERATED} from [`keywords.txt`](keywords.txt). {payload['note']}",
        "",
    ]
    for phrase in phrases:
        paragraphs.append((phrase, False))
        lines.append(f"- {phrase}")
    lines.append("")
    write_bundle(source.parent / "keywords", payload, paragraphs, "\n".join(lines))


def main() -> None:
    executed_keywords()
    literature_strings()
    lexicon()
    discourse()
    october_term_blocks()
    legacy_scraper_keywords()
    print("wrote working-list downloads")


if __name__ == "__main__":
    main()
