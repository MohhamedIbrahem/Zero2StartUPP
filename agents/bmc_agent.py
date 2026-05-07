from agents.base_agent import BaseAgent
from agents.prompts.bmc_prompt import BMC_PROMPT
from state.shared_state import GraphState
from schemas.bmc import BMC

class BMCAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = BMC

    def build_prompt(self, state: GraphState) -> str:
        parsed_idea = state.get("parsed_idea") or {}
        industry = parsed_idea.get("industry", "Technology") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "industry", "Technology")
        target_audience = parsed_idea.get("target_audience", "General consumers") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "target_audience", "General consumers")
        region = parsed_idea.get("region", "Global") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "region", "Global")

        return BMC_PROMPT.format(
            idea=state["idea"],
            industry=industry,
            target_audience=target_audience,
            region=region
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)
        return {"bmc": parsed}

def bmc_node(state: GraphState) -> dict:
    return BMCAgent().run(state)