import requests
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """
    Use this tool EXCLUSIVELY to get the precise weather forecast for a specific location.
    Pass only the name of the city as the location argument.
    """
    try:
        # Το format=3 επιστρέφει καθαρό κείμενο (π.χ. "Athens: ☀️ +22°C")
        response = requests.get(f"https://wttr.in/{location}?format=3")
        return response.text
    except Exception as e:
        return "Weather service unavailable."