from langchain.tools import tool
import requests
import os

@tool
def get_weather(city: str) -> str:
    """Fetch current weather for a given city using WeatherAPI."""
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        return "Weather API key is missing. Please check your .env file."
    
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            return f"WeatherAPI Error: {data['error']['message']}"
        
        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        wind_kph = data["current"]["wind_kph"]
        humidity = data["current"]["humidity"]

        return (f"Weather in {location}:\n"
                f"Temperature: {temp_c}°C\n"
                f"Condition: {condition}\n"
                f"Wind: {wind_kph} kph\n"
                f"Humidity: {humidity}%")
    except Exception as e:
        return f"Failed to retrieve weather: {str(e)}"
