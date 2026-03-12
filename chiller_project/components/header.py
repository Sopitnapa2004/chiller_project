"""
Header and sidebar components for the Chiller System Dashboard.
Provides branding, navigation, system info, and configuration options.
"""

import streamlit as st
from datetime import datetime
import config


def _render_branding_section() -> None:
    """
    Render the branding section in the sidebar with logo and title.
    """
    logo_col, text_col = st.sidebar.columns([1, 2], gap="small")

    with logo_col:
        st.image(config.SEAGATE_LOGO_PATH, width=config.LOGO_WIDTH_SIDEBAR)

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


def _render_navigation_section() -> None:
    """
    Render navigation links in the sidebar.
    """
    st.sidebar.page_link("app.py", label="Dashboard")
    st.sidebar.page_link("pages/1_Trend_Monitoring.py", label="Trend Monitoring")
    st.sidebar.page_link("pages/2_Analytics.py", label="Analytics")
    st.sidebar.page_link("pages/3_Alerts.py", label="Alerts")
    st.sidebar.markdown("---")


def _render_target_section(target: float) -> None:
    """
    Render the current target power/ton setting display.
    
    Args:
        target: Current target power/ton value
    """
    st.sidebar.write("**Target Power/Ton**")
    st.sidebar.success(f"{target:.2f} kW/Ton")
    st.sidebar.markdown("---")


def _render_system_info_section() -> None:
    """
    Render system information such as last update time and data points.
    """
    st.sidebar.write("**System Info**")
    
    # Get current date for display
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.sidebar.caption(f"Last updated: {current_date}")
    st.sidebar.caption("Data points: 8")
    st.sidebar.markdown("---")


def _render_settings_section(target: float) -> None:
    """
    Render the settings expander with configuration options.
    
    Args:
        target: Current target power/ton value
    """
    with st.sidebar.expander("⚙️ Settings"):
        new_target = st.number_input(
            "Target Power/Ton",
            min_value=config.MIN_TARGET_POWER_TON,
            max_value=config.MAX_TARGET_POWER_TON,
            value=float(target),
            step=0.01,
            format="%.2f",
        )
        if st.button("Update Target", key="update_target"):
            st.session_state.target_power_ton = new_target
            st.rerun()


def render_sidebar(target: float) -> None:
    """
    Render the complete sidebar with all sections.
    
    Args:
        target: Current target power/ton value
    """
    _render_branding_section()
    _render_navigation_section()
    _render_target_section(target)
    _render_system_info_section()
    _render_settings_section(target)


def render_header() -> None:
    """
    Render the main header with facility branding and title.
    """
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    logo_col, title_col = st.columns([1.1, 5], gap="medium")

    with logo_col:
        st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
        st.image(config.SEAGATE_LOGO_PATH, width=config.LOGO_WIDTH_HEADER)

    with title_col:
        st.markdown(f"""
        <div class="header-wrap">
            <div class="header-title">{config.FACILITY_NAME}</div>
            <div class="header-subtitle">{config.FACILITY_SUBTITLE}</div>
        </div>
        """, unsafe_allow_html=True)