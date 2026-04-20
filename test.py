from graph.orchestrator import build_graph
from utils.executor import run_graph 
graph = build_graph()

result = run_graph(graph, {
    "idea": "A modern fried chicken restaurant in Cairo, Egypt, focused on high-quality crispy chicken with unique Egyptian-inspired flavors, targeting middle-income young adults and families, offering dine-in, takeaway, and delivery through apps like Talabat and Uber Eats, with a strong brand identity and competitive pricing.ch as tuk-tuks and ride-sharing, reducing wait times and improving route efficiency for daily commuters."
})

print(result)