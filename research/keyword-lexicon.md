# Keyword Lexicon

Status: **working catalog**, 2026-08-29 (English tables unchanged 2026-08-31). This is the **sentiment / stance coding lexicon**: categorized to match the research questions, sorted inside each category. It is not a literature-validated thesaurus and not permission to collect.

## Keyword systems map (2026-08-31)

Saintiment maintains **three separate instruments** — do not mix them:

| Instrument | File | Role |
| --- | --- | --- |
| Literature retrieval | [keyword-literature-strings.md](keyword-literature-strings.md) | Scopus S-A1, WoS W-A1, supplements — copy-paste protocol |
| Discourse-retrieval catalog | [keyword-discourse-catalog.md](keyword-discourse-catalog.md) | EN/FA/DE platform search terms (not a harvest plan) |
| Sentiment / stance coding | **this file** | Post-sample coding; **sentiment lemmas are DO-NOT-RETRIEVE** |

Host decisions and evaluation map: [keyword-systems.md](keyword-systems.md). Teammate vs published analogues: [keyword-source-identification.md](keyword-source-identification.md).

Use with the [search-scope and storage note](keywords-search-storage.md). Search **architecture context AND generative-AI cue** first. Add a skill category only as a second filter. Do not search sentiment words (*excited*, *hype*, *threat*).

## Map to the project

| Catalog section | Serves | Layer |
| --- | --- | --- |
| 1 Architecture discourse | Every item must sit in this discourse | A — required context |
| 2 Generative AI | Every item must concern GenAI or a named GenAI tool | A — required context |
| 3 Deskilling and labour | RQ1 overarching deskilling talk | B — skill filter |
| 4 Soft skills | RQ2, RQ2a, RQ2b | B — skill filter |
| 5 Hard skills | RQ3, RQ3a, RQ3b | B — skill filter |
| 6 Stakeholders | RQ4 role language | W — coding / optional retrieve |
| 7 Exclusions | Software-architecture and other false positives | X — NOT / exclude code |
| 8 Persian / 9 German | Optional later passes | Same layers; do not mix without a language field |
| 10 Hashtags | X and similar surfaces | High noise |

**Term** is the sort key. **Variants** are spelling, plural, or hyphen forms of the same idea. A product name is a search cue, not a claim that the product causes deskilling.

---

## Core set

Minimum terms for the stated aim: sentiment about **GenAI and deskilling in architectural discourse**, with soft skills, hard skills, and stakeholders. First English pass should be built from this set; the full catalog expands it.

### Core — architecture (A)

architectural · architectural design · architect · architects · architecture firm · architecture student · architecture studio · archviz

### Core — generative AI (A)

AI rendering · ChatGPT · DALL-E · GenAI · generative AI · Midjourney · Stable Diffusion

### Core — RQ1 deskilling (B)

de-skilling · deskilling · replace architects · reskilling · skill loss · upskilling

### Core — RQ2a creativity (B)

authorship · creativity · design thinking

### Core — RQ2b judgment (B)

critical thinking · judgement · judgment · professional judgment

### Core — RQ3a technical / environmental (B)

building performance · environmental design · technical skills

### Core — RQ3b representation / digital (B)

BIM · computational design · hand drawing · rendering · representation

### Core — RQ4 stakeholders (W)

academic · industry leader · practitioner · principal · student

### Core — exclusions (X)

cloud architect · enterprise architecture · software architect · solutions architect

---

## 1. Architecture discourse

### 1.1 Profession and titles

| Term | Variants | Notes |
| --- | --- | --- |
| architect | architects | Collides with software architect; keep an exclusion |
| architect of record | | |
| architectural | | Safer than bare *architecture* |
| architectural design | | Core pair with GenAI |
| architectural designer | | |
| architectural rendering | | Also RQ3b |
| architectural visualization | architectural visualisation | Also RQ3b |
| archviz | ArchViz | Also RQ3b |
| architectural intern | intern architect | |
| associate architect | | |
| chartered architect | | UK / Commonwealth |
| design architect | | |
| design principal | | Also RQ4 |
| intern architect | architectural intern | |
| junior architect | | Also RQ1 pipeline |
| licensed architect | | |
| principal architect | | Also RQ4 |
| project architect | | |
| registered architect | | |
| senior architect | | |
| starchitect | starchitects | Rhetorical; small volume |
| supervising architect | | |

### 1.2 Practice and workplaces

