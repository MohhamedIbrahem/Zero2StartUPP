from utils.llm import LLMClient
from utils.json_parser import safe_parse_json
import json

RANKING_PROMPT = """You are a relevance scoring engine for a startup research pipeline.
Evaluate the following search results for their relevance to the target startup idea.

TARGET STARTUP:
Idea: {idea}
Industry: {industry}
Region: {region}

SEARCH RESULTS TO EVALUATE:
{results_json}

RULES:
1. Score each result from 0 to 10 based on how relevant it is as a direct competitor or highly comparable business.
2. A score of 10 means it's an exact competitor in the exact region.
3. A score of 0 means it's irrelevant (e.g., wrong industry, wrong country, or it's a software provider/tool instead of a competitor).
4. Give heavy penalties (scores < 4) to businesses clearly operating in completely different countries (e.g. Italy, USA, UK when the target is Egypt).
5. Give heavy penalties to B2B SaaS platforms if the startup is a local B2C business (like a restaurant or supermarket).

You MUST return a JSON object exactly matching this schema:
{{
    "scored_results": [
        {{
            "id": 0,
            "score": 8,
            "reason": "Brief explanation of the score"
        }}
    ]
}}
"""

def filter_and_rank_results(results: list, idea: str, region: str, industry: str) -> list:
    """
    Takes a list of search result dictionaries: [{"title": "...", "snippet": "...", "link": "..."}]
    Returns a filtered, sorted list of results that scored >= 7.
    """
    if not results:
        return []

    # Prepare data for LLM
    results_to_eval = []
    for idx, r in enumerate(results):
        results_to_eval.append({
            "id": idx,
            "title": r.get("title", ""),
            "snippet": r.get("snippet", ""),
            "url": r.get("link", "")
        })

    prompt = RANKING_PROMPT.format(
        idea=idea,
        industry=industry,
        region=region,
        results_json=json.dumps(results_to_eval, indent=2)
    )

    llm = LLMClient()
    try:
        raw_response = llm.generate(prompt)
        parsed = safe_parse_json(raw_response)
        
        scored_items = parsed.get("scored_results", [])
        
        # Create a mapping of id to score
        score_map = {}
        for item in scored_items:
            score_map[item.get("id")] = item.get("score", 0)

        # Filter and inject scores
        filtered = []
        for idx, r in enumerate(results):
            score = score_map.get(idx, 0)
            if score >= 7:
                r["relevance_score"] = score
                filtered.append(r)

        # Sort descending by score
        filtered.sort(key=lambda x: x["relevance_score"], reverse=True)
        return filtered

    except Exception as e:
        print(f"Ranking failed: {e}")
        # Fallback: return everything if ranking fails
        return results
