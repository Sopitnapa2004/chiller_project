import streamlit as st


def render_back_button(page_path="app.py", label="← Back to Dashboard"):
    col1, _ = st.columns([1, 5])
    with col1:
        st.page_link(page_path, label=label)