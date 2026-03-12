"""
KPI (Key Performance Indicator) card components for the Chiller System Dashboard.
Displays key system metrics in attractive card layouts.
"""

import streamlit as st
import pandas as pd
from typing import Tuple, Optional

import config


def _get_efficiency_rating(efficiency: float) -> Tuple[str, str]:
    """
    Get efficiency rating label and color based on percentage.
    
    Args:
        efficiency: Efficiency percentage
        
    Returns:
        Tuple of (rating_label, color_hex)
    """
    if efficiency >= config.EFFICIENCY_EXCELLENT:
        return "Excellent", "#22C55E"
    elif efficiency >= config.EFFICIENCY_MODERATE:
        return "Moderate", "#F59E0B"
    else:
        return "Low", "#EF4444"


def _render_kpi_card(
    column: st.delta_generator.DeltaGenerator,
    label: str,
    value: str,
    note: str,
    note_color: Optional[str] = None,
) -> None:
    """
    Helper to render a single KPI card inside a given column.

    Args:
        column: Streamlit column object where the card should appear.
        label: KPI label text.
        value: KPI value to display (already formatted).
        note: Supplemental note text below the value.
        note_color: Optional CSS color for the note text.
    """
    with column:
        with st.container(border=True):
            st.markdown(f'<div class="kpi-label">{label}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-value">{value}</div>', unsafe_allow_html=True)
            style = f' style="color:{note_color};"' if note_color else ""
            st.markdown(f'<div class="kpi-note"{style}>{note}</div>', unsafe_allow_html=True)


def render_kpi_section(latest: pd.Series, target: float) -> None:
    """
    Render the KPI metrics section with four cards.

    The cards are:
    1. Power/Ton (current vs target)
    2. Total Power (kW)
    3. Target Power/Ton
    4. Efficiency (%) derived from power/ton and target

    Args:
        latest: Latest record as pandas Series with system metrics.
        target: Target power/ton threshold for comparison.
    """
    k1, k2, k3, k4 = st.columns(4, gap="medium")

    # Validate inputs
    if not isinstance(latest, pd.Series):
        raise TypeError("latest must be a pandas Series")
    if target <= 0:
        raise ValueError("target must be a positive number")

    # Calculate efficiency safely
    power_per_ton = latest.get("power_per_ton", 0) or 0
    efficiency = (target / power_per_ton * 100) if power_per_ton > 0 else 0


    # KPI 1: Power/Ton
    status_note = "Above target" if power_per_ton > target else "Normal"
    status_color = "#F59E0B" if power_per_ton > target else "#22C55E"
    _render_kpi_card(k1, "Power/Ton", f"{power_per_ton:.2f}", status_note, status_color)

    # KPI 2: Total Power
    total_power = latest.get("total_power", 0)
    _render_kpi_card(k2, "Total Power (kW)", f"{total_power:.0f}", "Combined equipment load")

    # KPI 3: Target Power/Ton
    _render_kpi_card(k3, "Target (kW/Ton)", f"{target:.2f}", "Configured threshold")

    # KPI 4: Efficiency
    note, color = _get_efficiency_rating(efficiency)
    _render_kpi_card(k4, "Efficiency (%)", f"{efficiency:.1f}%", note, color)
