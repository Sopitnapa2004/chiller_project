import streamlit as st

import config
from components.cards import render_equipment_card, render_kpi_card
from components.charts import render_power_trend_chart
from components.header import render_header, render_sidebar
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


def _get_building_stats(building_data):
    if building_data.empty:
        return {
            "units": 0,
            "power_per_ton": 0.0,
            "active_alerts": 0,
            "status": "No Data",
        }

    total_power = float(building_data["power_kw"].sum())
    total_ton = float(building_data["ton"].sum())
    power_per_ton = (total_power / total_ton) if total_ton > 0 else 0.0
    active_alerts = int(building_data["status"].isin(config.STATUS_ALERT_VALUES).sum())

    if (building_data["status"] == config.STATUS_CRITICAL).any():
        status = config.STATUS_CRITICAL
    elif (building_data["status"] == config.STATUS_WARNING).any():
        status = config.STATUS_WARNING
    elif (building_data["status"] == config.STATUS_CHECK).any():
        status = config.STATUS_CHECK
    else:
        status = config.STATUS_NORMAL

    return {
        "units": int(building_data["unit_id"].nunique()),
        "power_per_ton": power_per_ton,
        "active_alerts": active_alerts,
        "status": status,
    }


def _get_building_card_html(building_name: str, units: int, ppt: float, alerts: int, status: str) -> str:
    status_color = {
        config.STATUS_NORMAL: "#22C55E",
        config.STATUS_CHECK: "#94A3B8",
        config.STATUS_WARNING: "#F59E0B",
        config.STATUS_CRITICAL: "#EF4444",
        "No Data": "#64748B",
    }.get(status, "#94A3B8")

    return f"""
    <div style="
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 16px 18px;
        min-height: 165px;
    ">
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-bottom:10px;
        ">
            <div style="
                font-size:0.98rem;
                font-weight:700;
                color:#F8FAFC;
                line-height:1.2;
            ">
                {building_name}
            </div>
            <div style="
                font-size:0.76rem;
                font-weight:700;
                color:{status_color};
                line-height:1.2;
            ">
                {status}
            </div>
        </div>

        <div style="font-size:0.76rem; color:#94A3B8; margin-bottom:2px;">Units</div>
        <div style="font-size:1.20rem; font-weight:700; color:#F1F5F9; margin-bottom:8px;">{units}</div>

        <div style="font-size:0.76rem; color:#94A3B8; margin-bottom:2px;">Power/Ton</div>
        <div style="font-size:1.20rem; font-weight:700; color:#F1F5F9; margin-bottom:8px;">{ppt:.2f}</div>

        <div style="font-size:0.76rem; color:#94A3B8; margin-bottom:2px;">Active Alerts</div>
        <div style="font-size:1.20rem; font-weight:700; color:#F1F5F9;">{alerts}</div>
    </div>
    """


