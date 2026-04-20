SWOT_PROMPT = """You are a senior strategic consultant with 20 years of experience in startup advisory.

Your task is to perform a comprehensive SWOT analysis for the following startup by synthesizing ALL provided data.

STARTUP IDEA: {idea}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}
REGION: {region}

BUSINESS MODEL CANVAS:
{bmc}

MARKET DATA:
{market}

COMPETITIVE ANALYSIS:
{competitors}

Using ALL the above data, generate a strategic SWOT analysis.

You MUST return ONLY a valid JSON object with this EXACT schema:
{{
    "strengths": [
        "strength1",
        "strength2",
        "strength3"
    ],
    "weaknesses": [
        "weakness1",
        "weakness2",
        "weakness3"
    ],
    "opportunities": [
        "opportunity1",
        "opportunity2",
        "opportunity3"
    ],
    "threats": [
        "threat1",
        "threat2",
        "threat3"
    ],
    "recommendations": [
        {{
            "priority": "HIGH",
            "action": "Specific strategic action to take",
            "reasoning": "Why this action is important based on the analysis"
        }},
        {{
            "priority": "MEDIUM",
            "action": "Another strategic action",
            "reasoning": "Supporting reasoning from the data"
        }},
        {{
            "priority": "LOW",
            "action": "Additional strategic action",
            "reasoning": "Reasoning based on market or competitive data"
        }}
    ]
}}

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or markdown
3. Do NOT wrap the JSON in code blocks
4. strengths, weaknesses, opportunities, threats MUST each have 3 to 5 items
5. Each SWOT item must be a specific, detailed sentence (not vague)
6. recommendations MUST have between 3 and 5 entries
7. Each recommendation MUST have all 3 fields: priority, action, reasoning
8. priority MUST be one of: "HIGH", "MEDIUM", "LOW"
9. Strengths must reference the business model or value proposition
10. Weaknesses must be honest and realistic, not sugar-coated
11. Opportunities must connect to market data or competitive gaps
12. Threats must reference real competitive or market risks
13. Recommendations must be actionable and tied to specific SWOT findings
14. Do NOT repeat information across SWOT categories
15. The JSON must be syntactically valid and parseable
16. All fields must contain non-empty values
17. Do not repeat similar ideas within the same category
18. Each recommendation must clearly map to at least one weakness, opportunity, or threat
19. At least one recommendation must be HIGH priority
20. Reasoning must reference specific data from BMC, market, or competitors

ANALYSIS GUIDELINES:
- Strengths: What advantages does this startup have based on its BMC?
- Weaknesses: What internal challenges or resource gaps exist?
- Opportunities: What market gaps or trends can be exploited?
- Threats: What external risks exist?
- Recommendations: What should the founder do FIRST, SECOND, THIRD?

RETURN ONLY JSON:"""