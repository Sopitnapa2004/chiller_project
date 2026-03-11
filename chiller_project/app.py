import streamlit as st

from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar, render_header
from components.kpi_cards import render_kpi_section
from components.alerts import render_alerts_section
from components.equipment import render_equipment_section

st.set_page_config(
    page_title="Chiller System Dashboard",
    page_icon="❄️",
    layout="wide",
)

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)
render_header()

s1, s2, s3 = st.columns(3, gap="medium")

with s1:
    with st.container(border=True):
        current_status = "Warning" if latest["power_per_ton"] > target_power_ton else "Normal"
        st.metric("System Status", current_status)

with s2:
    with st.container(border=True):
        st.metric("Last Updated", "2026-03-10 15:00")

with s3:
    with st.container(border=True):
        active_alerts = 1 if latest["power_per_ton"] > target_power_ton else 0
        st.metric("Active Alerts", active_alerts)

st.markdown("<br>", unsafe_allow_html=True)

render_kpi_section(latest, target_power_ton)

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([2, 1], gap="medium")

with left:
    with st.container(border=True):
        st.markdown("### Power/Ton Trend")
        if len(df) > 0:
            chart_df = df[["timestamp", "power_per_ton"]].copy().set_index("timestamp")
            st.line_chart(chart_df, use_container_width=True)
        else:
            st.info("No trend data available.")

with right:
    render_alerts_section(latest, target_power_ton)

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Summary Insight")
    if latest["power_per_ton"] > target_power_ton:
        st.warning("The system is currently operating above the target Power/Ton.")
        st.write("Recommended focus areas:")
        st.write("- Condenser Pump")
        st.write("- Cooling Tower")
        st.write("- Chiller load distribution")
    else:
        st.success("The system is operating within the target range.")
        st.write("No immediate action is required.")

st.markdown("<br>", unsafe_allow_html=True)

if len(df) > 0:
    render_equipment_section(latest)
else:
    with st.container(border=True):
        st.markdown("### Equipment Status")
        st.info("No equipment data available.")

st.markdown(
    """
    <div class="footer-note">
        Prototype version using Python + Pandas + Streamlit |
        Data Source: sample_data.csv
    </div>
    """,
    unsafe_allow_html=True,
)