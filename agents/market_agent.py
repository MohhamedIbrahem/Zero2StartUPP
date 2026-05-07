from agents.base_agent import BaseAgent
from agents.prompts.market_prompt import MARKET_PROMPT
from state.shared_state import GraphState
from tools.search_tools import tavily_search
from schemas.market import MarketAnalysis

class MarketAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = MarketAnalysis

    def build_prompt(self, state: GraphState) -> str:
        parsed_idea = state.get("parsed_idea") or {}
        industry = parsed_idea.get("industry", "Technology") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "industry", "Technology")
        region = parsed_idea.get("region", "Global") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "region", "Global")
        target_audience = parsed_idea.get("target_audience", "General consumers") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "target_audience", "General consumers")

        query = f"market size {industry} {region} statistics TAM SAM SOM"
        search_results = tavily_search(query)

        return MARKET_PROMPT.format(
            idea=state["idea"],
            industry=industry,
            target_audience=target_audience,
            region=region,
            search_results=search_results
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)
        return {"market": parsed}

def market_node(state: GraphState) -> dict:
    return MarketAgent().run(state)