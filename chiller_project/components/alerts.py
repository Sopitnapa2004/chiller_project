"""
Alert display components for the Chiller System Dashboard.
"""

import streamlit as st
import pandas as pd
import config


def render_alerts_section(latest: pd.Series, target: float) -> None:
    """
    Render an alerts section showing power/ton status and recommendations.
    
    Args:
        latest: Latest record as pandas Series with system metrics
        target: Target power/ton threshold for comparison
    """
    with st.container(border=True):
        st.markdown("### Alerts")

        if latest.get("power_per_ton", 0) > target:
            st.warning("⚠️ Power/Ton สูงกว่าเป้าหมาย")
            st.markdown("""
            <div class="alert-list">
            • ตรวจสอบ Condenser Pump<br>
            • ตรวจสอบ Cooling Tower<br>
            • ตรวจสอบโหลดของ Chiller
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("✅ ระบบอยู่ในเกณฑ์ปกติ")