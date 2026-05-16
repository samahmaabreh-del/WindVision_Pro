# dust_analysis.py
import numpy as np
import pandas as pd


class DustAnalyzer:
    def __init__(self):
        self.dust_coefficients = {
            'low': {'efficiency_loss': 0.03, 'accumulation_rate': 0.5},
            'medium': {'efficiency_loss': 0.10, 'accumulation_rate': 1.0},
            'high': {'efficiency_loss': 0.20, 'accumulation_rate': 2.0},
            'storm': {'efficiency_loss': 0.40, 'accumulation_rate': 5.0}
        }

    def analyze_dust_impact(self, wind_speed, dust_level, days_since_cleaning):
        if dust_level > 80:
            dust_category = 'storm'
        elif dust_level > 50:
            dust_category = 'high'
        elif dust_level > 20:
            dust_category = 'medium'
        else:
            dust_category = 'low'

        efficiency_loss = self.dust_coefficients[dust_category]['efficiency_loss']
        accumulation_factor = min(days_since_cleaning / 30, 1)
        total_loss = efficiency_loss * (1 + accumulation_factor)
        total_loss = min(total_loss, 0.60)

        if wind_speed > 15:
            cleaning_effect = min((wind_speed - 15) / 10, 0.3)
            total_loss = max(total_loss - cleaning_effect, 0)

        affected_turbines = self._get_affected_turbines(dust_category)

        return {
            'dust_category': dust_category,
            'dust_level': dust_level,
            'efficiency_loss_percent': total_loss * 100,
            'affected_turbines': affected_turbines,
            'recommendation': self._get_cleaning_recommendation(total_loss, days_since_cleaning)
        }

    def _get_affected_turbines(self, dust_category):
        if dust_category == 'storm':
            return "جميع التوربينات - تأثير شديد"
        elif dust_category == 'high':
            return "التوربينات في المناطق المكشوفة - تأثير كبير"
        elif dust_category == 'medium':
            return "التوربينات الأقرب للمصادر - تأثير متوسط"
        else:
            return "تأثير بسيط على جميع التوربينات"

    def _get_cleaning_recommendation(self, efficiency_loss, days_since_cleaning):
        if efficiency_loss > 0.3:
            return "🔴 تنظيف عاجل - فقدان كبير في الكفاءة"
        elif efficiency_loss > 0.15:
            return "🟠 تنظيف مطلوب - جدول تنظيف خلال 3 أيام"
        elif efficiency_loss > 0.05:
            return "🟡 تنظيف دوري - جدول تنظيف خلال أسبوع"
        else:
            return "🟢 كفاءة جيدة - لا حاجة للتنظيف حالياً"

    def predict_dust_accumulation(self, days=30):
        month = pd.Timestamp.now().month
        if month in [6, 7, 8, 9]:
            daily_accumulation = 1.5
        elif month in [3, 4, 5, 10]:
            daily_accumulation = 1.0
        else:
            daily_accumulation = 0.5

        accumulation = [min(daily_accumulation * i, 60) for i in range(days + 1)]

        return {
            'daily_accumulation_rate': daily_accumulation,
            'days_to_cleaning': 30 / daily_accumulation if daily_accumulation > 0 else 30,
            'projected_accumulation': accumulation
        }