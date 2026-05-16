# export_10days_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("=" * 60)
print("جاري توليد ملف بيانات 10 أيام")
print("=" * 60)

# ============================================
# 1. توليد بيانات التوربينات (38 توربين)
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
        'capacity_kw': 3000,
        'efficiency_base': round(efficiency, 3)
    })

# ============================================
# 2. توليد بيانات 10 أيام (240 ساعة)
# ============================================
days = 10
hours = days * 24  # 240 ساعة

# إنشاء التواريخ
start_date = datetime.now()
timestamps = []
for i in range(hours):
    ts = start_date - timedelta(hours=hours - i)
    timestamps.append(ts)

# توليد سرعة الرياح
shape, scale = 2.2, 8.5
wind_speed = np.random.weibull(shape, hours) * scale
wind_speed = np.clip(wind_speed, 0, 25)

# ============================================
# 3. إنشاء البيانات لكل توربين لكل ساعة
# ============================================
data = []

for turbine in turbines_list:
    for idx, ts in enumerate(timestamps):
        # تأثير موسمي
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

# ============================================
# 4. حفظ الملف
# ============================================
df = pd.DataFrame(data)
df.to_csv('wind_data_10days.csv', index=False)

# ============================================
# 5. عرض الملخص
# ============================================
print("\n✅ تم إنشاء الملف بنجاح!")
print("=" * 60)
print(f"\n📁 اسم الملف: wind_data_10days.csv")
print(f"📊 المدة الزمنية: 10 أيام (240 ساعة)")
print(f"📊 عدد التوربينات: 38 توربين")
print(f"📊 عدد الصفوف: {len(df):,} صف")
print(f"📊 عدد الأعمدة: {len(df.columns)} عمود")

print("\n📋 الأعمدة الموجودة في الملف:")
columns = ['timestamp', 'year', 'month', 'day', 'hour',
           'turbine_id', 'turbine_name',
           'wind_speed_ms', 'temperature_c',
           'humidity_percent', 'pressure_hpa',
           'actual_power_output_kw', 'turbine_status']

for i, col in enumerate(columns, 1):
    print(f"   {i}. {col}")

print("\n📊 عينة من البيانات (أول 5 صفوف):")
print(df.head().to_string())

print("\n✅ الملف جاهز للتسليم. موجود في مجلد المشروع.")