| Term | Variants | Notes |
| --- | --- | --- |
| architectural discourse | | Rare on social posts; useful on ResearchGate |
| architectural office | architecture office | |
| architectural practice | architecture practice | |
| architecture firm | architecture firms | |
| architecture studio | architectural studio | Art-studio noise |
| atelier | | |
| boutique practice | boutique firm | |
| professional practice | | |

### 1.3 Education

| Term | Variants | Notes |
| --- | --- | --- |
| architectural education | architecture education | RQ4 |
| architecture school | architecture schools | |
| architecture student | architecture students | RQ4 |
| BArch | B.Arch | |
| design crit | crit, critique | |
| design jury | review jury | |
| design studio | studio | Weak alone |
| MArch | M.Arch | |
| Part 1 | RIBA Part 1 | UK pathway |
| Part 2 | RIBA Part 2 | |
| Part 3 | RIBA Part 3 | |
| studio culture | | |
| year-out | year out | UK; also RQ4 |

### 1.4 Institutions

| Term | Variants | Notes |
| --- | --- | --- |
| ACSA | | Schools (North America) |
| AIA | | Acronym collisions |
| ARB | Architects Registration Board | UK |
| NAAB | | Accreditation |
| RAIA | Australian Institute of Architects | |
| RAIC | | Canada |
| RIBA | | Also the institute’s own content |
| UIA | | International |

### 1.5 Design process

| Term | Variants | Notes |
| --- | --- | --- |
| as-built | as built | |
| concept design | conceptual design | Overlaps RQ2a |
| construction administration | CA | |
| construction documentation | CD, CDs | |
| design development | DD | |
| feasibility | feasibility study | Broad |
| pre-design | predesign | |
| programming | architectural programming | Software collision |
| schematic design | SD | |
| site analysis | | |

### 1.6 Built-environment adjacent — optional scope

The original sketch is architectural discourse. These terms stay out of the core set until the team includes them.

| Term | Variants | Notes |
| --- | --- | --- |
| building design | | Construction-industry bleed |
| built environment | | Broader than architecture |
| interior architecture | | |
| interior design | | Weaker architecture cue |
| landscape architecture | landscape architect | |
| urban design | | Planning bleed |
| urban planning | city planning | |
| urbanism | | |

---

## 2. Generative AI

### 2.1 Generic names

| Term | Variants | Notes |
| --- | --- | --- |
| AI design | | Very broad |
| AI-aided design | AI aided design | |
| AI-assisted design | AI assisted design | |
| AI-generated | AI generated | |
| artificial intelligence | AI | *AI* alone is too short |
| gen AI | gen-AI | |
| GenAI | | |
| generative AI | generative A.I. | Preferred phrase |
| generative artificial intelligence | | Formal |
| machine learning | ML | Broader than GenAI; flag |

### 2.2 Visual and spatial generation

| Term | Variants | Notes |
| --- | --- | --- |
| AI rendering | AI render, AI-rendered | Strong architecture hit-rate expected |
| AI visualization | AI visualisation | |
| diffusion model | diffusion models | |
| image generation | image generator | Broad |
| text-to-3D | text to 3D | |
| text-to-BIM | text to BIM | Emerging phrase |
| text-to-image | text to image, txt2img | |

### 2.3 Language models and copilots

| Term | Variants | Notes |
| --- | --- | --- |
| ChatGPT | Chat GPT | Needs architecture AND |
| Claude | | Name collisions |
| Copilot | Microsoft Copilot | Software bleed; see exclusions |
| Gemini | Google Gemini | Name collisions |
| GPT | GPT-4, GPT-5 | Too short alone |
| large language model | large language models | |
| LLM | LLMs | Acronym collisions |
| OpenAI | | |
| prompt | prompts | Weak alone |
| prompt engineering | | |
| prompting | | |

### 2.4 Named tools used in design practice

Inclusion means people may name the tool instead of saying *generative AI*.

| Term | Variants | Notes |
| --- | --- | --- |
| Adobe Firefly | Firefly | |
| Autodesk Forma | Forma | *Forma* alone is weak |
| ComfyUI | | Practitioner tooling |
| DALL-E | DALL·E, Dall-E, DALL-E 3 | |
| Finch | Finch3D | Name collisions |
| Flux | | Name collisions |
| Hypar | | |
| Ideogram | | |
| Leonardo AI | Leonardo | |
| LookX | | Architecture-facing; confirm current name before a live search |
| Maket | Maket.ai | |
| Midjourney | MJ | High volume in visual practice |
| mnml | mnml.ai | |
| Runway | Runway ML | Video bleed |
| SketchUp Diffusion | | |
| Snaptrude | | |
| Sora | | Video; optional |
| Spacemaker | | Often discussed with Forma |
| Stable Diffusion | SD | |
| TestFit | | |
| Veras | Chaos Veras | |
| Visoid | | |

