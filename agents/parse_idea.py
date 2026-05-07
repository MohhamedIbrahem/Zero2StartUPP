from agents.base_agent import BaseAgent
from agents.prompts.parse_idea_prompt import PARSE_IDEA_PROMPT
from state.shared_state import GraphState
from langsmith import traceable
from schemas.parsed_idea import ParsedIdea

class ParseIdeaAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = ParsedIdea

    def build_prompt(self, state: GraphState) -> str:
        return PARSE_IDEA_PROMPT.format(idea=state["idea"])

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)
        return {"parsed_idea": parsed}

@traceable(name="parse_idea_agent")
def parse_idea_node(state: GraphState) -> dict:
    return ParseIdeaAgent().run(state)