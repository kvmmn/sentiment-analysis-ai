#!/usr/bin/env python3
"""Generate the Saintiment keyword lexicon PDF (minimal black-on-white layout).

Requires: pip install reportlab
Output: research/keyword-lexicon.pdf
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "research" / "keyword-lexicon.pdf"

FONT_INTER = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
FONT_INTER_SB = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_INTER_B = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_NOTO = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_NOTO_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"

PAGE_W, PAGE_H = A4
MARGIN = 22 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
LINE = 5.6 * mm
HIGHLIGHT_FILL = colors.HexColor("#F2F2F2")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Inter", FONT_INTER))
    pdfmetrics.registerFont(TTFont("Inter-SemiBold", FONT_INTER_SB))
    pdfmetrics.registerFont(TTFont("Inter-Bold", FONT_INTER_B))
    pdfmetrics.registerFont(TTFont("Noto", FONT_NOTO))
    pdfmetrics.registerFont(TTFont("Noto-Bold", FONT_NOTO_B))


CATEGORIES = [
    ("A", "Architecture / built environment", "Layer A — discovery context"),
    ("G", "Generative AI & tools", "Layer A — GenAI cues"),
    ("S", "Skill, labour, deskilling", "Layer B — profession & labour"),
    ("K", "Soft skills & judgment", "Layer B — creativity & judgment"),
    ("H", "Hard / technical / environmental", "Layer B — technical competence"),
    ("R", "Representation & digital practice", "Layer B — drawing & digital"),
    ("W", "Stakeholder / role vocabulary", "RQ4 coding & retrieval"),
    ("X", "Exclusion / false-positive control", "Mark as exclude, do not silently drop"),
]

LEXICON: dict[str, dict] = {
    "layer_a_architecture": {
        "title": "Layer A — Architecture context",
        "code": "A",
        "lang": "EN",
        "note": "Require architectural context. Pair every term with a GenAI cue (Layer G).",
        "terms": [
            ("architect", True),
            ("architects", True),
            ("architectural", True),
            ("architectural design", False),
            ("architectural practice", True),
            ("architectural education", False),
            ("architectural discourse", False),
            ("architecture firm", True),
            ("architecture studio", False),
            ("architecture school", False),
            ("architecture student", True),
            ("architecture office", False),
            ("licensed architect", False),
            ("registered architect", False),
            ("architect of record", False),
            ("junior architect", False),
            ("intern architect", False),
            ("associate architect", False),
            ("principal architect", False),
            ("design principal", False),
            ("starchitect", False),
            ("AIA", False),
            ("RIBA", False),
            ("RAIA / Australian Institute of Architects", False),
            ("NAAB", False),
            ("built environment", False),
            ("building design", False),
            ("urban design", False),
            ("urbanism", False),
            ("landscape architecture", False),
            ("interior architecture", False),
            ("schematic design", False),
            ("design development", False),
            ("construction documentation", False),
            ("construction administration", False),
            ("design studio", False),
            ("studio culture", False),
            ("design crit", False),
            ("design jury", False),
            ("Part 1 architect", False),
            ("Part 2 architect", False),
            ("Part 3 architect", False),
            ("architectural visualization", False),
            ("archviz", True),
            ("architectural rendering", False),
            ("facade / façade", False),
            ("building envelope", False),
            ("massing", False),
            ("floor plan", False),
            ("concept design", False),
            ("conceptual design", False),
        ],
    },
    "layer_a_genai": {
        "title": "Layer A — Generative AI & named tools",
        "code": "G",
        "lang": "EN",
        "note": "Neutral discovery set. generative design = older CAD sense; tag separately from GenAI.",
        "terms": [
            ("generative AI", True),
            ("GenAI", True),
            ("gen AI", False),
            ("generative artificial intelligence", False),
            ("AI-generated", False),
            ("AI generated", False),
            ("text-to-image", True),
            ("text to image", False),
            ("image generation", False),
            ("AI rendering", True),
            ("AI visualization / visualisation", False),
            ("AI-assisted design", False),
            ("AI-aided design", False),
            ("AI design", False),
            ("large language model", False),
            ("LLM", True),
            ("prompt", False),
            ("prompting", False),
            ("prompt engineering", False),
            ("ChatGPT", True),
            ("GPT", False),
            ("OpenAI", False),
            ("Claude", False),
            ("Gemini", False),
            ("Copilot", False),
            ("Midjourney", True),
            ("DALL-E / DALL·E / Dall-E", True),
            ("Stable Diffusion", True),
            ("Flux", False),
            ("Adobe Firefly", False),
            ("Leonardo AI", False),
            ("Ideogram", False),
            ("ComfyUI", False),
            ("diffusion model", False),
            ("LookX", False),
            ("Veras", False),
            ("Finch / Finch3D", False),
            ("TestFit", False),
            ("Spacemaker", False),
            ("Autodesk Forma", False),
            ("Forma", False),
            ("Maket / Maket.ai", False),
            ("Hypar", False),
            ("Snaptrude", False),
            ("Visoid", False),
            ("Runway", False),
            ("Sora", False),
            ("Revit AI", False),
            ("Rhino AI", False),
            ("Grasshopper AI", False),
            ("generative design", True),
        ],
    },
    "layer_b_deskilling": {
        "title": "Layer B — Deskilling & labour",
        "code": "S",
        "lang": "EN",
        "note": "Use only with Layer A, or as a second filter on architecture + GenAI hits.",
        "terms": [
            ("deskilling", True),
            ("de-skilling / de skilling", True),
            ("skill loss", True),
            ("skill erosion", False),
            ("skill atrophy", False),
            ("losing skills", False),
            ("lost skills", False),
            ("dumbing down", False),
            ("replace architects", True),
            ("replacing architects", False),
            ("architect replacement", False),
            ("automate architecture", False),
            ("automated design", False),
            ("automation of design", False),
            ("job displacement", True),
            ("job loss", False),
            ("junior pipeline", False),
            ("training pipeline", False),
            ("apprenticeship", False),
            ("fewer juniors", False),
            ("craft", False),
            ("craftsmanship", False),
            ("tacit knowledge", False),
            ("professional expertise", False),
            ("commoditization / commodification", False),
            ("obsolescence", False),
            ("obsolete skills", False),
            ("reskilling", True),
            ("upskilling", True),
            ("skill shift", False),
            ("skill transformation", False),
            ("new skills", False),
            ("future of the profession", True),
            ("future of architecture", False),
            ("future of architects", False),
            ("AI will replace", False),
            ("human in the loop", False),
            ("cheaper design", False),
            ("faster cheaper", False),
        ],
    },
    "layer_b_soft": {
        "title": "Layer B — Soft skills & judgment",
        "code": "K",
        "lang": "EN",
        "note": "RQ2a / RQ2b. Always combine with Layer A + G.",
        "terms": [
            ("soft skills", True),
            ("creativity", True),
            ("creative thinking", False),
            ("design thinking", True),
            ("originality", False),
            ("authorship", True),
            ("authorial", False),
            ("imagination", False),
            ("artistic", False),
            ("aesthetic", False),
            ("taste", False),
            ("conceptual thinking", False),
            ("idea generation", False),
            ("storytelling", False),
            ("narrative", False),
            ("client communication", False),
            ("presentation skills", False),
            ("collaboration", False),
            ("empathy", False),
            ("judgment / judgement", True),
            ("professional judgment", True),
            ("design judgment", False),
            ("critical thinking", True),
            ("critical judgment", False),
            ("decision-making", False),
            ("design intuition", False),
            ("intuition", False),
            ("expertise", False),
            ("cognitive skills", False),
            ("spatial reasoning", False),
            ("discernment", False),
            ("problem-solving", False),
        ],
    },
    "layer_b_hard": {
        "title": "Layer B — Hard / technical / environmental",
        "code": "H",
        "lang": "EN",
        "note": "RQ3a. Environmental and regulatory competence.",
        "terms": [
            ("hard skills", True),
            ("technical skills", True),
            ("technical knowledge", False),
            ("environmental design", True),
            ("environmental performance", False),
            ("building performance", True),
            ("building science", False),
            ("energy modeling / modelling", False),
            ("daylighting", False),
            ("thermal comfort", False),
            ("passive design", False),
            ("sustainability", False),
            ("carbon", False),
            ("life-cycle / LCA", False),
            ("building codes", True),
            ("building regulations", False),
            ("zoning", False),
            ("code compliance", False),
            ("fire safety", False),
            ("accessibility", False),
            ("structural design", False),
            ("MEP", False),
            ("detailing", True),
            ("construction detailing", False),
            ("construction knowledge", False),
            ("buildability", False),
            ("materials knowledge", False),
            ("specification / specifications", False),
            ("technical drawing", False),
            ("working drawings", False),
        ],
    },
    "layer_b_representation": {
        "title": "Layer B — Representation & digital practice",
        "code": "R",
        "lang": "EN",
        "note": "RQ3b. Drawing, BIM, rendering, computational workflows.",
        "terms": [
            ("representation", False),
            ("architectural representation", False),
            ("drawing", False),
            ("hand drawing", True),
            ("drafting / draughting", False),
            ("CAD", False),
            ("BIM", True),
            ("Revit", True),
            ("AutoCAD", False),
            ("Rhino / Rhinoceros", False),
            ("Grasshopper", False),
            ("SketchUp", False),
            ("ArchiCAD", False),
            ("Vectorworks", False),
            ("Lumion", False),
            ("Enscape", False),
            ("V-Ray", False),
            ("Twinmotion", False),
            ("Unreal Engine", False),
            ("rendering", True),
            ("visualization / visualisation", True),
            ("3D modeling / modelling", False),
            ("computational design", True),
            ("parametric design", True),
            ("algorithmic design", False),
            ("digital skills", False),
            ("scripting", False),
            ("visual programming", False),
            ("digital fabrication", False),
            ("Photoshop", False),
            ("post-production", False),
            ("collage", False),
            ("diagram", False),
            ("section / elevation / perspective", False),
        ],
    },
    "stakeholders": {
        "title": "Stakeholder vocabulary",
        "code": "W",
        "lang": "EN",
        "note": "For RQ4. Infer role from self-identification in text, not from photos.",
        "terms": [
            ("practitioner", True),
            ("practicing / practising architect", True),
            ("professional practice", False),
            ("academic", True),
            ("professor", False),
            ("lecturer", False),
            ("educator", False),
            ("faculty", False),
            ("architecture researcher", False),
            ("student", True),
            ("architecture student", True),
            ("graduate student", False),
            ("intern", False),
            ("year-out", False),
            ("industry leader", False),
            ("thought leader", False),
            ("principal", False),
            ("partner", False),
            ("director", False),
            ("practice director", False),
            ("firm owner", False),
            ("Dean / head of school", False),
            ("developer", False),
            ("client", False),
            ("critic", False),
        ],
    },
    "exclusions": {
        "title": "Exclusion & control terms",
        "code": "X",
        "lang": "EN",
        "note": "Log matches; mark relevance_status: exclude. Do not silently drop from raw batch.",
        "terms": [
            ("software architect", True),
            ("solutions architect / solution architect", True),
            ("enterprise architect / enterprise architecture", True),
            ("cloud architect", True),
            ("data architect", False),
            ("information architect", False),
            ("security architect", False),
            ("systems architect", False),
            ("IT architect", False),
            ("TOGAF / Zachman", False),
            ("computer architecture / CPU architecture / chip architecture", True),
            ("instruction set", False),
            ("microservices", False),
            ("naval architect", False),
            ("GitHub Copilot", False),
        ],
    },
    "persian": {
        "title": "Persian seed terms",
        "code": "FA",
        "lang": "FA",
        "note": "Optional second pass. Do not mix with English without a language field.",
        "terms": [
            ("معماری", True),
            ("معمار", True),
            ("معماران", False),
            ("طراحی معماری", False),
            ("دفتر معماری", False),
            ("آموزش معماری", False),
            ("دانشجوی معماری", True),
            ("آتلیه معماری", False),
            ("رندر معماری", False),
            ("ویژوالایز", False),
            ("هوش مصنوعی مولد", True),
            ("هوش مصنوعی", False),
            ("هوش مصنوعی در معماری", True),
            ("طراحی با هوش مصنوعی", False),
            ("رندر با هوش مصنوعی", False),
            ("میدجرنی", True),
            ("چت‌جی‌پی‌تی / چت جی پی تی", True),
            ("مهارت‌زدایی", True),
            ("کاهش مهارت", False),
            ("از دست رفتن مهارت", False),
            ("زوال مهارت", False),
            ("جایگزینی معمار", True),
            ("بیکاری معماران", False),
            ("اتوماسیون طراحی", False),
            ("مهارت نرم", True),
            ("خلاقیت", True),
            ("تفکر طراحی", False),
            ("قضاوت حرفه‌ای", False),
            ("سلیقه", False),
            ("مهارت سخت", False),
            ("مهارت فنی", False),
            ("طراحی محیطی", False),
            ("دانش ساخت", False),
            ("جزئیات اجرایی", False),
            ("مقررات ملی ساختمان", False),
            ("ترسیم", False),
            ("دست‌رسمی / اسکیس", False),
            ("نقشه‌کشی", False),
            ("مدل‌سازی", False),
            ("بیم / BIM", True),
            ("طراحی پارامتریک", False),
            ("طراحی محاسباتی", False),
            ("حرفه‌مند", False),
            ("حرفه‌ای", False),
            ("دانشگاهی / آکادمیک", False),
            ("دانشجو", False),
            ("مدیر دفتر", False),
            ("کارفرما", False),
        ],
    },
    "german": {
        "title": "German seed terms",
        "code": "DE",
        "lang": "DE",
        "note": "Optional second pass. Not selected for first collection.",
        "terms": [
            ("Architektur", True),
            ("Architekt / Architektin / Architekten", True),
            ("Architekturbüro", False),
            ("Architekturstudium", False),
            ("generative KI", True),
            ("Künstliche Intelligenz", False),
            ("KI-generiert", False),
            ("Midjourney", True),
            ("Dequalifizierung", True),
            ("Entqualifizierung", False),
            ("Kompetenzverlust", False),
            ("Kreativität", True),
            ("Design Thinking", False),
            ("Urteilsvermögen", False),
            ("fachliches Urteil", False),
            ("technische Fähigkeiten", False),
            ("umweltgerechtes Entwerfen", False),
            ("Darstellung", False),
            ("Visualisierung", True),
            ("Handzeichnung", False),
            ("BIM", True),
        ],
    },
}


class LexiconPDF:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.c = canvas.Canvas(str(path), pagesize=A4)
        self.page_num = 0

    def save(self) -> None:
        self.c.save()

    def new_page(self) -> None:
        if self.page_num:
            self.c.showPage()
        self.page_num += 1
        self.c.setFillColor(colors.black)
        self.c.setStrokeColor(colors.black)

    def footer(self) -> None:
        self.c.setFont("Inter", 8)
        self.c.drawRightString(PAGE_W - MARGIN, 12 * mm, f"{self.page_num}")
        self.c.setFont("Inter", 8)
        self.c.drawString(MARGIN, 12 * mm, "Saintiment · keyword lexicon draft")

    def draw_cover(self) -> None:
        self.new_page()
        y = PAGE_H - 48 * mm
        self.c.setFont("Inter-SemiBold", 28)
        self.c.drawString(MARGIN, y, "Keyword Lexicon")
        y -= 14 * mm
        self.c.setFont("Inter", 13)
        self.c.drawString(MARGIN, y, "Saintiment research · working draft")
        y -= 22 * mm
        self.c.setFont("Inter", 10.5)
        lines = [
            "Generative AI and deskilling in architectural discourse.",
            "Seed terms for team review — not permission to collect.",
            "Source: research/keywords-search-storage.md · 2026-08-29",
        ]
        for line in lines:
            self.c.drawString(MARGIN, y, line)
            y -= LINE
        y -= 8 * mm
        self.c.setFont("Inter-SemiBold", 10)
        self.c.drawString(MARGIN, y, "Essential terms are highlighted.")
        self.footer()

    def draw_categories(self) -> None:
        self.new_page()
        y = PAGE_H - MARGIN
        self.c.setFont("Inter-SemiBold", 20)
        self.c.drawString(MARGIN, y, "Categories")
        y -= 10 * mm
        self.c.setFont("Inter", 10)
        self.c.drawString(
            MARGIN,
            y,
            "Two search layers: A discovers architecture + GenAI; B filters skill terms inside that set.",
        )
        y -= 12 * mm

        col_code = MARGIN
        col_label = MARGIN + 14 * mm
        col_layer = MARGIN + 78 * mm
        self.c.setFont("Inter-SemiBold", 9)
        self.c.drawString(col_code, y, "Code")
        self.c.drawString(col_label, y, "Category")
        self.c.drawString(col_layer, y, "Layer / use")
        y -= 2 * mm
        self.c.setLineWidth(0.4)
        self.c.line(MARGIN, y, PAGE_W - MARGIN, y)
        y -= 6 * mm

        self.c.setFont("Inter", 10)
        for code, label, layer in CATEGORIES:
            self.c.setFont("Inter-Bold", 10)
            self.c.drawString(col_code, y, code)
            self.c.setFont("Inter", 10)
            self.c.drawString(col_label, y, label)
            self.c.drawString(col_layer, y, layer)
            y -= LINE

        y -= 8 * mm
        self.c.setFont("Inter-SemiBold", 11)
        self.c.drawString(MARGIN, y, "Search rules")
        y -= 7 * mm
        self.c.setFont("Inter", 9.5)
        rules = [
            "1. Require architectural context — never search GenAI alone.",
            "2. Layer A must run without Layer B (neutral discovery).",
            "3. Do not search sentiment words (excited, hype, threat…).",
            "4. Record the query string with every captured item.",
            "5. Treat EN, FA, and DE as separate language passes.",
            "6. Exclude IT/software-architecture hits by documented rules.",
        ]
        for rule in rules:
            self.c.drawString(MARGIN, y, rule)
            y -= LINE - 0.8 * mm

        y -= 4 * mm
        self.c.setFont("Inter", 9.5)
        self.c.drawString(
            MARGIN,
            y,
            "Query logic: (architecture context) AND (GenAI cue) AND optional (skill cue) NOT (exclusion)",
        )
        self.footer()

    def draw_query_page(self) -> None:
        self.new_page()
        y = PAGE_H - MARGIN
        self.c.setFont("Inter-SemiBold", 20)
        self.c.drawString(MARGIN, y, "Query version 1 (pilot)")
        y -= 10 * mm
        self.c.setFont("Inter", 10)
        self.c.drawString(MARGIN, y, "Planning strings — adapt operators to the permitted interface.")
        y -= 12 * mm

        blocks = [
            (
                "A1 — neutral discovery",
                '(architect OR architectural OR "architecture firm" OR "architecture student" OR archviz)\n'
                'AND ("generative AI" OR GenAI OR Midjourney OR "AI rendering" OR ChatGPT OR "DALL-E" OR "Stable Diffusion")\n'
                'NOT ("software architect" OR "solutions architect" OR "enterprise architecture" OR "cloud architect")',
            ),
            (
                "B1 — deskilling inside topic",
                "A1 AND (deskilling OR de-skilling OR skill loss OR replace architects OR upskilling OR reskilling)",
            ),
            (
                "Scope defaults",
                "English first · from 2022-11-30 · one permitted source per batch · pilot 80–120 Layer-A hits",
            ),
        ]
        for heading, body in blocks:
            self.c.setFont("Inter-SemiBold", 10.5)
            self.c.drawString(MARGIN, y, heading)
            y -= 6 * mm
            self.c.setFont("Inter", 9)
            for line in body.split("\n"):
                if y < 28 * mm:
                    self.footer()
                    self.new_page()
                    y = PAGE_H - MARGIN
                self.c.drawString(MARGIN + 2 * mm, y, line)
                y -= 4.8 * mm
            y -= 6 * mm
        self.footer()

    def _term_width(self, term: str, font: str, size: float) -> float:
        return pdfmetrics.stringWidth(term, font, size)

    def _draw_term_chip(
        self,
        term: str,
        essential: bool,
        x: float,
        y: float,
        font_latin: str,
        font_bold: str,
        size: float,
        rtl: bool = False,
    ) -> tuple[float, float]:
        pad_x = 2.8 * mm
        pad_y = 1.6 * mm
        font = font_bold if essential else font_latin
        tw = self._term_width(term, font, size)
        chip_w = tw + 2 * pad_x
        chip_h = size + 2 * pad_y

        if essential:
            self.c.setFillColor(HIGHLIGHT_FILL)
            self.c.setStrokeColor(colors.black)
            self.c.setLineWidth(0.25)
            self.c.roundRect(x, y - pad_y, chip_w, chip_h, 1.5 * mm, fill=1, stroke=0)
            self.c.setFillColor(colors.black)

        self.c.setFont(font, size)
        text_x = x + pad_x
        if rtl:
            text_x = x + pad_x
        self.c.drawString(text_x, y, term)
        return chip_w + 3 * mm, chip_h

    def draw_term_page(self, section: dict) -> None:
        self.new_page()
        y = PAGE_H - MARGIN
        code = section["code"]
        lang = section["lang"]

        self.c.setFont("Inter-SemiBold", 20)
        self.c.drawString(MARGIN, y, section["title"])
        y -= 8 * mm
        self.c.setFont("Inter-Bold", 10)
        self.c.drawString(MARGIN, y, f"Category {code} · {lang}")
        y -= 6 * mm
        self.c.setFont("Inter", 9.5)
        note = section["note"]
        for chunk_start in range(0, len(note), 95):
            self.c.drawString(MARGIN, y, note[chunk_start : chunk_start + 95])
            y -= 4.8 * mm
        y -= 4 * mm

        essential_count = sum(1 for _, e in section["terms"] if e)
        total = len(section["terms"])
        self.c.setFont("Inter", 9)
        self.c.drawString(
            MARGIN,
            y,
            f"{total} terms · {essential_count} essential (highlighted)",
        )
        y -= 10 * mm

        use_noto = section["lang"] == "FA"
        font_latin = "Noto" if use_noto else "Inter"
        font_bold = "Noto-Bold" if use_noto else "Inter-Bold"
        size = 9.5 if not use_noto else 10

        x = MARGIN
        row_h = 0.0
        gap_y = 2.4 * mm

        for term, essential in section["terms"]:
            pad_x = 2.8 * mm
            pad_y = 1.6 * mm
            font = font_bold if essential else font_latin
            tw = self._term_width(term, font, size)
            chip_w = tw + 2 * pad_x
            chip_h = size + 2 * pad_y + gap_y

            if x + chip_w > PAGE_W - MARGIN:
                x = MARGIN
                y -= row_h + gap_y
                row_h = 0.0

            if y < 24 * mm:
                self.footer()
                self.new_page()
                y = PAGE_H - MARGIN - 6 * mm
                x = MARGIN
                row_h = 0.0
                self.c.setFont("Inter-SemiBold", 11)
                self.c.drawString(MARGIN, y, section["title"] + " (continued)")
                y -= 12 * mm

            chip_w_used, chip_h_used = self._draw_term_chip(
                term, essential, x, y, font_latin, font_bold, size
            )
            row_h = max(row_h, chip_h_used)
            x += chip_w_used

        self.footer()

    def draw_hashtags(self) -> None:
        self.new_page()
        y = PAGE_H - MARGIN
        self.c.setFont("Inter-SemiBold", 20)
        self.c.drawString(MARGIN, y, "Hashtags (optional)")
        y -= 10 * mm
        self.c.setFont("Inter", 10)
        self.c.drawString(MARGIN, y, "High noise — always combine with a human relevance pass.")
        y -= 12 * mm
        tags = [
            ("#architecture", True),
            ("#Midjourney", True),
            ("#AIarchitecture", True),
            ("#ArchViz", True),
            ("#GenerativeAI", True),
            ("#LookX", False),
        ]
        x = MARGIN
        for tag, essential in tags:
            w, _ = self._draw_term_chip(tag, essential, x, y, "Inter", "Inter-Bold", 10)
            x += w
        self.footer()


def main() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = LexiconPDF(OUTPUT)
    doc.draw_cover()
    doc.draw_categories()
    doc.draw_query_page()

    order = [
        "layer_a_architecture",
        "layer_a_genai",
        "layer_b_deskilling",
        "layer_b_soft",
        "layer_b_hard",
        "layer_b_representation",
        "stakeholders",
        "exclusions",
        "persian",
        "german",
    ]
    for key in order:
        doc.draw_term_page(LEXICON[key])
    doc.draw_hashtags()
    doc.save()
    print(f"Wrote {OUTPUT} ({doc.page_num} pages)")


if __name__ == "__main__":
    main()
