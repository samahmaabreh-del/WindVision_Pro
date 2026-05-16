# pages/data_upload.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def show_data_upload():
    lang = st.session_state.get('lang', 'en')

    # ========== النصوص المترجمة ==========
    if lang == 'ar':
        title = "📂 إدارة البيانات"
        subtitle = "رفع وعرض وإدارة بيانات مزرعة الرياح"
        upload_title = "📤 رفع بيانات جديدة"
        choose_file = "اختر ملف CSV"
        file_loaded = "تم تحميل الملف"
        file_size = "حجم الملف"
        preview_title = "📊 معاينة البيانات"
        stats_title = "📈 إحصائيات البيانات"
        rows_label = "صفوف"
        columns_label = "أعمدة"
        total_power = "إجمالي الطاقة"
        avg_efficiency = "متوسط الكفاءة"
        save_btn = "💾 حفظ في قاعدة البيانات"
        save_success = "✅ تم حفظ البيانات بنجاح"
        existing_title = "🗄️ إدارة البيانات الموجودة"
        export_btn = "📥 تصدير جميع البيانات"
        clear_btn = "🗑️ مسح جميع البيانات"
        confirm_warning = "⚠️ سيتم حذف جميع البيانات. هل أنت متأكد؟"
        confirm_btn = "تأكيد الحذف"
        clear_success = "تم مسح البيانات"
        chart_title = "📊 توزيع الإنتاج"
        power_label = "القدرة (كيلوواط)"
        turbine_label = "التوربين"
        export_info = "ميزة التصدير - سيتم تصدير جميع البيانات إلى CSV"
        developed_by = "تم التطوير بواسطة: سماح محمود معابره"
        mwh = "ميجاواط/ساعة"
        no_data = "لا توجد بيانات للعرض"
    else:
        title = "📂 Data Management"
        subtitle = "Upload, view and manage wind farm data"
        upload_title = "📤 Upload New Data"
        choose_file = "Choose CSV file"
        file_loaded = "File loaded"
        file_size = "File size"
        preview_title = "📊 Data Preview"
        stats_title = "📈 Data Statistics"
        rows_label = "Rows"
        columns_label = "Columns"
        total_power = "Total Power"
        avg_efficiency = "Average Efficiency"
        save_btn = "💾 Save to Database"
        save_success = "✅ Data saved successfully"
        existing_title = "🗄️ Existing Data Management"
        export_btn = "📥 Export All Data"
        clear_btn = "🗑️ Clear All Data"
        confirm_warning = "⚠️ This will delete all data. Are you sure?"
        confirm_btn = "Confirm Delete"
        clear_success = "Data cleared"
        chart_title = "📊 Power Distribution"
        power_label = "Power (kW)"
        turbine_label = "Turbine"
        export_info = "Export feature - would export all data to CSV"
        developed_by = "Developed by: Samah Mahmoud Ma'abreh"
        mwh = "MWh"
        no_data = "No data to display"

    # CSS
    st.markdown("""
    <style>
    .upload-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #28a745;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title(title)
    st.markdown(f"### {subtitle}")
    st.markdown("---")

    # قسم رفع البيانات
    st.markdown(f"## {upload_title}")

    with st.container():
        uploaded_file = st.file_uploader(
            choose_file,
            type=['csv'],
            help="CSV file with columns: timestamp, wind_speed_ms, power_output_kw, efficiency_percent"
        )

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(file_loaded, uploaded_file.name)
            with col2:
                st.metric(file_size, f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric(rows_label, len(df))

            st.markdown("---")
            st.markdown(f"## {preview_title}")
            st.dataframe(df.head(20), use_container_width=True)

            st.markdown("---")
            st.markdown(f"## {stats_title}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(rows_label, len(df))
            with col2:
                st.metric(columns_label, len(df.columns))

            if 'power_output_kw' in df.columns:
                total = df['power_output_kw'].sum() / 1000
                with col3:
                    st.metric(total_power, f"{total:.1f} {mwh}")

            if 'efficiency_percent' in df.columns:
                avg_eff = df['efficiency_percent'].mean()
                with col4:
                    st.metric(avg_efficiency, f"{avg_eff:.1f}%")

            st.markdown("---")

            if 'power_output_kw' in df.columns and 'turbine_name' in df.columns:
                st.markdown(f"## {chart_title}")
                turbine_power = df.groupby('turbine_name')['power_output_kw'].sum().reset_index()
                turbine_power = turbine_power.sort_values('power_output_kw', ascending=False).head(10)

                fig = px.bar(
                    turbine_power,
                    x='turbine_name',
                    y='power_output_kw',
                    title=chart_title,
                    labels={'turbine_name': turbine_label, 'power_output_kw': power_label},
                    color='power_output_kw',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(save_btn, use_container_width=True, type="primary"):
                    st.success(save_success)

    st.markdown("---")
    st.markdown(f"## {existing_title}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(export_btn, use_container_width=True):
            st.info(export_info)
    with col2:
        if st.button(clear_btn, use_container_width=True):
            st.warning(confirm_warning)
            if st.button(confirm_btn):
                st.error(clear_success)

    st.markdown("---")

    # معلومات تنسيق الملف
    with st.expander("📋 File Format Requirements"):
        if lang == 'ar':
            st.markdown("يجب أن يحتوي ملف CSV على الأعمدة التالية:")
            st.markdown("- timestamp (التاريخ والوقت)")
            st.markdown("- wind_speed_ms (سرعة الرياح)")
            st.markdown("- power_output_kw (إنتاج الطاقة)")
            st.markdown("- efficiency_percent (نسبة الكفاءة)")
            st.markdown("- turbine_name (اسم التوربين - اختياري)")
        else:
            st.markdown("The CSV file should contain the following columns:")
            st.markdown("- timestamp (Date and time)")
            st.markdown("- wind_speed_ms (Wind speed)")
            st.markdown("- power_output_kw (Power output)")
            st.markdown("- efficiency_percent (Efficiency percentage)")
            st.markdown("- turbine_name (Turbine name - optional)")

    st.markdown("---")
    st.caption(developed_by)