### 2.5 Older “generative design” — keep separate

| Term | Variants | Notes |
| --- | --- | --- |
| algorithmic design | | Pre-GenAI computational tradition |
| generative design | | Optimization / CAD sense; do not merge with GenAI counts |
| topology optimization | topology optimisation | |

---

## 3. Deskilling and labour — RQ1

Use only with sections 1 and 2, or as a filter on an already retrieved architecture+GenAI set.

### 3.1 Skill loss and deskilling

| Term | Variants | Notes |
| --- | --- | --- |
| de-skilling | de skilling | |
| deskill | deskilled, deskills | |
| deskilling | | Core lemma |
| dumbing down | dumbed down | Informal |
| skill atrophy | | |
| skill degradation | | |
| skill erosion | | |
| skill loss | loss of skill, lost skills | |
| losing skills | lose skills | |
| unskilled | de-skilled | Ambiguous |

### 3.2 Replacement and automation

| Term | Variants | Notes |
| --- | --- | --- |
| AI will replace | AI won't replace, AI will not replace | Stance in the text; not a sentiment search |
| architect replacement | | |
| automate architecture | automating architecture | |
| automated design | | Also RQ3 |
| automation of design | design automation | |
| cheaper design | cheaper and faster | |
| job displacement | | |
| job loss | jobs lost | Very broad |
| replace architects | replacing architects, replaced architects | |
| redundant | redundancy | Broad |

### 3.3 Training pipeline and craft

| Term | Variants | Notes |
| --- | --- | --- |
| apprenticeship | apprentice | |
| commodification | commoditization | |
| craft | | Ambiguous |
| craftsmanship | craftsperson | |
| fewer juniors | no juniors | |
| junior pipeline | | |
| professional autonomy | | |
| professional expertise | | Also RQ2b |
| tacit knowledge | | Also RQ2b |
| training pipeline | | |

### 3.4 Skill change and the profession’s future

Keep the counter-pole. RQ1 is about the discussion, not only anxiety.

| Term | Variants | Notes |
| --- | --- | --- |
| future of architects | | |
| future of architecture | | Noisy, grandiose |
| future of the profession | future of the professions | |
| future skills | | |
| human in the loop | human-in-the-loop | Also RQ2b |
| new skills | | Weak |
| obsolescence | obsolete skills | |
| reskilling | re-skilling, reskill | |
| skill shift | | |
| skill transformation | | |
| upskilling | up-skilling, upskill | |

---

## 4. Soft skills — RQ2

### 4.1 Creativity and design thinking — RQ2a

| Term | Variants | Notes |
| --- | --- | --- |
| aesthetic | aesthetics | |
| artistic | artistry | |
| authorship | authorial, author | |
| conceptual thinking | | |
| creative process | | |
| creative thinking | | |
| creativity | creative | Very common; needs 1+2 |
| design thinking | Design Thinking | Management-speak bleed |
| idea generation | ideation | |
| imagination | imaginative | |
| innovation | innovative | Noisy |
| inspiration | | Weak |
| originality | original | |
| taste | | Also RQ2b |
| vision | design vision | Weak |

### 4.2 Cognitive skills and judgment — RQ2b

| Term | Variants | Notes |
| --- | --- | --- |
| cognitive skills | cognition | Rare in posts |
| critical judgment | critical judgement | |
| critical thinking | | |
| decision-making | decision making | |
| design evaluation | | |
| design intuition | | |
| design judgment | design judgement | |
| discernment | | |
| evaluation | | Weak |
| expertise | expert | |
| intuition | | Weak alone |
| judgement | | British spelling |
| judgment | | American spelling |
| problem-solving | problem solving | Weak |
| professional judgment | professional judgement | Preferred RQ2b phrase |
| professional responsibility | | |
| reasoning | | |
| spatial reasoning | spatial thinking | |
| wisdom | | Rare |

### 4.3 Other professional soft skills — optional under RQ2

| Term | Variants | Notes |
| --- | --- | --- |
| client communication | | |
| collaboration | collaborative | Weak |
| communication | communication skills | Broad |
| empathy | | |
| leadership | | Broad |
| narrative | | Weak |
| negotiation | | |
| presentation skills | presentation | |
| soft skills | soft-skill | Parent term for RQ2 |
| storytelling | | |
| teamwork | | Weak |

