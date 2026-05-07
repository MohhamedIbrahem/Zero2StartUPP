import json
from datetime import datetime
from agents.base_agent import BaseAgent
from state.shared_state import GraphState
from schemas.bmc import BMC
from pydantic import ValidationError

FIX_PROMPT = """You are an expert business analyst checking a Business Model Canvas.
The following BMC data contains empty fields, placeholder text, or missing sections.
Using the original startup idea, please fill in the missing/broken parts and return a complete, valid BMC.

STARTUP IDEA:
{idea}

BROKEN BMC DATA:
{broken_data}
"""

class BMCCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = BMC

    def build_prompt(self, state: GraphState) -> str:
        # We only call build_prompt if we need the LLM to fix it
        return FIX_PROMPT.format(
            idea=state["idea"],
            broken_data=json.dumps(self.broken_data, indent=2)
        )

    def run(self, state: GraphState) -> dict:
        data = state.get("bmc")
        retries = state.get("bmc_retries", 0)
        
        # 1. Check if data is completely missing or structurally unrecoverable
        if data is None:
            return self._handle_retry(retries, "bmc_data_missing")

        try:
            if isinstance(data, dict):
                validated = BMC.model_validate(data)
            else:
                validated = BMC.model_validate(data.model_dump())
        except ValidationError as e:
            return self._handle_retry(retries, f"schema_validation_failed")

        # 2. Check for empty strings or placeholders
        broken_fields = []
        for field, value in validated.model_dump().items():
            if not value or value.strip() in ["", "...", "TBD", "N/A", "fill in", "null", "None"]:
                broken_fields.append(field)

        if not broken_fields:
            # Everything is perfect
            return {"bmc": validated}

        # 3. Auto-correct using LLM
        self.broken_data = validated.model_dump()
        try:
            fixed_dict = super().run(state)
            fixed_validated = BMC.model_validate(fixed_dict)
            
            event = {
                "event": "data_corrected",
                "step": "bmc_checker",
                "corrections": [{"field": f, "issue": "empty_or_placeholder", "action": "rewrote_with_context"} for f in broken_fields],
                "timestamp": datetime.now().isoformat()
            }
            return {"bmc": fixed_validated, "events": [event]}
        except Exception:
            # If LLM fix fails, trigger retry
            return self._handle_retry(retries, "auto_correction_failed")

    def _handle_retry(self, retries: int, reason: str) -> dict:
        if retries < 2:
            event = {
                "event": "retry_triggered",
                "step": "bmc_checker",
                "reason": reason,
                "retry_count": retries + 1,
                "timestamp": datetime.now().isoformat()
            }
            return {"bmc_retries": retries + 1, "events": [event]}
        else:
            # Fallback
            event = {
                "event": "fallback_used",
                "step": "bmc_checker",
                "reason": "max_retries_exceeded",
                "timestamp": datetime.now().isoformat()
            }
            return {"bmc": self._get_fallback(), "events": [event]}

    def _get_fallback(self) -> BMC:
        return BMC(
            value_proposition="To be analyzed",
            customer_segments="To be analyzed",
            channels="To be analyzed",
            customer_relationships="To be analyzed",
            revenue_streams="To be analyzed",
            key_resources="To be analyzed",
            key_activities="To be analyzed",
            key_partners="To be analyzed",
            cost_structure="To be analyzed"
        )

def bmc_checker_node(state: GraphState) -> dict:
    return BMCCheckerAgent().run(state)
