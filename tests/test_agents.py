from graph.orchestrator import build_graph
import json
import uuid

def test_pipeline():
    graph = build_graph()
    
    state = {
        "idea": "Electronics & Gaming Store in Cairo",
        "run_id": str(uuid.uuid4())
    }
    
    print("Running graph...")
    result = graph.invoke(state)
    
    print("\n=== FINAL STATE ===")
    for k, v in result.items():
        if hasattr(v, "model_dump"):
            print(f"{k}: {json.dumps(v.model_dump(), indent=2)}")
        else:
            print(f"{k}: {v}")

if __name__ == "__main__":
    test_pipeline()
