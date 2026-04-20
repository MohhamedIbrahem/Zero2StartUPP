import json
import re
from typing import Any, Dict


def safe_parse_json(text: str) -> Dict[str, Any]:
    """
    Safely parse JSON from LLM output.

    Steps:
    1. Try direct JSON parsing
    2. Clean markdown/code blocks
    3. Extract JSON substring
    4. Fallback with error
    """

    # 🔹 Step 1 — Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 🔹 Step 2 — Remove markdown code blocks ```json ... ```
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # 🔹 Step 3 — Extract JSON substring
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass

    # 🔹 Step 4 — Final fallback
    return {
        "error": "invalid_json",
        "raw": text
    }