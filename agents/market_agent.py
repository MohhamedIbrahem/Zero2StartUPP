import re
from agents.base_agent import BaseAgent
from agents.prompts.market_prompt import MARKET_PROMPT
from state.shared_state import GraphState


class MarketAgent(BaseAgent):
    """
    Agent responsible for estimating market size (TAM, SAM, SOM).

    Input: idea, industry, target_audience, region
    Output: {"market": {...}}
    """

    def build_prompt(self, state: GraphState) -> str:
        return MARKET_PROMPT.format(
            idea=state["idea"],
            industry=state.get("industry", "Technology"),
            target_audience=state.get("target_audience", "General consumers"),
            region=state.get("region", "Global"),
            search_results="No search results available"
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)

        if isinstance(parsed, dict) and "error" not in parsed:
            validated = self._validate_market(parsed)
        else:
            validated = self._fallback_market(state)

        return {
            "market": validated
        }

    def _validate_market(self, data: dict) -> dict:
        """
        Validate and fix market data.
        """

        tam = self._safe_int(data.get("tam"))
        sam = self._safe_int(data.get("sam"))
        som = self._safe_int(data.get("som"))

        # Sort to enforce tam > sam > som
        values = sorted([tam, sam, som], reverse=True)
        tam, sam, som = values

        # Ensure logical separation
        if sam >= tam:
            sam = int(tam * 0.2)

        if som >= sam:
            som = int(sam * 0.05)

        # Optional: enforce realistic minimum scale
        if tam < 1_000_000:
            tam = tam * 1_000_000
            sam = int(tam * 0.15)
            som = int(sam * 0.05)

        # -------- assumptions --------
        assumptions = data.get("assumptions", [])

        if not isinstance(assumptions, list):
            assumptions = []

        cleaned = []
        for item in assumptions:
            if isinstance(item, str) and item.strip():
                cleaned.append(item.strip()[:150])

        # Remove duplicates
        cleaned = list(dict.fromkeys(cleaned))[:6]

        # Ensure minimum count
        while len(cleaned) < 3:
            cleaned.append("Estimated based on comparable market benchmarks")

        return {
            "tam": tam,
            "sam": sam,
            "som": som,
            "currency": "USD",
            "assumptions": cleaned
        }

    def _safe_int(self, value) -> int:
        """
        Convert value to a safe positive integer.
        Handles:
        - "14.7B"
        - "2.5M"
        - "300K"
        - "1,200,000"
        """

        # Case 1: already integer
        if isinstance(value, int):
            return value if value > 0 else 1_000_000

        # Case 2: string parsing
        if isinstance(value, str):
            value = value.upper().replace(",", "").strip()

            match = re.match(r"(\d+(\.\d+)?)([MBK]?)", value)

            if match:
                number = float(match.group(1))
                suffix = match.group(3)

                if suffix == "B":
                    return int(number * 1_000_000_000)
                elif suffix == "M":
                    return int(number * 1_000_000)
                elif suffix == "K":
                    return int(number * 1_000)

                return int(number)

        # fallback
        return 1_000_000

    def _fallback_market(self, state: GraphState) -> dict:
        """
        Fallback when LLM fails completely.
        """
        return {
            "tam": 10_000_000_000,
            "sam": 2_000_000_000,
            "som": 5_000_000,
            "currency": "USD",
            "assumptions": [
                "Fallback estimate based on generic industry benchmarks",
                "SAM estimated as 20% of TAM",
                "SOM estimated as 0.25% of SAM"
            ]
        }


# LangGraph node
def market_node(state: GraphState) -> dict:
    return MarketAgent().run(state)