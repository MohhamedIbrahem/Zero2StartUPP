import json
from datetime import datetime
from agents.base_agent import BaseAgent
from state.shared_state import GraphState
from schemas.swot import SWOT
from pydantic import ValidationError

FIX_PROMPT = """You are a Strategic Advisor checking a SWOT Analysis.
The following SWOT data contains duplicate, vague, or misplaced items (e.g. less than 3 words).
Using the cross-agent context provided, please rewrite the vague items into specific, actionable statements, reclassify misplaced items, and ensure each quadrant has at least 2 strong items.
Return a complete, valid JSON matching the schema.

STARTUP IDEA:
{idea}

CROSS-AGENT CONTEXT:
BMC: {bmc}
Market: {market}
Competitors: {competitors}

BROKEN SWOT DATA:
{broken_data}
"""

class SWOTCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = SWOT

    def build_prompt(self, state: GraphState) -> str:
        # Serialize context
        bmc = state.get("bmc")
        market = state.get("market")
        competitors = state.get("competitors")
        
        return FIX_PROMPT.format(
            idea=state["idea"],
            bmc=json.dumps(bmc.model_dump() if bmc else {}),
            market=json.dumps(market.model_dump() if market else {}),
            competitors=json.dumps(competitors.model_dump() if competitors else {}),
            broken_data=json.dumps(self.broken_data, indent=2)
        )

    def run(self, state: GraphState) -> dict:
        data = state.get("swot")
        retries = state.get("swot_retries", 0)
        
        if data is None:
            return self._handle_retry(retries, "swot_data_missing")

        try:
            if isinstance(data, dict):
                validated = SWOT.model_validate(data)
            else:
                validated = SWOT.model_validate(data.model_dump())
        except ValidationError:
            return self._handle_retry(retries, "schema_validation_failed")

        issues = []
        
        quadrants = {
            "strengths": validated.strengths,
            "weaknesses": validated.weaknesses,
            "opportunities": validated.opportunities,
            "threats": validated.threats
        }

        # Check for empty, generic, or duplicate
        all_items = set()
        for q_name, items in quadrants.items():
            if not items or len(items) < 2:
                issues.append(f"too_few_items_in_{q_name}")
            
            for item in items:
                # Check for duplicates
                if item.lower() in all_items:
                    issues.append("duplicate_items")
                all_items.add(item.lower())

                # Check for vague items
                if len(item.split()) < 3:
                    issues.append(f"vague_item_in_{q_name}")

        if not issues:
            return {"swot": validated}

        # Auto-correct using LLM
        self.broken_data = validated.model_dump()
        try:
            fixed_dict = super().run(state)
            fixed_validated = SWOT.model_validate(fixed_dict)
            
            # De-duplicate issue list for reporting
            unique_issues = list(set(issues))
            event = {
                "event": "data_corrected",
                "step": "swot_checker",
                "corrections": [{"issue": issue, "action": "rewrote_with_context"} for issue in unique_issues],
                "timestamp": datetime.now().isoformat()
            }
            return {"swot": fixed_validated, "events": [event]}
        except Exception:
            return self._handle_retry(retries, "auto_correction_failed")

    def _handle_retry(self, retries: int, reason: str) -> dict:
        if retries < 2:
            return {
                "swot_retries": retries + 1, 
                "events": [{
                    "event": "retry_triggered",
                    "step": "swot_checker",
                    "reason": reason,
                    "retry_count": retries + 1,
                    "timestamp": datetime.now().isoformat()
                }]
            }
        else:
            return {
                "swot": self._get_fallback(), 
                "events": [{
                    "event": "fallback_used",
                    "step": "swot_checker",
                    "reason": "max_retries_exceeded",
                    "timestamp": datetime.now().isoformat()
                }]
            }

    def _get_fallback(self) -> SWOT:
        return SWOT(
            strengths=["Innovative approach", "Strong technical foundation"],
            weaknesses=["High initial setup costs", "Lack of brand awareness"],
            opportunities=["Growing demand in the target market", "Potential for strategic partnerships"],
            threats=["Established competitors", "Rapidly changing technology landscape"]
        )

def swot_checker_node(state: GraphState) -> dict:
    return SWOTCheckerAgent().run(state)
