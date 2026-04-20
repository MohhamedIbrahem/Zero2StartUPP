from langgraph.graph import StateGraph, END
from state.shared_state import GraphState
from langsmith import traceable


# 🔹 Import ALL agent nodes
from agents.parse_idea import parse_idea_node
from agents.bmc_agent import bmc_node
from agents.market_agent import market_node
from agents.competitors_agent import competitors_node
from agents.swot_agent import swot_node
from agents.ui_agent import ui_node


def aggregate_node(state: GraphState):
    """
    Barrier node:
    Ensures all parallel agents finished before continuing.
    """
    return state


def build_graph():
    builder = StateGraph(GraphState)

    # -------------------------
    # 🔹 Nodes
    # -------------------------
    builder.add_node("parse_idea", parse_idea_node)

    builder.add_node("bmc", bmc_node)
    builder.add_node("market", market_node)
    builder.add_node("competitors", competitors_node)

    builder.add_node("aggregate", aggregate_node)

    builder.add_node("swot", swot_node)
    builder.add_node("ui", ui_node)

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
    # 🔹 Barrier (join)
    # -------------------------
    builder.add_edge("bmc", "aggregate")
    builder.add_edge("market", "aggregate")
    builder.add_edge("competitors", "aggregate")

    # -------------------------
    # 🔹 Final Flow
    # -------------------------
    builder.add_edge("aggregate", "swot")
    builder.add_edge("swot", "ui")
    builder.add_edge("ui", END)

    return builder.compile()



