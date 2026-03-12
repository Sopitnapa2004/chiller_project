"""
Global CSS styles for the Chiller System Dashboard.
Provides consistent dark theme styling across all pages.
"""

import streamlit as st


def load_global_styles() -> None:
    """
    Load and apply global CSS styles to the Streamlit application.
    Implements a professional dark theme with proper spacing and typography.
    """
    st.markdown("""
    <style>
    .stApp {
        background: #0F172A;
    }

    .block-container {
        max-width: 88rem;
        padding-top: 1.2rem;
        padding-bottom: 1.4rem;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.08);
        padding-top: 0.75rem;
    }

    .header-wrap {
        background: #1F2937;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 22px 24px;
        min-height: 108px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.20);
    }

    .header-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F9FAFB;
        margin-bottom: 0.35rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }

    .header-subtitle {
        font-size: 0.95rem;
        color: #D1D5DB;
        font-weight: 500;
    }

    .kpi-label {
        font-size: 0.8rem;
        color: #9CA3AF;
        margin-bottom: 0.55rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .kpi-value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #F9FAFB;
        line-height: 1;
        letter-spacing: -0.03em;
    }

    .kpi-note {
        font-size: 0.78rem;
        color: #9CA3AF;
        margin-top: 0.5rem;
        font-weight: 600;
    }

    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-top: 0.7rem;
        margin-bottom: 0.2rem;
        text-align: center;
    }

    .status-normal {
        color: #22C55E;
        font-weight: 800;
        font-size: 0.9rem;
        text-align: center;
    }

    .status-check {
        color: #F59E0B;
        font-weight: 800;
        font-size: 0.9rem;
        text-align: center;
    }

    .small-text {
        color: #9CA3AF;
        font-size: 0.78rem;
        text-align: center;
        margin-top: 0.25rem;
    }

    .alert-list {
        font-size: 0.92rem;
        color: #F9FAFB;
        line-height: 1.8;
        font-weight: 500;
    }

    .footer-note {
        color: #9CA3AF;
        font-size: 0.75rem;
        margin-top: 1rem;
        text-align: center;
        padding-top: 10px;
        padding-bottom: 6px;
        border-top: 1px solid rgba(255,255,255,0.08);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #1F2937;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 0.35rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.20);
    }

    .stButton > button {
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.55rem 1rem;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.22);
    }

    .stButton > button:hover {
        opacity: 0.96;
    }

    div[data-baseweb="select"] > div,
    .stNumberInput > div > div > input,
    .stDateInput input {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #F9FAFB !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #9CA3AF;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #F9FAFB;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)