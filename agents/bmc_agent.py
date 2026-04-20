from agents.base_agent import BaseAgent
from agents.prompts.bmc_prompt import BMC_PROMPT
from state.shared_state import GraphState


BMC_REQUIRED_FIELDS = [
    "customer_segments",
    "value_propositions",
    "channels",
    "customer_relationships",
    "revenue_streams",
    "key_resources",
    "key_activities",
    "key_partners",
    "cost_structure"
]


class BMCAgent(BaseAgent):

    def build_prompt(self, state: GraphState) -> str:
        return BMC_PROMPT.format(
            idea=state["idea"],
            industry=state.get("industry", "Technology"),
            target_audience=state.get("target_audience", "General consumers"),
            region=state.get("region", "Global")
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)

        if isinstance(parsed, dict) and "error" not in parsed:
            validated = self._validate_bmc(parsed)
        else:
            validated = self._get_fallback_bmc(state["idea"])

        return {
            "bmc": validated
        }

    def _validate_bmc(self, data: dict) -> dict:
        validated = {}

        for field in BMC_REQUIRED_FIELDS:
            value = data.get(field)

            if value is None:
                validated[field] = [f"To be determined - {field.replace('_', ' ')}"]
                continue

            if not isinstance(value, list):
                validated[field] = [str(value).strip()[:120]]
                continue

            cleaned = []

            for item in value:
                if isinstance(item, str) and item.strip():
                    cleaned.append(item.strip()[:120])
                elif item is not None and str(item).strip():
                    cleaned.append(str(item).strip()[:120])

            cleaned = list(dict.fromkeys(cleaned))[:5]

            if len(cleaned) == 0:
                cleaned = [f"To be determined - {field.replace('_', ' ')}"]

            while len(cleaned) < 2:
                cleaned.append(f"Additional {field.replace('_', ' ')}")

            validated[field] = cleaned

        return validated

    def _get_fallback_bmc(self, idea: str) -> dict:
        fallback = {}

        for field in BMC_REQUIRED_FIELDS:
            readable = field.replace("_", " ").title()
            fallback[field] = [
                f"{readable} to be analyzed for: {idea[:80]}",
                f"Additional {readable.lower()} analysis needed"
            ]

        return fallback


def bmc_node(state: GraphState) -> dict:
    return BMCAgent().run(state)