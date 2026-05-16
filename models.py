# models.py - إضافة دالة power_curve
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from datetime import datetime


class WindTurbineModels:
    def __init__(self):
        self.production_models = {}
        self.maintenance_model = None
        self.is_trained = False

    def power_curve(self, wind_speed_ms, rated_power=3000, cut_in=3, rated_speed=12, cut_out=25):
        """منحنى قدرة التوربين Vestas V112-3.0 MW"""
        if wind_speed_ms < cut_in or wind_speed_ms > cut_out:
            return 0
        elif wind_speed_ms < rated_speed:
            return rated_power * ((wind_speed_ms - cut_in) / (rated_speed - cut_in)) ** 3
        else:
            return rated_power

    def train_production_model(self, production_data):
        features = ['wind_speed_ms', 'hour', 'month']

        for turbine_id in production_data['turbine_id'].unique():
            turbine_data = production_data[production_data['turbine_id'] == turbine_id].copy()
            turbine_data['hour'] = pd.to_datetime(turbine_data['timestamp']).dt.hour
            turbine_data['month'] = pd.to_datetime(turbine_data['timestamp']).dt.month

            X = turbine_data[features].values
            y = turbine_data['power_output_kw'].values

            model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
            model.fit(X, y)
            self.production_models[turbine_id] = model

        self.is_trained = True
        return True

    def predict_production(self, turbine_id, wind_speed_ms, temperature, humidity, pressure, hour, month):
        if not self.is_trained or turbine_id not in self.production_models:
            return self.power_curve(wind_speed_ms)

        model = self.production_models[turbine_id]
        features = np.array([[wind_speed_ms, hour, month]])
        prediction = model.predict(features)[0]
        return max(0, prediction)

    # باقي الدوال كما هي...