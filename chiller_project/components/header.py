import streamlit as st
import config
from datetime import datetime


def render_sidebar(target: float) -> None:
    logo_col, text_col = st.sidebar.columns([1, 2])
    with logo_col:
        st.image(config.SEAGATE_LOGO_PATH, width=config.LOGO_WIDTH_SIDEBAR)
    with text_col:
        st.markdown(
            """
            <div style="padding-top: 8px;">
                <div style="font-size: 16px; font-weight: 800; color: #F8FAFC;">
                    Chiller<br>Operations
                </div>
                <div style="font-size: 11px; color: #94A3B8;">MANAGEMENT SYSTEM</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.sidebar.page_link("app.py", label="📊 Dashboard")
    st.sidebar.page_link("pages/2_Engineering_Analytics.py", label="📈 Engineering Analytics")

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.sidebar.markdown(
        f"""
        <div style="font-size: 0.8rem; color:#94A3B8;">Performance Target</div>
        <div style="font-size: 1.5rem; color:#3B82F6; font-weight:800;">{target:.2f}</div>
        <div style="font-size: 0.75rem; color:#64748B;">kW/Ton</div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.sidebar.caption(f"Updated: {datetime.now().strftime('%m/%d %H:%M')}")


def render_header() -> None:
    logo_col, title_col = st.columns([1.1, 5])
    with logo_col:
        st.image(config.SEAGATE_LOGO_PATH, width=config.LOGO_WIDTH_HEADER)
    with title_col:
        st.markdown(
            f"""
            <div class="header-wrap">
                <div class="header-title">{config.FACILITY_NAME}</div>
                <div class="header-subtitle">{config.FACILITY_SUBTITLE}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )