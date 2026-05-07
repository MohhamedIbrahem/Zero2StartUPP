import json
import re
from datetime import datetime
from agents.base_agent import BaseAgent
from state.shared_state import GraphState
from schemas.market import MarketAnalysis
from pydantic import ValidationError

FIX_PROMPT = """You are a Market Analyst checking Market Analysis data.
The following data has issues:
{issues}

Based on the startup idea, fix these issues and return a complete, valid JSON matching the schema.
If there is a math/hierarchy violation (e.g. TAM < SAM or SAM < SOM), adjust the numbers so they are mathematically logical (TAM > SAM > SOM) while preserving the reasoning in the assumptions. Make sure numbers use standard suffixes (T, B, M, K).

STARTUP IDEA:
{idea}

BROKEN DATA:
{broken_data}
"""

class MarketCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = MarketAnalysis

    def build_prompt(self, state: GraphState) -> str:
        return FIX_PROMPT.format(
            idea=state["idea"],
            issues=json.dumps(self.current_issues, indent=2),
            broken_data=json.dumps(self.broken_data, indent=2)
        )

    def _parse_val(self, v: str) -> float:
        v = v.upper().replace(",", "").replace("$", "")
        match = re.search(r"(\d+(\.\d+)?)([TMBK]?)", v)
        if not match: return 0
        number = float(match.group(1))
        suffix = match.group(3)
        if suffix == "T": return number * 1e12
        if suffix == "B": return number * 1e9
        if suffix == "M": return number * 1e6
        if suffix == "K": return number * 1e3
        return number

    def _format_val(self, v: float) -> str:
        if v >= 1e12: 
            val = v/1e12
            return f"${val:g}T" if val.is_integer() else f"${val:.1f}T"
        if v >= 1e9: 
            val = v/1e9
            return f"${val:g}B" if val.is_integer() else f"${val:.1f}B"
        if v >= 1e6: 
            val = v/1e6
            return f"${val:g}M" if val.is_integer() else f"${val:.1f}M"
        if v >= 1e3: 
            val = v/1e3
            return f"${val:g}K" if val.is_integer() else f"${val:.1f}K"
        return f"${v:g}"

    def run(self, state: GraphState) -> dict:
        data = state.get("market")
        retries = state.get("market_retries", 0)
        
        if data is None:
            return self._handle_retry(retries, "market_data_missing")

        try:
            if isinstance(data, dict):
                validated = MarketAnalysis.model_validate(data)
            else:
                validated = MarketAnalysis.model_validate(data.model_dump())
        except ValidationError:
            return self._handle_retry(retries, "schema_validation_failed")

        issues = []
        corrections = []

        # 1. Math check
        tam = self._parse_val(validated.tam)
        sam = self._parse_val(validated.sam)
        som = self._parse_val(validated.som)

        if tam < sam or sam < som or tam == 0:
            issues.append(f"hierarchy_violated: Evaluated as TAM={tam}, SAM={sam}, SOM={som}. TAM must be > SAM, and SAM must be > SOM. Currently this is False.")

        # 2. Check for missing lists
        if not validated.assumptions:
            issues.append("missing_assumptions")
        if not validated.market_trends:
            issues.append("missing_market_trends")

        # 3. Check for raw unformatted floating point artifacts in the strings
        # We can detect if they don't have suffixes and are just weird floats
        if not re.search(r"[TMBK]", validated.tam.upper()) and "." in validated.tam:
            issues.append(f"formatting_artifact_in_tam: {validated.tam} lacks magnitude suffix.")
        
        # Format the values nicely just in case they are valid but slightly ugly (e.g. $1.50B -> $1.5B)
        # But only if there are no math issues, to avoid hiding the math issue
        if not issues:
            validated.tam = self._format_val(tam)
            validated.sam = self._format_val(sam)
            validated.som = self._format_val(som)
            return {"market": validated}

        # Auto-correct using LLM
        self.broken_data = validated.model_dump()
        self.current_issues = issues
        try:
            fixed_dict = super().run(state)
            fixed_validated = MarketAnalysis.model_validate(fixed_dict)
            
            # Re-format just in case the LLM returned weird floats
            fixed_tam = self._parse_val(fixed_validated.tam)
            fixed_sam = self._parse_val(fixed_validated.sam)
            fixed_som = self._parse_val(fixed_validated.som)
            
            fixed_validated.tam = self._format_val(fixed_tam)
            fixed_validated.sam = self._format_val(fixed_sam)
            fixed_validated.som = self._format_val(fixed_som)
            
            event = {
                "event": "data_corrected",
                "step": "market_checker",
                "corrections": [{"issue": issue, "action": "rewrote_with_context"} for issue in issues],
                "timestamp": datetime.now().isoformat()
            }
            return {"market": fixed_validated, "events": [event]}
        except Exception:
            return self._handle_retry(retries, "auto_correction_failed")

    def _handle_retry(self, retries: int, reason: str) -> dict:
        if retries < 2:
            return {
                "market_retries": retries + 1, 
                "events": [{
                    "event": "retry_triggered",
                    "step": "market_checker",
                    "reason": reason,
                    "retry_count": retries + 1,
                    "timestamp": datetime.now().isoformat()
                }]
            }
        else:
            return {
                "market": self._get_fallback(), 
                "events": [{
                    "event": "fallback_used",
                    "step": "market_checker",
                    "reason": "max_retries_exceeded",
                    "timestamp": datetime.now().isoformat()
                }]
            }

    def _get_fallback(self) -> MarketAnalysis:
        return MarketAnalysis(
            tam="$10B",
            sam="$1B",
            som="$100M",
            assumptions=["Fallback estimate based on generic industry benchmarks"],
            market_trends=["Digital transformation"]
        )

def market_checker_node(state: GraphState) -> dict:
    return MarketCheckerAgent().run(state)
