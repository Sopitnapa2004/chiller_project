import streamlit as st


def _render_branding_section():
    logo_col, text_col = st.sidebar.columns([1, 2], gap="small")

    with logo_col:
        st.image("images/seagate_logo.png", width=95)

    with text_col:
        st.markdown("""
        <div style="padding-top: 7px;">
            <div style="font-size: 19px; font-weight: 700; color: white; line-height: 1.2;">
                Chiller System
            </div>
            <div style="font-size: 12px; color: #AEB7C2; margin-top: 2px;">
                Prototype Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("---")


def _render_navigation_section():
    st.sidebar.page_link("app.py", label="Dashboard")
    st.sidebar.page_link("pages/1_Trend_Monitoring.py", label="Trend Monitoring")
    st.sidebar.page_link("pages/2_Analytics.py", label="Analytics")
    st.sidebar.page_link("pages/3_Alerts.py", label="Alerts")
    st.sidebar.markdown("---")


def _render_target_section(target):
    st.sidebar.write("**Target Power/Ton**")
    st.sidebar.success(f"{target:.2f} kW/Ton")
    st.sidebar.markdown("---")


def _render_system_info_section():
    st.sidebar.write("**System Info**")
    st.sidebar.caption("Last updated: 2026-03-10 15:00")
    st.sidebar.caption("Data points: 8")
    st.sidebar.markdown("---")


def _render_settings_section(target):
    with st.sidebar.expander("⚙️ Settings"):
        new_target = st.number_input(
            "Target Power/Ton",
            min_value=0.10,
            max_value=2.00,
            value=float(target),
            step=0.01,
            format="%.2f",
        )
        if st.button("Update Target", key="update_target"):
            st.session_state.target_power_ton = new_target
            st.rerun()


def render_sidebar(target):
    _render_branding_section()
    _render_navigation_section()
    _render_target_section(target)
    _render_system_info_section()
    _render_settings_section(target)


def render_header():
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

    logo_col, title_col = st.columns([1.1, 5], gap="medium")

    with logo_col:
        st.markdown("<div style='height: 26px;'></div>", unsafe_allow_html=True)
        st.image("images/seagate_logo.png", width=120)

    with title_col:
        st.markdown("""
        <div class="header-wrap">
            <div class="header-title">SEAGATE KORAT FACILITY</div>
            <div class="header-subtitle">Chiller System Optimization & Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)