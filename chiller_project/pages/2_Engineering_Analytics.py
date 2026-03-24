import streamlit as st

import config
from components.alerts import render_alert_summary
from components.cards import render_kpi_card
from components.charts import render_power_trend_chart
from components.header import render_sidebar
from components.styles import load_global_styles
from components.tables import render_dataframe_section
from services.alert_service import get_active_alerts, get_equipment_overview
from services.building_service import get_building_overview
from services.diagnostic_service import apply_diagnostics
from services.summary_service import get_system_summary
from utils.data_loader import get_latest_snapshot, get_time_series, load_chiller_data


def initialize_session_state() -> None:
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def main() -> None:
    st.set_page_config(page_title="Engineering Analytics", page_icon="📈", layout="wide")
    initialize_session_state()
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)

    st.markdown(
        """
        <div class="section-title" style="font-size: 1.7rem; margin-bottom: 3px;">Engineering Analytics</div>
        <div class="section-subtitle" style="font-size: 0.9rem; margin-bottom: 10px;">
            Comprehensive diagnostics, trend analysis, and fleet-wide exception reporting
        </div>
        """,
        unsafe_allow_html=True,
    )

    raw_df = load_chiller_data(config.DEFAULT_DATA_FILE)
    latest_df = apply_diagnostics(get_latest_snapshot(raw_df), st.session_state.target_power_ton)

    summary = get_system_summary(latest_df, st.session_state.target_power_ton)
    building_df = get_building_overview(latest_df)
    alert_df = get_active_alerts(latest_df)
    equipment_df = get_equipment_overview(latest_df)

    k1, k2, k3, k4 = st.columns([1.15, 1, 1, 1], gap="small")
    render_kpi_card(k1, "Fleet Power/Ton", f"{summary['fleet_power_ton']:.2f}", "Overall fleet efficiency")
    render_kpi_card(k2, "Buildings", f"{summary['buildings_monitored']}", "Monitored facilities")
    render_kpi_card(k3, "Units Online", f"{summary['units_online']}", "Reporting assets")
    render_kpi_card(k4, "Active Alerts", f"{summary['active_alerts']}", "Open diagnostic exceptions")

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    render_power_trend_chart(get_time_series(raw_df), "System Performance Trend", height=300)

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    top_left, top_right = st.columns([1.1, 1], gap="small")
    with top_left:
        render_alert_summary(alert_df)

    with top_right:
        render_dataframe_section(
            "Equipment Status Snapshot",
            equipment_df[[
                "equipment_type",
                "status",
                "units",
                "active_alerts",
                "power_per_ton",
            ]],
            "Current fleet condition by equipment class",
        )

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1], gap="small")

    with left:
        render_dataframe_section(
            "Site-wide Building Metrics",
            building_df[[
                "building",
                "status",
                "units",
                "active_alerts",
                "total_power_kw",
                "total_ton",
                "power_per_ton",
            ]],
            "Performance analysis by facility",
        )

    with right:
        render_dataframe_section(
            "Equipment Inventory & Status",
            equipment_df[[
                "equipment_type",
                "status",
                "units",
                "active_alerts",
                "total_power_kw",
                "avg_power_kw",
                "power_per_ton",
            ]],
            "Fleet-wide aggregation by equipment class",
        )

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    render_dataframe_section(
        "Alert Diagnostics & Recommendations",
        alert_df[[
            "building",
            "unit_id",
            "equipment_type",
            "power_kw",
            "power_per_ton",
            "status",
            "diagnosis",
            "recommendation",
        ]],
        "Units flagged by rule-based diagnostics with engineering guidance",
    )


if __name__ == "__main__":
    main()