import streamlit as st


def render_alerts_section(latest, target):
    with st.container(border=True):
        st.markdown("### Alerts")

        if latest["power_per_ton"] > target:
            st.warning("Power/Ton สูงกว่าเป้าหมาย")
            st.markdown("""
            <div class="alert-list">
            • ตรวจสอบ Condenser Pump<br>
            • ตรวจสอบ Cooling Tower<br>
            • ตรวจสอบโหลดของ Chiller
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("ระบบอยู่ในเกณฑ์ปกติ")