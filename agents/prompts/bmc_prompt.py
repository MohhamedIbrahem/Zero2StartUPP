BMC_PROMPT = """You are a world-class startup strategist and business model expert.

Your task is to generate a complete Business Model Canvas (BMC) for the following startup.

STARTUP IDEA: {idea}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}
REGION: {region}

You MUST return ONLY a valid JSON object with this EXACT schema:
{{
    "customer_segments": ["segment1", "segment2", "segment3"],
    "value_propositions": ["prop1", "prop2", "prop3"],
    "channels": ["channel1", "channel2", "channel3"],
    "customer_relationships": ["relationship1", "relationship2"],
    "revenue_streams": ["stream1", "stream2", "stream3"],
    "key_resources": ["resource1", "resource2", "resource3"],
    "key_activities": ["activity1", "activity2", "activity3"],
    "key_partners": ["partner1", "partner2", "partner3"],
    "cost_structure": ["cost1", "cost2", "cost3"]
}}

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or markdown
3. Do NOT wrap the JSON in code blocks
4. ALL 9 fields are REQUIRED
5. Each field MUST be an array of strings
6. Each array MUST have between 2 and 5 items
7. Each item must be a concise phrase (max 15 words)
8. Items must be specific to THIS startup, not generic
9. Revenue streams must include realistic monetization strategies
10. Cost structure must reflect actual operational costs
11. The JSON must be syntactically valid and parseable
12. Do not include trailing commas
13. All arrays must contain only non-empty strings
14. Do not repeat items across arrays
15. Ensure all elements are realistic and logically consistent

RETURN ONLY JSON:"""