from typing import Dict, Any, Type
from pydantic import BaseModel
import json

from utils.llm import LLMClient
from utils.json_parser import safe_parse_json
from state.shared_state import GraphState

class BaseAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.schema_class: Type[BaseModel] | None = None

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
        2. Append JSON schema if available
        3. Call LLM
        4. Parse JSON safely
        """

        prompt = self.build_prompt(state)
        
        if self.schema_class:
            schema_json = json.dumps(self.schema_class.model_json_schema(), indent=2)
            prompt += f"\n\nYou MUST return a JSON object that strictly adheres to the following JSON schema:\n{schema_json}"

        raw_output = self.llm.generate(prompt)
        parsed_output = safe_parse_json(raw_output)

        return parsed_output
