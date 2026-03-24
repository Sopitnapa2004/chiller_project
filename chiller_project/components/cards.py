import streamlit as st
import config


def get_status_class(status: str) -> str:
    mapping = {
        config.STATUS_NORMAL: "status-normal",
        config.STATUS_CHECK: "status-check",
        config.STATUS_WARNING: "status-warning",
        config.STATUS_CRITICAL: "status-critical",
    }
    return mapping.get(status, "status-check")


def render_kpi_card(column, label: str, value: str, note: str, note_color: str | None = None) -> None:
    with column:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="padding: 6px 0;">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if note:
                style = f' style="color:{note_color};"' if note_color else ""
                st.markdown(f'<div class="kpi-note"{style}>{note}</div>', unsafe_allow_html=True)


def render_equipment_card(
    image_path: str,
    title: str,
    status: str,
    note: str,
    power_kw: float,
    power_per_ton: float,
    page_path: str,
) -> None:
    with st.container(border=True):
        _, img_col, _ = st.columns([0.7, 2.6, 0.7])
        with img_col:
            st.image(image_path, width=config.EQUIPMENT_CARD_WIDTH)

        st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{get_status_class(status)}">{status}</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.12);">
                <div class="small-text">• {note}</div>
                <div class="small-text" style="margin-top: 8px;">⚡ {power_kw:,.1f} kW</div>
                <div class="small-text">📊 {power_per_ton:,.2f} kW/Ton</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.page_link(page_path, label="→ View Details")
