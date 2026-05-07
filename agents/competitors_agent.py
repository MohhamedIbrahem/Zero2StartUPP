from agents.base_agent import BaseAgent
from agents.prompts.competitors_prompt import COMPETITORS_PROMPT
from state.shared_state import GraphState
from tools.search_tools import serper_search
from tools.scrape_tools import firecrawl_scrape
from tools.retrieval_filters import filter_and_rank_results
from schemas.competitors import Competitors

class CompetitorsAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.schema_class = Competitors

    def build_prompt(self, state: GraphState) -> str:
        parsed_idea = state.get("parsed_idea") or {}
        industry = parsed_idea.get("industry", "Technology") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "industry", "Technology")
        region = parsed_idea.get("region", "Global") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "region", "Global")
        target_audience = parsed_idea.get("target_audience", "General consumers") if isinstance(parsed_idea, dict) else getattr(parsed_idea, "target_audience", "General consumers")

        query = f"top competitors or businesses similar to '{state['idea']}' in {region}"
        raw_search_results = serper_search(query)

        # 🔥 Rank and Filter
        filtered_results = filter_and_rank_results(
            results=raw_search_results,
            idea=state["idea"],
            region=region,
            industry=industry
        )

        # Extract highly relevant URLs
        urls = [r["link"] for r in filtered_results]

        # Format filtered snippets for the LLM
        snippets = [f"{r['title']} - {r['snippet']} ({r['link']})" for r in filtered_results]
        search_results_str = "\n".join(snippets) if snippets else "No highly relevant search results found."

        # 🔥 Scrape top 3 filtered URLs
        scraped_chunks = []
        for url in urls[:3]:
            content = firecrawl_scrape(url)
            scraped_chunks.append(f"URL: {url}\n{content}")

        scrape_results = "\n\n".join(scraped_chunks)

        return COMPETITORS_PROMPT.format(
            idea=state["idea"],
            industry=industry,
            target_audience=target_audience,
            region=region,
            search_results=search_results_str,
            scrape_results=scrape_results
        )

    def run(self, state: GraphState) -> dict:
        parsed = super().run(state)
        return {"competitors": parsed}

def competitors_node(state: GraphState) -> dict:
    return CompetitorsAgent().run(state)