import streamlit as st


def load_global_styles() -> None:
    st.markdown("""
    <style>
    .stApp {
        background: #0F172A;
    }

    .block-container {
        max-width: 88rem;
        padding-top: 1.25rem;
        padding-bottom: 1.5rem;
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
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.20);
    }

    .header-title {
        font-size: 1.95rem;
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
        font-size: 0.82rem;
        color: #9CA3AF;
        margin-bottom: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F9FAFB;
        line-height: 1;
        letter-spacing: -0.03em;
    }

    .kpi-note {
        font-size: 0.78rem;
        color: #9CA3AF;
        margin-top: 0.55rem;
        font-weight: 600;
    }

    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #F9FAFB;
        margin-top: 0.75rem;
        margin-bottom: 0.25rem;
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
        transition: box-shadow 0.22s ease, border-color 0.22s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
        border-color: rgba(59, 130, 246, 0.22);
    }

    .stButton > button {
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.55rem 1rem;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.22);
        transition: transform 0.18s ease, box-shadow 0.18s ease, opacity 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.28);
        opacity: 0.98;
    }

    div[data-baseweb="select"] > div,
    .stNumberInput > div > div > input,
    .stDateInput input {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        color: #F9FAFB !important;
    }

    details {
        border-radius: 14px;
        overflow: hidden;
    }

    button[data-baseweb="tab"] {
        font-weight: 700;
        color: #9CA3AF;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #F9FAFB;
    }

    [data-testid="stMetricLabel"] {
        color: #9CA3AF;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #F9FAFB;
        font-weight: 800;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.08);
    }

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)