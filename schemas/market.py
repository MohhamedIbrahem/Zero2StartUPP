from pydantic import BaseModel

class MarketAnalysis(BaseModel):
    tam: str
    sam: str
    som: str
    assumptions: list[str]
    market_trends: list[str]
