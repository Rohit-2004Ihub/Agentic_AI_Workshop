from langchain.tools import tool
from duckduckgo_search import DDGS

@tool
def get_attractions(city: str) -> str:
    """Search for top tourist attractions in a city."""
    with DDGS() as ddgs:
        results = ddgs.text(f"Top tourist attractions in {city}", max_results=5)
    return "\n".join([res["body"] for res in results])
