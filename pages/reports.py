# pages/reports.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


def show_reports(production_df, turbines_df, current_weather):
    lang = st.session_state.get('lang', 'en')

    # ========== النصوص المترجمة ==========
    if lang == 'ar':
        # العناوين الرئيسية
        title = "📄 التقارير والتحليلات"
        subtitle = "إنشاء وتصدير تقارير الأداء"
        report_type_label = "اختر نوع التقرير"

        # أنواع التقارير
        daily_report = "تقرير الأداء اليومي"
        weekly_summary = "ملخص أسبوعي"
        monthly_analysis = "تحليل شهري"
        turbine_health = "تقرير صحة التوربين"
        environmental = "تقرير الأثر البيئي"

        # التسميات المشتركة
        select_date = "اختر التاريخ"
        select_month = "اختر الشهر"
        select_turbine = "اختر التوربين"
        total_production = "إجمالي الإنتاج"
        avg_efficiency = "متوسط الكفاءة"
        peak_production = "ذروة الإنتاج"
        operating_days = "أيام التشغيل"
        current_status = "الحالة الحالية"
        total_clean_energy = "إجمالي الطاقة النظيفة"
        co2_emissions = "انبعاثات CO₂ الموفرة"
        trees_eq = "ما يعادل أشجار"

        # أزرار
        download_report = "📥 تحميل التقرير"
        report_preview = "📄 معاينة التقرير"

        # رسائل
        no_data = f"لا توجد بيانات متاحة"
        weekly_total = "الإجمالي الأسبوعي"
        avg_daily = "متوسط الإنتاج اليومي"
        co2_saved_weekly = "CO₂ الموفر (أسبوعياً)"
        monthly_total = "الإجمالي الشهري"
        co2_saved_monthly = "CO₂ الموفر (شهرياً)"

        # Environmental
        env_summary = "ملخص الأثر البيئي"
        clean_energy_gen = "إجمالي الطاقة النظيفة المولدة"
        co2_avoided = "انبعاثات CO₂ التي تم تجنبها"
        oil_saved = "نفط تم توفيره"
        monthly_co2 = "توفير CO₂ شهرياً"

        # Developed by
        developed_by = "تم التطوير بواسطة: سماح محمود معابره"

        # أعمدة الرسم البياني
        hour_label = "الساعة"
        power_label = "القدرة (كيلوواط)"
        date_label = "التاريخ"
        production_label = "الإنتاج (كيلوواط)"
        efficiency_label = "الكفاءة (%)"

    else:
        # العناوين الرئيسية
        title = "📄 Reports & Analytics"
        subtitle = "Generate and export performance reports"
        report_type_label = "Select Report Type"

        # أنواع التقارير
        daily_report = "Daily Performance Report"
        weekly_summary = "Weekly Summary"
        monthly_analysis = "Monthly Analysis"
        turbine_health = "Turbine Health Report"
        environmental = "Environmental Impact Report"

        # التسميات المشتركة
        select_date = "Select Date"
        select_month = "Select Month"
        select_turbine = "Select Turbine"
        total_production = "Total Production"
        avg_efficiency = "Average Efficiency"
        peak_production = "Peak Production"
        operating_days = "Operating Days"
        current_status = "Current Status"
        total_clean_energy = "Total Clean Energy"
        co2_emissions = "CO₂ Emissions Saved"
        trees_eq = "Trees Equivalent"

        # أزرار
        download_report = "📥 Download Report"
        report_preview = "📄 Report Preview"

        # رسائل
        no_data = f"No data available"
        weekly_total = "Weekly Total"
        avg_daily = "Average Daily Production"
        co2_saved_weekly = "CO₂ Saved (Weekly)"
        monthly_total = "Monthly Total"
        co2_saved_monthly = "CO₂ Saved (Monthly)"

        # Environmental
        env_summary = "Environmental Impact Summary"
        clean_energy_gen = "Total Clean Energy Generated"
        co2_avoided = "CO₂ Emissions Avoided"
        oil_saved = "Oil Saved"
        monthly_co2 = "Monthly CO₂ Savings"

        # Developed by
        developed_by = "Developed by: Samah Mahmoud Ma'abreh"

        # أعمدة الرسم البياني
        hour_label = "Hour"
        power_label = "Power (kW)"
        date_label = "Date"
        production_label = "Production (kWh)"
        efficiency_label = "Efficiency (%)"

    # ========== عرض الصفحة ==========
    st.title(title)
    st.markdown(subtitle)
    st.markdown("---")

    report_type = st.selectbox(
        report_type_label,
        [daily_report, weekly_summary, monthly_analysis, turbine_health, environmental]
    )

    st.markdown("---")

    # ============================================
    # 1. Daily Performance Report
    # ============================================
    if report_type == daily_report:
        st.subheader(daily_report)

        report_date = st.date_input(select_date, datetime.now())
        filtered_data = production_df[pd.to_datetime(production_df['timestamp']).dt.date == report_date]

        if len(filtered_data) > 0:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(total_production, f"{filtered_data['power_output_kw'].sum() / 1000:.1f} MWh")
            with col2:
                st.metric(avg_efficiency, f"{filtered_data['efficiency_percent'].mean():.1f}%")
            with col3:
                st.metric(peak_production, f"{filtered_data['power_output_kw'].max() / 1000:.1f} MW")

            hourly_data = filtered_data.groupby(filtered_data['timestamp'].dt.hour)[
                'power_output_kw'].sum().reset_index()
            fig = px.line(
                hourly_data,
                x='timestamp',
                y='power_output_kw',
                title=f"Hourly Production - {report_date}",
                labels={'timestamp': hour_label, 'power_output_kw': power_label},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # معاينة التقرير
            st.markdown("---")
            st.subheader(report_preview)

            preview_text = f"""
            ═══════════════════════════════════════════════════════════
                              WINDVISION PRO - OFFICIAL REPORT
            ═══════════════════════════════════════════════════════════

            Report Type: {daily_report}
            Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Generated by: Samah Mahmoud Ma'abreh

            ───────────────────────────────────────────────────────────

            📊 KEY METRICS:

            • {total_production}: {filtered_data['power_output_kw'].sum() / 1000:.1f} MWh
            • {avg_efficiency}: {filtered_data['efficiency_percent'].mean():.1f}%
            • {peak_production}: {filtered_data['power_output_kw'].max() / 1000:.1f} MW
            • Active Turbines: {len(filtered_data['turbine_id'].unique())}

            ───────────────────────────────────────────────────────────

            🌍 ENVIRONMENTAL IMPACT:

            • CO₂ Saved: {filtered_data['power_output_kw'].sum() / 1000 * 0.55:.1f} tons
            • Trees Equivalent: {filtered_data['power_output_kw'].sum() / 1000 * 0.55 * 45:.0f} trees

            ───────────────────────────────────────────────────────────

            Report generated by WindVision Pro - Tafila Wind Farm Management System
            {developed_by}

            ═══════════════════════════════════════════════════════════
            """

            st.text(preview_text)

            csv = filtered_data.to_csv(index=False)
            st.download_button(
                download_report,
                csv,
                f"daily_report_{report_date}.csv",
                "text/csv"
            )
        else:
            st.warning(f"{no_data} {report_date}")

    # ============================================
    # 2. Weekly Summary
    # ============================================
    elif report_type == weekly_summary:
        st.subheader(weekly_summary)

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        weekly_data = production_df[
            (pd.to_datetime(production_df['timestamp']) >= start_date) &
            (pd.to_datetime(production_df['timestamp']) <= end_date)
            ]

        daily_summary = weekly_data.groupby(weekly_data['timestamp'].dt.date).agg({
            'power_output_kw': 'sum',
            'efficiency_percent': 'mean'
        }).reset_index()

        daily_summary.columns = ['Date', 'Total Production (kWh)', 'Avg Efficiency (%)']
        daily_summary['Total Production (MWh)'] = daily_summary['Total Production (kWh)'] / 1000

        st.dataframe(daily_summary, use_container_width=True)

        fig = px.bar(
            daily_summary,
            x='Date',
            y='Total Production (MWh)',
            title='Daily Production - Last 7 Days',
            color='Avg Efficiency (%)',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

        total_weekly = daily_summary['Total Production (MWh)'].sum()
        avg_efficiency = daily_summary['Avg Efficiency (%)'].mean()

        st.info(f"📈 **{weekly_total}:** {total_weekly:.1f} MWh | **{avg_efficiency}:** {avg_efficiency:.1f}%")

        # معاينة التقرير
        st.markdown("---")
        st.subheader(report_preview)

        preview_text = f"""
        ═══════════════════════════════════════════════════════════
                          WINDVISION PRO - OFFICIAL REPORT
        ═══════════════════════════════════════════════════════════

        Report Type: {weekly_summary}
        Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
        Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Generated by: Samah Mahmoud Ma'abreh

        ───────────────────────────────────────────────────────────

        📊 WEEKLY METRICS:

        • {weekly_total}: {total_weekly:.1f} MWh
        • {avg_efficiency}: {avg_efficiency:.1f}%
        • {avg_daily}: {total_weekly / 7:.1f} MWh/day

        ───────────────────────────────────────────────────────────

        🌍 ENVIRONMENTAL IMPACT:

        • {co2_saved_weekly}: {total_weekly * 0.55:.1f} tons
        • Trees Equivalent: {total_weekly * 0.55 * 45:.0f} trees

        ───────────────────────────────────────────────────────────

        Report generated by WindVision Pro - Tafila Wind Farm Management System
        {developed_by}

        ═══════════════════════════════════════════════════════════
        """

        st.text(preview_text)

    # ============================================
    # 3. Monthly Analysis
    # ============================================
    elif report_type == monthly_analysis:
        st.subheader(monthly_analysis)

        months = production_df['timestamp'].dt.strftime('%Y-%m').unique()
        selected_month = st.selectbox(select_month, sorted(months, reverse=True))

        monthly_data = production_df[production_df['timestamp'].dt.strftime('%Y-%m') == selected_month]

        if len(monthly_data) > 0:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(total_production, f"{monthly_data['power_output_kw'].sum() / 1000:.1f} MWh")
            with col2:
                st.metric(avg_efficiency, f"{monthly_data['efficiency_percent'].mean():.1f}%")
            with col3:
                st.metric(operating_days, monthly_data['timestamp'].dt.date.nunique())

            daily_monthly = monthly_data.groupby(monthly_data['timestamp'].dt.date)[
                'power_output_kw'].sum().reset_index()
            fig = px.line(
                daily_monthly,
                x='timestamp',
                y='power_output_kw',
                title=f'Daily Production - {selected_month}',
                labels={'timestamp': date_label, 'power_output_kw': production_label},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            total_monthly = monthly_data['power_output_kw'].sum() / 1000
            avg_efficiency_monthly = monthly_data['efficiency_percent'].mean()

            # معاينة التقرير
            st.markdown("---")
            st.subheader(report_preview)

            preview_text = f"""
            ═══════════════════════════════════════════════════════════
                              WINDVISION PRO - OFFICIAL REPORT
            ═══════════════════════════════════════════════════════════

            Report Type: {monthly_analysis}
            Month: {selected_month}
            Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Generated by: Samah Mahmoud Ma'abreh

            ───────────────────────────────────────────────────────────

            📊 MONTHLY METRICS:

            • {monthly_total}: {total_monthly:.1f} MWh
            • {avg_efficiency}: {avg_efficiency_monthly:.1f}%
            • {avg_daily}: {total_monthly / 30:.1f} MWh/day

            ───────────────────────────────────────────────────────────

            🌍 ENVIRONMENTAL IMPACT:

            • {co2_saved_monthly}: {total_monthly * 0.55:.1f} tons
            • Trees Equivalent: {total_monthly * 0.55 * 45:.0f} trees

            ───────────────────────────────────────────────────────────

            Report generated by WindVision Pro - Tafila Wind Farm Management System
            {developed_by}

            ═══════════════════════════════════════════════════════════
            """

            st.text(preview_text)

    # ============================================
    # 4. Turbine Health Report
    # ============================================
    elif report_type == turbine_health:
        st.subheader(turbine_health)

        selected_turbine = st.selectbox(select_turbine, turbines_df['name'].tolist())
        turbine_data = production_df[production_df['turbine_name'] == selected_turbine]

        if len(turbine_data) > 0:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(total_production, f"{turbine_data['power_output_kw'].sum() / 1000:.1f} MWh")
            with col2:
                st.metric(avg_efficiency, f"{turbine_data['efficiency_percent'].mean():.1f}%")
            with col3:
                st.metric(current_status, turbine_data.iloc[-1]['status'])

            fig = px.line(
                turbine_data,
                x='timestamp',
                y='efficiency_percent',
                title=f'Efficiency Trend - {selected_turbine}',
                labels={'timestamp': date_label, 'efficiency_percent': efficiency_label},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            avg_eff = turbine_data['efficiency_percent'].mean()
            total_prod = turbine_data['power_output_kw'].sum() / 1000

            # معاينة التقرير
            st.markdown("---")
            st.subheader(report_preview)

            preview_text = f"""
            ═══════════════════════════════════════════════════════════
                              WINDVISION PRO - OFFICIAL REPORT
            ═══════════════════════════════════════════════════════════

            Report Type: {turbine_health}
            Turbine: {selected_turbine}
            Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            Generated by: Samah Mahmoud Ma'abreh

            ───────────────────────────────────────────────────────────

            📊 TURBINE METRICS:

            • {total_production}: {total_prod:.1f} MWh
            • {avg_efficiency}: {avg_eff:.1f}%
            • {current_status}: {turbine_data.iloc[-1]['status']}

            ───────────────────────────────────────────────────────────

            Report generated by WindVision Pro - Tafila Wind Farm Management System
            {developed_by}

            ═══════════════════════════════════════════════════════════
            """

            st.text(preview_text)

    # ============================================
    # 5. Environmental Impact Report
    # ============================================
    elif report_type == environmental:
        st.subheader(environmental)

        total_production_val = production_df['power_output_kw'].sum() / 1000
        co2_saved = total_production_val * 0.55
        trees_equivalent = co2_saved * 45

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(total_clean_energy, f"{total_production_val:.0f} MWh")
        with col2:
            st.metric(co2_emissions, f"{co2_saved:.0f} tons")
        with col3:
            st.metric(trees_eq, f"{trees_equivalent:.0f} trees")

        st.success(f"""
        🌍 **{env_summary}:**

        By generating {total_production_val:.0f} MWh of clean wind energy, Tafila Wind Farm has:
        - Avoided {co2_saved:.0f} tons of CO₂ emissions
        - Equivalent to planting {trees_equivalent:.0f} trees
        - Saved approximately {total_production_val * 0.25:.0f} barrels of oil
        """)

        monthly_impact = production_df.groupby(production_df['timestamp'].dt.strftime('%Y-%m')).agg({
            'power_output_kw': 'sum'
        }).reset_index()
        monthly_impact['CO₂ Saved (tons)'] = monthly_impact['power_output_kw'] / 1000 * 0.55

        fig = px.bar(
            monthly_impact,
            x='timestamp',
            y='CO₂ Saved (tons)',
            title=monthly_co2,
            color='CO₂ Saved (tons)',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

        # معاينة التقرير
        st.markdown("---")
        st.subheader(report_preview)

        preview_text = f"""
        ═══════════════════════════════════════════════════════════
                          WINDVISION PRO - OFFICIAL REPORT
        ═══════════════════════════════════════════════════════════

        Report Type: {environmental}
        Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Generated by: Samah Mahmoud Ma'abreh

        ───────────────────────────────────────────────────────────

        🌍 {env_summary}:

        • {clean_energy_gen}: {total_production_val:.0f} MWh
        • {co2_avoided}: {co2_saved:.0f} tons
        • {trees_eq}: {trees_equivalent:.0f} trees
        • {oil_saved}: {total_production_val * 0.25:.0f} barrels

        ───────────────────────────────────────────────────────────

        Report generated by WindVision Pro - Tafila Wind Farm Management System
        {developed_by}

        ═══════════════════════════════════════════════════════════
        """

        st.text(preview_text)

    st.markdown("---")
    st.caption(developed_by)