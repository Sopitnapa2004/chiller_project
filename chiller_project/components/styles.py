import streamlit as st


def load_global_styles() -> None:
    st.markdown(
        """
        <style>

        /* Background */
        .stApp {
            background: linear-gradient(135deg, #0a0f1c 0%, #0f172a 100%);
        }

        .block-container {
            max-width: 88rem;
            padding: 1.2rem 1.6rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.55);
            backdrop-filter: blur(9px);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        .header-wrap {
            border-bottom: 1px solid rgba(255,255,255,0.04);
            padding-bottom: 6px;
            margin-bottom: 12px;
        }

        .header-title {
            font-size: 1.55rem;
            font-weight: 700;
            color: #F8FAFC;
        }

        .header-subtitle {
            font-size: 0.85rem;
            color: #94A3B8;
        }

        /* Section Titles */
        .section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #F1F5F9;
        }

        .section-subtitle {
            font-size: 0.8rem;
            color: #94A3B8;
            margin-bottom: 0.5rem;
        }

        /* Card Containers */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(14px);
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.1);
            padding: 1rem 1.2rem;
        }

        /* KPI Styles */
        .kpi-label {
            font-size: 0.7rem;
            color: #A5B4FC;
            text-transform: uppercase;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 800;
            color: #F8FAFC;
            text-shadow: 0 0 12px rgba(96,165,250,0.4);
        }

        .kpi-note {
            font-size: 0.8rem;
            color: #CBD5E1;
        }

        /* Status Styles */
        .status-normal { color: #22c55e; }
        .status-check { color: #9ca3af; }
        .status-warning { color: #fbbf24; }
        .status-critical { color: #ef4444; }

        .card-title {
            font-size: 0.95rem;
            font-weight: 650;
            color: #F8FAFC;
            text-align: center;
        }

        .small-text {
            font-size: 0.75rem;
            color: #94A3B8;
            text-align: center;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