---

## 5. Hard skills — RQ3

### 5.1 Technical and environmental — RQ3a

| Term | Variants | Notes |
| --- | --- | --- |
| accessibility | accessible design | Broad |
| buildability | constructability | |
| building codes | building code | |
| building envelope | envelope | |
| building performance | | |
| building physics | | |
| building regulations | | |
| building science | | |
| carbon | embodied carbon | Weak alone |
| code compliance | | |
| construction detailing | | |
| construction knowledge | | |
| daylighting | daylight analysis | |
| detailing | detail | Also RQ3b |
| energy analysis | | |
| energy modeling | energy modelling | |
| environmental design | | From the original sketch |
| environmental performance | | |
| fire safety | fire protection | |
| hard skills | hard-skill | Parent term for RQ3 |
| HVAC | | |
| LCA | life cycle, life-cycle assessment | |
| materials knowledge | material knowledge, materials | |
| MEP | | |
| net zero | net-zero | Broad |
| passive design | | |
| specification | specifications, spec | |
| structural design | | Engineering bleed |
| sustainability | sustainable design | Very broad |
| technical competence | | |
| technical drawing | | Also RQ3b |
| technical knowledge | | |
| technical skills | | From the original sketch |
| thermal comfort | | |
| working drawings | | Also RQ3b |
| zoning | | Planning bleed |

### 5.2 Representation, digital, computational — RQ3b

| Term | Variants | Notes |
| --- | --- | --- |
| 2D drawing | two-dimensional | |
| 3D modeling | 3D modelling | |
| algorithmic design | | Also 2.5 |
| architectural representation | | |
| CAD | CADD | |
| collage | | |
| computational design | | |
| diagram | diagramming | Weak |
| digital fabrication | | Optional scope |
| digital skills | digital literacy | |
| drafting | draughting | |
| drawing | drawings | Weak alone |
| elevation | elevations | Weak alone |
| hand drawing | hand-drawing, hand-drawn | |
| orthographic | | |
| parametric design | parametric | Pre-GenAI tradition |
| perspective | perspectives | Weak alone |
| post-production | post production | |
| rendering | render, renders | |
| representation | | Philosophical bleed |
| scripting | | Software bleed |
| section | sections | Weak alone |
| sketch | sketching, sketches | |
| visual programming | | |
| visualization | visualisation, viz | |

### 5.3 Software used as skill proxies — RQ3b

| Term | Variants | Notes |
| --- | --- | --- |
| ArchiCAD | Archicad | |
| AutoCAD | | |
| Blender | | Games / general 3D bleed |
| Enscape | | |
| Grasshopper | GH | Insect collisions if unanchored |
| Illustrator | Adobe Illustrator | Weak |
| InDesign | | Weak |
| Lumion | | |
| Photoshop | PS | Weak |
| Revit | | |
| Rhino | Rhinoceros, Rhino 3D | |
| SketchUp | | |
| Twinmotion | | |
| Unreal Engine | Unreal | Games bleed |
| V-Ray | Vray, VRay | |
| Vectorworks | | |

---

## 6. Stakeholders — RQ4

Do not infer a role from a name or photo. Prefer self-identification in the text or a consented profile field. Overlap and *unknown* are allowed.

### 6.1 Practitioners

| Term | Variants | Notes |
| --- | --- | --- |
| practitioner | practitioners | |
| practicing architect | practising architect | |
| professional practice | | Also 1.2 |

### 6.2 Academics

| Term | Variants | Notes |
| --- | --- | --- |
| academic | academics | |
| educator | educators | |
| faculty | | |
| lecturer | lecturers | |
| professor | professors, assistant professor, associate professor | |
| researcher | researchers | Broad |
| scholar | scholars | |
| studio tutor | studio instructor | |
| Dean | head of school | |

### 6.3 Students and early career

| Term | Variants | Notes |
| --- | --- | --- |
| architecture student | architecture students | |
| early career | early-career | |
| graduate student | postgraduate | |
| intern | internship | Also practitioner path |
| student | students | Weak alone |
| undergraduate | undergrad | |
| year-out | year out | |

### 6.4 Industry leaders and practice leads

| Term | Variants | Notes |
| --- | --- | --- |
| director | practice director, managing director | |
| firm owner | founder, co-founder | |
| industry leader | industry leaders | |
| partner | equity partner | |
| principal | principals | |
| thought leader | | Marketing; weak evidence |

