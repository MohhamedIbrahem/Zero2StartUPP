import sys
sys.path.append("d:\\Courses\\DEPI R4 Genrative AI\\zero2satartup_project\\Project\\Zero2StartUPP")

from state.shared_state import GraphState
from agents.competitors_checker_agent import competitors_checker_node

def test_competitors_relevance():
    state = {
        "idea": "fried chicken restaurant in Tanta",
        "competitors": {
            "competitors": [
                {
                    "name": "Talabat",
                    "pricing_model": "Commission-based",
                    "strengths": "Wide restaurant network, fast delivery",
                    "market_gap": "No personalized meal planning for users"
                },
                {
                    "name": "Breadfast",
                    "pricing_model": "Subscription-based",
                    "strengths": "Grocery delivery, wide product range",
                    "market_gap": "Limited integration with local farmers"
                },
                {
                    "name": "KFC Egypt",
                    "pricing_model": "Menu-based pricing",
                    "strengths": "Branded food, wide outlet network",
                    "market_gap": "Limited vegetarian options"
                }
            ]
        },
        "competitors_retries": 0
    }
    
    print("Testing CompetitorsChecker auto-correction on irrelevant data...")
    result = competitors_checker_node(state)
    
    print("\nResult:")
    print(result.get("competitors").model_dump_json(indent=2))
    
    print("\nEvents:")
    for ev in result.get("events", []):
        print(ev)

if __name__ == "__main__":
    test_competitors_relevance()
