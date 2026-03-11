import streamlit as st
from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button

st.set_page_config(page_title="Chiller Detail", page_icon="❄️", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)
render_back_button()

st.title("Chiller Detail")
st.write("Detailed monitoring and analysis for the Chiller unit.")

top1, top2 = st.columns([1, 3], gap="medium")

with top1:
    with st.container(border=True):
        st.image("images/chiller.png", use_container_width=True)

with top2:
    with st.container(border=True):
        st.markdown("### Current Overview")
        st.write("Main cooling equipment responsible for chilled water generation.")
        st.write(f"**Current Power:** {latest['chiller_kw']:.1f} kW")
        efficiency = (420 / latest["chiller_kw"]) * 100 if latest["chiller_kw"] > 0 else 0
        st.write(f"**Efficiency:** {efficiency:.1f}%")
        st.success("Status: Normal")

st.markdown("<br>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3, gap="medium")

with m1:
    with st.container(border=True):
        st.metric("Current Power", f"{latest['chiller_kw']:.1f} kW")

with m2:
    with st.container(border=True):
        efficiency = (420 / latest["chiller_kw"]) * 100 if latest["chiller_kw"] > 0 else 0
        st.metric("Efficiency", f"{efficiency:.1f}%")

with m3:
    with st.container(border=True):
        st.metric("Status", "Normal")

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns([2, 1], gap="medium")

with left:
    with st.container(border=True):
        st.markdown("### Chiller Power Trend")
        chart_df = df[["timestamp", "chiller_kw"]].copy().set_index("timestamp")
        st.line_chart(chart_df, use_container_width=True)

with right:
    with st.container(border=True):
        st.markdown("### Current Status")
        st.success("Operating within normal range")
        st.write("No abnormal power spike detected.")
        st.write("Load trend appears stable.")