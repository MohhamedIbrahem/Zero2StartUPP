import json
from datetime import datetime
from agents.base_agent import BaseAgent
from state.shared_state import GraphState
from schemas.competitors import Competitors, Competitor
from pydantic import ValidationError
from utils.json_parser import safe_parse_json

FIX_PROMPT = """You are a Market Analyst checking Competitor Analysis data.
The following data has issues: missing fields, too few competitors, duplicates, or IRRELEVANT competitors. 
Based on the startup idea, fix these issues. If the competitors are irrelevant (e.g. delivery apps instead of actual restaurants), REPLACE them with true direct competitors.
Return a complete, valid JSON matching the schema with exactly 3 unique and plausible competitors.

STARTUP IDEA:
{idea}

ISSUES FOUND:
{issues}

BROKEN DATA:
{broken_data}
"""

class CompetitorsCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = Competitors

    def build_prompt(self, state: GraphState) -> str:
        return FIX_PROMPT.format(
            idea=state["idea"],
            issues=json.dumps(self.current_issues, indent=2),
            broken_data=json.dumps(self.broken_data, indent=2)
        )

    def run(self, state: GraphState) -> dict:
        data = state.get("competitors")
        retries = state.get("competitors_retries", 0)
        
        if data is None:
            return self._handle_retry(retries, "competitors_data_missing")

        try:
            if isinstance(data, dict):
                validated = Competitors.model_validate(data)
            else:
                validated = Competitors.model_validate(data.model_dump())
        except ValidationError:
            return self._handle_retry(retries, "schema_validation_failed")

        issues = []
        # Check for duplicates
        names = set()
        has_duplicates = False
        for c in validated.competitors:
            if c.name.lower() in names:
                has_duplicates = True
            names.add(c.name.lower())

        if has_duplicates:
            issues.append("duplicate_competitors")

        # Check for length
        if len(validated.competitors) < 3:
            issues.append("too_few_competitors")

        # Check for empty fields or generic names
        has_empty_or_generic = False
        for c in validated.competitors:
            if not c.name or c.name in ["Competitor A", "Company X", "Generic Competitor"]:
                has_empty_or_generic = True
            if not c.pricing_model or not c.strengths or not c.market_gap:
                has_empty_or_generic = True

        if has_empty_or_generic:
            issues.append("empty_or_generic_fields")

        # Check Relevance using LLM
        competitor_names = [c.name for c in validated.competitors]
        relevance_prompt = f"""You are a relevance checker.
Startup Idea: {state['idea']}
Competitors provided: {competitor_names}

Are these competitors DIRECTLY competing in the exact same market space as the startup?
For example, if the startup is a specific type of restaurant, delivery apps (like UberEats, Talabat) or grocery stores are NOT direct competitors. Other restaurants of the same type ARE.

Return ONLY a JSON object: {{"is_relevant": true or false, "reason": "explanation of why they are or are not relevant"}}
"""
        try:
            relevance_res = self.llm.generate(relevance_prompt)
            relevance_data = safe_parse_json(relevance_res)
            if relevance_data and relevance_data.get("is_relevant") is False:
                issues.append(f"irrelevant_competitors: {relevance_data.get('reason')}")
        except Exception:
            pass # If relevance check fails, we proceed with other checks

        if not issues:
            return {"competitors": validated}

        # Auto-correct using LLM
        self.broken_data = validated.model_dump()
        self.current_issues = issues
        try:
            fixed_dict = super().run(state)
            fixed_validated = Competitors.model_validate(fixed_dict)
            
            event = {
                "event": "data_corrected",
                "step": "competitors_checker",
                "corrections": [{"issue": issue, "action": "rewrote_with_context"} for issue in issues],
                "timestamp": datetime.now().isoformat()
            }
            return {"competitors": fixed_validated, "events": [event]}
        except Exception:
            return self._handle_retry(retries, "auto_correction_failed")

    def _handle_retry(self, retries: int, reason: str) -> dict:
        if retries < 2:
            return {
                "competitors_retries": retries + 1, 
                "events": [{
                    "event": "retry_triggered",
                    "step": "competitors_checker",
                    "reason": reason,
                    "retry_count": retries + 1,
                    "timestamp": datetime.now().isoformat()
                }]
            }
        else:
            return {
                "competitors": self._get_fallback(), 
                "events": [{
                    "event": "fallback_used",
                    "step": "competitors_checker",
                    "reason": "max_retries_exceeded",
                    "timestamp": datetime.now().isoformat()
                }]
            }

    def _get_fallback(self) -> Competitors:
        return Competitors(
            competitors=[
                Competitor(
                    name="Generic Competitor 1",
                    pricing_model="Subscription",
                    strengths="Established presence",
                    market_gap="Lack of personalization"
                ),
                Competitor(
                    name="Generic Competitor 2",
                    pricing_model="Freemium",
                    strengths="Large user base",
                    market_gap="Poor customer support"
                ),
                Competitor(
                    name="Generic Competitor 3",
                    pricing_model="One-time",
                    strengths="Simple interface",
                    market_gap="Outdated features"
                )
            ]
        )

def competitors_checker_node(state: GraphState) -> dict:
    return CompetitorsCheckerAgent().run(state)
