# auth.py
import streamlit as st
import hashlib

USERS_DB = {
    "EMP001": {
        "name": "Ahmad Al-Madani",
        "role": "Data Science and AI Student",
        "password_hash": hashlib.sha256("1234".encode()).hexdigest()
    },
    "EMP002": {
        "name": "Sara Al-Omari",
        "role": "Data Science and AI Student",
        "password_hash": hashlib.sha256("5678".encode()).hexdigest()
    },
    "EMP003": {
        "name": "Mohammed Al-Taher",
        "role": "Data Science and AI Student",
        "password_hash": hashlib.sha256("9012".encode()).hexdigest()
    }
}


def check_auth(user_id, password):
    if user_id in USERS_DB:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return USERS_DB[user_id]["password_hash"] == password_hash
    return False


def login_screen():
    # Get current language
    current_lang = st.session_state.get('language', 'en')

    if current_lang == 'ar':
        title_text = "WindVision Pro"
        subtitle_text = "نظام إدارة مزارع الرياح"
        employee_placeholder = "🔐 الرقم الوظيفي (مثال: EMP001)"
        password_placeholder = "🔑 الرقم السري"
        login_text = "تسجيل الدخول"
        error_text = "❌ الرقم الوظيفي أو الرقم السري غير صحيح"
        footer_text = "جميع الحقوق محفوظة"
        dev_text = "تم التطوير بواسطة: سماح محمود معابره"
    else:
        title_text = "WindVision Pro"
        subtitle_text = "Wind Farm Management System"
        employee_placeholder = "🔐 Employee ID (Example: EMP001)"
        password_placeholder = "🔑 Password"
        login_text = "Login"
        error_text = "❌ Invalid Employee ID or Password"
        footer_text = "All Rights Reserved"
        dev_text = "Developed by: Samah Mahmoud Ma'abreh"

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('https://images.pexels.com/photos/414837/pexels-photo-414837.jpeg?auto=compress&cs=tinysrgb&w=1920&h=1080&dpr=2');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .login-container {{
        max-width: 450px;
        margin: 100px auto;
        padding: 40px;
        background: rgba(0, 0, 0, 0.85);
        border-radius: 20px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}

    .login-title {{
        font-size: 48px;
        font-weight: bold;
        color: #0a5c2e;
        margin-bottom: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}

    .login-subtitle {{
        font-size: 18px;
        color: #0a5c2e;
        margin-bottom: 30px;
    }}

    .stTextInput > div > div > input {{
        background: white;
        color: #333;
        font-size: 16px;
        border-radius: 10px;
        padding: 12px;
    }}

    .stButton > button {{
        background: #0a5c2e;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        width: 100%;
    }}

    .stButton > button:hover {{
        background: #0a8c3e;
    }}

    hr {{
        background: rgba(255, 255, 255, 0.3);
        margin: 20px 0;
    }}

    .stCaption {{
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        st.markdown(f'<div class="login-title">{title_text}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="login-subtitle">{subtitle_text}</div>', unsafe_allow_html=True)

        st.markdown("---")

        user_id = st.text_input("", placeholder=employee_placeholder, label_visibility="collapsed")
        password = st.text_input("", placeholder=password_placeholder, type="password", label_visibility="collapsed")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_btn = st.button(login_text, use_container_width=True)

        if login_btn:
            if check_auth(user_id, password):
                st.session_state['authenticated'] = True
                st.session_state['user'] = USERS_DB[user_id]
                st.rerun()
            else:
                st.error(error_text)

        st.markdown("---")
        st.caption(f"© 2025 WindVision Pro - {footer_text}")
        st.caption(dev_text)
        st.markdown('</div>', unsafe_allow_html=True)