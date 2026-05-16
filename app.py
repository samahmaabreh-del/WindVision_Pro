# app.py
import streamlit as st
import time

st.set_page_config(page_title="WindVision Pro", page_icon="💨", layout="wide")

import pandas as pd
import numpy as np
from datetime import datetime

from auth import login_screen, check_auth
from data_generator import get_ready_data
from models import WindTurbineModels
from weather_api import get_weather_for_tafilah
from storm_prediction import StormPredictor
from dust_analysis import DustAnalyzer
from alerts import AlertSystem

from pages.dashboard import show_dashboard
from pages.operations import show_operations
from pages.maintenance import show_maintenance
from pages.planning import show_planning
from pages.simulation import show_simulation
from pages.reports import show_reports
from pages.data_upload import show_data_upload

# ============================================
# Authentication
# ============================================
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['lang'] = 'en'

if not st.session_state['authenticated']:
    login_screen()
    st.stop()


# ============================================
# Load Data
# ============================================
@st.cache_data
def load_all_data():
    progress_text = st.empty()
    progress_bar = st.progress(0)

    progress_text.text("Loading wind speed data...")
    progress_bar.progress(20)
    time.sleep(0.3)

    data = get_ready_data()

    progress_text.text("Processing turbine data...")
    progress_bar.progress(50)
    time.sleep(0.3)

    progress_text.text("Generating production data...")
    progress_bar.progress(80)
    time.sleep(0.3)

    progress_text.text("Finalizing...")
    progress_bar.progress(100)
    time.sleep(0.2)

    progress_text.empty()
    progress_bar.empty()

    return data


@st.cache_resource
def load_models():
    return WindTurbineModels()


with st.spinner('🔄 Loading WindVision Pro... Please wait'):
    data = load_all_data()
    models = load_models()

turbines_df = data['turbines']
production_df = data['production']
wind_df = data['wind']
turbine_specs = data['turbine_specs']

if 'hour' not in production_df.columns:
    production_df['hour'] = pd.to_datetime(production_df['timestamp']).dt.hour
if 'month' not in production_df.columns:
    production_df['month'] = pd.to_datetime(production_df['timestamp']).dt.month


def power_curve(wind_speed_ms):
    rated_power = turbine_specs['rated_power_kw']
    cut_in = turbine_specs['cut_in_wind_speed_ms']
    rated_speed = turbine_specs['rated_wind_speed_ms']
    cut_out = turbine_specs['cut_out_wind_speed_ms']

    if wind_speed_ms < cut_in or wind_speed_ms > cut_out:
        return 0
    elif wind_speed_ms < rated_speed:
        return rated_power * ((wind_speed_ms - cut_in) / (rated_speed - cut_in)) ** 3
    else:
        return rated_power


models.power_curve = power_curve
models.train_production_model(production_df)

current_weather = get_weather_for_tafilah()

storm_predictor = StormPredictor()
dust_analyzer = DustAnalyzer()
alert_system = AlertSystem()

# ============================================
# Sidebar Navigation with Translation
# ============================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3125/3125713.png", width=60)
st.sidebar.title("WindVision Pro")
st.sidebar.markdown("---")

# Language selector
lang = st.sidebar.radio("Language", ["English", "العربية"], horizontal=True)
if lang == "العربية":
    st.session_state['lang'] = 'ar'
else:
    st.session_state['lang'] = 'en'

st.sidebar.markdown("---")

# Menu - translated
if st.session_state['lang'] == 'ar':
    menu_options = ["🏠 لوحة التحكم", "⚙️ التشغيل", "🔧 الصيانة", "📊 التخطيط", "🎮 المحاكاة", "📄 التقارير",
                    "📂 رفع البيانات"]
    logout_text = "تسجيل الخروج"
    user_label = "الاسم"
    program_label = "البرنامج"
    program_text = "علوم البيانات والذكاء الاصطناعي"
else:
    menu_options = ["🏠 Dashboard", "⚙️ Operations", "🔧 Maintenance", "📊 Planning", "🎮 Simulation", "📄 Reports",
                    "📂 Data Upload"]
    logout_text = "Logout"
    user_label = "Name"
    program_label = "Program"
    program_text = "Data Science and AI"

selected = st.sidebar.radio("", menu_options)

st.sidebar.markdown("---")
st.sidebar.info(f"{user_label}: {st.session_state['user']['name']}")
st.sidebar.info(f"{program_label}: {program_text}")
st.sidebar.markdown("---")
st.sidebar.caption("Developed by: Samah Mahmoud Ma'abreh")

if st.sidebar.button(logout_text, use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

# ============================================
# Page Routing
# ============================================
if selected == menu_options[0]:
    show_dashboard(production_df, turbines_df, current_weather, turbine_specs)
elif selected == menu_options[1]:
    show_operations(production_df, turbines_df, current_weather, models, turbine_specs)
elif selected == menu_options[2]:
    show_maintenance(production_df, turbines_df, current_weather, alert_system, turbine_specs)
elif selected == menu_options[3]:
    show_planning(production_df, turbines_df, models, turbine_specs, wind_df)
elif selected == menu_options[4]:
    show_simulation(turbines_df, production_df, models, current_weather, turbine_specs)
elif selected == menu_options[5]:
    show_reports(production_df, turbines_df, current_weather)
elif selected == menu_options[6]:
    show_data_upload()