import pytest
from weather import get_weather_forecast, check_sunny_days

def test_check_sunny_days():
    weather_list = ["sunny", "partly cloudy", "clear", "rain"]
    assert check_sunny_days(weather_list, 2) == True
    assert check_sunny_days(weather_list, 3) == False
    assert check_sunny_days(weather_list, 4) == False

def test_invalid_time_window():
    forecast = get_weather_forecast("Seattle", 10)
    assert forecast == [] 