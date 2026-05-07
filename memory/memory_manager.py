import json
import os
from typing import Dict, Any, List
import hashlib

MEMORY_FILE = "memory_store.json"

class MemoryManager:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _get_hash(self, idea: str) -> str:
        return hashlib.md5(idea.lower().strip().encode()).hexdigest()

    def get_memory(self, idea: str) -> List[Dict[str, Any]]:
        idea_hash = self._get_hash(idea)
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(idea_hash, [])

    def save_memory(self, state: Dict[str, Any]):
        idea = state.get("idea")
        run_id = state.get("run_id")
        if not idea or not run_id:
            return
            
        idea_hash = self._get_hash(idea)
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Serialize Pydantic objects or dicts
        serialized_state = {}
        for k, v in state.items():
            if hasattr(v, "model_dump"):
                serialized_state[k] = v.model_dump()
            else:
                serialized_state[k] = v
                
        if idea_hash not in data:
            data[idea_hash] = []
        elif isinstance(data[idea_hash], dict):
            data[idea_hash] = [data[idea_hash]]
            
        # Update existing run if it exists, otherwise append
        existing_idx = next((i for i, run in enumerate(data[idea_hash]) if run.get("run_id") == run_id), None)
        if existing_idx is not None:
            data[idea_hash][existing_idx] = serialized_state
        else:
            data[idea_hash].append(serialized_state)
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def memory_save_node(state: dict) -> dict:
    """
    LangGraph node to save final state into memory.
    """
    manager = MemoryManager()
    manager.save_memory(state)
    return state
