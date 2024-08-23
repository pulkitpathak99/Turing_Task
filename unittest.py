import unittest
from unittest.mock import patch
from claaude_opus import get_weather, get_forecast, get_alerts, display_weather, display_forecast, display_alerts

class WeatherAppTests(unittest.TestCase):
    @patch("your_app.requests.get")
    def test_get_weather(self, mock_get):
        # Mock the API response for get_weather
        mock_response = {
            "name": "London",
            "main": {
                "temp": 15.5,
                "humidity": 60
            },
            "weather": [
                {
                    "description": "clear sky"
                }
            ],
            "wind": {
                "speed": 5.2
            }
        }
        mock_get.return_value.json.return_value = mock_response
        
        # Call the get_weather function
        weather = get_weather("API_KEY", "London")
        
        # Assert the expected output
        self.assertEqual(weather["city"], "London")
        self.assertEqual(weather["temperature"], 15.5)
        self.assertEqual(weather["description"], "clear sky")
        self.assertEqual(weather["humidity"], 60)
        self.assertEqual(weather["wind_speed"], 5.2)
    
    @patch("your_app.requests.get")
    def test_get_forecast(self, mock_get):
        # Mock the API response for get_forecast
        mock_response = {
            "list": [
                {
                    "dt_txt": "2023-06-01 12:00:00",
                    "main": {
                        "temp": 20.0
                    },
                    "weather": [
                        {
                            "description": "few clouds"
                        }
                    ],
                    "pop": 0.2,
                    "wind": {
                        "speed": 3.5
                    }
                },
                # Add more forecast items as needed
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        
        # Call the get_forecast function
        forecast = get_forecast("API_KEY", "London")
        
        # Assert the expected output
        self.assertEqual(len(forecast), 1)  # Assuming only one forecast item
        self.assertEqual(forecast[0]["date"], "2023-06-01")
        self.assertEqual(forecast[0]["temperature"], 20.0)
        self.assertEqual(forecast[0]["description"], "few clouds")
        self.assertEqual(forecast[0]["precipitation"], 0.2)
        self.assertEqual(forecast[0]["wind_speed"], 3.5)
    
    @patch("your_app.requests.get")
    def test_get_alerts(self, mock_get):
        # Mock the API response for get_alerts
        mock_response = {
            "list": [
                {
                    "alerts": [
                        {
                            "event": "Heat Wave",
                            "description": "High temperatures expected."
                        }
                    ]
                }
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        
        # Call the get_alerts function
        alerts = get_alerts("API_KEY", "London")
        
        # Assert the expected output
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["event"], "Heat Wave")
        self.assertEqual(alerts[0]["description"], "High temperatures expected.")
    
    # Add more test methods for other functions like display_weather, display_forecast, display_alerts

if __name__ == "__main__":
    unittest.main()