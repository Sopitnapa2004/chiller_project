"""
Trend Monitoring Page - Chiller System Dashboard
Provides trend analysis charts and statistics for chiller system metrics.
"""

import streamlit as st
import pandas as pd
from utils.data_loader import load_chiller_data
from components.styles import load_global_styles
from components.header import render_sidebar
from components.navigation import render_back_button
import config


def _initialize_session_state() -> None:
    """Initialize session state with default values."""
    if "target_power_ton" not in st.session_state:
        st.session_state.target_power_ton = config.DEFAULT_TARGET_POWER_TON


def _load_data() -> pd.DataFrame:
    """Load data with error handling."""
    try:
        return load_chiller_data(config.DEFAULT_DATA_FILE)
    except FileNotFoundError as e:
        st.error(f"❌ Data file not found: {e}")
        st.stop()
    except ValueError as e:
        st.error(f"❌ Invalid CSV schema: {e}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()


def _build_metric_series(
    df: pd.DataFrame,
    metric_type: str,
    building_filter: str = "All",
    equipment_filter: str = "All",
    unit_filter: str = "All"
) -> pd.Series:
    """
    Build a time series for the selected metric with filters applied.
    
    Args:
        df: Input dataframe
        metric_type: Type of metric to analyze
        building_filter: Building filter value
        equipment_filter: Equipment type filter value
        unit_filter: Unit ID filter value
        
    Returns:
        Pandas Series indexed by timestamp
    """
    filtered_df = df.copy()
    
    if building_filter != "All":
        filtered_df = filtered_df[filtered_df["building"] == building_filter]
    if equipment_filter != "All":
        filtered_df = filtered_df[filtered_df["equipment_type"] == equipment_filter]
    if unit_filter != "All":
        filtered_df = filtered_df[filtered_df["unit_id"] == unit_filter]
    
    if metric_type == "power_per_ton_building":
        trend_df = (
            filtered_df.groupby(["timestamp", "building"], as_index=False)
            .agg(total_power=("power_kw", "sum"), ton=("ton", "mean"))
        )
        trend_df["power_per_ton_building"] = trend_df.apply(
            lambda row: row["total_power"] / row["ton"] if row["ton"] > 0 else 0,
            axis=1
        )
        return trend_df["power_per_ton_building"]
    else:
        return filtered_df.groupby("timestamp", as_index=False)[metric_type].mean()


def main() -> None:
    """Main page logic."""
    # Setup
    st.set_page_config(page_title="Trend Monitoring", page_icon="📈", layout="wide")
    _initialize_session_state()
    
    load_global_styles()
    render_sidebar(st.session_state.target_power_ton)
    render_back_button()
    
    st.title("Trend Monitoring")
    st.write("📈 Track system performance trends across buildings and equipment")
    
    # Load data
    df = _load_data()
    
    # ==================== Filters ====================
    with st.expander("🔍 Filters", expanded=True):
        st.markdown("<div style='padding:0 8px;'>", unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4, gap="medium")

        with f1:
            building_options = (
                ["All"] + sorted(df["building"].dropna().unique().tolist())
                if "building" in df.columns else ["All"]
            )
            selected_building = st.selectbox("Building", building_options)

        with f2:
            equipment_options = (
                ["All"] + sorted(df["equipment_type"].dropna().unique().tolist())
                if "equipment_type" in df.columns else ["All"]
            )
            selected_equipment = st.selectbox("Equipment Type", equipment_options)

        with f3:
            filtered_for_unit = df.copy()
            if selected_building != "All":
                filtered_for_unit = filtered_for_unit[filtered_for_unit["building"] == selected_building]
            if selected_equipment != "All":
                filtered_for_unit = filtered_for_unit[filtered_for_unit["equipment_type"] == selected_equipment]
            
            unit_options = (
                ["All"] + sorted(filtered_for_unit["unit_id"].dropna().unique().tolist())
                if "unit_id" in filtered_for_unit.columns else ["All"]
            )
            selected_unit = st.selectbox("Unit ID", unit_options)

        with f4:
            metric_type = st.selectbox(
                "Metric",
                ["power_kw", "ton", "power_per_ton_building"],
                help="Select the metric to display in trend"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📅 Date Range", expanded=False):
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=df["timestamp"].min().date()
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=df["timestamp"].max().date()
            )
    
    # Apply filters
    filtered_df = df[
        (df["timestamp"].dt.date >= start_date) &
        (df["timestamp"].dt.date <= end_date)
    ].copy()
    
    if selected_building != "All":
        filtered_df = filtered_df[filtered_df["building"] == selected_building]
    if selected_equipment != "All":
        filtered_df = filtered_df[filtered_df["equipment_type"] == selected_equipment]
    if selected_unit != "All":
        filtered_df = filtered_df[filtered_df["unit_id"] == selected_unit]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== Trend Chart & Statistics ====================
    left, right = st.columns([2, 1], gap="medium")
    
    with left:
        with st.container(border=True):
            st.markdown("### Trend Chart")
            
            if len(filtered_df) == 0:
                st.warning("⚠️ No data available for selected filters.")
            else:
                if metric_type == "power_per_ton_building":
                    trend_df = (
                        filtered_df.groupby(["timestamp", "building"], as_index=False)
                        .agg(total_power=("power_kw", "sum"), ton=("ton", "mean"))
                    )
                    trend_df["power_per_ton_building"] = trend_df.apply(
                        lambda row: row["total_power"] / row["ton"] if row["ton"] > 0 else 0,
                        axis=1
                    )
                    chart_df = trend_df[["timestamp", "power_per_ton_building"]].set_index("timestamp")
                else:
                    chart_df = (
                        filtered_df.groupby("timestamp", as_index=False)[metric_type]
                        .mean()
                        .set_index("timestamp")
                    )
                
                st.line_chart(chart_df, use_container_width=True)
    
    with right:
        with st.container(border=True):
            st.markdown("### Statistics")
            
            if len(filtered_df) == 0:
                st.warning("⚠️ No data available.")
            else:
                if metric_type == "power_per_ton_building":
                    stats_df = (
                        filtered_df.groupby(["timestamp", "building"], as_index=False)
                        .agg(total_power=("power_kw", "sum"), ton=("ton", "mean"))
                    )
                    stats_df["power_per_ton_building"] = stats_df.apply(
                        lambda row: row["total_power"] / row["ton"] if row["ton"] > 0 else 0,
                        axis=1
                    )
                    metric_series = stats_df["power_per_ton_building"]
                else:
                    metric_series = filtered_df[metric_type]
                
                st.metric("Average", f"{metric_series.mean():.2f}")
                st.metric("Maximum", f"{metric_series.max():.2f}")
                st.metric("Minimum", f"{metric_series.min():.2f}")
                st.metric("Std Dev", f"{metric_series.std():.2f}")


if __name__ == "__main__":
    main()