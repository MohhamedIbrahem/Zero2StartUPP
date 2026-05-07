from pydantic import BaseModel

class Competitor(BaseModel):
    name: str
    pricing_model: str
    strengths: str
    market_gap: str

class Competitors(BaseModel):
    competitors: list[Competitor]
