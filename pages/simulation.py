# pages/simulation.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime


def show_simulation(turbines_df, production_df, models, current_weather, turbine_specs):
    lang = st.session_state.get('lang', 'en')

    # ========== النصوص المترجمة ==========
    if lang == 'ar':
        title = "🎮 محاكاة مزرعة الرياح"
        subtitle = "جرب سيناريوهات مختلفة وشاهد تأثيرها على إنتاج الطاقة"
        controls = "⚙️ إعدادات المحاكاة"
        scenario_text = "اختر السيناريو"
        normal_text = "تشغيل عادي"
        failure_text = "عطل توربين"
        wind_change_text = "تغير سرعة الرياح"
        dust_text = "عاصفة ترابية"
        add_text = "إضافة توربينات جديدة"
        drop_text = "انخفاض الكفاءة"
        wind_analysis = "🌬️ تحليل سرعة الرياح"
        normal_speed = "السرعة الطبيعية"
        current_speed = "السرعة الحالية"
        cut_out = "سرعة الإيقاف"
        max_survival = "الحد الأقصى للتحمل"
        results = "📊 نتائج المحاكاة"
        active_text = "التوربينات النشطة"
        total_text = "الإنتاج الكلي"
        comparison = "📊 مقارنة الإنتاج"
        impact = "📋 تحليل التأثير"
        financial = "التأثير المالي"
        co2 = "تأثير CO₂"
        recommendations = "💡 التوصيات"
    else:
        title = "🎮 Wind Farm Simulation"
        subtitle = "Test different scenarios and see their impact on energy production"
        controls = "⚙️ Simulation Controls"
        scenario_text = "Select Scenario"
        normal_text = "Normal Operation"
        failure_text = "Turbine Failure"
        wind_change_text = "Wind Speed Change"
        dust_text = "Dust Storm"
        add_text = "Add New Turbines"
        drop_text = "Efficiency Drop"
        wind_analysis = "🌬️ Wind Speed Analysis"
        normal_speed = "Normal Speed"
        current_speed = "Current Speed"
        cut_out = "Cut-out Speed"
        max_survival = "Max Survival"
        results = "📊 Simulation Results"
        active_text = "Active Turbines"
        total_text = "Total Production"
        comparison = "📊 Production Comparison"
        impact = "📋 Impact Analysis"
        financial = "Financial Impact"
        co2 = "CO₂ Impact"
        recommendations = "💡 Recommendations"

    st.title(title)
    st.markdown(subtitle)
    st.markdown("---")

    st.sidebar.header(controls)

    scenario = st.sidebar.selectbox(scenario_text,
                                    [normal_text, failure_text, wind_change_text, dust_text, add_text, drop_text])

    normal_wind = current_weather['wind_speed']
    normal_temp = current_weather['temperature']
    normal_humidity = current_weather['humidity']
    normal_pressure = current_weather['pressure']

    wind_speed = normal_wind
    efficiency_factor = 1.0
    active_turbines = len(turbines_df)

    cut_in = turbine_specs['cut_in_wind_speed_ms']
    rated_speed = turbine_specs['rated_wind_speed_ms']
    cut_out_speed = turbine_specs['cut_out_wind_speed_ms']
    max_survival_speed = turbine_specs['max_survival_wind_speed_ms']

    if scenario == failure_text:
        st.warning("⚠️ Turbine Failure Mode" if lang == 'en' else "⚠️ وضع عطل التوربين")
        failed = st.sidebar.number_input("Number of failed turbines" if lang == 'en' else "عدد التوربينات المعطلة", 1,
                                         10, 1)
        active_turbines = len(turbines_df) - failed
        st.info(f"❌ {failed} turbine(s) out of service" if lang == 'en' else f"❌ {failed} توربين خارج الخدمة")

    elif scenario == wind_change_text:
        st.info("💨 Wind Speed Adjustment" if lang == 'en' else "💨 تعديل سرعة الرياح")
        wind_speed = st.sidebar.slider("Wind Speed (m/s)" if lang == 'en' else "سرعة الرياح (م/ث)", 0.0, 60.0,
                                       normal_wind, 0.5)

        st.markdown("---")
        st.markdown(wind_analysis)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(normal_speed, f"{normal_wind:.1f} m/s")
        with c2:
            st.metric(current_speed, f"{wind_speed:.1f} m/s", delta=f"{wind_speed - normal_wind:.1f}")
        with c3:
            st.metric(cut_out, f"{cut_out_speed} m/s")
        with c4:
            st.metric(max_survival, f"{max_survival_speed} m/s")

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=wind_speed,
            title={'text': "Wind Speed (m/s)"},
            delta={'reference': normal_wind},
            gauge={
                'axis': {'range': [0, 60]},
                'bar': {'color': "#0a5c2e"},
                'steps': [
                    {'range': [0, cut_in], 'color': "lightgray"},
                    {'range': [cut_in, rated_speed], 'color': "lightgreen"},
                    {'range': [rated_speed, cut_out_speed], 'color': "green"},
                    {'range': [cut_out_speed, max_survival_speed], 'color': "orange"},
                    {'range': [max_survival_speed, 60], 'color': "red"}
                ],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.9, 'value': cut_out_speed}
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        if wind_speed > cut_out_speed:
            st.error(
                f"🚨 WARNING: Wind speed exceeds cut-out speed! Turbines STOP. Production = ZERO" if lang == 'en' else f"🚨 تحذير: سرعة الرياح تتجاوز حد الإيقاف! التوربينات تتوقف. الإنتاج = صفر")
            active_turbines = 0

    elif scenario == dust_text:
        st.error("🌪️ Dust Storm Mode" if lang == 'en' else "🌪️ وضع العاصفة الترابية")
        dust = st.sidebar.slider("Dust Level (%)" if lang == 'en' else "مستوى الغبار (%)", 0, 100, 50)
        efficiency_factor = 1 - (dust / 100) * 0.6
        st.warning(
            f"Efficiency reduced to {efficiency_factor * 100:.0f}%" if lang == 'en' else f"الكفاءة انخفضت إلى {efficiency_factor * 100:.0f}%")

    elif scenario == add_text:
        st.success("➕ Expansion Mode" if lang == 'en' else "➕ وضع التوسع")
        new = st.sidebar.number_input("New turbines to add" if lang == 'en' else "توربينات جديدة للإضافة", 1, 20, 3)
        active_turbines = len(turbines_df) + new
        st.info(
            f"Adding {new} new turbines. Total: {active_turbines}" if lang == 'en' else f"إضافة {new} توربين جديد. الإجمالي: {active_turbines}")

    elif scenario == drop_text:
        st.warning("📉 General Efficiency Drop" if lang == 'en' else "📉 انخفاض عام في الكفاءة")
        efficiency_factor = st.sidebar.slider("Efficiency (%)" if lang == 'en' else "الكفاءة (%)", 30, 100, 80) / 100
        st.info(
            f"All turbines at {efficiency_factor * 100:.0f}% efficiency" if lang == 'en' else f"جميع التوربينات بكفاءة {efficiency_factor * 100:.0f}%")

    sample = turbines_df.iloc[0]

    if wind_speed > cut_out_speed:
        total = 0
    else:
        base = models.predict_production(sample['turbine_id'], wind_speed, normal_temp, normal_humidity,
                                         normal_pressure, datetime.now().hour, datetime.now().month)
        total = base * active_turbines * efficiency_factor / 1000

    normal_base = models.predict_production(sample['turbine_id'], normal_wind, normal_temp, normal_humidity,
                                            normal_pressure, datetime.now().hour, datetime.now().month)
    normal_total = normal_base * len(turbines_df) / 1000

    diff = total - normal_total
    diff_percent = (diff / normal_total) * 100 if normal_total > 0 else 0

    st.markdown("---")
    st.header(results)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(current_speed if lang == 'en' else "سرعة الرياح", f"{wind_speed:.1f} m/s",
                  delta=f"{wind_speed - normal_wind:.1f}")
    with c2:
        st.metric(active_text, f"{active_turbines} / {len(turbines_df)}")
    with c3:
        st.metric(total_text, f"{total:.1f} MW")

    st.subheader(comparison)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Normal' if lang == 'en' else 'طبيعي', 'Simulation' if lang == 'en' else 'محاكاة'],
                         y=[normal_total, total], marker_color=['#2a5298', '#f5576c'], width=[0.3, 0.3]))
    fig.update_layout(title="Normal vs Simulation Production" if lang == 'en' else "الإنتاج الطبيعي مقابل المحاكاة",
                      yaxis_title="Production (MW)" if lang == 'en' else "الإنتاج (ميجاواط)", height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(impact)

    loss = abs(diff)
    c1, c2 = st.columns(2)
    with c1:
        if diff > 0:
            st.success(
                f"📈 Production Increase: +{diff:.1f} MW (+{diff_percent:.1f}%)" if lang == 'en' else f"📈 زيادة في الإنتاج: +{diff:.1f} ميجاواط (+{diff_percent:.1f}%)")
        elif diff < 0:
            st.error(
                f"📉 Production Decrease: {diff:.1f} MW ({diff_percent:.1f}%)" if lang == 'en' else f"📉 انخفاض في الإنتاج: {diff:.1f} ميجاواط ({diff_percent:.1f}%)")
        else:
            st.info("No change in production" if lang == 'en' else "لا تغيير في الإنتاج")
    with c2:
        st.metric(financial, f"${loss * 120:,.0f} per hour" if lang == 'en' else f"${loss * 120:,.0f} لكل ساعة")
        st.metric(co2, f"{loss * 0.55:.1f} tons per hour" if lang == 'en' else f"{loss * 0.55:.1f} طن لكل ساعة")

    st.markdown("---")
    st.header(recommendations)

    if wind_speed < cut_in:
        st.warning(
            f"🔴 Wind speed too low ({wind_speed:.1f} m/s). No power generation." if lang == 'en' else f"🔴 سرعة الرياح منخفضة جداً ({wind_speed:.1f} م/ث). لا يوجد توليد.")
    elif wind_speed > cut_out_speed:
        st.error(
            f"🔴 CRITICAL: Wind speed exceeds cut-out limit. Turbines stopped." if lang == 'en' else f"🔴 خطير: سرعة الرياح تتجاوز حد الإيقاف. التوربينات متوقفة.")
    elif efficiency_factor < 0.7:
        st.warning(
            f"⚠️ Low efficiency ({efficiency_factor * 100:.0f}%). Schedule cleaning." if lang == 'en' else f"⚠️ كفاءة منخفضة ({efficiency_factor * 100:.0f}%). جدول تنظيف.")
    else:
        st.success("✅ Normal operation. Continue monitoring." if lang == 'en' else "✅ تشغيل طبيعي. استمر في المراقبة.")