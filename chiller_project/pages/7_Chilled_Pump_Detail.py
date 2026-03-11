import streamlit as st
from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button

st.set_page_config(page_title="Chilled Pump Detail", page_icon="💧", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)
render_back_button()

st.title("Chilled Pump Detail")
st.write("Detailed monitoring and analysis for the Chilled Pump.")

top1, top2 = st.columns([1, 3], gap="medium")

with top1:
    with st.container(border=True):
        st.image("images/chilled_pump.png", use_container_width=True)

with top2:
    with st.container(border=True):
        st.markdown("### Current Overview")
        st.write("Circulates chilled water to the distribution side and connected loads.")
        st.write(f"**Current Power:** {latest['chilled_pump_kw']:.1f} kW")
        efficiency = (40 / latest["chilled_pump_kw"]) * 100 if latest["chilled_pump_kw"] > 0 else 0
        st.write(f"**Efficiency:** {efficiency:.1f}%")
        st.success("Status: Normal")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Chilled Pump Power Trend")
    chart_df = df[["timestamp", "chilled_pump_kw"]].copy().set_index("timestamp")
    st.line_chart(chart_df, use_container_width=True)