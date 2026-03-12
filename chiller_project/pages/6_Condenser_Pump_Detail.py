"""
Condenser Pump Detail Page - Chiller System Dashboard
Detailed monitoring and analysis for the Condenser Pump equipment.
"""

import streamlit as st
from utils.data_loader import load_chiller_data, get_latest_row
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button
import config


def _initialize_session_state() -> None:
    """Initialize session state with default values."""
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def _load_data():
    """Load data with error handling."""
    try:
        df = load_chiller_data(config.DEFAULT_DATA_FILE)
        latest = get_latest_row(df)
        return df, latest
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def _safe_efficiency(baseline: float, power: float) -> float:
    """Safely calculate efficiency percentage."""
    return (baseline / power * 100) if power > 0 else 0.0


def main() -> None:
    """Main page logic."""
    st.set_page_config(page_title="Condenser Pump Detail", page_icon="🔧", layout="wide")
    _initialize_session_state()
    
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_back_button()
    
    st.title("Condenser Pump Unit - Detailed Analysis")
    st.write("📊 In-depth monitoring and performance metrics for the Condenser Pump")
    
    # Load data
    df, latest = _load_data()
    
    # ==================== Current Overview ====================
    st.markdown("### Current Overview")
    
    top1, top2 = st.columns([1, 3], gap="medium")
    
    with top1:
        with st.container(border=True):
            st.image(config.CONDENSER_PUMP_IMAGE_PATH, use_container_width=True)
    
    with top2:
        with st.container(border=True):
            pump_kw = latest.get("condenser_pump_kw", 0)
            efficiency = _safe_efficiency(config.CONDENSER_PUMP_BASELINE_TON, pump_kw)
            
            st.write(f"**Status:** ⚠️ Check")
            st.write(f"**Current Power:** {pump_kw:.1f} kW")
            st.write(f"**Efficiency:** {efficiency:.1f}%")
            st.write(f"**Baseline Capacity:** {config.CONDENSER_PUMP_BASELINE_TON} Ton")
            st.info("This unit requires attention. Monitor for irregular power consumption patterns.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Trend Chart ====================
    with st.container(border=True):
        st.markdown("### Power Consumption Trend")
        if "condenser_pump_kw" in df.columns:
            chart_df = df[["timestamp", "condenser_pump_kw"]].copy().set_index("timestamp")
            st.line_chart(chart_df, use_container_width=True)
        else:
            st.info("No trend data available")


if __name__ == "__main__":
    main()