import streamlit as st
import config
from components.charts import render_power_trend_chart
from components.header import render_sidebar
from components.navigation import render_back_button
from components.styles import load_global_styles
from components.tables import render_dataframe_section
from services.diagnostic_service import apply_diagnostics
from utils.data_loader import get_latest_snapshot, get_time_series, load_chiller_data


def initialize_session_state() -> None:
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def main() -> None:
    st.set_page_config(page_title="Condenser Pump Detail", page_icon="💧", layout="wide")
    initialize_session_state()
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_back_button()

    st.markdown(
        """
        <div class="section-title" style="font-size: 1.8rem; margin-bottom: 4px;">💧 Condenser Pump Systems</div>
        <div class="section-subtitle" style="font-size: 0.95rem; margin-bottom: 12px;">
            Equipment diagnostics, performance trends, and operational analysis
        </div>
        """,
        unsafe_allow_html=True,
    )

    raw_df = load_chiller_data(config.DEFAULT_DATA_FILE)
    detail_raw = get_time_series(raw_df, equipment_type=config.EQUIPMENT_CONDENSER_PUMP)
    detail_latest = apply_diagnostics(get_latest_snapshot(detail_raw), st.session_state.target_power_ton)

    total_power = float(detail_latest["power_kw"].sum()) if not detail_latest.empty else 0.0
    total_ton = float(detail_latest["ton"].sum()) if not detail_latest.empty else 0.0
    kwrt = (total_power / total_ton) if total_ton > 0 else 0.0

    m1, m2, m3, m4 = st.columns([1, 1.15, 1.15, 1], gap="small")
    m1.metric("Units", int(detail_latest["unit_id"].nunique()) if not detail_latest.empty else 0)
    m2.metric("Total Power", f"{total_power:.0f} kW")
    m3.metric("Load", f"{total_ton:.0f} RT")
    m4.metric("Power/Ton", f"{kwrt:.2f}")

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    render_power_trend_chart(detail_raw, "Condenser Pump Performance Trend", height=285)

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    render_dataframe_section(
        "Condenser Pump Fleet - Operating Parameters",
        detail_latest[[
            "building",
            "unit_id",
            "power_kw",
            "ton",
            "power_per_ton",
            "cond_water_flow",
            "status",
            "diagnosis",
            "recommendation",
        ]],
        "Real-time operating metrics with thermohydraulic analysis and diagnostics",
    )


if __name__ == "__main__":
    main()