def main() -> None:
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.LAYOUT,
    )

    initialize_session_state()
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_header()

    raw_df = load_chiller_data(config.DEFAULT_DATA_FILE)
    latest_df = apply_diagnostics(
        get_latest_snapshot(raw_df),
        st.session_state.target_power_ton
    )

    summary = get_system_summary(latest_df, st.session_state.target_power_ton)
    building_df = get_building_overview(latest_df)
    alert_df = get_active_alerts(latest_df)
    equipment_df = get_equipment_overview(latest_df)

    top_left, top_right = st.columns([4.2, 1.3], gap="small")
    with top_left:
        st.markdown(
            '<div class="section-title" style="font-size: 1.05rem;">Operations View</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="section-subtitle" style="margin-bottom: 0.25rem;">Site-level chiller performance and equipment condition</div>',
            unsafe_allow_html=True,
        )
    with top_right:
        with st.container(border=True):
            st.markdown(
                '<div class="section-title" style="margin-bottom: 0.35rem;">Target kW/Ton</div>',
                unsafe_allow_html=True,
            )
            st.session_state.target_power_ton = st.number_input(
                "Target kW/Ton",
                min_value=config.MIN_TARGET_POWER_TON,
                max_value=config.MAX_TARGET_POWER_TON,
                value=float(st.session_state.target_power_ton),
                step=0.01,
                label_visibility="collapsed",
            )

    st.markdown("<div style='margin-bottom: 4px;'></div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns([1.15, 1.15, 1, 1], gap="small")
    render_kpi_card(k1, "Fleet Power/Ton", f"{summary['fleet_power_ton']:.2f}", "Overall site performance")
    render_kpi_card(k2, "Total Cooling Load", f"{summary['total_ton']:.0f}", "RT")
    render_kpi_card(k3, "Units Online", f"{summary['units_online']}", "Reporting units")
    render_kpi_card(k4, "Active Alerts", f"{summary['active_alerts']}", "Rule-based exceptions")

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([2.65, 1.15], gap="small")
    with left:
        render_power_trend_chart(get_time_series(raw_df), "Site Performance Trend", height=290)
    with right:
        with st.container(border=True):
            st.markdown('<div class="section-title">Current Focus</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-subtitle" style="margin-bottom: 0.35rem;">Quick operational summary for immediate review</div>',
                unsafe_allow_html=True,
            )
            st.metric("Buildings", summary["buildings_monitored"])
            st.metric("Target", f"{summary['target_power_ton']:.2f} kW/Ton")
            st.metric("Power (kW)", f"{summary['total_power_kw']:.1f}")
            if summary["active_alerts"] > 0:
                st.warning("Exceptions detected in current snapshot")
            else:
                st.success("System is currently stable")

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-title">Building Overview</div>
        <div class="section-subtitle">Performance and alert distribution by building</div>
        """,
        unsafe_allow_html=True,
    )

    building_names = config.BUILDING_NAMES
    for row_start in range(0, len(building_names), 3):
        cols = st.columns(3, gap="small")
        row_items = building_names[row_start:row_start + 3]

        for col, building_name in zip(cols, row_items):
            stats_df = latest_df[latest_df["building"] == building_name]
            stats = _get_building_stats(stats_df)

            with col:
                st.markdown(
                    _get_building_card_html(
                        building_name=building_name,
                        units=stats["units"],
                        ppt=stats["power_per_ton"],
                        alerts=stats["active_alerts"],
                        status=stats["status"],
                    ),
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    left_table, right_table = st.columns([1.2, 1], gap="small")
    with left_table:
        render_dataframe_section(
            "Building Performance Table",
            building_df[[
                "building",
                "status",
                "units",
                "active_alerts",
                "total_power_kw",
                "total_ton",
                "power_per_ton",
            ]],
            "Structured overview for site comparison",
        )
    with right_table:
        render_dataframe_section(
            "Equipment Type Overview",
            equipment_df[[
                "equipment_type",
                "status",
                "units",
                "active_alerts",
                "total_power_kw",
                "avg_power_kw",
                "power_per_ton",
            ]],
            "Aggregated equipment condition across the site",
        )

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Equipment Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle" style="margin-bottom: 0.35rem;">High-level condition by major equipment category</div>',
        unsafe_allow_html=True,
    )

    eq_cols = st.columns(4, gap="small")
    for idx, equipment_name in enumerate([
        config.EQUIPMENT_CHILLER,
        config.EQUIPMENT_COOLING_TOWER,
        config.EQUIPMENT_CONDENSER_PUMP,
        config.EQUIPMENT_CHILLED_PUMP,
    ]):
        equipment_data = latest_df[latest_df["equipment_type"] == equipment_name]
        total_power = float(equipment_data["power_kw"].sum()) if not equipment_data.empty else 0.0
        total_ton = float(equipment_data["ton"].sum()) if not equipment_data.empty else 0.0
        power_per_ton = (total_power / total_ton) if total_ton > 0 else 0.0

        if not equipment_data.empty:
            if (equipment_data["status"] == config.STATUS_CRITICAL).any():
                status = config.STATUS_CRITICAL
            elif (equipment_data["status"] == config.STATUS_WARNING).any():
                status = config.STATUS_WARNING
            elif (equipment_data["status"] == config.STATUS_CHECK).any():
                status = config.STATUS_CHECK
            else:
                status = config.STATUS_NORMAL
        else:
            status = config.STATUS_NORMAL

        with eq_cols[idx]:
            render_equipment_card(
                image_path=config.EQUIPMENT_IMAGE_MAP[equipment_name],
                title=equipment_name,
                status=status,
                note="Condition-based summary",
                power_kw=total_power,
                power_per_ton=power_per_ton,
                page_path=config.DETAIL_PAGE_MAP[equipment_name],
            )

    st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

    render_dataframe_section(
        "Exception Detail",
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
        "Units currently outside preferred operating conditions",
    )


if __name__ == "__main__":
    main()