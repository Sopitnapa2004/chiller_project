import streamlit as st


def render_kpi_section(latest, target):
    k1, k2, k3, k4 = st.columns(4, gap="medium")

    efficiency = (target / latest["power_per_ton"]) * 100 if latest["power_per_ton"] > 0 else 0

    with k1:
        with st.container(border=True):
            st.markdown('<div class="kpi-label">Power/Ton</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-value">{latest["power_per_ton"]:.2f}</div>', unsafe_allow_html=True)
            if latest["power_per_ton"] > target:
                st.markdown('<div class="kpi-note" style="color:#FFB84D;">⚠️ Above target</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="kpi-note" style="color:#22C55E;">✅ Normal</div>', unsafe_allow_html=True)

    with k2:
        with st.container(border=True):
            st.markdown('<div class="kpi-label">Total Power (kW)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-value">{latest["total_power"]:.0f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-note">Combined equipment load</div>', unsafe_allow_html=True)

    with k3:
        with st.container(border=True):
            st.markdown('<div class="kpi-label">Target (kW/Ton)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-value">{target:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="kpi-note">Configured threshold</div>', unsafe_allow_html=True)

    with k4:
        with st.container(border=True):
            st.markdown('<div class="kpi-label">Efficiency (%)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="kpi-value">{efficiency:.1f}%</div>', unsafe_allow_html=True)

            if efficiency >= 90:
                note = "✅ Excellent"
                color = "#22C55E"
            elif efficiency >= 75:
                note = "⚠️ Moderate"
                color = "#F59E0B"
            else:
                note = "❌ Low"
                color = "#EF4444"

            st.markdown(f'<div class="kpi-note" style="color:{color};">{note}</div>', unsafe_allow_html=True)