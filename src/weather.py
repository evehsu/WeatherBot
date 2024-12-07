import logging
import os
import httpx
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from functools import wraps
from utils.logging_config import logger

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return []
    return wrapper

def get_lat_lon(location: str) -> tuple[float, float]:
    """
    Args:
        location: location string, such as "Seattle", "Yellowstone National Park"

    Returns:
        tuple[float, float]: Latitude and longitude coordinates
    """
    geolocator = Nominatim(user_agent="myWeatherBot")
    location_data = geolocator.geocode(location)
    if location_data:
        return location_data.latitude, location_data.longitude
    else:
        return None, None

def fetch_url(url):
    logging.info(f"Fetching URL: {url}")
    with httpx.Client() as client:
        return client.get(url)

@error_handler
def get_7day_forecast(lat, lon):
    url = f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}"
    response = fetch_url(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forecast = soup.find(id="seven-day-forecast-body")
    days = forecast.find_all(class_="tombstone-container")
    return [day.find(class_="short-desc").get_text().lower() for day in days]

@error_handler
def get_14day_forecast(lat, lon):
    try:
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        if not api_key:
            logger.error("API key not found")
            raise ValueError("OpenWeatherMap API key not found")
        
        url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=14&appid={api_key}"
        response = fetch_url(url).json()
        
        if response.get('cod') != '200':
            logger.error("API error response", extra={
                'error_code': response.get('cod'),
                'error_message': response.get('message')
            })
            raise ValueError(f"API error: {response.get('message', 'Unknown error')}")
        
        forecast_data = response['list']
        return [day['weather'][0]['main'].lower() for day in forecast_data]
    except Exception as e:
        logger.error("Failed to get 14-day forecast", extra={
            'latitude': lat,
            'longitude': lon,
            'error': str(e),
            'error_type': type(e).__name__
        })
        raise

def get_weather_forecast(location: str, time_window: int = 7):
    """
    Get weather forecast for a given location for the specified number of days.

    Args:
        location (str): Location name, e.g. "seattle", "yellowstone national park"
        time_window (int): Number of days for forecast, either 7 or 14 (default: 7)

    Returns:
        list: Weather forecast for the specified number of days
    """
    try:
        lat, lon = get_lat_lon(location)
        if not lat or not lon:
            logger.error("Could not find coordinates", extra={
                'location': location
            })
            return []

        logger.info("Retrieved coordinates", extra={
            'location': location,
            'latitude': lat,
            'longitude': lon
        })

        if time_window == 7:
            forecast = get_7day_forecast(lat, lon)
        elif time_window == 14:
            forecast = get_14day_forecast(lat, lon)
        else:
            logger.error("Invalid time window", extra={
                'location': location,
                'time_window': time_window
            })
            return []

        logger.info("Weather forecast retrieved", extra={
            'location': location,
            'time_window': time_window,
            'forecast': forecast
        })
        return forecast
    except Exception as e:
        logger.error("Failed to get weather forecast", extra={
            'location': location,
            'time_window': time_window,
            'error': str(e),
            'error_type': type(e).__name__
        })
        return []

def check_sunny_days(weather_list: list[str], sunny_threshold: int = 2) -> bool:
    sunny_keywords = ["sunny", "clear"]
    sunny_days = sum(1 for weather in weather_list if any(keyword in weather.lower() for keyword in sunny_keywords))
    return sunny_days >= sunny_threshold 