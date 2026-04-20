from agents.base_agent import BaseAgent
from agents.prompts.parse_idea_prompt import PARSE_IDEA_PROMPT
from utils.json_parser import safe_parse_json
from utils.llm import call_llm
from state.shared_state import GraphState


class ParseIdeaAgent(BaseAgent):
    """
    Extract structured metadata from a startup idea.
    """

    def run(self, state: GraphState) -> dict:
        idea = state["idea"]

        prompt = PARSE_IDEA_PROMPT.format(idea=idea)

        raw_response = call_llm(prompt)
        # Optional debug
        # print("[ParseIdeaAgent] Raw:", raw_response)

        parsed = safe_parse_json(raw_response)

        # Handle invalid JSON
        if not isinstance(parsed, dict) or "error" in parsed:
            parsed = self._default_output()
        else:
            parsed = self._validate_and_clean(parsed)

        return {
            "industry": parsed["industry"],
            "target_audience": parsed["target_audience"],
            "region": parsed["region"]
        }

    def _validate_and_clean(self, data: dict) -> dict:
        required_fields = ["industry", "target_audience", "region"]

        for field in required_fields:
            value = data.get(field)

            if not isinstance(value, str) or not value.strip():
                data[field] = self._get_default(field)
            else:
                data[field] = value.strip()

        # Ensure region fallback
        if not data.get("region"):
            data["region"] = "Global"

        return data

    def _get_default(self, field: str) -> str:
        defaults = {
            "industry": "Technology",
            "target_audience": "General consumers",
            "region": "Global"
        }
        return defaults.get(field, "Unknown")

    def _default_output(self) -> dict:
        return {
            "industry": "Technology",
            "target_audience": "General consumers",
            "region": "Global"
        }


def parse_idea_node(state: GraphState) -> dict:
    agent = ParseIdeaAgent()
    return agent.run(state)