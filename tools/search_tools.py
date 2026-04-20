from tavily import TavilyClient
import requests
from langsmith import traceable
from config import Config

client = TavilyClient(api_key=Config.TAVILY_API_KEY)

@traceable(name="tavily_search")
def tavily_search(query: str, max_results: int = 5) -> str:
    """
    Perform Tavily search and return formatted text.
    """

    try:
        response = client.search(
            query=query,
            max_results=max_results
        )

        results = []

        for r in response.get("results", []):
            title = r.get("title", "")
            content = r.get("content", "")

            results.append(f"{title}: {content}")

        if not results:
            return "No relevant search results found."

        return "\n".join(results)

    except Exception as e:
        return f"Search failed: {str(e)}"
    


def extract_urls(search_text: str) -> list:
    import re
    return re.findall(r"https?://[^\s\)]+", search_text)


def is_valid_result(link: str) -> bool:
    blocked_domains = [
        "facebook.com",
        "instagram.com",
        "reddit.com",
        "similarweb.com"
    ]

    return not any(domain in link for domain in blocked_domains)

@traceable(name="serper_search")
def serper_search(query: str) -> str:
    try:
        url = "https://google.serper.dev/search"

        payload = {"q": query}
        headers = {
            "X-API-KEY": Config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        results = []

        for r in data.get("organic", []):
            link = r.get("link", "")

            if not is_valid_result(link):
                continue

            title = r.get("title", "")
            snippet = r.get("snippet", "")

            results.append(f"{title} - {snippet} ({link})")

            if len(results) >= 5:
                break

        return "\n".join(results)

    except Exception as e:
        return f"Search failed: {str(e)}"