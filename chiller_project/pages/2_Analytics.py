import streamlit as st
import pandas as pd

from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")
latest = get_latest_row(df)

load_global_styles()
render_sidebar(target_power_ton)

st.title("Analytics")
st.write("วิเคราะห์สถานะระบบเบื้องต้น")

m1, m2, m3 = st.columns(3, gap="medium")

with m1:
    with st.container(border=True):
        st.metric("Average Power/Ton", f"{df['power_per_ton'].mean():.2f}")

with m2:
    with st.container(border=True):
        st.metric("Max Power/Ton", f"{df['power_per_ton'].max():.2f}")

with m3:
    with st.container(border=True):
        st.metric("Min Power/Ton", f"{df['power_per_ton'].min():.2f}")

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns(2, gap="medium")

with left:
    with st.container(border=True):
        st.markdown("### Condenser Side")
        st.write("- ตรวจสอบ Condenser Pump")
        st.write("- ตรวจสอบ Cooling Tower")
        st.write("- ตรวจสอบการระบายความร้อน")

with right:
    with st.container(border=True):
        st.markdown("### Evaporator Side")
        st.write("- ตรวจสอบ Chilled Pump")
        st.write("- ตรวจสอบโหลดของ Chiller")
        st.write("- ตรวจสอบสมดุลการทำงาน")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("### Recommendation")
    if latest["power_per_ton"] > target_power_ton:
        st.warning("System is operating above target Power/Ton")
        st.write("1. ตรวจสอบปั๊มที่ใช้พลังงานสูง")
        st.write("2. ตรวจสอบ Cooling Tower")
        st.write("3. ตรวจสอบโหลดของ Chiller")
    else:
        st.success("System is operating within target range")
        st.write("✅ ระบบทำงานได้อย่างมีประสิทธิภาพ")