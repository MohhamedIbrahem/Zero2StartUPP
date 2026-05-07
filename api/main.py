from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
import json
import uuid
import datetime
from graph.orchestrator import build_graph

app = FastAPI(title="Zero2StartUPP API")
graph = build_graph()

class AnalyzeRequest(BaseModel):
    idea: str

def serialize_state(state):
    res = {}
    for k, v in state.items():
        if hasattr(v, "model_dump"):
            res[k] = v.model_dump()
        else:
            res[k] = v
    return res

@app.post("/api/v1/analyze")
async def analyze(req: AnalyzeRequest):
    run_id = str(uuid.uuid4())
    input_state = {"idea": req.idea, "run_id": run_id}
    final_state = graph.invoke(input_state)
    return serialize_state(final_state)

@app.post("/api/v1/analyze/stream")
async def analyze_stream(req: AnalyzeRequest):
    run_id = str(uuid.uuid4())
    input_state = {"idea": req.idea, "run_id": run_id}
    
    async def event_generator():
        try:
            async for output in graph.astream(input_state):
                for node_name, state_update in output.items():
                    # Emit custom events if present
                    events = state_update.get("events", [])
                    for ev in events:
                        yield {
                            "event": ev.get("event", "custom_event"),
                            "data": json.dumps(ev)
                        }
                        
                    # Emit node completion
                    yield {
                        "event": "node_completed",
                        "data": json.dumps({
                            "step": node_name,
                            "status": "completed",
                            "timestamp": datetime.datetime.now().isoformat()
                        })
                    }
            
            # Final state
            final_state = graph.invoke(input_state)
            yield {
                "event": "final_result",
                "data": json.dumps({
                    "status": "completed",
                    "data": serialize_state(final_state)
                })
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({
                    "step": "unknown",
                    "message": str(e),
                    "timestamp": datetime.datetime.now().isoformat()
                })
            }

    return EventSourceResponse(event_generator())
