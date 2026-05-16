# export_all_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================
# توليد جميع البيانات
# ============================================

print("جاري توليد البيانات...")

# 1. بيانات التوربينات (38 توربين Vestas V112-3.0 MW)
print("1. جاري توليد بيانات التوربينات...")

turbines_data = []
for i in range(1, 39):
    # توزيع واقعي للتوربينات في الطفيلة
    row = ((i - 1) // 7)
    col = ((i - 1) % 7)
    spacing = 0.008
    lat = 30.7040 + (row - 2.5) * spacing
    lon = 35.6930 + (col - 3) * spacing

    # كفاءة واقعية
    if i <= 2:
        efficiency = round(random.uniform(0.55, 0.65), 3)
    elif i <= 5:
        efficiency = round(random.uniform(0.70, 0.80), 3)
    else:
        efficiency = round(random.uniform(0.88, 0.97), 3)

    turbines_data.append({
        'turbine_id': i,
        'turbine_name': f'Turbine_{i:02d}',
        'latitude': round(lat, 6),
        'longitude': round(lon, 6),
        'capacity_kw': 3000,
        'capacity_mw': 3.0,
        'efficiency_percent': round(efficiency * 100, 1),
        'manufacturer': 'Vestas',
        'model': 'V112-3.0 MW',
        'rotor_diameter_m': 112,
        'hub_height_m': 84,
        'installation_year': 2015
    })

turbines_df = pd.DataFrame(turbines_data)
turbines_df.to_csv('01_turbines_data.csv', index=False)
print(f"   ✅ تم حفظ 01_turbines_data.csv ({len(turbines_df)} صف)")

# 2. بيانات سرعة الرياح (90 يوم × 24 ساعة)
print("2. جاري توليد بيانات سرعة الرياح...")

days = 90
hours = days * 24
timestamps = [datetime.now() - timedelta(hours=x) for x in range(hours, 0, -1)]
timestamps.reverse()

# معاملات Weibull لمنطقة الطفيلة
shape = 2.2
scale = 8.5

wind_speed = np.random.weibull(shape, hours) * scale
wind_speed = np.clip(wind_speed, 0, 25)

# تأثير موسمي
wind_data = []
for i, ts in enumerate(timestamps):
    month = ts.month
    if month in [12, 1, 2]:
        seasonal = random.uniform(1.2, 1.4)
    elif month in [6, 7, 8]:
        seasonal = random.uniform(0.6, 0.8)
    else:
        seasonal = random.uniform(0.9, 1.1)

    ws = round(wind_speed[i] * seasonal, 2)
    ws = max(0, min(ws, 25))

    wind_data.append({
        'timestamp': ts.strftime('%Y-%m-%d %H:00:00'),
        'wind_speed_ms': ws,
        'hour': ts.hour,
        'day': ts.day,
        'month': ts.month,
        'year': ts.year,
        'season': 'Winter' if month in [12, 1, 2] else 'Spring' if month in [3, 4, 5] else 'Summer' if month in [6, 7,
                                                                                                                 8] else 'Autumn'
    })

wind_df = pd.DataFrame(wind_data)
wind_df.to_csv('02_wind_speed_data.csv', index=False)
print(f"   ✅ تم حفظ 02_wind_speed_data.csv ({len(wind_df)} صف)")

# 3. بيانات الطقس
print("3. جاري توليد بيانات الطقس...")

weather_data = []
for i, row in wind_df.iterrows():
    ws = row['wind_speed_ms']
    temp = round(22 - (ws * 0.3) + random.normalvariate(0, 2), 1)
    temp = max(5, min(40, temp))

    humidity = round(70 - (temp - 20) * 1.2 + random.normalvariate(0, 5), 1)
    humidity = max(20, min(95, humidity))

    pressure = round(1013 + random.normalvariate(0, 3), 1)
    wind_dir = round(random.uniform(0, 360), 1)

    weather_data.append({
        'timestamp': row['timestamp'],
        'temperature_c': temp,
        'humidity_percent': humidity,
        'pressure_hpa': pressure,
        'wind_direction_deg': wind_dir
    })

weather_df = pd.DataFrame(weather_data)
weather_df.to_csv('03_weather_data.csv', index=False)
print(f"   ✅ تم حفظ 03_weather_data.csv ({len(weather_df)} صف)")

# 4. بيانات الإنتاج (أكبر ملف)
print("4. جاري توليد بيانات الإنتاج (قد يستغرق دقيقة)...")


def power_curve(wind_speed_ms):
    if wind_speed_ms < 3:
        return 0
    elif wind_speed_ms < 12:
        return 3000 * ((wind_speed_ms - 3) / 9) ** 3
    elif wind_speed_ms < 25:
        return 3000
    else:
        return 0


production_data = []
total_records = len(turbines_df) * len(wind_df)
count = 0

for _, turbine in turbines_df.iterrows():
    efficiency = turbine['efficiency_percent'] / 100

    for _, wind_row in wind_df.iterrows():
        ws = wind_row['wind_speed_ms']
        theoretical = power_curve(ws)
        actual = theoretical * efficiency * random.uniform(0.97, 1.03)
        actual = max(0, round(actual, 1))

        current_efficiency = round((actual / theoretical) * 100, 1) if theoretical > 0 else 0

        if efficiency < 0.65:
            status = "Failure"
        elif efficiency < 0.80:
            status = "Maintenance Required"
        else:
            status = "Good"

        production_data.append({
            'turbine_id': turbine['turbine_id'],
            'turbine_name': turbine['turbine_name'],
            'timestamp': wind_row['timestamp'],
            'wind_speed_ms': ws,
            'power_output_kw': actual,
            'theoretical_power_kw': round(theoretical, 1),
            'efficiency_percent': current_efficiency,
            'status': status
        })

        count += 1
        if count % 10000 == 0:
            print(f"   ... تم توليد {count} من {total_records} سجل")

production_df = pd.DataFrame(production_data)
production_df.to_csv('04_production_data.csv', index=False)
print(f"   ✅ تم حفظ 04_production_data.csv ({len(production_df)} صف)")

# 5. بيانات الصيانة
print("5. جاري توليد بيانات الصيانة...")

maintenance_data = []
for _, turbine in turbines_df.iterrows():
    turbine_prod = production_df[production_df['turbine_id'] == turbine['turbine_id']]
    avg_efficiency = turbine_prod['efficiency_percent'].mean()

    if avg_efficiency < 65:
        maint_type = "Urgent"
        days = random.randint(1, 2)
        priority = 1
        action = "Immediate inspection and repair required"
    elif avg_efficiency < 80:
        maint_type = "Required"
        days = random.randint(3, 7)
        priority = 2
        action = "Schedule maintenance within this week"
    elif avg_efficiency < 90:
        maint_type = "Periodic"
        days = random.randint(8, 20)
        priority = 3
        action = "Routine maintenance recommended"
    else:
        maint_type = "Good"
        days = random.randint(30, 60)
        priority = 4
        action = "No action needed, continue monitoring"

    maintenance_data.append({
        'turbine_id': turbine['turbine_id'],
        'turbine_name': turbine['turbine_name'],
        'maintenance_type': maint_type,
        'days_to_maintenance': days,
        'priority': priority,
        'avg_efficiency_percent': round(avg_efficiency, 1),
        'recommended_action': action
    })

maintenance_df = pd.DataFrame(maintenance_data)
maintenance_df.to_csv('05_maintenance_data.csv', index=False)
print(f"   ✅ تم حفظ 05_maintenance_data.csv ({len(maintenance_df)} صف)")

# ============================================
# عرض ملخص البيانات
# ============================================
print("\n" + "=" * 60)
print("✅ تم تصدير جميع البيانات بنجاح!")
print("=" * 60)
print("\n📁 الملفات المصدرة:")

import os

files = [
    '01_turbines_data.csv',
    '02_wind_speed_data.csv',
    '03_weather_data.csv',
    '04_production_data.csv',
    '05_maintenance_data.csv'
]

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024
        df = pd.read_csv(f)
        print(f"   📄 {f}: {len(df):,} صف | {size:.1f} KB")

print("\n📊 ملخص البيانات:")
print(f"   • عدد التوربينات: 38")
print(f"   • المدة الزمنية: 90 يوم (2,160 ساعة)")
print(f"   • إجمالي قراءات الإنتاج: 82,080")
print(f"   • إجمالي حجم البيانات: حوالي 20 ميجابايت")

print("\n✅ البيانات جاهزة للتسليم. الملفات موجودة في مجلد المشروع.")