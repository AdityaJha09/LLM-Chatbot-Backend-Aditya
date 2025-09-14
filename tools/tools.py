# tools.py
"""
Define custom tools/functions that can be called by the OpenAI API via function calling.
"""
import requests
from typing import Dict

def get_current_time() -> Dict[str, str]:
    """A sample tool that returns the current server time."""
    from datetime import datetime
    now = datetime.utcnow().isoformat() + 'Z'
    return {"current_time": now}

def get_weather(location: str) -> Dict[str, str]:
    """Get current weather for a given location using a public weather API."""
    # Use helper to get lat/lon for the location
    latlon = get_lat_lon(location)
    if "error" in latlon:
        return {"location": location, "error": latlon["error"]}
    lat, lon = latlon["latitude"], latlon["longitude"]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current_weather", {})
        return {"location": location, "weather": weather}
    except Exception as e:
        return {"location": location, "error": str(e)}

def get_lat_lon(location: str):
    """Helper function to get latitude and longitude for a place using Open-Meteo Geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            lat = results[0].get("latitude")
            lon = results[0].get("longitude")
            return {"latitude": lat, "longitude": lon}
        else:
            return {"error": f"No results found for location: {location}"}
    except Exception as e:
        return {"error": str(e)}

# Add more tools here as needed
