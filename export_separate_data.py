# export_separate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("=" * 60)
print("جاري توليد ملفات البيانات لفترات زمنية مختلفة")
print("=" * 60)

# ============================================
# 1. توليد بيانات التوربينات (ثابتة)
# ============================================
turbines_list = []
for i in range(1, 39):
    row = ((i - 1) // 7)
    col = ((i - 1) % 7)
    spacing = 0.008
    lat = 30.7040 + (row - 2.5) * spacing
    lon = 35.6930 + (col - 3) * spacing

    if i <= 2:
        efficiency = random.uniform(0.55, 0.65)
    elif i <= 5:
        efficiency = random.uniform(0.70, 0.80)
    else:
        efficiency = random.uniform(0.88, 0.97)

    turbines_list.append({
        'turbine_id': i,
        'turbine_name': f'Turbine_{i:02d}',
        'latitude': round(lat, 6),
        'longitude': round(lon, 6),
        'capacity_kw': 3000,
        'efficiency_base': round(efficiency, 3)
    })

turbines_df = pd.DataFrame(turbines_list)


# ============================================
# 2. دالة توليد البيانات لفترة زمنية معينة
# ============================================
def generate_data_for_period(days, start_date=None):
    """توليد بيانات كاملة لفترة زمنية محددة"""

    if start_date is None:
        start_date = datetime.now()

    hours = days * 24
    timestamps = []
    for i in range(hours):
        ts = start_date - timedelta(hours=hours - i)
        timestamps.append(ts)

    # توليد سرعة الرياح
    shape, scale = 2.2, 8.5
    wind_speed = np.random.weibull(shape, hours) * scale
    wind_speed = np.clip(wind_speed, 0, 25)

    data = []

    for turbine in turbines_list:
        for idx, ts in enumerate(timestamps):
            month = ts.month
            if month in [12, 1, 2]:
                seasonal = random.uniform(1.2, 1.4)
            elif month in [6, 7, 8]:
                seasonal = random.uniform(0.6, 0.8)
            else:
                seasonal = random.uniform(0.9, 1.1)

            ws = wind_speed[idx] * seasonal
            ws = round(max(0, min(ws, 25)), 2)

            # درجة الحرارة
            temp = round(22 - (ws * 0.3) + random.normalvariate(0, 2), 1)
            temp = max(5, min(40, temp))

            # الرطوبة
            humidity = round(70 - (temp - 20) * 1.2 + random.normalvariate(0, 5), 1)
            humidity = max(20, min(95, humidity))

            # الضغط الجوي
            pressure = round(1013 + random.normalvariate(0, 3), 1)

            # اتجاه الرياح
            wind_dir = round(random.uniform(0, 360), 1)

            # حساب الإنتاج
            def calc_power(w):
                if w < 3:
                    return 0
                elif w < 12:
                    return 3000 * ((w - 3) / 9) ** 3
                elif w < 25:
                    return 3000
                else:
                    return 0

            theoretical = calc_power(ws)
            actual = theoretical * turbine['efficiency_base'] * random.uniform(0.97, 1.03)
            actual = max(0, round(actual, 1))

            if theoretical > 0:
                operating_efficiency = round((actual / theoretical) * 100, 1)
            else:
                operating_efficiency = 0

            # حالة التوربين
            if turbine['efficiency_base'] < 0.65:
                status = "Failure"
            elif turbine['efficiency_base'] < 0.80:
                status = "Maintenance Required"
            else:
                status = "Good"

            data.append({
                'timestamp': ts.strftime('%Y-%m-%d %H:00:00'),
                'year': ts.year,
                'month': ts.month,
                'day': ts.day,
                'hour': ts.hour,
                'turbine_id': turbine['turbine_id'],
                'turbine_name': turbine['turbine_name'],
                'wind_speed_ms': ws,
                'temperature_c': temp,
                'humidity_percent': humidity,
                'pressure_hpa': pressure,
                'actual_power_output_kw': actual,
                'turbine_status': status
            })

    return pd.DataFrame(data)


# ============================================
# 3. إنشاء الملفات
# ============================================

# ملف يوم واحد (24 ساعة)
print("\n📁 جاري إنشاء ملف يوم واحد...")
df_1day = generate_data_for_period(1)
df_1day.to_csv('wind_data_1day.csv', index=False)
print(f"   ✅ wind_data_1day.csv: {len(df_1day):,} صف | {len(df_1day.columns)} عمود")

# ملف 5 أيام (120 ساعة)
print("\n📁 جاري إنشاء ملف 5 أيام...")
df_5days = generate_data_for_period(5)
df_5days.to_csv('wind_data_5days.csv', index=False)
print(f"   ✅ wind_data_5days.csv: {len(df_5days):,} صف | {len(df_5days.columns)} عمود")

# ملف 90 يوم (الأصلي)
print("\n📁 جاري إنشاء ملف 90 يوم...")
df_90days = generate_data_for_period(90)
df_90days.to_csv('wind_data_90days.csv', index=False)
print(f"   ✅ wind_data_90days.csv: {len(df_90days):,} صف | {len(df_90days.columns)} عمود")

# ============================================
# 4. عرض الملخص
# ============================================
print("\n" + "=" * 60)
print("✅ تم إنشاء جميع الملفات بنجاح!")
print("=" * 60)

print("\n📁 الملفات التي تم إنشاؤها:")

import os

files = [
    ('wind_data_1day.csv', 'يوم واحد (24 ساعة)'),
    ('wind_data_5days.csv', '5 أيام (120 ساعة)'),
    ('wind_data_90days.csv', '90 يوم (2,160 ساعة)')
]

for fname, desc in files:
    if os.path.exists(fname):
        size = os.path.getsize(fname) / 1024
        df = pd.read_csv(fname)
        print(f"\n   📄 {fname}")
        print(f"      📊 {desc}")
        print(f"      📊 عدد الصفوف: {len(df):,}")
        print(f"      📊 عدد الأعمدة: {len(df.columns)}")
        print(f"      💾 حجم الملف: {size:.1f} KB")

print("\n📋 الأعمدة الموجودة في جميع الملفات:")
columns = ['timestamp', 'year', 'month', 'day', 'hour', 'turbine_id', 'turbine_name',
           'wind_speed_ms', 'temperature_c', 'humidity_percent', 'pressure_hpa',
           'actual_power_output_kw', 'turbine_status']

for i, col in enumerate(columns, 1):
    print(f"   {i}. {col}")

print("\n✅ جميع الملفات جاهزة للتسليم. موجودة في مجلد المشروع.")