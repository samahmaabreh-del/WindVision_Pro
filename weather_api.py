# weather_api.py
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class WeatherAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"

    def get_current_weather(self, lat, lon):
        if self.api_key:
            try:
                url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
                response = requests.get(url, timeout=5)
                data = response.json()
                return {
                    'wind_speed': data['wind']['speed'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_direction': data['wind']['deg'],
                    'timestamp': datetime.now()
                }
            except:
                return self._get_simulated_weather(lat, lon)
        else:
            return self._get_simulated_weather(lat, lon)

    def get_forecast(self, lat, lon, days=5):
        if self.api_key:
            try:
                url = f"{self.base_url}/forecast?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
                response = requests.get(url, timeout=5)
                data = response.json()
                forecasts = []
                for item in data['list'][:days * 8]:
                    forecasts.append({
                        'timestamp': item['dt_txt'],
                        'wind_speed': item['wind']['speed'],
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'pressure': item['main']['pressure']
                    })
                return pd.DataFrame(forecasts)
            except:
                return self._get_simulated_forecast(lat, lon, days)
        else:
            return self._get_simulated_forecast(lat, lon, days)

    def _get_simulated_weather(self, lat, lon):
        return {
            'wind_speed': max(0, 7.5 + np.random.normal(0, 2)),
            'temperature': 22 + np.random.normal(0, 3),
            'humidity': 50 + np.random.normal(0, 10),
            'pressure': 1013 + np.random.normal(0, 3),
            'wind_direction': np.random.uniform(0, 360),
            'timestamp': datetime.now()
        }

    def _get_simulated_forecast(self, lat, lon, days):
        forecasts = []
        now = datetime.now()
        for i in range(days * 24):
            timestamp = now + timedelta(hours=i)
            month = timestamp.month
            if month in [12, 1, 2]:
                wind_factor = 1.3
                temp_factor = -5
            elif month in [6, 7, 8]:
                wind_factor = 0.7
                temp_factor = 10
            else:
                wind_factor = 1.0
                temp_factor = 0
            hour = timestamp.hour
            daily_factor = 1 + 0.2 * np.sin(np.pi * (hour - 12) / 12)
            wind_speed = max(0, 7.5 * wind_factor * daily_factor + np.random.normal(0, 1))
            temperature = 22 + temp_factor + 5 * np.sin(np.pi * (hour - 14) / 12) + np.random.normal(0, 1)
            forecasts.append({
                'timestamp': timestamp,
                'wind_speed': wind_speed,
                'temperature': temperature,
                'humidity': 60 + np.random.normal(0, 10),
                'pressure': 1013 + np.random.normal(0, 3)
            })
        return pd.DataFrame(forecasts)


def get_weather_for_tafilah(api_key=None):
    api = WeatherAPI(api_key)
    return api.get_current_weather(30.7040, 35.6930)