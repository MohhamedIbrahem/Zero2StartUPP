import requests
from langsmith import traceable
from config import Config




@traceable(name="firecrawl_scrape")
def firecrawl_scrape(url: str) -> str:
    """
    Robust scraping with validation + fallback
    """

    try:
        endpoint = "https://api.firecrawl.dev/v1/scrape"

        headers = {
            "Authorization": f"Bearer {Config.FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True
        }

        response = requests.post(endpoint, json=payload, headers=headers)

        # 🔥 Check status
        if response.status_code != 200:
            return f"Scrape failed (status {response.status_code})"

        data = response.json()

        # 🔥 Extract content safely
        markdown = (
            data.get("data", {}).get("markdown")
            or data.get("markdown")
            or ""
        )

        if not markdown or len(markdown.strip()) < 50:
            return f"Scrape empty or blocked for: {url}"

        return markdown[:2000]  # limit size

    except Exception as e:
        return f"Scrape error: {str(e)}"