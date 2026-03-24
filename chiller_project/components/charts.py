import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_power_trend_chart(df: pd.DataFrame, title: str = "Performance Trend", height: int = 300) -> None:
    with st.container(border=True):
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Average power per ton across selected scope</div>',
            unsafe_allow_html=True,
        )

        if df.empty:
            st.info("No trend data available")
            return

        trend_df = (
            df.sort_values("timestamp")
            .groupby("timestamp", as_index=False)["power_per_ton"]
            .mean()
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=trend_df["timestamp"],
                y=trend_df["power_per_ton"],
                mode="lines",
                line=dict(width=2, color="#60A5FA"),
                hovertemplate="Time: %{x}<br>Power/Ton: %{y:.2f}<extra></extra>",
            )
        )

        fig.update_layout(
            height=height,
            margin=dict(l=12, r=12, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E5E7EB"),
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.08)",
                zeroline=False,
            ),
        )

        st.plotly_chart(fig, use_container_width=True)