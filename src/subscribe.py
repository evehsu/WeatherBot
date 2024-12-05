import logging
from pydantic import BaseModel, validator
from typing import List
import os
from weather import get_weather_forecast, check_sunny_days
from notification import send_email
from database import save_subscriber, get_subscriber_by_email, get_all_subscribers
from subscribe_objects import Subscriber, Subscription

def manage_subscription(subscription: Subscription) -> Subscriber:
    # Get existing subscriber data if it exists
    existing_subscriber = get_subscriber_by_email(subscription.email)
    
    # Prepare new destinations and their corresponding thresholds/windows
    new_destinations = subscription.locations
    
    if existing_subscriber:
        # Update existing subscriber's data
        # Combine existing and new destinations, keeping most recent ones first
        combined_destinations = [
            dest for dest in existing_subscriber.user_destination 
            if dest not in new_destinations
        ] + new_destinations
        # Limit to allowed number of destinations

        combined_destinations = combined_destinations[-existing_subscriber.num_allowed_destination:]
        
        subscriber = Subscriber(
            user_email=subscription.email,
            user_destination=combined_destinations,
            sunny_threshold=[subscription.sunny_threshold] * len(combined_destinations),
            time_window=[subscription.time_window] * len(combined_destinations)
        )
    else:
        # Create new subscriber
        subscriber = Subscriber(
            user_email=subscription.email,
            user_destination=new_destinations,
            sunny_threshold=[subscription.sunny_threshold] * len(new_destinations),
            time_window=[subscription.time_window] * len(new_destinations)
        )
    
    # Save to database
    save_subscriber(subscriber)
    return subscriber

async def check_weather_for_single_subscription(subscription: Subscription):
    subscriber = manage_subscription(subscription)
    for i, location in enumerate(subscriber.user_destination):
        weather_forecast = get_weather_forecast(
            location, 
            subscriber.time_window[i]
        )
        logging.info(f"Weather Forecast results for {location}: {weather_forecast}")
        if check_sunny_days(weather_forecast, subscriber.sunny_threshold[i]):
            subject = f'''Welcome to Getaway Weather: Good weather notification for {location}'''
            body = f"""There are at least {subscriber.sunny_threshold[i]} sunny days in the next {subscriber.time_window[i]} days.
                    The weather forecast is:\n{'\n'.join(weather_forecast)}"""
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")
            send_email(sender_email, sender_password, subscriber.user_email, subject, body)

def check_weather_for_subscribers():
    """Load subscribers from database and check weather for each"""
    subscribers = get_all_subscribers()
    logging.info(f"Checking weather for {len(subscribers)} subscribers")
    
    for subscriber in subscribers:
        for i, location in enumerate(subscriber.user_destination):
            logging.info(f"Processing subscription for {subscriber.user_email} in {location}")
            weather_forecast = get_weather_forecast(
                location, 
                subscriber.time_window[i]
            )
            logging.info(f"Weather forecast: {weather_forecast}")
            if check_sunny_days(weather_forecast, subscriber.sunny_threshold[i]):
                logging.info("Sunny days threshold met, sending email")
                subject = f"Good weather notification for {location}"
                body = f"""There are at least {subscriber.sunny_threshold[i]} sunny days in the next {subscriber.time_window[i]} days.
                        The weather forecast is:\n{'\n'.join(weather_forecast)}"""
                sender_email = os.getenv("SENDER_EMAIL")
                sender_password = os.getenv("SENDER_PASSWORD")
                send_email(sender_email, sender_password, subscriber.user_email, subject, body) 