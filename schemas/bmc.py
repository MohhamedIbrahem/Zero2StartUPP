from pydantic import BaseModel

class BMC(BaseModel):
    value_proposition: str
    customer_segments: str
    channels: str
    customer_relationships: str
    revenue_streams: str
    key_resources: str
    key_activities: str
    key_partners: str
    cost_structure: str
