# Weather Bot

A Python-based weather bot that helps you planning your getaways with good weather on your desired destination.

It currently does:
1. checks the weather forecast for a specified location using forcast.weather.gov API and OpenWeatherMap API 
2. sends email notification when the number of sunny days is greater than or equal to a specified threshold in the following 1 or 2 weeks.


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

Execute the script using the following command:
```
python src/main.py [OPTIONS]
```

### Options:

| Option | Short | Type | Required | Default | Description |
|--------|-------|------|----------|---------|-------------|
| `--location` | `-loc` | string | Yes | - | Destination for weather forecast |
| `--email` | `-e` | string | Yes | - | Email address for notifications |
| `--time_window` | `-tw` | int | No | 7 | Forecast period (7 or 14 days) |
| `--sunny_threshold` | `-st` | int | No | 2 | Minimum number of sunny days for alert |

**Note:** For a 14-day forecast, ensure you have a pro account with OpenWeatherMap.

### Example:

```
python src/main.py --location London --email myemail@gmail.com --time_window 4 --sunny_threshold 2
```
This command will check the weather forecast for London in the next 1 week and send an email notification if there are at least 2 sunny days.

The script could be be scheduled daily, and when receive a notification for good weather, it's time to pack your luggage and enjoy your vacation!

## Contributing

We welcome contributions to improve the bot! If you have any suggestions or bug fixes, please open an issue or submit a pull request.
