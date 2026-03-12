"""
Alerts Page - Chiller System Dashboard
Displays active system alerts and anomalies by building and equipment.
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_chiller_data, get_latest_snapshot
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button
import config


def _initialize_session_state() -> None:
    """Initialize session state with default values."""
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def _load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load data with error handling."""
    try:
        df = load_chiller_data(config.DEFAULT_DATA_FILE)
        latest_df = get_latest_snapshot(df)
        return df, latest_df
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.stop()
    except ValueError as e:
        st.error(f"❌ Invalid CSV schema: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def _get_alert_dataframe(latest_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter dataframe to only show alerts.
    
    Args:
        latest_df: Latest snapshot dataframe
        
    Returns:
        Filtered dataframe with only alert status records
    """
    if "status" not in latest_df.columns:
        return pd.DataFrame()
    
    return latest_df[latest_df["status"].isin(config.STATUS_ALERT_VALUES)].copy()


def _render_alert_summary(alert_df: pd.DataFrame) -> None:
    """Render alert summary metrics."""
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        buildings_with_issues = (
            alert_df["building"].nunique() if len(alert_df) > 0 and "building" in alert_df.columns else 0
        )
        st.metric("Buildings with Issues", buildings_with_issues)
    
    with col2:
        units_with_issues = (
            alert_df["unit_id"].nunique() if len(alert_df) > 0 and "unit_id" in alert_df.columns else 0
        )
        st.metric("Units with Issues", units_with_issues)
    
    with col3:
        st.metric("Total Alerts", len(alert_df))


def _render_alert_filters(alert_df: pd.DataFrame) -> tuple[str, str]:
    """
    Render filter controls for alerts.
    
    Args:
        alert_df: Alerts dataframe
        
    Returns:
        Tuple of (selected_building, selected_equipment)
    """
    f1, f2 = st.columns(2, gap="medium")
    
    with f1:
        building_options = (
            ["All"] + sorted(alert_df["building"].dropna().unique().tolist())
            if len(alert_df) > 0 and "building" in alert_df.columns
            else ["All"]
        )
        selected_building = st.selectbox("Building", building_options)
    
    with f2:
        equipment_options = (
            ["All"] + sorted(alert_df["equipment_type"].dropna().unique().tolist())
            if len(alert_df) > 0 and "equipment_type" in alert_df.columns
            else ["All"]
        )
        selected_equipment = st.selectbox("Equipment Type", equipment_options)
    
    return selected_building, selected_equipment


def _render_alert_table(filtered_alerts: pd.DataFrame) -> None:
    """Render the active alerts data table."""
    with st.container(border=True):
        st.markdown("### Active Alerts")
        
        if len(filtered_alerts) > 0:
            display_cols = [col for col in ["building", "unit_id", "equipment_type", "power_kw", "status"] 
                          if col in filtered_alerts.columns]
            st.dataframe(
                filtered_alerts[display_cols],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.success("✅ No active alerts found.")


def _render_building_alert_summary(alert_df: pd.DataFrame) -> None:
    """Render alert summary grouped by building."""
    with st.container(border=True):
        st.markdown("### Alert Summary by Building")
        
        if len(alert_df) > 0 and "building" in alert_df.columns:
            building_alerts = (
                alert_df.groupby("building", as_index=False)
                .agg(
                    active_alerts=("unit_id", "count"),
                    affected_units=("unit_id", "nunique") if "unit_id" in alert_df.columns else lambda x: 1,
                )
            )
            st.dataframe(building_alerts, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No building-level alert data available.")


def main() -> None:
    """Main page logic."""
    # Setup
    st.set_page_config(page_title="Alerts", page_icon="🚨", layout="wide")
    _initialize_session_state()
    
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_back_button()
    
    st.title("Alerts")
    st.write("🚨 System alerts and anomalies by building and equipment")
    
    # Load data
    df, latest_df = _load_data()
    
    # Get alerts only
    alert_df = _get_alert_dataframe(latest_df)
    
    # ==================== Alert Summary ====================
    st.markdown("### Alert Summary")
    _render_alert_summary(alert_df)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Filters ====================
    if len(alert_df) > 0:
        st.markdown("### Filters")
        selected_building, selected_equipment = _render_alert_filters(alert_df)
        
        # Apply filters
        filtered_alerts = alert_df.copy()
        
        if selected_building != "All":
            filtered_alerts = filtered_alerts[filtered_alerts["building"] == selected_building]
        
        if selected_equipment != "All":
            filtered_alerts = filtered_alerts[filtered_alerts["equipment_type"] == selected_equipment]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ==================== Alert Table ====================
        _render_alert_table(filtered_alerts)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Building Alert Summary ====================
    _render_building_alert_summary(alert_df)


if __name__ == "__main__":
    main()