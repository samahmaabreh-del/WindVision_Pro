# data_generator.py
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random


class WindDataGenerator:
    def __init__(self, num_turbines=38, location="Tafila"):
        self.num_turbines = num_turbines
        self.location = location
        self.weibull_shape = 2.2
        self.weibull_scale = 8.5
        self.farm_center_lat = 30.7040
        self.farm_center_lon = 35.6930

        self.turbine_specs = {
            'manufacturer': 'Vestas',
            'model': 'V112-3.0 MW',
            'rated_power_kw': 3000,
            'rotor_diameter_m': 112,
            'hub_height_m': 84,
            'cut_in_wind_speed_ms': 3,
            'rated_wind_speed_ms': 12,
            'cut_out_wind_speed_ms': 25,
            'max_survival_wind_speed_ms': 52.5
        }

    def generate_turbines(self):
        turbines = []
        for i in range(1, self.num_turbines + 1):
            row = ((i - 1) // 7)
            col = ((i - 1) % 7)
            spacing = 0.008
            lat = self.farm_center_lat + (row - 2.5) * spacing
            lon = self.farm_center_lon + (col - 3) * spacing

            # كفاءة واقعية
            if i <= 2:
                efficiency = random.uniform(0.55, 0.65)
            elif i <= 5:
                efficiency = random.uniform(0.70, 0.80)
            else:
                efficiency = random.uniform(0.88, 0.97)

            turbines.append({
                'turbine_id': i,
                'name': f'Turbine-{i:02d}',
                'lat': lat,
                'lon': lon,
                'capacity_kw': self.turbine_specs['rated_power_kw'],
                'efficiency_base': efficiency,
                'installation_date': datetime(2015, random.randint(1, 12), random.randint(1, 28)),
                'manufacturer': self.turbine_specs['manufacturer'],
                'model': self.turbine_specs['model']
            })
        return pd.DataFrame(turbines)

    def power_curve(self, wind_speed_ms):
        rated_power = self.turbine_specs['rated_power_kw']
        cut_in = self.turbine_specs['cut_in_wind_speed_ms']
        rated_speed = self.turbine_specs['rated_wind_speed_ms']
        cut_out = self.turbine_specs['cut_out_wind_speed_ms']

        if wind_speed_ms < cut_in or wind_speed_ms > cut_out:
            return 0
        elif wind_speed_ms < rated_speed:
            return rated_power * ((wind_speed_ms - cut_in) / (rated_speed - cut_in)) ** 3
        else:
            return rated_power

    def generate_wind_speed(self, days=90):
        hours = days * 24
        timestamps = [datetime.now() - timedelta(hours=x) for x in range(hours, 0, -1)]
        wind_speed = np.random.weibull(self.weibull_shape, hours) * self.weibull_scale
        wind_speed = np.clip(wind_speed, 0, 25)

        seasonal = []
        for ts in timestamps:
            month = ts.month
            if month in [12, 1, 2]:
                seasonal.append(random.uniform(1.2, 1.4))
            elif month in [6, 7, 8]:
                seasonal.append(random.uniform(0.6, 0.8))
            else:
                seasonal.append(random.uniform(0.9, 1.1))

        wind_speed = wind_speed * np.array(seasonal)
        wind_speed = np.clip(wind_speed, 0, 25)

        return pd.DataFrame({
            'timestamp': timestamps,
            'wind_speed_ms': wind_speed,
            'hour': [ts.hour for ts in timestamps],
            'month': [ts.month for ts in timestamps]
        })

    def generate_production_data(self, wind_df, turbines_df):
        all_data = []
        for _, turbine in turbines_df.iterrows():
            efficiency = turbine['efficiency_base']
            for _, row in wind_df.iterrows():
                wind_speed = row['wind_speed_ms']
                theoretical = self.power_curve(wind_speed)
                actual = theoretical * efficiency * random.uniform(0.97, 1.03)
                actual = max(0, actual)

                if efficiency < 0.65:
                    status = "Failure"
                elif efficiency < 0.80:
                    status = "Maintenance Required"
                else:
                    status = "Good"

                all_data.append({
                    'turbine_id': turbine['turbine_id'],
                    'turbine_name': turbine['name'],
                    'timestamp': row['timestamp'],
                    'wind_speed_ms': wind_speed,
                    'power_output_kw': actual,
                    'efficiency_percent': efficiency * 100,
                    'status': status
                })
        return pd.DataFrame(all_data)

    def generate_all_data(self, days=90):
        turbines_df = self.generate_turbines()
        wind_df = self.generate_wind_speed(days)
        production_df = self.generate_production_data(wind_df, turbines_df)

        return {
            'turbines': turbines_df,
            'wind': wind_df,
            'production': production_df,
            'turbine_specs': self.turbine_specs
        }


def get_ready_data():
    generator = WindDataGenerator(num_turbines=38)
    return generator.generate_all_data(days=90)