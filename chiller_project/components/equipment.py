"""
Equipment display components for the Chiller System Dashboard.
Shows individual equipment status, power consumption, and efficiency metrics.
"""

import streamlit as st
import pandas as pd
import config


def render_equipment_card(
    image_path: str,
    title: str,
    status: str,
    note: str,
    power_kw: float = None,
    efficiency: float = None,
    page_path: str = None,
) -> None:
    """
    Render a single equipment status card.
    
    Args:
        image_path: Path to equipment image
        title: Equipment name/title
        status: Status text ("Normal", "Check", "Warning", "Critical")
        note: Short description note
        power_kw: Optional power consumption in kW
        efficiency: Optional efficiency percentage
        page_path: Optional path to detailed equipment page
    """
    status_class = (
        "status-normal" if status == config.STATUS_NORMAL else "status-check"
    )

    with st.container(border=True):
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.image(image_path, width=config.Equipment_CARD_WIDTH)

        st.markdown(
            f'<div class="card-title">{title}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="{status_class}">{status}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="small-text">{note}</div>',
            unsafe_allow_html=True
        )

        if power_kw is not None:
            st.markdown(
                f'<div class="small-text">Power: {power_kw:.1f} kW</div>',
                unsafe_allow_html=True
            )

        if efficiency is not None:
            st.markdown(
                f'<div class="small-text">Efficiency: {efficiency:.1f}%</div>',
                unsafe_allow_html=True
            )

        if page_path:
            st.page_link(page_path, label="View Details")


def _safe_efficiency_calc(baseline_ton: float, power_kw: float) -> float:
    """
    Safely calculate equipment efficiency percentage.
    
    Args:
        baseline_ton: Baseline ton capacity for the equipment
        power_kw: Actual power consumption in kW
        
    Returns:
        Efficiency as percentage, or 0 if calculation fails
    """
    if power_kw <= 0:
        return 0.0
    return (baseline_ton / power_kw) * 100


def render_equipment_section(latest: pd.Series) -> None:
    """
    Render the complete equipment status section with 4 equipment cards.
    
    Args:
        latest: Latest record as pandas Series containing equipment power values
    """
    st.markdown("### Equipment Status")

    e1, e2, e3, e4 = st.columns(4, gap="medium")

    # Calculate efficiency for each equipment
    chiller_eff = _safe_efficiency_calc(
        config.CHILLER_BASELINE_TON,
        latest.get("chiller_kw", 0)
    )
    tower_eff = _safe_efficiency_calc(
        config.COOLING_TOWER_BASELINE_TON,
        latest.get("cooling_tower_kw", 0)
    )
    condenser_eff = _safe_efficiency_calc(
        config.CONDENSER_PUMP_BASELINE_TON,
        latest.get("condenser_pump_kw", 0)
    )
    chilled_eff = _safe_efficiency_calc(
        config.CHILLED_PUMP_BASELINE_TON,
        latest.get("chilled_pump_kw", 0)
    )

    with e1:
        render_equipment_card(
            config.CHILLER_IMAGE_PATH,
            config.EQUIPMENT_CHILLER,
            config.STATUS_NORMAL,
            "Main cooling unit",
            latest.get("chiller_kw", 0),
            chiller_eff,
            "pages/4_Chiller_Detail.py"
        )

    with e2:
        render_equipment_card(
            config.COOLING_TOWER_IMAGE_PATH,
            config.EQUIPMENT_COOLING_TOWER,
            config.STATUS_NORMAL,
            "Heat rejection",
            latest.get("cooling_tower_kw", 0),
            tower_eff,
            "pages/5_Cooling_Tower_Detail.py"
        )

    with e3:
        render_equipment_card(
            config.CONDENSER_PUMP_IMAGE_PATH,
            config.EQUIPMENT_CONDENSER_PUMP,
            config.STATUS_CHECK,
            "High pressure side",
            latest.get("condenser_pump_kw", 0),
            condenser_eff,
            "pages/6_Condenser_Pump_Detail.py"
        )

    with e4:
        render_equipment_card(
            config.CHILLED_PUMP_IMAGE_PATH,
            config.EQUIPMENT_CHILLED_PUMP,
            config.STATUS_NORMAL,
            "Low pressure side",
            latest.get("chilled_pump_kw", 0),
            chilled_eff,
            "pages/7_Chilled_Pump_Detail.py"
        )