# Weather Bot

A Python-based weather bot that checks the forecast for a specified location and sends email notifications for sunny days.

## Features

- Fetches 7-day or 14-day weather forecasts
- Geocoding support for location input
- Email notifications for sunny weather
- Configurable sunny day threshold
- Error handling and logging

## Prerequisites

- Python 3.7+
- OpenWeatherMap API key
- Gmail account for sending emails

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-bot.git
   cd weather-bot
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following:
   ```
   OPENWEATHERMAP_API_KEY=your_api_key_here
   GMAIL_USERNAME=your_gmail_username
   GMAIL_PASSWORD=your_gmail_app_password
   ```

## Usage

Run the script with the following command:
