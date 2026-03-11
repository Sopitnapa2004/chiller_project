import streamlit as st


def render_equipment_card(
    image_path,
    title,
    status,
    note,
    power_kw=None,
    efficiency=None,
    page_path=None,
):
    status_class = "status-normal" if status == "Normal" else "status-check"

    with st.container(border=True):
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.image(image_path, width=105)

        st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{status_class}">{status}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="small-text">{note}</div>', unsafe_allow_html=True)

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


def render_equipment_section(latest):
    st.markdown("### Equipment Status")

    e1, e2, e3, e4 = st.columns(4, gap="medium")

    chiller_eff = (420 / latest["chiller_kw"]) * 100 if latest["chiller_kw"] > 0 else 0
    tower_eff = (50 / latest["cooling_tower_kw"]) * 100 if latest["cooling_tower_kw"] > 0 else 0
    condenser_eff = (30 / latest["condenser_pump_kw"]) * 100 if latest["condenser_pump_kw"] > 0 else 0
    chilled_eff = (40 / latest["chilled_pump_kw"]) * 100 if latest["chilled_pump_kw"] > 0 else 0

    with e1:
        render_equipment_card(
            "images/chiller.png",
            "Chiller",
            "Normal",
            "Main cooling unit",
            latest["chiller_kw"],
            chiller_eff,
            "pages/4_Chiller_Detail.py",
        )

    with e2:
        render_equipment_card(
            "images/cooling_tower.png",
            "Cooling Tower",
            "Normal",
            "Heat rejection",
            latest["cooling_tower_kw"],
            tower_eff,
            "pages/5_Cooling_Tower_Detail.py",
        )

    with e3:
        render_equipment_card(
            "images/condenser_pump.png",
            "Condenser Pump",
            "Check",
            "High pressure side",
            latest["condenser_pump_kw"],
            condenser_eff,
            "pages/6_Condenser_Pump_Detail.py",
        )

    with e4:
        render_equipment_card(
            "images/chilled_pump.png",
            "Chilled Pump",
            "Normal",
            "Low pressure side",
            latest["chilled_pump_kw"],
            chilled_eff,
            "pages/7_Chilled_Pump_Detail.py",
        )