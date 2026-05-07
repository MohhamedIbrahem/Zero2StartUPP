from state.shared_state import GraphState
from agents.bmc_checker_agent import bmc_checker_node

def test_bmc_checker_auto_correction():
    state = {
        "idea": "An AI-powered app that helps busy professionals find quick 15-minute home workouts.",
        "bmc": {
            "value_proposition": "Quick workouts",
            "customer_segments": "",
            "channels": "TBD",
            "customer_relationships": "Automated",
            "revenue_streams": "Subscription",
            "key_resources": "AI Models",
            "key_activities": "Training models",
            "key_partners": "None",
            "cost_structure": "Servers"
        },
        "bmc_retries": 0
    }
    
    print("Testing BMCChecker auto-correction on broken data...")
    result = bmc_checker_node(state)
    
    print("\nResult:")
    print(result.get("bmc").model_dump_json(indent=2))
    
    print("\nEvents:")
    for ev in result.get("events", []):
        print(ev)

if __name__ == "__main__":
    test_bmc_checker_auto_correction()
