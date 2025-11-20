from fastapi import FastAPI
from libs.engine_core.rules import load_style_moments, load_signatures
from libs.models.avatar import AvatarStateRequest

app = FastAPI(title="Essonify Avatar API")

style_moments = load_style_moments()
signatures = load_signatures()

@app.get("/")
def health():
    return {"ok": True, "service": "avatar"}

@app.get("/meta")
def meta():
    return {
        "signatures": list(signatures.keys()),
        "moments": list(style_moments.keys())
    }

@app.post("/state")
def state(req: AvatarStateRequest):
    sig = signatures.get(req.signature)
    if not sig:
        return {"error":"Unknown signature"}
    moment = style_moments.get(req.style_moment)
    if not moment:
        return {"error":"Unknown style_moment"}

    # MVP avatar state (text-first; hook into stylist later)
    color_profile = {
        "palette": req.palette or "Latte Warm",
        "base_colors": sig.get("palette_core", [])[:3],
        "accents": sig.get("palette_accents", [])[:2]
    }
    emotion = {
        "state": "confident" if req.style_moment == "Boardroom Pitch" else "easy",
        "expression": "soft smile" if req.style_moment != "Boardroom Pitch" else "focused",
        "posture": "upright" if req.style_moment == "Boardroom Pitch" else "relaxed"
    }
    style = {
        "signature": req.signature,
        "outfit_ref": "from stylist (future wire)",
        "hair_style": "low polished bun" if req.presentation=="Femme" else "neat side part",
        "makeup": "soft matte neutrals" if req.presentation=="Femme" else None
    }

    return {
        "avatar": {
            "identity": {"presentation": req.presentation, "season": req.season},
            "color_profile": color_profile,
            "style": style,
            "moment": {"context": req.style_moment, "formality": moment["formality"]},
            "emotion": emotion
        }
    }
