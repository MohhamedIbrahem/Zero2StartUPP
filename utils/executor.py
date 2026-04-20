from langsmith import traceable

@traceable(name="full_graph_execution")
def run_graph(graph, input_data):
    return graph.invoke(input_data)