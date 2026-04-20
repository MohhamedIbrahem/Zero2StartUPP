from agents.base_agent import BaseAgent
from agents.prompts.ui_prompt import UI_PROMPT
from state.shared_state import GraphState


class UIAgent(BaseAgent):
    """
    Agent responsible for generating a React TSX dashboard
    from the full startup analysis.
    """

    def build_prompt(self, state: GraphState) -> str:
        return UI_PROMPT.format(
            idea=state["idea"],
            bmc=state.get("bmc", {}),
            market=state.get("market", {}),
            competitors=state.get("competitors", {}),
            swot=state.get("swot", {})
        )

    def run(self, state: GraphState) -> dict:
        prompt = self.build_prompt(state)
        raw_code = self.llm.generate(prompt)

        cleaned = self._clean_tsx(raw_code)

        return {
            "ui_code": cleaned
        }

    def _clean_tsx(self, code: str) -> str:
        """
        Clean TSX output from markdown or noise.
        """

        if not isinstance(code, str):
            return self._fallback_ui()

        # 🔹 remove markdown blocks
        code = code.replace("```tsx", "").replace("```", "").strip()

        # 🔹 basic sanity checks
        if "import React" not in code:
            return self._fallback_ui()

        if "export default" not in code:
            return self._fallback_ui()

        # 🔹 fix common cut issues
        code = code.replace("Fitnes", "Fitness")
        code = code.replace("CA \nNVAS", "CANVAS")

        # 🔹 prevent Tailwind dynamic class crash
        code = self._fix_tailwind_classes(code)

        return code

    def _fix_tailwind_classes(self, code: str) -> str:
        """
        Replace dynamic Tailwind classes with safe static mapping.
        """

        if "bg-${recommendation.priority.toLowerCase()}" in code:
            replacement = """
const priorityColors = {
  High: "bg-red-100 text-red-800",
  Medium: "bg-yellow-100 text-yellow-800",
  Low: "bg-green-100 text-green-800"
};
"""
            code = replacement + code

            code = code.replace(
                "bg-${recommendation.priority.toLowerCase()}-100 text-${recommendation.priority.toLowerCase()}-800",
                "priorityColors[recommendation.priority]"
            )

        return code

    def _fallback_ui(self) -> str:
        """
        Minimal fallback UI
        """
        return """import React from 'react';

const StartupReport = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Startup Report</h1>
      <p>Unable to generate full UI. Please try again.</p>
    </div>
  );
};

export default StartupReport;
"""


# LangGraph node
def ui_node(state: GraphState) -> dict:
    return UIAgent().run(state)