from langchain.tools import tool
from tools.overpass_search import get_clothing_stores

@tool
def fetch_nearby_stores(location: str) -> str:
    """
    Given a location string (e.g., '12.9716,77.5946'), fetch nearby clothing stores.
    """
    try:
        lat, lon = map(float, location.split(","))
        stores = get_clothing_stores(lat, lon)
        return "\n".join(stores)
    except Exception as e:
        return f"Error: {e}"
