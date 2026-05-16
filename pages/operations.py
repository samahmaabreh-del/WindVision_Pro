# pages/operations.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def show_operations(production_df, turbines_df, current_weather, models, turbine_specs):
    lang = st.session_state.get('lang', 'en')

    if lang == 'ar':
        st.title("⚙️ قسم التشغيل")
        st.markdown("مراقبة فورية والتحكم في الإنتاج")
        total_text = "إجمالي الإنتاج"
        avg_text = "متوسط الكفاءة"
        active_text = "التوربينات النشطة"
        wind_text = "سرعة الرياح الحالية"
        curve_title = "📊 منحنى قدرة التوربين"
        specs_title = "📋 المواصفات الفنية"
        ranking_title = "🏆 ترتيب أداء التوربينات"
        param_text = "الخاصية"
        value_text = "القيمة"
    else:
        st.title("⚙️ Operations Department")
        st.markdown("Real-time monitoring and production control")
        total_text = "Total Power Output"
        avg_text = "Average Efficiency"
        active_text = "Active Turbines"
        wind_text = "Current Wind Speed"
        curve_title = "📊 Wind Turbine Power Curve"
        specs_title = "📋 Technical Specifications"
        ranking_title = "🏆 Turbine Performance Ranking"
        param_text = "Parameter"
        value_text = "Value"

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    total_power = production_df['power_output_kw'].sum() / 1000
    avg_eff = production_df['efficiency_percent'].mean()
    active = len(production_df[production_df['power_output_kw'] > 0]['turbine_id'].unique())
    total = len(turbines_df)

    with col1:
        st.metric(total_text, f"{total_power:.1f} MWh")
    with col2:
        st.metric(avg_text, f"{avg_eff:.1f}%")
    with col3:
        st.metric(active_text, f"{active} / {total}")
    with col4:
        st.metric(wind_text, f"{current_weather['wind_speed']:.1f} m/s")

    st.markdown("---")

    st.subheader(curve_title)
    wind_speeds = list(range(0, 31))
    powers = [models.power_curve(w) for w in wind_speeds]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wind_speeds, y=powers, mode='lines+markers', line=dict(color='#0a5c2e', width=3)))
    fig.add_vline(x=3, line_dash="dash", line_color="gray", annotation_text="Cut-in: 3 m/s")
    fig.add_vline(x=12, line_dash="dash", line_color="blue", annotation_text="Rated: 12 m/s")
    fig.add_vline(x=25, line_dash="dash", line_color="red", annotation_text="Cut-out: 25 m/s")
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander(specs_title):
        specs = pd.DataFrame([
            ("Manufacturer", turbine_specs['manufacturer']),
            ("Model", turbine_specs['model']),
            ("Rated Power", f"{turbine_specs['rated_power_kw'] / 1000:.1f} MW"),
            ("Rotor Diameter", f"{turbine_specs['rotor_diameter_m']} m"),
            ("Hub Height", f"{turbine_specs['hub_height_m']} m"),
            ("Cut-in Speed", f"{turbine_specs['cut_in_wind_speed_ms']} m/s"),
            ("Rated Speed", f"{turbine_specs['rated_wind_speed_ms']} m/s"),
            ("Cut-out Speed", f"{turbine_specs['cut_out_wind_speed_ms']} m/s")
        ], columns=[param_text, value_text])
        st.dataframe(specs, hide_index=True, use_container_width=True)