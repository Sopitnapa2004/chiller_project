"""
Navigation utilities for the Chiller System Dashboard.
Provides common navigation components across pages.
"""

import streamlit as st


def render_back_button(
    page_path: str = "app.py",
    label: str = "← Back to Dashboard"
) -> None:
    """
    Render a back navigation button at the top of a page.
    
    Args:
        page_path: Path to the page to navigate back to (default: app.py)
        label: Button label text (default: "← Back to Dashboard")
    """
    col1, _ = st.columns([1, 5])
    with col1:
        st.page_link(page_path, label=label)