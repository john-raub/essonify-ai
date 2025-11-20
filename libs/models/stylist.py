from pydantic import BaseModel

class RecommendRequest(BaseModel):
    signature: str
    style_moment: str
    temp_f: float = 68.0
    precip: bool = False
    budget_tier: str | None = None
