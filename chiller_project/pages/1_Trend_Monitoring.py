import streamlit as st
import pandas as pd

from utils.data_loader import load_chiller_data
from components.styles import load_global_styles
from components.header import render_sidebar

st.set_page_config(page_title="Trend Monitoring", page_icon="📈", layout="wide")

if "target_power_ton" not in st.session_state:
    st.session_state.target_power_ton = 0.75

target_power_ton = st.session_state.target_power_ton

df = load_chiller_data("sample_data.csv")

load_global_styles()
render_sidebar(target_power_ton)

st.title("Trend Monitoring")
st.write("ติดตามแนวโน้มของพารามิเตอร์ต่าง ๆ ในระบบ")

st.markdown("### Time Range")
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime(df["timestamp"].min()).date())

with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime(df["timestamp"].max()).date())

df["timestamp"] = pd.to_datetime(df["timestamp"])
filtered_df = df[
    (df["timestamp"].dt.date >= start_date) &
    (df["timestamp"].dt.date <= end_date)
]

st.markdown("---")

parameter = st.selectbox(
    "Select Parameter",
    [
        "power_per_ton",
        "total_power",
        "chiller_kw",
        "cooling_tower_kw",
        "condenser_pump_kw",
        "chilled_pump_kw",
        "ton",
    ],
)

left, right = st.columns([2, 1], gap="medium")

with left:
    with st.container(border=True):
        st.markdown(f"### Trend: {parameter.replace('_', ' ').title()}")
        if len(filtered_df) > 0:
            trend_df = filtered_df[["timestamp", parameter]].copy().set_index("timestamp")
            st.line_chart(trend_df, use_container_width=True)
        else:
            st.warning("No data available for selected time range")

with right:
    with st.container(border=True):
        st.markdown("### Statistics")
        if len(filtered_df) > 0:
            stats_df = filtered_df[[parameter]].describe().T
            st.dataframe(stats_df, use_container_width=True)

            st.markdown("#### Key Metrics")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Average", f"{filtered_df[parameter].mean():.2f}")
                st.metric("Minimum", f"{filtered_df[parameter].min():.2f}")
            with c2:
                st.metric("Maximum", f"{filtered_df[parameter].max():.2f}")
                st.metric("Std Dev", f"{filtered_df[parameter].std():.2f}")
        else:
            st.warning("No data available for selected time range")