# pages/maintenance.py
import streamlit as st
import pandas as pd
import plotly.express as px


def show_maintenance(production_df, turbines_df, current_weather, alert_system, turbine_specs):
    lang = st.session_state.get('lang', 'en')

    if lang == 'ar':
        st.title("🔧 قسم الصيانة")
        st.markdown("صيانة استباقية ومراقبة صحة التوربينات")
        urgent_text = "صيانة عاجلة"
        required_text = "صيانة مطلوبة"
        good_text = "حالة جيدة"
        schedule_text = "📋 جدول الصيانة"
        efficiency_title = "📊 ترتيب كفاءة التوربينات"
        recommendations_title = "💡 توصيات الصيانة"
        efficiency_text = "الكفاءة"
    else:
        st.title("🔧 Maintenance Department")
        st.markdown("Predictive maintenance and turbine health monitoring")
        urgent_text = "Urgent Maintenance"
        required_text = "Required Maintenance"
        good_text = "Good Condition"
        schedule_text = "📋 Maintenance Schedule"
        efficiency_title = "📊 Turbine Efficiency Ranking"
        recommendations_title = "💡 Maintenance Recommendations"
        efficiency_text = "Efficiency"

    st.markdown("---")

    # حساب حالة التوربينات
    turbine_status = []
    for _, turbine in turbines_df.iterrows():
        prod = production_df[production_df['turbine_id'] == turbine['turbine_id']]
        if len(prod) > 0:
            eff = prod['efficiency_percent'].mean()
            if eff < 65:
                priority = "Urgent"
            elif eff < 80:
                priority = "Required"
            else:
                priority = "Good"
        else:
            eff = 85
            priority = "Good"
        turbine_status.append({'name': turbine['name'], 'efficiency': eff, 'priority': priority})

    df = pd.DataFrame(turbine_status)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(urgent_text, len(df[df['priority'] == 'Urgent']))
    with col2:
        st.metric(required_text, len(df[df['priority'] == 'Required']))
    with col3:
        st.metric(good_text, len(df[df['priority'] == 'Good']))

    st.markdown("---")
    st.subheader(schedule_text)

    urgent_df = df[df['priority'] == 'Urgent']
    required_df = df[df['priority'] == 'Required']

    if len(urgent_df) > 0:
        st.error("⚠️ URGENT - Next 24 Hours" if lang == 'en' else "⚠️ عاجل - خلال 24 ساعة")
        for _, t in urgent_df.iterrows():
            st.markdown(f"🚨 **{t['name']}** - {efficiency_text}: {t['efficiency']:.1f}%")

    if len(required_df) > 0:
        st.warning("🔧 REQUIRED - Within 3-7 Days" if lang == 'en' else "🔧 مطلوب - خلال 3-7 أيام")
        for _, t in required_df.iterrows():
            st.markdown(f"⚠️ **{t['name']}** - {efficiency_text}: {t['efficiency']:.1f}%")

    if len(urgent_df) == 0 and len(required_df) == 0:
        st.success("✅ All turbines are in good condition" if lang == 'en' else "✅ جميع التوربينات في حالة جيدة")

    st.markdown("---")
    st.subheader(efficiency_title)

    fig = px.bar(df, x='name', y='efficiency', color='efficiency', color_continuous_scale='RdYlGn',
                 range_color=[50, 100])
    fig.add_hline(y=85, line_dash="dash", line_color="green", annotation_text="Target 85%")
    fig.add_hline(y=70, line_dash="dash", line_color="orange", annotation_text="Warning 70%")
    st.plotly_chart(fig, use_container_width=True)