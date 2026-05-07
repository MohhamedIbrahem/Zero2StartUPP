from typing import TypedDict, Optional, Annotated
import operator
from schemas.parsed_idea import ParsedIdea
from schemas.bmc import BMC
from schemas.market import MarketAnalysis
from schemas.competitors import Competitors
from schemas.swot import SWOT

class GraphState(TypedDict, total=False):
    # 🔹 INPUT
    idea: str
    run_id: str

    # 🔹 DERIVED (from parse_idea)
    parsed_idea: Optional[ParsedIdea]

    # 🔹 AGENT OUTPUTS
    bmc: Optional[BMC]
    market: Optional[MarketAnalysis]
    competitors: Optional[Competitors]
    swot: Optional[SWOT]

    # 🔹 SSE Events
    events: Annotated[list[dict], operator.add]

    # 🔹 Retries Tracking
    bmc_retries: int
    market_retries: int
    competitors_retries: int
    swot_retries: int