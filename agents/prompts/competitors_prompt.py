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

STRICT RULES:
1. Return ONLY the JSON object, nothing else
2. Do NOT add any explanation, commentary, or markdown
3. Do NOT wrap the JSON in code blocks
4. STRICT GROUNDING: Only use claims explicitly supported by the SEARCH RESULTS and SCRAPED WEBSITE DATA.
5. STRICT GROUNDING: Do not infer operational capabilities unless directly mentioned.
6. STRICT GROUNDING: Do not invent competitors, features, or pricing. 
7. STRICT GROUNDING: If evidence quality is low, return fewer competitors instead of hallucinating. Do not guess.
8. Pricing must be specific based on evidence (mention actual prices or tiers if known). If exact pricing is unknown, describe the pricing model if supported by evidence.
9. Each competitor must be a REAL company supported by the provided data.
10. value_proposition must be one concise sentence (max 20 words).
11. market_gaps must be actionable insights based on evidence, not vague statements.
12. The JSON must be syntactically valid and parseable.

EXAMPLES OF GOOD market_gaps:
- "No competitor offers AI-personalized plans for users with less than 20 min daily"
- "Most competitors lack integration with corporate wellness programs"
- "Pricing gap: no quality option between free apps and $30+/month premium services"

RETURN ONLY JSON:"""