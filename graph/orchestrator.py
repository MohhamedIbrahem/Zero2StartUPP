from langgraph.graph import StateGraph, END
from state.shared_state import GraphState

# 🔹 Import generation nodes
from agents.parse_idea import parse_idea_node
from agents.bmc_agent import bmc_node
from agents.market_agent import market_node
from agents.competitors_agent import competitors_node
from agents.swot_agent import swot_node

# 🔹 Import checker nodes
from agents.bmc_checker_agent import bmc_checker_node
from agents.market_checker_agent import market_checker_node
from agents.competitors_checker_agent import competitors_checker_node
from agents.swot_checker_agent import swot_checker_node

# 🔹 Import memory
from memory.memory_manager import memory_save_node

def aggregate_node(state: GraphState):
    """
    Barrier node:
    Ensures all parallel agents finished before continuing.
    """
    return state

# --- Routers ---
def route_bmc(state: GraphState) -> str:
    events = state.get("events", [])
    if events and events[-1].get("event") == "retry_triggered" and events[-1].get("step") == "bmc_checker":
        return "bmc"
    return "aggregate"

def route_market(state: GraphState) -> str:
    events = state.get("events", [])
    if events and events[-1].get("event") == "retry_triggered" and events[-1].get("step") == "market_checker":
        return "market"
    return "aggregate"

def route_competitors(state: GraphState) -> str:
    events = state.get("events", [])
    if events and events[-1].get("event") == "retry_triggered" and events[-1].get("step") == "competitors_checker":
        return "competitors"
    return "aggregate"

def route_swot(state: GraphState) -> str:
    events = state.get("events", [])
    if events and events[-1].get("event") == "retry_triggered" and events[-1].get("step") == "swot_checker":
        return "swot"
    return "memory_save"

def build_graph():
    builder = StateGraph(GraphState)

    # -------------------------
    # 🔹 Nodes
    # -------------------------
    builder.add_node("parse_idea", parse_idea_node)

    builder.add_node("bmc", bmc_node)
    builder.add_node("market", market_node)
    builder.add_node("competitors", competitors_node)

    builder.add_node("bmc_checker", bmc_checker_node)
    builder.add_node("market_checker", market_checker_node)
    builder.add_node("competitors_checker", competitors_checker_node)

    builder.add_node("aggregate", aggregate_node)

    builder.add_node("swot", swot_node)
    builder.add_node("swot_checker", swot_checker_node)
    
    builder.add_node("memory_save", memory_save_node)

    # -------------------------
    # 🔹 Entry Point
    # -------------------------
    builder.set_entry_point("parse_idea")

    # -------------------------
    # 🔹 Parallel Execution
    # -------------------------
    builder.add_edge("parse_idea", "bmc")
    builder.add_edge("parse_idea", "market")
    builder.add_edge("parse_idea", "competitors")

    # -------------------------
    # 🔹 Checkers (Generation -> Checker)
    # -------------------------
    builder.add_edge("bmc", "bmc_checker")
    builder.add_edge("market", "market_checker")
    builder.add_edge("competitors", "competitors_checker")

    # -------------------------
    # 🔹 Conditional Routing (Checker -> Generation or Aggregate)
    # -------------------------
    builder.add_conditional_edges("bmc_checker", route_bmc, {"bmc": "bmc", "aggregate": "aggregate"})
    builder.add_conditional_edges("market_checker", route_market, {"market": "market", "aggregate": "aggregate"})
    builder.add_conditional_edges("competitors_checker", route_competitors, {"competitors": "competitors", "aggregate": "aggregate"})

    # -------------------------
    # 🔹 Final Flow
    # -------------------------
    builder.add_edge("aggregate", "swot")
    builder.add_edge("swot", "swot_checker")
    builder.add_conditional_edges("swot_checker", route_swot, {"swot": "swot", "memory_save": "memory_save"})
    builder.add_edge("memory_save", END)

    return builder.compile()
