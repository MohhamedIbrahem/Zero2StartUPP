from agents.base_agent import BaseAgent
from agents.prompts.swot_prompt import SWOT_PROMPT
from state.shared_state import GraphState
from schemas.swot import SWOT

class SWOTAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = SWOT

    def build_prompt(self, state: GraphState) -> str:
        parsed_idea = state.get("parsed_idea") or {}
        industry = parsed_idea.get("industry", "Technology") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "industry", "Technology")
        region = parsed_idea.get("region", "Global") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "region", "Global")
        target_audience = parsed_idea.get("target_audience", "General consumers") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "target_audience", "General consumers")

        return SWOT_PROMPT.format(
            idea=state["idea"],
            industry=industry,
            target_audience=target_audience,
            region=region,
            bmc=state.get("bmc", {}),
            market=state.get("market", {}),
            competitors=state.get("competitors", {})
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)
        return {"swot": parsed}

def swot_node(state: GraphState) -> dict:
    return SWOTAgent().run(state)