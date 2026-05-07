SWOT_PROMPT = """You are a strategic business consultant.

Your task is to generate a SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats) for the following startup, using the context provided.

STARTUP IDEA: {idea}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}
REGION: {region}

CONTEXT FROM PREVIOUS ANALYSIS:
Business Model Canvas:
{bmc}

Market Analysis:
{market}

Competitors:
{competitors}

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or markdown
3. Do NOT wrap the JSON in code blocks
4. All four quadrants (strengths, weaknesses, opportunities, threats) are REQUIRED
5. Ensure items are specific to this startup and its context
6. Draw directly from the provided BMC, Market, and Competitor data
7. The JSON must be syntactically valid and parseable

RETURN ONLY JSON:"""