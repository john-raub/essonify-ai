from fastapi import FastAPI
from libs.engine_core.rules import load_taxonomies, load_style_moments, load_signatures, load_inventory
from libs.models.stylist import RecommendRequest

app = FastAPI(title="Essonify Stylist API")

# Load once
taxonomies = load_taxonomies()
style_moments = load_style_moments()
signatures = load_signatures()
inventory = load_inventory()

@app.get("/")
def health():
    return {"ok": True, "service": "stylist"}

@app.get("/meta")
def meta():
    return {
        "signatures": list(signatures.keys()),
        "moments": list(style_moments.keys()),
        "inventory_rows": len(inventory)
    }

@app.post("/recommend")
def recommend(req: RecommendRequest):
    sig = signatures.get(req.signature)
    if not sig:
        return {"error":"Unknown signature"}
    moment = style_moments.get(req.style_moment)
    if not moment:
        return {"error":"Unknown style_moment"}

    # naive gates (formality + optional budget tier)
    df = inventory.copy()
    df = df[(df["formality_min"] <= moment["formality"]) & (df["formality_max"] >= moment["formality"])]
    if req.budget_tier:
        df = df[df["price_tier"] == req.budget_tier]

    # simple scoring: core palette color match + signature keyword in tags
    core_colors = set([c for c in sig.get("palette_core", []) if isinstance(c, str)])
    df["color_match"] = df["color"].apply(lambda c: 1 if c in core_colors else 0)
    key = req.signature.lower().split()[0]  # 'classic'/'bohemian'
    df["sig_match"] = df["tags"].fillna("").str.contains(key, case=False).astype(int)
    df["score"] = df["color_match"] + df["sig_match"]

    top = df.sort_values("score", ascending=False).head(5)
    return {
        "signature": req.signature,
        "style_moment": req.style_moment,
        "outfits": [
            {
                "item_id": r["id"],
                "type": r["type"],
                "subtype": r["subtype"],
                "color": r["color"],
                "fabric": r["fabric"],
                "score": float(r["score"])
            } for _, r in top.iterrows()
        ],
        "note": "MVP logic—replace with rule engine later."
    }
