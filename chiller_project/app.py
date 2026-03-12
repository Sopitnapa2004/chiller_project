"""
Chiller System Dashboard - Main Application
Multi-building chiller system monitoring and optimization dashboard.
Provides real-time insights into power consumption, efficiency, and system health.
"""

import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_chiller_data,
    get_latest_snapshot,
    get_system_summary,
    get_building_overview,
)
from components.styles import load_global_styles
from components.header import render_sidebar, render_header
from components.kpi_cards import render_kpi_section
from components.equipment import render_equipment_section
from components.alerts import render_alerts_section
import config


def _initialize_session_state() -> None:
    """Initialize Streamlit session state with default values."""
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def _setup_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.LAYOUT,
    )


def _load_and_prepare_data() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """
    Load and prepare dashboard data.
    
    Returns:
        Tuple of (full_dataframe, latest_snapshot, summary_dict)
        
    Raises:
        FileNotFoundError: If data file not found
        ValueError: If CSV schema invalid
    """
    try:
        df = load_chiller_data(config.DEFAULT_DATA_FILE)
        latest_df = get_latest_snapshot(df)
        summary = get_system_summary(
            latest_df,
            st.session_state.target_power_ton
        )
        return df, latest_df, summary
    except FileNotFoundError as e:
        st.error(f"❌ Data Error: {e}")
        st.stop()
    except ValueError as e:
        st.error(f"❌ Schema Error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        st.stop()


def main() -> None:
    """Main application entry point."""
    # Setup
    _setup_page()
    _initialize_session_state()
    
    # Load styles and header
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_header()
    
    st.title("Dashboard")
    st.write("📊 Real-time monitoring of chiller system performance across all facilities")
    
    # Load data with error handling
    df, latest_df, summary = _load_and_prepare_data()
    
    # ==================== Summary Metrics ====================
    st.markdown("### System Overview")
    
    m1, m2, m3, m4 = st.columns(4, gap="medium")
    
    with m1:
        with st.container(border=True):
            st.metric("Status", summary["overall_status"])
    
    with m2:
        with st.container(border=True):
            st.metric("Buildings", summary["buildings_monitored"])
    
    with m3:
        with st.container(border=True):
            st.metric("Units Online", summary["units_online"])
    
    with m4:
        with st.container(border=True):
            st.metric("Active Alerts", summary["active_alerts"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== KPI Cards ====================
    render_kpi_section(latest_df.iloc[0], st.session_state.target_power_ton)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Equipment Status ====================
    render_equipment_section(latest_df.iloc[0])
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Alerts & Building Overview ====================
    col_left, col_right = st.columns([1, 1], gap="medium")
    
    with col_left:
        render_alerts_section(latest_df.iloc[0], st.session_state.target_power_ton)
    
    with col_right:
        with st.container(border=True):
            st.markdown("### Building Overview")
            building_df = get_building_overview(latest_df)
            if not building_df.empty:
                st.dataframe(
                    building_df[["building", "units", "total_power", "power_per_ton", "status"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No multi-building data available")
    
    st.markdown("<br>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()