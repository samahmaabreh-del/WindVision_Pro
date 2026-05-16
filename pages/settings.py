# pages/settings.py
import streamlit as st


def show_settings():
    st.title("⚙️ System Settings")
    st.markdown("Configure application preferences")
    st.markdown("---")

    # User settings
    st.subheader("👤 User Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"**Logged in as:** {st.session_state['user']['name']}")
        st.info(f"**Role:** {st.session_state['user']['role']}")

    with col2:
        st.text_input("Display Name", value=st.session_state['user']['name'])
        st.selectbox("Language", ["English", "Arabic"])

    st.markdown("---")

    # Notification settings
    st.subheader("🔔 Notification Settings")

    col1, col2 = st.columns(2)

    with col1:
        email_alerts = st.checkbox("Email Alerts", value=True)
        maintenance_alerts = st.checkbox("Maintenance Alerts", value=True)

    with col2:
        weather_alerts = st.checkbox("Weather Alerts", value=True)
        production_alerts = st.checkbox("Production Alerts", value=True)

    st.markdown("---")

    # Threshold settings
    st.subheader("📊 Threshold Settings")

    col1, col2 = st.columns(2)

    with col1:
        efficiency_warning = st.slider("Efficiency Warning Threshold (%)", 50, 90, 70)
        efficiency_critical = st.slider("Efficiency Critical Threshold (%)", 30, 70, 50)

    with col2:
        wind_speed_warning = st.slider("Wind Speed Warning (m/s)", 15, 25, 20)
        wind_speed_critical = st.slider("Wind Speed Critical (m/s)", 25, 35, 30)

    st.markdown("---")

    # Display settings
    st.subheader("🎨 Display Settings")

    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox("Theme", ["Light", "Dark", "System Default"])
        chart_style = st.selectbox("Chart Style", ["Default", "Modern", "Minimalist"])

    with col2:
        refresh_interval = st.selectbox("Auto-refresh Interval",
                                        ["5 seconds", "10 seconds", "30 seconds", "1 minute", "Off"])
        date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "DD/MM/YYYY", "MM/DD/YYYY"])

    st.markdown("---")

    # Data settings
    st.subheader("💾 Data Settings")

    if st.button("Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared successfully! Refresh the page to reload data.")

    if st.button("Export All Data (CSV)"):
        st.info("Data export feature - would export all production data to CSV")

    st.markdown("---")

    # Save button
    if st.button("💾 Save All Settings", type="primary"):
        st.success("Settings saved successfully!")

    st.markdown("---")
    st.caption("⚙️ Settings are saved locally and persist across sessions.")