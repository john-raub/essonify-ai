import json, pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # .../libs
DATA = ROOT / "data"

def _load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)

def load_taxonomies():
    return _load_json(DATA / "taxonomies.json")

def load_style_moments():
    return _load_json(DATA / "style_moments.json")

def load_signatures():
    return {
        "Classic Sophisticate": _load_json(DATA / "signatures" / "classic_sophisticate.json"),
        "Bohemian Nomad": _load_json(DATA / "signatures" / "bohemian_nomad.json"),
        "Classic Rebel": _load_json(DATA / "signatures" / "classic_rebel.json"),
    }

def load_inventory():
    return pd.read_csv(DATA / "inventory_seed.csv")
