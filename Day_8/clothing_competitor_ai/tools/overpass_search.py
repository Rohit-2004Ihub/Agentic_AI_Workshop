import requests

def get_clothing_stores(lat: float, lon: float, radius=1000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    node
      ["shop"="clothes"]
      (around:{radius},{lat},{lon});
    out;
    """

    try:
        response = requests.post(overpass_url, data=query)
        response.raise_for_status()

        data = response.json()
        elements = data.get("elements", [])
        stores = []

        for el in elements:
            name = el.get("tags", {}).get("name", "Unnamed Store")
            lat = el.get("lat")
            lon = el.get("lon")
            stores.append(f"{name} (lat: {lat}, lon: {lon})")

        return stores

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Response: {response.text}")
        return ["Error fetching data. Try again later."]
    except requests.exceptions.RequestException as err:
        print(f"Request error: {err}")
        return ["Network error occurred."]
    except ValueError:
        print("Failed to decode JSON")
        return ["Invalid response format."]
