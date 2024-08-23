import requests
import json
from geopy.geocoders import Nominatim
from datetime import datetime

# OpenWeatherMap API key (replace with your own)
API_KEY = "c46e4ebb2ecba00893691e992f5e7239"

def get_location():
    geolocator = Nominatim(user_agent="weather_app")
    location = input("Enter your city or address: ")
    try:
        loc = geolocator.geocode(location)
        return loc.latitude, loc.longitude
    except:
        print("Unable to find the location. Please try again.")
        return None

def get_weather(lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",  # For Celsius
        "exclude": "minutely,hourly,alerts"  # Exclude unnecessary data
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print("Error fetching weather data")
        return None

def display_current_weather(weather_data):
    if weather_data:
        current = weather_data['current']
        print("\nCurrent Weather Conditions:")
        print(f"Temperature: {current['temp']}°C")
        print(f"Feels like: {current['feels_like']}°C")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind Speed: {current['wind_speed']} m/s")
        print(f"Weather: {current['weather'][0]['description'].capitalize()}")
    else:
        print("No weather data available.")

def display_forecast(weather_data):
    if weather_data and 'daily' in weather_data:
        print("\n7-Day Weather Forecast:")
        for day in weather_data['daily'][:7]:  # First 7 days
            date = datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d')
            print(f"\nDate: {date}")
            print(f"Temperature: {day['temp']['day']}°C (Min: {day['temp']['min']}°C, Max: {day['temp']['max']}°C)")
            print(f"Precipitation: {day['pop'] * 100}% chance")
            print(f"Rain: {day.get('rain', 0)} mm")
            print(f"Wind Speed: {day['wind_speed']} m/s")
            print(f"Weather: {day['weather'][0]['description'].capitalize()}")
    else:
        print("No forecast data available.")

def main():
    print("Welcome to the Weather Forecast App!")
    
    location = get_location()
    if location:
        lat, lon = location
        weather_data = get_weather(lat, lon)
        if weather_data:
            display_current_weather(weather_data)
            display_forecast(weather_data)
        else:
            print("Unable to fetch weather data.")
    else:
        print("Unable to proceed without a valid location.")

if __name__ == "__main__":
    main()