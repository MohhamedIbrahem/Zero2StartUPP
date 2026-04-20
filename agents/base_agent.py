from typing import Dict, Any

from utils.llm import LLMClient
from utils.json_parser import safe_parse_json
from state.shared_state import GraphState


class BaseAgent:
    def __init__(self):
        self.llm = LLMClient()

    def build_prompt(self, state: GraphState) -> str:
        """
        Each agent must override this method
        to define its own prompt.
        """
        raise NotImplementedError

    def run(self, state: GraphState) -> Dict[str, Any]:
        """
        Standard execution flow:
        1. Build prompt
        2. Call LLM
        3. Parse JSON safely
        4. Return partial state
        """

        prompt = self.build_prompt(state)

        raw_output = self.llm.generate(prompt)

        parsed_output = safe_parse_json(raw_output)

        return parsed_output
    