### 6.5 Adjacent — usually not RQ4 as written

| Term | Variants | Notes |
| --- | --- | --- |
| client | clients | |
| critic | critics | |
| developer | developers | Real-estate / software collision |
| journalist | | |

---

## 7. Exclusions

Code matches `exclude`. Do not silently delete them from a raw batch if the platform returned them.

| Term | Variants | Why |
| --- | --- | --- |
| application architect | | IT |
| AWS architect | Azure architect | Cloud certifications |
| chip architecture | | Hardware |
| cloud architect | | IT |
| computer architecture | | Hardware |
| CPU architecture | | Hardware |
| data architect | | IT |
| enterprise architect | enterprise architecture | IT |
| GitHub Copilot | | Usually software engineering |
| information architect | IA | UX / IT |
| instruction set | ISA | Hardware |
| IT architect | | IT |
| microservices | | Software |
| naval architect | naval architecture | Different profession |
| network architect | | IT |
| Salesforce architect | | IT |
| security architect | | IT |
| software architect | software architecture | Primary false positive |
| solution architect | solutions architect | IT |
| systems architect | system architect | IT |
| TOGAF | Zachman | Enterprise-architecture frameworks |

---

## 8. Persian — optional second pass

Same categories as English. **Not selected** for the first pass.

### 8.1 Architecture (A)

آتلیه معماری · آموزش معماری · دفتر معماری · دانشجوی معماری · طراحی معماری · معمار · معماران · معماری

### 8.2 Generative AI (A)

چت‌جی‌پی‌تی · چت جی پی تی · رندر با هوش مصنوعی · طراحی با هوش مصنوعی · میدجرنی · هوش مصنوعی · هوش مصنوعی در معماری · هوش مصنوعی مولد

### 8.3 RQ1 deskilling (B)

اتوماسیون طراحی · از دست رفتن مهارت · بیکاری معماران · جایگزینی معمار · زوال مهارت · کاهش مهارت · مهارت‌زدایی

### 8.4 RQ2 soft skills (B)

تفکر طراحی · خلاقیت · سلیقه · قضاوت حرفه‌ای · مهارت نرم

### 8.5 RQ3 hard skills (B)

بیم · جزئیات اجرایی · دانش ساخت · دست‌رسمی · اسکیس · طراحی پارامتریک · طراحی محیطی · طراحی محاسباتی · ترسیم · مهارت سخت · مهارت فنی · مدل‌سازی · مقررات ملی ساختمان · نقشه‌کشی · ویژوالایز · رندر معماری

### 8.6 RQ4 stakeholders (W)

آکادمیک · حرفه‌مند · دانشجو · دانشگاهی · کارفرما · مدیر دفتر

---

## 9. German — optional second pass

**Not selected** for the first pass.

### 9.1 Architecture (A)

Architekt · Architekten · Architektin · Architektur · Architekturbüro · Architekturstudium

### 9.2 Generative AI (A)

generative KI · KI-generiert · Künstliche Intelligenz · Midjourney

### 9.3 RQ1 deskilling (B)

Dequalifizierung · Entqualifizierung · Kompetenzverlust

### 9.4 RQ2 soft skills (B)

Design Thinking · fachliches Urteil · Kreativität · Urteilsvermögen

### 9.5 RQ3 hard skills (B)

BIM · Darstellung · Handzeichnung · technische Fähigkeiten · umweltgerechtes Entwerfen · Visualisierung

---

## 10. Hashtags

Always pair with a human relevance pass. Sorted.

#AIarchitecture · #AIA · #ArchViz · #architect · #architecture · #architecturestudent · #GenerativeAI · #LookX · #Midjourney · #RIBA · #StableDiffusion

---

## Counts

| Block | Rows / items |
| --- | --- |
| Core set (unique lemmas) | 40 |
| 1 Architecture | 66 |
| 2 Generative AI | 48 |
| 3 RQ1 deskilling | 40 |
| 4 RQ2 soft skills | 43 |
| 5 RQ3 hard skills | 68 |
| 6 RQ4 stakeholders | 28 |
| 7 Exclusions | 21 |
| 8 Persian | 42 |
| 9 German | 20 |
| 10 Hashtags | 11 |

English catalog (sections 1–7, including core overlap) is the first-pass working list. Persian and German are expansion lists only.

## Team edit

Strike or add rows in place. Freeze **query version 1** from the core set after that pass. Do not grow a corpus until a source is permitted and a relevance pilot exists.
