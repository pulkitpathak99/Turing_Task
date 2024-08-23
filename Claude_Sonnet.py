import requests
import json
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch
import os
import jsonify
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, request, redirect, session

# API key and base URL for OpenWeatherMap API
API_KEY = "c46e4ebb2ecba00893691e992f5e7239"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
OAUTH_CLIENT_ID = "249786480722-1j3tcna11r1b4341boreckftb2m01hof.apps.googleusercontent.com"
OAUTH_CLIENT_SECRET = "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"
OAUTH_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
OAUTH_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


app = Flask(__name__)
app.secret_key = os.urandom(24)
client = WebApplicationClient(OAUTH_CLIENT_ID)



class WeatherApp:
    def __init__(self):
        self.location = None
        self.user = None

    def get_current_weather(self, location):
        """Get current weather conditions for a given location."""
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params)
        data = json.loads(response.text)
        return data

    def get_forecast(self, location):
        """Get 7-day weather forecast for a given location."""
        params = {
            "q": location,
            "appid": API_KEY,
            "units": "metric",
            "cnt": 7 * 8  # 7 days * 8 data points per day
        }
        response = requests.get(FORECAST_URL, params=params)
        data = json.loads(response.text)
        return data

    def get_weather_alerts(self, location):
        """Get weather alerts for a given location."""
        # Note: OpenWeatherMap's free tier doesn't include weather alerts.
        # This is a placeholder implementation.
        params = {
            "q": location,
            "appid": API_KEY,
        }
        response = requests.get(BASE_URL, params=params)
        data = json.loads(response.text)
        # Check for extreme conditions (this is a simple example)
        alerts = []
        if data['main']['temp'] > 35:
            alerts.append("Heat Wave Alert: Temperature exceeds 35°C")
        elif data['main']['temp'] < 0:
            alerts.append("Freeze Alert: Temperature below 0°C")
        if data.get('rain', {}).get('1h', 0) > 50:
            alerts.append("Heavy Rain Alert: More than 50mm rain in last hour")
        return alerts

    def display_current_weather(self, data):
        """Display current weather conditions."""
        print(f"Current weather in {data['name']}:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
        print(f"Description: {data['weather'][0]['description']}")

    def display_forecast(self, data):
        """Display 7-day weather forecast."""
        print("\n7-Day Forecast:")
        for day in data['list'][::8]:  # Get one data point per day
            date = datetime.fromtimestamp(day['dt'])
            print(f"\nDate: {date.strftime('%Y-%m-%d')}")
            print(f"Temperature: {day['main']['temp']}°C")
            print(f"Precipitation: {day.get('rain', {}).get('3h', 0)} mm")
            print(f"Wind Speed: {day['wind']['speed']} m/s")

    def display_alerts(self, alerts):
        """Display weather alerts."""
        if alerts:
            print("\nWeather Alerts:")
            for alert in alerts:
                print(f"- {alert}")
        else:
            print("\nNo current weather alerts.")

    def set_location(self, location):
        """Set the user's preferred location."""
        self.location = location

    def get_saved_location(self):
        """Get the user's saved location."""
        return self.location
    
    def set_user(self, user):
        """Set the current user."""
        self.user = user

    def get_user(self):
        """Get the current user."""
        return self.user

@app.route('/login')
def login():
    """Initiate Google OAuth login process."""
    authorization_url, state = client.prepare_authorization_request(
        OAUTH_AUTHORIZE_URL,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"]
    )
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route('/login/callback')
def callback():
    """Handle Google OAuth callback and token exchange."""
    token = client.fetch_token(
        OAUTH_TOKEN_URL,
        client_secret=OAUTH_CLIENT_SECRET,
        authorization_response=request.url
    )
    
    # Store the token in the session
    session['oauth_token'] = token
    
    # Fetch user information
    userinfo_response = requests.get(
        OAUTH_USER_INFO_URL,
        headers={'Authorization': f"Bearer {token['access_token']}"}
    )
    userinfo = userinfo_response.json()

    # Store user information in session or database
    session['user_id'] = userinfo['id']
    session['user_email'] = userinfo['email']

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """Display user dashboard after successful login."""
    if 'user_email' not in session:
        return redirect('/login')
    return f"Welcome to your weather dashboard, {session['user_email']}!"


@app.route('/set_location', methods=['POST'])
def set_location():
    """Set user's preferred location."""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    location = request.json.get('location')
    user = user.query.get(session['user_id'])
    user.preferred_location = location
    db.session.commit()
    return jsonify({"message": "Location set successfully"})

@app.route('/get_weather')
def get_weather():
    """Get weather for user's preferred location."""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    user = user.query.get(session['user_id'])
    if not user.preferred_location:
        return jsonify({"error": "No preferred location set"}), 400
    weather_app = WeatherApp()
    current_weather = weather_app.get_current_weather(user.preferred_location)
    forecast = weather_app.get_forecast(user.preferred_location)
    alerts = weather_app.get_weather_alerts(user.preferred_location)
    return jsonify({
        "current_weather": current_weather,
        "forecast": forecast,
        "alerts": alerts
    })


def main():
    weather_app = WeatherApp()
    while True:
        print("\nWeather Forecast App")
        print("1. Get Current Weather")
        print("2. Get 7-Day Forecast")
        print("3. Check Weather Alerts")
        print("4. Set Preferred Location")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            location = weather_app.get_saved_location() or input("Enter location: ")
            data = weather_app.get_current_weather(location)
            weather_app.display_current_weather(data)
        elif choice == '2':
            location = weather_app.get_saved_location() or input("Enter location: ")
            data = weather_app.get_forecast(location)
            weather_app.display_forecast(data)
        elif choice == '3':
            location = weather_app.get_saved_location() or input("Enter location: ")
            alerts = weather_app.get_weather_alerts(location)
            weather_app.display_alerts(alerts)
        elif choice == '4':
            location = input("Enter your preferred location: ")
            weather_app.set_location(location)
            print(f"Location set to {location}")
        elif choice == '5':
            print("Thank you for using the Weather Forecast App!")
            break
        else:
            print("Invalid choice. Please try again.")

class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        self.weather_app = WeatherApp()

    @patch('requests.get')
    def test_get_current_weather(self, mock_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({
            "name": "London",
            "main": {"temp": 15, "humidity": 80},
            "wind": {"speed": 5},
            "weather": [{"description": "Cloudy"}]
        }).encode('utf-8')
        mock_get.return_value = mock_response

        data = self.weather_app.get_current_weather("London")
        self.assertEqual(data['name'], "London")
        self.assertEqual(data['main']['temp'], 15)

    @patch('requests.get')
    def test_get_forecast(self, mock_get):
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({
            "list": [
                {
                    "dt": 1628524800,
                    "main": {"temp": 20},
                    "wind": {"speed": 3},
                    "rain": {"3h": 0.5}
                }
            ] * 56  # 7 days * 8 data points per day
        }).encode('utf-8')
        mock_get.return_value = mock_response

        data = self.weather_app.get_forecast("London")
        self.assertEqual(len(data['list']), 56)
        self.assertEqual(data['list'][0]['main']['temp'], 20)

if __name__ == "__main__":
    main()
    # Uncomment the line below to run unit tests
    #unittest.main()