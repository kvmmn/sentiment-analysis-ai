"""
================================================================================
UNIT TESTS: KAVEH'S INDEPENDENT ANALYTICAL PIPELINE
================================================================================
Verifies mathematical correctness of clause valence shifters, context-window
isolation, 2D stance quadrant mapping, and stakeholder inference rules.
================================================================================
"""

import math
import numpy as np
import pandas as pd

from src.analysis.kaveh_analytical_pipeline import (
    score_clause_valence,
    score_aspect_sentiment_windowed,
    compute_2d_discursive_stance,
    classify_stakeholder_multisignal,
    compute_bimodality_coefficient
)

def test_score_clause_valence_basic():
    # Direct positive
    v_pos = score_clause_valence("This tool is innovative and efficient.")
    assert v_pos > 0.0

    # Direct negative
    v_neg = score_clause_valence("This is a severe threat and causes skill loss.")
    assert v_neg < 0.0

def test_score_clause_valence_negation_inversion():
    # "not a threat" should flip negative into positive/neutral
    v_flip = score_clause_valence("AI is not a threat to creative practice.")
    assert v_flip > 0.0

    # "not innovative" should flip positive into negative
    v_neg_flip = score_clause_valence("The output is not innovative or collaborative.")
    assert v_neg_flip < 0.0

def test_score_clause_valence_intensifiers():
    v_normal = score_clause_valence("The model is efficient.")
    v_intense = score_clause_valence("The model is extremely efficient.")
    assert v_intense > v_normal

def test_score_aspect_sentiment_window_isolation():
    text = (
        "We are seeing incredible creativity and innovative ideation with diffusion models. "
        "However, regarding code compliance and structural physics, it remains completely unreliable."
    )
    pol, aspects = score_aspect_sentiment_windowed(text)

    # RQ2a_Creativity should be strongly positive
    assert not math.isnan(aspects["RQ2a_Creativity"])
    assert aspects["RQ2a_Creativity"] > 0.2

    # RQ3a_TechnicalEnvironmental should be negative
    assert not math.isnan(aspects["RQ3a_TechnicalEnvironmental"])
    assert aspects["RQ3a_TechnicalEnvironmental"] < 0.0

    # Unmentioned aspect should be NaN
    assert math.isnan(aspects["RQ3b_RepresentationBIM"])

def test_compute_2d_discursive_stance():
    # Co-pilot agency + positive valence
    text_aug = "AI is our collaborative partner and co-pilot, empowering architects to elevate design."
    ag, vl, quad = compute_2d_discursive_stance(text_aug)
    assert ag > 0.0
    assert vl > 0.0
    assert quad == "Q1: Empowered Augmentation"

    # Autonomous replacement + negative valence
    text_sub = "Autonomous systems will automate and replace drafting, threatening the future of architects with displacement."
    ag2, vl2, quad2 = compute_2d_discursive_stance(text_sub)
    assert ag2 < 0.0
    assert vl2 < 0.0
    assert quad2 == "Q3: Existential Displacement"

def test_classify_stakeholder_multisignal():
    # Signal 1: Academic post-nominal
    row_acad = pd.Series({"author_name": "Dr. Sarah Jenkins", "author_headline": "", "content_cleaned": "Discussing design.", "search_query": ""})
    assert classify_stakeholder_multisignal(row_acad) == "Academic"

    # Signal 2: Practitioner post-nominal
    row_prac = pd.Series({"author_name": "David Miller, AIA", "author_headline": "", "content_cleaned": "Project delivery.", "search_query": ""})
    assert classify_stakeholder_multisignal(row_prac) == "Practitioner"

    # Signal 3: In-text self-id
    row_text_prac = pd.Series({"author_name": "Alex", "author_headline": "", "content_cleaned": "In our firm, our clients expect fast BIM drawings.", "search_query": ""})
    assert classify_stakeholder_multisignal(row_text_prac) == "Practitioner"

    row_text_acad = pd.Series({"author_name": "Elena", "author_headline": "", "content_cleaned": "In the studio, teaching architecture students how to sketch.", "search_query": ""})
    assert classify_stakeholder_multisignal(row_text_acad) == "Academic"

def test_bimodality_coefficient():
    # Uniform bimodal distribution: [-1]*50 + [1]*50
    bimodal_data = pd.Series([-1.0] * 50 + [1.0] * 50)
    bc, skew, kurt = compute_bimodality_coefficient(bimodal_data)
    # Bimodal coefficient for two equal peaks should be near 1.0 (>> 0.555)
    assert bc > 0.8
