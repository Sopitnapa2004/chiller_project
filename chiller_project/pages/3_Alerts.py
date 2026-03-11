import streamlit as st
import pandas as pd

from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar

st.set_page_config(page_title="Alerts", page_icon="🚨", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)

df["power_alert"] = df["power_per_ton"].apply(
    lambda x: "Critical" if x > target_power_ton * 1.2 else ("Warning" if x > target_power_ton else "Normal")
)

alert_df = df[df["power_alert"] != "Normal"][["timestamp", "power_per_ton", "power_alert"]].copy()

st.title("Alerts")
st.write("รายการแจ้งเตือนของระบบ")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Critical Alerts", len(alert_df[alert_df["power_alert"] == "Critical"]))

with col2:
    st.metric("Warning Alerts", len(alert_df[alert_df["power_alert"] == "Warning"]))

with col3:
    st.metric("Total Alerts", len(alert_df))

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    if len(alert_df) > 0:
        st.warning(f"พบ {len(alert_df)} เหตุการณ์ที่ต้องตรวจสอบ")
        st.dataframe(alert_df, use_container_width=True, hide_index=True)
    else:
        st.success("ไม่พบเหตุการณ์ผิดปกติ")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Current Status")
    if latest["power_per_ton"] > target_power_ton:
        st.error("Current system status: Warning")
        st.write(f"Power/Ton: {latest['power_per_ton']:.2f} (Target: {target_power_ton:.2f})")
    else:
        st.success("Current system status: Normal")
        st.write(f"Power/Ton: {latest['power_per_ton']:.2f} (Target: {target_power_ton:.2f})")