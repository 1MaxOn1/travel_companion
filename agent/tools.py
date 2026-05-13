from ddgs import DDGS

def search_internet(query: str) -> dict:
    if not query:
        return {"error": "Empty query"}
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            return {
                "source": "DuckDuckGo",
                "results": [
                    {"title": r.get("title"), "link": r.get("href"), "snippet": r.get("body")}
                    for r in results
                ]
            }
    except Exception as e:
        return {"error": str(e)}