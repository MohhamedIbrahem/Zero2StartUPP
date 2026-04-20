from agents.base_agent import BaseAgent
from agents.prompts.competitors_prompt import COMPETITORS_PROMPT
from state.shared_state import GraphState


REQUIRED_FIELDS = [
    "name",
    "url",
    "pricing",
    "value_proposition",
    "strengths",
    "weaknesses"
]


class CompetitorsAgent(BaseAgent):
    """
    Agent responsible for competitor analysis.

    Input: idea, industry, target_audience, region
    Output: {"competitors": {...}}
    """

    def build_prompt(self, state: GraphState) -> str:
        return COMPETITORS_PROMPT.format(
            idea=state["idea"],
            industry=state.get("industry", "Technology"),
            target_audience=state.get("target_audience", "General consumers"),
            region=state.get("region", "Global"),
            search_results="No search results available",
            scrape_results="No scraped data available"
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)

        if isinstance(parsed, dict) and "error" not in parsed:
            validated = self._validate(parsed)
        else:
            validated = self._fallback(state)

        return {
            "competitors": validated
        }

    def _validate(self, data: dict) -> dict:
        # -------- competitors --------
        comps = data.get("competitors", [])

        if not isinstance(comps, list):
            comps = []

        cleaned_comps = []

        for comp in comps:
            if not isinstance(comp, dict):
                continue

            validated_comp = {}

            for field in REQUIRED_FIELDS:
                value = comp.get(field)

                if isinstance(value, str) and value.strip():
                    validated_comp[field] = value.strip()[:150]
                else:
                    validated_comp[field] = f"Unknown {field}"

            # basic URL fix
            if not validated_comp["url"].startswith("http"):
                validated_comp["url"] = "https://example.com"

            cleaned_comps.append(validated_comp)

        # remove duplicates by name
        seen = set()
        unique_comps = []
        for c in cleaned_comps:
            if c["name"] not in seen:
                unique_comps.append(c)
                seen.add(c["name"])

        # enforce limits
        unique_comps = unique_comps[:5]

        while len(unique_comps) < 3:
            unique_comps.append(self._dummy_competitor())

        # -------- market gaps --------
        gaps = data.get("market_gaps", [])

        if not isinstance(gaps, list):
            gaps = []

        cleaned_gaps = []

        for g in gaps:
            if isinstance(g, str) and g.strip():
                cleaned_gaps.append(g.strip()[:150])

        cleaned_gaps = list(dict.fromkeys(cleaned_gaps))[:5]

        while len(cleaned_gaps) < 2:
            cleaned_gaps.append("Unaddressed niche opportunity in the market")

        return {
            "competitors": unique_comps,
            "market_gaps": cleaned_gaps
        }

    def _dummy_competitor(self) -> dict:
        return {
            "name": "Generic Competitor",
            "url": "https://example.com",
            "pricing": "Subscription-based model",
            "value_proposition": "General solution in the market",
            "strengths": "Established presence",
            "weaknesses": "Lack of specialization"
        }

    def _fallback(self, state: GraphState) -> dict:
        return {
            "competitors": [
                self._dummy_competitor(),
                self._dummy_competitor(),
                self._dummy_competitor()
            ],
            "market_gaps": [
                "Lack of personalization in current solutions",
                "No strong focus on target audience needs"
            ]
        }


# LangGraph node
def competitors_node(state: GraphState) -> dict:
    return CompetitorsAgent().run(state)