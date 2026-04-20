COMPETITORS_PROMPT = """You are a competitive intelligence analyst specializing in startup ecosystems.

Your task is to identify and analyze the top competitors for the following startup.

STARTUP IDEA: {idea}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}
REGION: {region}

SEARCH RESULTS (competitors found online):
{search_results}

SCRAPED WEBSITE DATA (from competitor homepages):
{scrape_results}

Using ALL available information above, provide a detailed competitive analysis.

You MUST return ONLY a valid JSON object with this EXACT schema:
{{
    "competitors": [
        {{
            "name": "Company Name",
            "url": "https://example.com",
            "pricing": "Description of their pricing model and price points",
            "value_proposition": "Their main value proposition in one sentence",
            "strengths": "Key competitive strengths",
            "weaknesses": "Known weaknesses or gaps"
        }}
    ],
    "market_gaps": [
        "gap1",
        "gap2",
        "gap3"
    ]
}}

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or markdown
3. Do NOT wrap the JSON in code blocks
4. competitors array MUST have between 3 and 5 entries
5. Each competitor MUST have ALL 6 fields (name, url, pricing, value_proposition, strengths, weaknesses)
6. market_gaps MUST have between 2 and 5 items
7. market_gaps should identify opportunities the NEW startup can exploit
8. If search/scrape data is empty, use your knowledge of the industry
9. Pricing must be specific (mention actual prices or tiers if known)
10. If exact pricing is unknown, describe the pricing model (freemium, subscription, etc.)
11. Each competitor must be a REAL company, not fictional
12. value_proposition must be one concise sentence (max 20 words)
13. market_gaps must be actionable insights, not vague statements
14. The JSON must be syntactically valid and parseable
15. All fields must be non-empty strings
16. Do not repeat the same competitor more than once
17. URLs must be valid and start with http or https
18. If scrape data is provided, do not invent details not present in it
19. strengths and weaknesses must be logically consistent with the value_proposition

EXAMPLES OF GOOD market_gaps:
- "No competitor offers AI-personalized plans for users with less than 20 min daily"
- "Most competitors lack integration with corporate wellness programs"
- "Pricing gap: no quality option between free apps and $30+/month premium services"

EXAMPLES OF BAD market_gaps:
- "The market is competitive"
- "There is room for improvement"

RETURN ONLY JSON:"""