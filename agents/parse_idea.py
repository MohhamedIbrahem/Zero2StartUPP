from agents.base_agent import BaseAgent
from agents.prompts.parse_idea_prompt import PARSE_IDEA_PROMPT
from state.shared_state import GraphState


class ParseIdeaAgent(BaseAgent):

    def build_prompt(self, state: GraphState) -> str:
        return PARSE_IDEA_PROMPT.format(idea=state["idea"])

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)

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
        fields = ["industry", "target_audience", "region"]

        for f in fields:
            val = data.get(f)
            if not isinstance(val, str) or not val.strip():
                data[f] = self._get_default(f)
            else:
                data[f] = val.strip()

        if not data.get("region"):
            data["region"] = "Global"

        return data

    def _get_default(self, field: str) -> str:
        return {
            "industry": "Technology",
            "target_audience": "General consumers",
            "region": "Global"
        }.get(field, "Unknown")

    def _default_output(self) -> dict:
        return {
            "industry": "Technology",
            "target_audience": "General consumers",
            "region": "Global"
        }


def parse_idea_node(state: GraphState) -> dict:
    return ParseIdeaAgent().run(state)