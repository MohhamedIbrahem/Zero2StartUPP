

class TestAgent(BaseAgent):
    def build_prompt(self, state):
        return 'Return JSON: {"test": "ok"}'


agent = TestAgent()

print(agent.run({"idea": "test"}))