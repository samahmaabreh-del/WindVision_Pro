# export_complete_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("جاري توليد البيانات الكاملة للمشروع...")

# ============================================
# 1. توليد بيانات التوربينات الأساسية
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
# 2. توليد بيانات الزمن (90 يوم × 24 ساعة)
# ============================================
days = 90
hours = days * 24
timestamps = []
current = datetime.now()
for i in range(hours):
    ts = current - timedelta(hours=hours - i)
    timestamps.append(ts)

# ============================================
# 3. توليد سرعة الرياح (Weibull distribution)
# ============================================
shape, scale = 2.2, 8.5
wind_speed = np.random.weibull(shape, hours) * scale
wind_speed = np.clip(wind_speed, 0, 25)

# ============================================
# 4. إنشاء DataFrame واحد جامع
# ============================================
print("جاري بناء قاعدة البيانات المتكاملة...")

complete_data = []

for turbine in turbines_list:
    for idx, ts in enumerate(timestamps):
        # سرعة الرياح مع تأثير موسمي
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


        # حساب الإنتاج (Power Curve)
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

        # كفاءة التشغيل
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

        complete_data.append({
            # معلومات الزمن
            'timestamp': ts.strftime('%Y-%m-%d %H:00:00'),
            'year': ts.year,
            'month': ts.month,
            'day': ts.day,
            'hour': ts.hour,
            'season': 'Winter' if ts.month in [12, 1, 2] else 'Spring' if ts.month in [3, 4,
                                                                                       5] else 'Summer' if ts.month in [
                6, 7, 8] else 'Autumn',

            # معلومات التوربين
            'turbine_id': turbine['turbine_id'],
            'turbine_name': turbine['turbine_name'],
            'latitude': turbine['latitude'],
            'longitude': turbine['longitude'],
            'capacity_kw': turbine['capacity_kw'],
            'efficiency_base': turbine['efficiency_base'],

            # بيانات الطقس
            'wind_speed_ms': ws,
            'wind_direction_deg': wind_dir,
            'temperature_c': temp,
            'humidity_percent': humidity,
            'pressure_hpa': pressure,

            # بيانات الإنتاج
            'theoretical_power_kw': round(theoretical, 1),
            'actual_power_output_kw': actual,
            'operating_efficiency_percent': operating_efficiency,

            # حالة التوربين والصيانة
            'turbine_status': status,
            'maintenance_priority': 1 if status == "Failure" else 2 if status == "Maintenance Required" else 4,
        })

# ============================================
# 5. تحويل إلى DataFrame وحفظ
# ============================================
df = pd.DataFrame(complete_data)


# إضافة عمود الصيانة الموصى بها
def get_maintenance_action(status):
    if status == "Failure":
        return "Immediate repair required"
    elif status == "Maintenance Required":
        return "Schedule maintenance within 3-7 days"
    else:
        return "Continue regular monitoring"


df['recommended_action'] = df['turbine_status'].apply(get_maintenance_action)

# حفظ الملف
df.to_csv('wind_farm_complete_data.csv', index=False)

# ============================================
# 6. عرض الملخص
# ============================================
print("\n" + "=" * 60)
print("✅ تم إنشاء الملف الجامع بنجاح!")
print("=" * 60)
print(f"\n📁 اسم الملف: wind_farm_complete_data.csv")
print(f"📊 عدد الصفوف: {len(df):,} صف")
print(f"📊 عدد الأعمدة: {len(df.columns)} عمود")
print(f"📊 حجم الملف: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

print("\n📋 الأعمدة الموجودة في الملف:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

print("\n📊 عينة من البيانات (أول 5 صفوف):")
print(df.head().to_string())

print("\n✅ الملف جاهز للتسليم. موجود في مجلد المشروع.")