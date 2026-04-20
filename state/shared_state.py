from typing import TypedDict, Optional, Dict, Any


class GraphState(TypedDict):
    # 🔹 INPUT
    idea: str

    # 🔹 DERIVED (from parse_idea)
    industry: Optional[str]
    target_audience: Optional[str]
    region: Optional[str]

    # 🔹 AGENT OUTPUTS
    bmc: Optional[Dict[str, Any]]
    market: Optional[Dict[str, Any]]
    competitors: Optional[Dict[str, Any]]
    swot: Optional[Dict[str, Any]]
    ui_code: Optional[str]