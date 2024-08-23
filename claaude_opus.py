import requests

def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        print("City not found.")
        return None
    
    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
    
    return weather

def get_forecast(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        print("City not found.")
        return None
    
    forecast = []
    for item in data["list"]:
        date = item["dt_txt"][:10]
        temperature = item["main"]["temp"]
        description = item["weather"][0]["description"]
        precipitation = item["pop"]
        wind_speed = item["wind"]["speed"]
        
        forecast_item = {
            "date": date,
            "temperature": temperature,
            "description": description,
            "precipitation": precipitation,
            "wind_speed": wind_speed
        }
        forecast.append(forecast_item)
    
    return forecast

def display_weather(weather):
    print(f"Current weather in {weather['city']}:")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Description: {weather['description']}")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Wind Speed: {weather['wind_speed']} m/s")

def display_forecast(forecast):
    print("7-day weather forecast:")
    for item in forecast:
        print(f"Date: {item['date']}")
        print(f"Temperature: {item['temperature']}°C")
        print(f"Description: {item['description']}")
        print(f"Precipitation: {item['precipitation']}%")
        print(f"Wind Speed: {item['wind_speed']} m/s")
        print("---")

def get_alerts(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        print("City not found.")
        return None
    
    alerts = []
    for item in data["list"]:
        if "alerts" in item:
            for alert in item["alerts"]:
                event = alert["event"]
                description = alert["description"]
                
                alert_item = {
                    "event": event,
                    "description": description
                }
                alerts.append(alert_item)
    
    return alerts

def display_alerts(alerts):
    if alerts:
        print("Weather Alerts:")
        for alert in alerts:
            print(f"Event: {alert['event']}")
            print(f"Description: {alert['description']}")
            print("---")
    else:
        print("No weather alerts.")

def main():
    api_key = "c46e4ebb2ecba00893691e992f5e7239"  # Replace with your OpenWeatherMap API key
    city = input("Enter the city name: ")
    
    weather = get_weather(api_key, city)
    forecast = get_forecast(api_key, city)
    alerts = get_alerts(api_key, city)
    
    if weather and forecast:
        display_weather(weather)
        print()
        display_alerts(alerts)
        print()
        display_forecast(forecast)
        
        

if __name__ == "__main__":
    main()

