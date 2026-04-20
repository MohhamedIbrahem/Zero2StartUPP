from agents.parse_idea import ParseIdeaAgent
from agents.bmc_agent import BMCAgent
from agents.market_agent import MarketAgent
from agents.competitors_agent import CompetitorsAgent
from agents.swot_agent import SWOTAgent
from agents.ui_agent import UIAgent
def test_pipeline():
    # Step 1: initial state
    state = {
        "idea": "AI-powered fitness app for busy professionals"
    }

    print("\n=== STEP 1: Parse Idea ===")
    parse_agent = ParseIdeaAgent()
    parsed_output = parse_agent.run(state)
    print(parsed_output)

    # merge state (زي LangGraph)
    state.update(parsed_output)

    print("\n=== STEP 2: BMC Agent ===")
    bmc_agent = BMCAgent()
    bmc_output = bmc_agent.run(state)
    print(bmc_output)

    # merge state
    state.update(bmc_output)

    print("\n=== STEP 3: Market Agent ===")
    market_agent = MarketAgent()
    market_output = market_agent.run(state)
    print(market_output)

    state.update(market_output)

    print("\n=== STEP 4: Competitors Agent ===")
    comp_agent = CompetitorsAgent()
    comp_output = comp_agent.run(state)
    print(comp_output)

    state.update(comp_output)


    print("\n=== STEP 5: SWOT Agent ===")
    swot_agent = SWOTAgent()
    swot_output = swot_agent.run(state)
    print(swot_output)

    state.update(swot_output)


    print("\n=== STEP 6: UI Agent ===")
    ui_agent = UIAgent()
    ui_output = ui_agent.run(state)

    print(ui_output["ui_code"][:500])  # أول 500 حرف بس
    state.update(ui_output)





    print("\n=== FINAL STATE ===")
    print(state)

if __name__ == "__main__":
    test_pipeline()



    
