# pages/planning.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta


def show_planning(production_df, turbines_df, models, turbine_specs, wind_df):
    st.title("📊 Planning Department")
    st.markdown("Production forecasting and expansion planning")
    st.markdown("---")

    # Production Forecast
    st.subheader("📈 Production Forecast")

    col1, col2 = st.columns(2)

    # Calculate forecasts
    daily_production = production_df['power_output_kw'].sum() / 1000 / 24
    monthly_production = daily_production * 30
    yearly_production = daily_production * 365

    with col1:
        st.metric("Daily Production", f"{daily_production:.1f} MWh")
        st.metric("Monthly Production", f"{monthly_production:.1f} MWh")
    with col2:
        st.metric("Yearly Production", f"{yearly_production:.1f} MWh")
        st.metric("CO₂ Saved (Yearly)", f"{yearly_production * 0.55:.0f} tons")

    st.markdown("---")

    # 7-Day Forecast Chart
    st.subheader("📊 7-Day Production Forecast")

    # Generate forecast data
    dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    forecast_values = []

    for i in range(7):
        # Simulate forecast based on historical patterns
        forecast = daily_production * np.random.uniform(0.7, 1.3)
        forecast_values.append(forecast)

    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=dates,
        y=forecast_values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#0a5c2e', width=3),
        marker=dict(size=10, color='#0a5c2e')
    ))

    # Add confidence interval
    fig_forecast.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=[v * 1.15 for v in forecast_values] + [v * 0.85 for v in forecast_values[::-1]],
        fill='toself',
        fillcolor='rgba(10, 92, 46, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval (85-115%)'
    ))

    fig_forecast.update_layout(
        title="Next 7 Days Production Forecast",
        xaxis_title="Date",
        yaxis_title="Production (MWh)",
        height=450
    )
    st.plotly_chart(fig_forecast, use_container_width=True)

    st.markdown("---")

    # Expansion Planning - Add New Turbines
    st.subheader("➕ Expansion Planning - Add New Turbines")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        new_turbines = st.number_input("Number of new turbines to evaluate", 1, 10, 3)

        # Wind speed at new location
        new_location_wind = st.slider("Expected wind speed at new location (m/s)", 5.0, 15.0, 8.5, 0.5)

        if st.button("🔍 Find Best Locations", type="primary"):
            st.session_state['analyze_locations'] = True
            st.session_state['new_turbines'] = new_turbines
            st.session_state['new_wind_speed'] = new_location_wind

    with col_right:
        st.info("""
        **Site Selection Criteria:**
        - Wind speed > 7 m/s
        - Distance from existing turbines > 500m
        - Access to grid connection
        - Land availability
        - Environmental impact assessment
        """)

    if st.session_state.get('analyze_locations', False):
        st.markdown("---")
        st.subheader("📍 Recommended Locations")

        # Tafila farm center
        center_lat = 30.7040
        center_lon = 35.6930

        # Generate potential sites
        potential_sites = []
        for i in range(st.session_state['new_turbines']):
            angle = i * (360 / st.session_state['new_turbines'])
            distance = 0.015 + (i * 0.005)
            lat = center_lat + distance * np.cos(np.radians(angle))
            lon = center_lon + distance * np.sin(np.radians(angle))

            # Calculate expected production
            expected_power = models.power_curve(st.session_state['new_wind_speed'])
            expected_production_mwh = expected_power * 24 / 1000

            potential_sites.append({
                'site_id': i + 1,
                'lat': lat,
                'lon': lon,
                'expected_power_kw': expected_power,
                'expected_production_mwh': expected_production_mwh,
                'efficiency': np.random.uniform(85, 95),
                'priority_score': np.random.uniform(60, 100)
            })

        # Sort by priority
        potential_sites.sort(key=lambda x: x['priority_score'], reverse=True)

        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

        # Existing turbines
        for _, turbine in turbines_df.iterrows():
            folium.Marker(
                location=[turbine['lat'], turbine['lon']],
                popup=f"Existing: {turbine['name']}",
                icon=folium.Icon(color='green', icon='ok-sign', prefix='glyphicon')
            ).add_to(m)

        # Potential sites
        for site in potential_sites:
            if site['site_id'] == 1:
                color = 'red'
                icon = 'star'
            else:
                color = 'orange'
                icon = 'plus-sign'

            popup_text = f"""
            <b>Site {site['site_id']}</b><br>
            ⚡ Expected Power: {site['expected_power_kw'] / 1000:.2f} MW<br>
            📊 Expected Daily: {site['expected_production_mwh']:.1f} MWh<br>
            🎯 Priority Score: {site['priority_score']:.0f}%
            """

            folium.Marker(
                location=[site['lat'], site['lon']],
                popup=folium.Popup(popup_text, max_width=250),
                icon=folium.Icon(color=color, icon=icon, prefix='fa')
            ).add_to(m)

        folium_static(m, width=700, height=500)

        # Display comparison table
        st.subheader("📊 Site Comparison")

        comparison_df = pd.DataFrame(potential_sites)
        comparison_df = comparison_df[[
            'site_id', 'expected_power_kw', 'expected_production_mwh',
            'efficiency', 'priority_score'
        ]]
        comparison_df.columns = [
            'Site ID', 'Expected Power (kW)', 'Expected Daily (MWh)',
            'Efficiency (%)', 'Priority Score (%)'
        ]
        comparison_df['Expected Power (MW)'] = comparison_df['Expected Power (kW)'] / 1000

        st.dataframe(comparison_df, use_container_width=True)

        # Best site recommendation
        best_site = potential_sites[0]
        st.success(f"""
        🏆 **BEST LOCATION RECOMMENDATION: Site {best_site['site_id']}**

        - Expected Power Output: {best_site['expected_power_kw'] / 1000:.2f} MW
        - Expected Daily Production: {best_site['expected_production_mwh']:.1f} MWh
        - Expected Yearly Production: {best_site['expected_production_mwh'] * 365:.0f} MWh
        - Priority Score: {best_site['priority_score']:.0f}%
        """)

        # Bar chart comparison
        fig_compare = px.bar(
            comparison_df,
            x='Site ID',
            y='Expected Daily (MWh)',
            title='Expected Daily Production by Site',
            color='Priority Score (%)',
            color_continuous_scale='Viridis',
            labels={'Expected Daily (MWh)': 'Expected Daily Production (MWh)'}
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("---")
    st.caption("📌 Planning department helps optimize wind farm expansion and production forecasting.")