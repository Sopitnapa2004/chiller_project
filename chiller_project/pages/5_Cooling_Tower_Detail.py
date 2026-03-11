import streamlit as st
from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button

st.set_page_config(page_title="Cooling Tower Detail", page_icon="🌀", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)
render_back_button()

st.title("Cooling Tower Detail")
st.write("Detailed monitoring and analysis for the Cooling Tower.")

top1, top2 = st.columns([1, 3], gap="medium")

with top1:
    with st.container(border=True):
        st.image("images/cooling_tower.png", use_container_width=True)

with top2:
    with st.container(border=True):
        st.markdown("### Current Overview")
        st.write("Heat rejection unit for condenser-side temperature control.")
        st.write(f"**Current Power:** {latest['cooling_tower_kw']:.1f} kW")
        efficiency = (50 / latest["cooling_tower_kw"]) * 100 if latest["cooling_tower_kw"] > 0 else 0
        st.write(f"**Efficiency:** {efficiency:.1f}%")
        st.success("Status: Normal")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Cooling Tower Power Trend")
    chart_df = df[["timestamp", "cooling_tower_kw"]].copy().set_index("timestamp")
    st.line_chart(chart_df, use_container_width=True)