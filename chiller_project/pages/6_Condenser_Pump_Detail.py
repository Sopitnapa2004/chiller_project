import streamlit as st
from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button

st.set_page_config(page_title="Condenser Pump Detail", page_icon="🔧", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)
render_back_button()

st.title("Condenser Pump Detail")
st.write("Detailed monitoring and analysis for the Condenser Pump.")

top1, top2 = st.columns([1, 3], gap="medium")

with top1:
    with st.container(border=True):
        st.image("images/condenser_pump.png", use_container_width=True)

with top2:
    with st.container(border=True):
        st.markdown("### Current Overview")
        st.write("Supports condenser-side water circulation and influences system efficiency.")
        st.write(f"**Current Power:** {latest['condenser_pump_kw']:.1f} kW")
        efficiency = (30 / latest["condenser_pump_kw"]) * 100 if latest["condenser_pump_kw"] > 0 else 0
        st.write(f"**Efficiency:** {efficiency:.1f}%")
        st.warning("Status: Check")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Condenser Pump Power Trend")
    chart_df = df[["timestamp", "condenser_pump_kw"]].copy().set_index("timestamp")
    st.line_chart(chart_df, use_container_width=True)