# storm_prediction.py
import numpy as np
from datetime import datetime, timedelta


class StormPredictor:
    def __init__(self):
        self.thresholds = {
            'warning': 20,
            'danger': 25,
            'critical': 30
        }

    def predict_storm(self, current_wind_speed, wind_forecast, pressure_trend):
        if current_wind_speed >= self.thresholds['critical']:
            severity = "critical"
            message = "🚨 خطر شديد! عاصفة خطيرة - أوقف جميع التوربينات فوراً"
            action = "STOP_ALL"
        elif current_wind_speed >= self.thresholds['danger']:
            severity = "danger"
            message = "⚠️ خطر! عاصفة قوية - استعد لإيقاف التوربينات"
            action = "PREPARE_STOP"
        elif current_wind_speed >= self.thresholds['warning']:
            severity = "warning"
            message = "⚡ تحذير! عاصفة متوقعة - راقب التوربينات عن كثب"
            action = "MONITOR"
        else:
            severity = "normal"
            message = "✅ لا توجد عواصف متوقعة - التشغيل طبيعي"
            action = "NORMAL"

        time_to_storm = self._estimate_time_to_storm(wind_forecast) if wind_forecast else None
        affected_turbines = self._get_affected_turbines(current_wind_speed)

        return {
            'severity': severity,
            'message': message,
            'action': action,
            'time_to_storm': time_to_storm,
            'affected_turbines': affected_turbines,
            'recommendations': self._get_recommendations(severity)
        }

    def _estimate_time_to_storm(self, wind_forecast):
        for forecast in wind_forecast:
            if forecast['wind_speed'] >= self.thresholds['warning']:
                time_diff = forecast['timestamp'] - datetime.now()
                return time_diff.total_seconds() / 3600
        return None

    def _get_affected_turbines(self, wind_speed):
        if wind_speed > 25:
            return "جميع التوربينات"
        elif wind_speed > 20:
            return "التوربينات في المناطق المكشوفة"
        else:
            return "لا توجد توربينات معرضة للخطر"

    def _get_recommendations(self, severity):
        recommendations = {
            'normal': ["استمر في التشغيل العادي", "راقب توقعات الطقس بانتظام"],
            'warning': ["قلل الإنتاج إلى 80% من القدرة", "جهز فرق الطوارئ", "راجع إجراءات السلامة"],
            'danger': ["أوقف التوربينات تدريجياً", "أبلغ غرفة التحكم", "فعّل خطة الطوارئ"],
            'critical': ["أوقف جميع التوربينات فوراً", "أخل المنطقة", "فعّل نظام الإنذار العام"]
        }
        return recommendations.get(severity, [])