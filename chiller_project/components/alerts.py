import pandas as pd
import streamlit as st
import config


def render_alert_summary(alert_df: pd.DataFrame) -> None:
    with st.container(border=True):
        st.markdown('<div class="section-title">Alert Summary</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Current rule-based exceptions requiring attention</div>',
            unsafe_allow_html=True,
        )

        if alert_df.empty:
            st.success("No active alerts")
            return

        critical = int((alert_df["status"] == config.STATUS_CRITICAL).sum())
        warning = int((alert_df["status"] == config.STATUS_WARNING).sum())
        check = int((alert_df["status"] == config.STATUS_CHECK).sum())

        c1, c2, c3 = st.columns(3)
        c1.metric("Critical", critical)
        c2.metric("Warning", warning)
        c3.metric("Check", check)