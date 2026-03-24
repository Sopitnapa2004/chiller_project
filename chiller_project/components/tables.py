import pandas as pd
import streamlit as st


def render_dataframe_section(title: str, df: pd.DataFrame, subtitle: str = "") -> None:
    with st.container(border=True):
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

        if subtitle:
            st.markdown(f'<div class="section-subtitle">{subtitle}</div>', unsafe_allow_html=True)

        if df.empty:
            st.info("No data available")
            return

        st.dataframe(df, use_container_width=True, hide_index=True)