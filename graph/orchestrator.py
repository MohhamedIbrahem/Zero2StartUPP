from langgraph.graph import StateGraph, END
from state.shared_state import GraphState


def dummy_parse_node(state: GraphState):
    """
    Temporary node (mock)
    """
    return {
        "industry": "test_industry",
        "target_audience": "test_audience",
        "region": "test_region"
    }


def build_graph():
    builder = StateGraph(GraphState)

    # Add node
    builder.add_node("parse_idea", dummy_parse_node)

    # Define flow
    builder.set_entry_point("parse_idea")
    builder.add_edge("parse_idea", END)

    return builder.compile()




