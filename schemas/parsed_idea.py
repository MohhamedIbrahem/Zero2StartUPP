from pydantic import BaseModel

class ParsedIdea(BaseModel):
    industry: str
    target_audience: str
    region: str
