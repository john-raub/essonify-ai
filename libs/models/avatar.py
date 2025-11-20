from pydantic import BaseModel

class AvatarStateRequest(BaseModel):
    signature: str
    style_moment: str
    palette: str | None = None      # e.g., "Latte Warm"
    presentation: str | None = "Femme"  # "Femme" or "Masc"
    season: str | None = "Spring"       # Spring/Summer/Fall/Winter
