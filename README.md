# Weather Bot

A Python-based weather bot that helps you planning your getaways with good weather on your desired destination.

It currently does:
1. checks the weather forecast for a specified location 
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

Run the script with the following command:
```
python src/main.py --loc YOUR_DESTINATION --email YOUR_EMAIL --time_window NUM_OF_FOLLOWING_DAYS --sunny_threshold NUM_OF_MIN_SUNNY_DAYS
```

This command will check the weather forecast for London in the next 2 days and send an email notification if there are at least 2 sunny days.

## Contributing

We welcome contributions to improve the bot! If you have any suggestions or bug fixes, please open an issue or submit a pull request.
