PARSE_IDEA_PROMPT = """You are a startup analyst AI.

Your task is to analyze the following startup idea and extract exactly 3 fields.

STARTUP IDEA:
{idea}

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or text before or after the JSON
3. Do NOT wrap the JSON in markdown code blocks
4. All values must be concise (max 10 words each)
5. If the region is not explicitly mentioned, default to "Global"
6. Preserve the exact geographic granularity mentioned in the idea (e.g., if a city like "Tanta" is mentioned, use "Tanta", do NOT generalize to "Egypt")
7. If the target audience is not clear, infer the most logical one
8. The industry must be a recognized sector name
9. The JSON must be syntactically valid and parseable

RETURN ONLY JSON:"""