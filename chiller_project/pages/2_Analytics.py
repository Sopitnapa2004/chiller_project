"""
Analytics Page - Chiller System Dashboard
Provides building-level and equipment-level analytics and insights.
"""

import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_chiller_data,
    get_latest_snapshot,
    get_building_overview,
    get_system_summary,
)
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button
import config


def _initialize_session_state() -> None:
    """Initialize session state with default values."""
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def _load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Load data with error handling."""
    try:
        df = load_chiller_data(config.DEFAULT_DATA_FILE)
        latest_df = get_latest_snapshot(df)
        building_df = get_building_overview(latest_df)
        summary = get_system_summary(latest_df, st.session_state.target_power_ton)
        return df, latest_df, building_df, summary
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.stop()
    except ValueError as e:
        st.error(f"❌ Invalid CSV schema: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def _render_summary_metrics(summary: dict) -> None:
    """Render summary KPI metrics."""
    m1, m2, m3 = st.columns(3, gap="medium")
    
    with m1:
        with st.container(border=True):
            st.metric("Fleet Power/Ton", f"{summary['fleet_power_ton']:.2f}")
    
    with m2:
        with st.container(border=True):
            st.metric("Total Buildings", summary["buildings_monitored"])
    
    with m3:
        with st.container(border=True):
            st.metric("Total Units", summary["units_online"])


def _render_building_analytics(building_df: pd.DataFrame, target: float) -> None:
    """Render building-level analytics section."""
    left, right = st.columns(2, gap="medium")
    
    with left:
        with st.container(border=True):
            st.markdown("### Building Performance")
            if not building_df.empty:
                st.dataframe(
                    building_df[["building", "status", "units", "active_alerts", "power_per_ton"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No building data available")
    
    with right:
        with st.container(border=True):
            st.markdown("### Key Insight")
            
            if not building_df.empty:
                worst_building = building_df.sort_values("power_per_ton", ascending=False).iloc[0]
                st.write(f"**Highest Power/Ton:** {worst_building['building']}")
                st.write(f"**Power/Ton:** {worst_building['power_per_ton']:.2f}")
                st.write(f"**Active Alerts:** {int(worst_building['active_alerts'])}")
                
                if worst_building["power_per_ton"] > target:
                    st.warning("⚠️ This building is operating above target.")
                else:
                    st.success("✅ All buildings are within acceptable range.")
            else:
                st.info("Insufficient data for analysis")


def _render_equipment_analytics(latest_df: pd.DataFrame) -> None:
    """Render equipment-type level analytics."""
    with st.container(border=True):
        st.markdown("### Equipment Type Overview")
        
        if "equipment_type" in latest_df.columns and not latest_df.empty:
            alert_values = config.STATUS_ALERT_VALUES
            equipment_df = (
                latest_df.groupby("equipment_type", as_index=False)
                .agg(
                    units=("unit_id", "nunique") if "unit_id" in latest_df.columns else lambda x: 1,
                    avg_power=("power_kw", "mean") if "power_kw" in latest_df.columns else lambda x: 0,
                    alerts=("status", lambda x: x.isin(alert_values).sum()) if "status" in latest_df.columns else lambda x: 0,
                )
            )
            
            st.dataframe(equipment_df, use_container_width=True, hide_index=True)
        else:
            st.info("No equipment type data available")


def _render_recommendations(summary: dict, target: float) -> None:
    """Render system recommendations based on analysis."""
    with st.container(border=True):
        st.markdown("### Recommendations")
        
        if summary["active_alerts"] > 0:
            st.warning(f"⚠️ {summary['active_alerts']} active issues detected in the system.")
            st.write("**Actions:**")
            st.write("- Prioritize buildings with highest Power/Ton")
            st.write("- Review units with status Check / Warning / Critical")
            st.write("- Inspect condenser-side equipment if power usage is elevated")
        else:
            st.success("✅ The monitored system is currently stable.")
            st.write("**Actions:**")
            st.write("- Continue normal monitoring schedule")
            st.write("- Maintain preventive inspection schedule")


def main() -> None:
    """Main page logic."""
    # Setup
    st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
    _initialize_session_state()
    
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_back_button()
    
    st.title("Analytics")
    st.write("📊 Analyze system performance at building and equipment levels")
    
    # Load data
    df, latest_df, building_df, summary = _load_data()
    
    # ==================== Summary Metrics ====================
    st.markdown("### System Summary")
    _render_summary_metrics(summary)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Building Analytics ====================
    st.markdown("### Building Level Analysis")
    _render_building_analytics(building_df, st.session_state.target_power_ton)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Equipment Analytics ====================
    st.markdown("### Equipment Analysis")
    _render_equipment_analytics(latest_df)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Recommendations ====================
    st.markdown("### System Insights")
    _render_recommendations(summary, st.session_state.target_power_ton)


if __name__ == "__main__":
    main()