"""Aspect definitions shared by calibration and analysis.

Two independent detectors per sentence:
  * keyword  — the RQ-grounded ontology of kaveh_analytical_pipeline.py (unchanged)
  * semantic — cosine similarity to prototype sentences, embedded with the same
               all-mpnet-base-v2 model used for the corpus
A sentence carries an aspect in the hybrid detector if either fires.
"""
ASPECTS = ["RQ1_Deskilling", "RQ2a_Creativity", "RQ2b_CognitiveJudgment",
           "RQ3a_TechnicalEnvironmental", "RQ3b_RepresentationBIM"]

ASPECT_FA = {
    "RQ1_Deskilling": "کاهش مهارت و کار",
    "RQ2a_Creativity": "خلاقیت و ایده‌پردازی",
    "RQ2b_CognitiveJudgment": "قضاوت و نظارت شناختی",
    "RQ3a_TechnicalEnvironmental": "فنی و محیطی",
    "RQ3b_RepresentationBIM": "بازنمایی، رندر و BIM",
}

PROTOTYPES = {
    "RQ1_Deskilling": [
        "AI will take away the skills architects used to learn by hand.",
        "Junior architects are losing basic drafting and design skills because AI does the work.",
        "Architects risk being replaced by automation and losing their jobs.",
        "Relying on AI makes designers dependent and erodes their expertise.",
    ],
    "RQ2a_Creativity": [
        "AI helps architects generate creative design concepts and ideas.",
        "Generative AI changes design ideation and the creative process.",
        "AI images threaten originality and lead to homogenized architectural aesthetics.",
        "Who is the author of a design created with AI?",
    ],
    "RQ2b_CognitiveJudgment": [
        "Architects must use critical thinking and judgment to verify what AI produces.",
        "Delegating decisions to AI weakens human judgment and intuition.",
        "AI hallucinations mean a professional must remain accountable for the decision.",
        "Design decisions still require human oversight and reasoning.",
    ],
    "RQ3a_TechnicalEnvironmental": [
        "AI supports energy modeling, daylight and sustainability analysis of buildings.",
        "Machine learning can check building code compliance and structural performance.",
        "AI tools optimize carbon, thermal comfort and environmental performance.",
        "Building physics simulation with artificial intelligence.",
    ],
    "RQ3b_RepresentationBIM": [
        "AI rendering tools turn sketches into photorealistic architectural visualizations.",
        "AI automates BIM modelling, Revit drawings and construction documents.",
        "Parametric design with Grasshopper and Rhino combined with AI.",
        "Generating floor plans and architectural drawings with AI.",
    ],
}

# Chosen in calibrate step (see analyze.py: aspect_calibration in results.json)
SEMANTIC_THRESHOLD = 0.50
