import argparse
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO)


def get_lat_lon(location: str) -> tuple[float, float]:
    """
    Args:
        location: location string, such as "Seattle", "Yellowstone National Park"

    Returns:
        _type_: _description_
    """
    geolocator = Nominatim(user_agent="myWeatherBot")
    location_data = geolocator.geocode(location)
    if location_data:
        return location_data.latitude, location_data.longitude
    else:
        return None, None


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            return []
    return wrapper


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
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    if not api_key:
        raise ValueError("OpenWeatherMap API key not found in environment variables")
    
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=14&appid={api_key}"
    response = fetch_url(url).json()
    
    if response['cod'] != 200:
        raise ValueError(f"API error: {response.get('message', 'Unknown error')}")
    
    forecast_data = response['list']
    return [day['weather'][0]['main'].lower() for day in forecast_data]


def get_weather_forecast(location: str, time_window: int = 7):
    """
    Get weather forecast for a given location for the specified number of days.

    Args:
        location (str): Location name, e.g. "seattle", "yellowstone national park"
        time_window (int): Number of days for forecast, either 7 or 14 (default: 7)

    Returns:
        list: Weather forecast for the specified number of days
    """
    lat, lon = get_lat_lon(location)
    if not lat or not lon:
        logging.error(f"Could not find coordinates for location: {location}")
        return []

    if time_window == 7:
        return get_7day_forecast(lat, lon)
    elif time_window == 14:
        return get_14day_forecast(lat, lon)
    else:
        logging.error(f"Invalid time window: {time_window}. Must be 7 or 14.")
        return []  # Return the last 3 days of the forecast


# Function to check for sunny days
def check_sunny_days(weather_list: list[str], sunny_threshold: int = 2) -> bool:
    sunny_keywords = ["sunny", "clear"]
    sunny_days = sum(1 for weather in weather_list if any(keyword in weather.lower() for keyword in sunny_keywords))
    return sunny_days >= sunny_threshold

# Function to send email
def send_email(sender_email, sender_password, target_email, subject, body):
    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = target_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, target_email, text)
    server.quit()
    
# Add these new classes at the top of the file
class Subscription(BaseModel):
    email: str
    location: str
    sunny_threshold: int = 2
    time_window: int = 7

    @validator('time_window')
    def must_be_7_or_14(cls, v):
        if v not in [7, 14]:
            raise ValueError('time_window must be either 7 or 14')
        return v

app = FastAPI()
scheduler = BackgroundScheduler()
subscriptions = []

@app.post("/subscribe")
async def subscribe(subscription: Subscription):
    subscriptions.append(subscription)
    # Test the subscription immediately
    try:
        await check_weather_for_single_subscription(subscription)
        return {"message": "Subscription successful and initial check completed"}
    except Exception as e:
        logging.error(f"Subscription added but initial check failed: {str(e)}")
        return {"message": "Subscription successful but initial check failed"}

async def check_weather_for_single_subscription(subscription: Subscription):
    weather_forecast = get_weather_forecast(
        subscription.location, 
        subscription.time_window
    )
    logging.info(f"Weather Forcast results: {weather_forecast}")
    if check_sunny_days(weather_forecast, subscription.sunny_threshold):
        subject = f'''Welcome to Getaway Weather: Good weather notification for {subscription.location}'''
        body = f"""There are at least {subscription.sunny_threshold} sunny days in the next {subscription.time_window} days.
                The weather forecast is:\n{'\n'.join(weather_forecast)}"""
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        send_email(sender_email, sender_password, subscription.email, subject, body)

def check_weather_for_subscribers():
    logging.info(f"Checking weather for {len(subscriptions)} subscribers")
    for subscription in subscriptions:
        logging.info(f"Processing subscription for {subscription.email} in {subscription.location}")
        weather_forecast = get_weather_forecast(
            subscription.location, 
            subscription.time_window
        )
        logging.info(f"Weather forecast: {weather_forecast}")
        if check_sunny_days(weather_forecast, subscription.sunny_threshold):
            logging.info("Sunny days threshold met, sending email")
            subject = f"Good weather notification for {subscription.location}"
            body = f"""There are at least {subscription.sunny_threshold} sunny days in the next {subscription.time_window} days.
                    The weather forecast is:\n{'\n'.join(weather_forecast)}"""
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")
            send_email(sender_email, sender_password, subscription.email, subject, body)

# Main script
if __name__ == "__main__":
    load_dotenv(override=True)
    scheduler.add_job(check_weather_for_subscribers, 'interval', hours=24)
    scheduler.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

