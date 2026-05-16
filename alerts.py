# alerts.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


class AlertSystem:
    def __init__(self):
        self.alerts = []

    def detect_failures(self, turbine_data, production_df, maintenance_df, current_weather):
        alerts = []

        for _, turbine in turbine_data.iterrows():
            turbine_id = turbine['turbine_id']
            turbine_prod = production_df[production_df['turbine_id'] == turbine_id]

            if len(turbine_prod) == 0:
                continue

            latest = turbine_prod.iloc[-1]
            efficiency = latest['efficiency_percent']
            power_output = latest['power_output_kw']
            theoretical_power = latest.get('theoretical_power',
                                           power_output / (efficiency / 100) if efficiency > 0 else 0)

            # كشف الأعطال الفورية
            if power_output == 0 and current_weather['wind_speed'] > 5:
                alerts.append({
                    'turbine_id': turbine_id,
                    'turbine_name': turbine['name'],
                    'type': 'immediate',
                    'severity': 'critical',
                    'message': f'⚠️ عطل فوري في التوربين {turbine["name"]} - انقطاع كامل مع وجود رياح',
                    'cause': 'احتمال عطل في المولد أو نظام التحكم',
                    'action': 'أوقف التوربين فوراً وأرسل فريق صيانة طارئ',
                    'affected_components': ['مولد', 'نظام تحكم', 'كابلات']
                })
            elif efficiency < 50 and power_output > 0:
                alerts.append({
                    'turbine_id': turbine_id,
                    'turbine_name': turbine['name'],
                    'type': 'immediate',
                    'severity': 'high',
                    'message': f'⚠️ كفاءة منخفضة جداً في التوربين {turbine["name"]} - {efficiency:.0f}%',
                    'cause': 'احتمال تلف في الشفرات أو نظام التوجيه',
                    'action': 'افحص التوربين خلال 24 ساعة',
                    'affected_components': ['شفرات', 'نظام توجيه', 'محامل']
                })
            elif 50 <= efficiency < 70:
                alerts.append({
                    'turbine_id': turbine_id,
                    'turbine_name': turbine['name'],
                    'type': 'upcoming',
                    'severity': 'medium',
                    'message': f'⚠️ تحذير: كفاءة منخفضة في التوربين {turbine["name"]} - {efficiency:.0f}%',
                    'cause': 'تراكم الغبار أو تآكل بسيط في المكونات',
                    'action': 'جدول صيانة خلال 3 أيام',
                    'affected_components': ['شفرات', 'فلتر هواء']
                })

        # تنبيهات الطقس
        if current_weather['wind_speed'] > 20:
            alerts.append({
                'turbine_id': None,
                'turbine_name': 'جميع التوربينات',
                'type': 'weather',
                'severity': 'high' if current_weather['wind_speed'] > 25 else 'medium',
                'message': f'🌪️ رياح قوية - السرعة {current_weather["wind_speed"]:.1f} م/ث',
                'cause': 'ظروف جوية قاسية',
                'action': 'استعد لإيقاف التوربينات إذا تجاوزت السرعة 25 م/ث',
                'affected_components': ['جميع المكونات']
            })

        if current_weather['temperature'] > 40:
            alerts.append({
                'turbine_id': None,
                'turbine_name': 'جميع التوربينات',
                'type': 'weather',
                'severity': 'medium',
                'message': f'🔥 حرارة مرتفعة - {current_weather["temperature"]:.0f}°C',
                'cause': 'موجة حر',
                'action': 'راقب درجة حرارة المحولات والمولدات',
                'affected_components': ['محولات', 'مولدات']
            })

        return alerts

    def get_priority_alerts(self, alerts):
        priority_order = {'critical': 1, 'high': 2, 'medium': 3, 'low': 4}
        return sorted(alerts, key=lambda x: priority_order.get(x['severity'], 5))

    def display_alerts(self, alerts):
        if not alerts:
            st.success("✅ لا توجد أعطال أو تنبيهات - جميع التوربينات تعمل بشكل طبيعي")
            return

        sorted_alerts = self.get_priority_alerts(alerts)

        for alert in sorted_alerts:
            if alert['severity'] == 'critical':
                st.error(f"🚨 {alert['message']}")
            elif alert['severity'] == 'high':
                st.error(f"⚠️ {alert['message']}")
            elif alert['severity'] == 'medium':
                st.warning(f"⚠️ {alert['message']}")
            else:
                st.info(f"ℹ️ {alert['message']}")

            with st.expander(f"🔍 تفاصيل - {alert['turbine_name']}"):
                st.markdown(f"**السبب المحتمل:** {alert['cause']}")
                st.markdown(f"**الإجراء الموصى به:** {alert['action']}")
                st.markdown(f"**المكونات المتأثرة:** {', '.join(alert['affected_components'])}")