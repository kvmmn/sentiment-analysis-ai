"""Built-environment vs software/business margin for each post (domain screening layer 3)."""
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

FEAT = Path(__file__).resolve().parents[3] / "_local" / "work" / "run013-multimethod"
BUILT_ENV = ["Architects designing buildings and houses.",
             "An AI rendering of an architectural project with realistic lighting.",
             "Urban design, landscape and sustainable buildings.",
             "A BIM model in Revit for a construction project.",
             "Architecture students in a design studio.",
             "Building performance, daylight and energy simulation for a facade.",
             "The architecture profession and architectural practice."]
SOFTWARE_BUSINESS = ["Software architecture and cloud infrastructure.",
                     "Enterprise AI governance, data platforms and business systems.",
                     "AI agents automating business workflows.",
                     "Leadership, management and business strategy with AI.",
                     "Coding, programming and software engineering.",
                     "Marketing, social media and personal branding."]

if __name__ == "__main__":
    E = np.load(FEAT / "emb_posts.npy")
    m = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    be = (E @ m.encode(BUILT_ENV, normalize_embeddings=True).T).max(1)
    sw = (E @ m.encode(SOFTWARE_BUSINESS, normalize_embeddings=True).T).max(1)
    np.save(FEAT / "be_margin.npy", be - sw)
    print("saved", len(be))
