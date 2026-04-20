from agents.base_agent import BaseAgent
from agents.prompts.swot_prompt import SWOT_PROMPT
from state.shared_state import GraphState


SWOT_KEYS = ["strengths", "weaknesses", "opportunities", "threats"]


class SWOTAgent(BaseAgent):
    """
    Agent responsible for generating SWOT analysis and strategic recommendations.

    Input:
        idea, bmc, market, competitors

    Output:
        {
            "swot": {
                strengths, weaknesses, opportunities, threats,
                recommendations
            }
        }
    """

    def build_prompt(self, state: GraphState) -> str:
        return SWOT_PROMPT.format(
            idea=state["idea"],
            industry=state.get("industry", "Technology"),
            target_audience=state.get("target_audience", "General consumers"),
            region=state.get("region", "Global"),
            bmc=state.get("bmc", {}),
            market=state.get("market", {}),
            competitors=state.get("competitors", {})
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)

        if isinstance(parsed, dict) and "error" not in parsed:
            validated = self._validate(parsed)
        else:
            validated = self._fallback()

        return {
            "swot": validated
        }

    def _validate(self, data: dict) -> dict:
        validated = {}

        # -------- SWOT lists --------
        for key in SWOT_KEYS:
            value = data.get(key)

            if not isinstance(value, list):
                value = []

            cleaned = []

            for item in value:
                if isinstance(item, str) and item.strip():
                    cleaned.append(item.strip()[:150])

            # remove duplicates
            cleaned = list(dict.fromkeys(cleaned))[:5]

            # enforce minimum
            while len(cleaned) < 3:
                cleaned.append(f"Additional {key} insight")

            validated[key] = cleaned

        # -------- recommendations --------
        recs = data.get("recommendations", [])

        if not isinstance(recs, list):
            recs = []

        cleaned_recs = []

        for r in recs:
            if not isinstance(r, dict):
                continue

            priority = r.get("priority", "Medium")
            action = r.get("action", "")
            reasoning = r.get("reasoning", "")

            if priority not in ["High", "Medium", "Low"]:
                priority = "Medium"

            if not isinstance(action, str) or not action.strip():
                action = "Define strategic initiative"

            if not isinstance(reasoning, str) or not reasoning.strip():
                reasoning = "Based on SWOT analysis insights"

            cleaned_recs.append({
                "priority": priority,
                "action": action.strip()[:150],
                "reasoning": reasoning.strip()[:200]
            })

        # limit recommendations
        cleaned_recs = cleaned_recs[:5]

        # ensure minimum recommendations
        while len(cleaned_recs) < 2:
            cleaned_recs.append({
                "priority": "Medium",
                "action": "Explore growth opportunities",
                "reasoning": "General strategic recommendation"
            })

        validated["recommendations"] = cleaned_recs

        return validated

    def _fallback(self) -> dict:
        return {
            "strengths": [
                "Innovative AI-driven concept",
                "Strong alignment with modern user needs",
                "Scalable digital platform"
            ],
            "weaknesses": [
                "High competition in the market",
                "Dependence on user adoption",
                "Initial development costs"
            ],
            "opportunities": [
                "Growing demand for digital fitness",
                "Expansion into corporate wellness",
                "Partnership opportunities"
            ],
            "threats": [
                "Established competitors",
                "Rapid technology changes",
                "Market saturation risk"
            ],
            "recommendations": [
                {
                    "priority": "High",
                    "action": "Differentiate with AI personalization",
                    "reasoning": "Key gap identified in competitors"
                },
                {
                    "priority": "Medium",
                    "action": "Target corporate partnerships",
                    "reasoning": "Untapped market opportunity"
                }
            ]
        }


# LangGraph node
def swot_node(state: GraphState) -> dict:
    return SWOTAgent().run(state)