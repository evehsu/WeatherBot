import requests
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Function to fetch weather forecast
def get_weather_forecast(location):
    api_key = "YOUR_API_KEY_HERE"
    url = f"http://api.openweathermap.org/data/2.5/forecast/daily?q={location}&cnt=16&appid={api_key}"
    response = requests.get(url)
    forecast_data = response.json()
    return forecast_data  # Return the last 3 days of the forecast

# Function to check for sunny days
def check_sunny_days(forecast):
    sunny_days = sum(1 for day in forecast if day['weather'][0]['main'] == 'Clear')
    return sunny_days >= 2

# Function to send email
def send_email(target_email):
    sender_email = "your.email@gmail.com"
    sender_password = "yourpassword"
    subject = "Sunny Days Alert!"
    body = "The forecast shows at least 2 sunny days in the next 3 days!"
    
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
    
# Main script
if __name__ == "__main__":
    print("$$$$$$$$$$ start $$$$$$$$")
    load_dotenv()
    api_key = os.getenv('API_KEY_OPENWEATHER')
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", "-loc", help="Location to check the weather forecast")
    parser.add_argument("--email", "-e", help="Email address to send the alert", required=False)
    args = parser.parse_args()

    location = args.location
    email = args.email

    forecast = get_weather_forecast(location)
    print(forecast)
    # if check_sunny_days(forecast):
    #     send_email(email)
