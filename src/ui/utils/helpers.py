"""Helper utilities for the Quake-Grade application."""


import streamlit as st

from ..utils.constants import (
    APP_ICON,
    APP_NAME,
    GITHUB_REPO_URL,
    MENU_ABOUT,
    SUBTITLE,
    TITLE,
    SOURCE_UPLOAD_TEXT,
    SOURCE_RANDOM_TEXT,
)


def initialize_session_state():
    """Initialize session state variables."""
    if 'df' not in st.session_state:
        st.session_state.df = None

    if 'upload_valid' not in st.session_state:
        st.session_state.upload_valid = True

    if 'missing_columns' not in st.session_state:
        st.session_state.missing_columns = []

    if 'data_source' not in st.session_state:
        st.session_state.data_source = None  # 'upload', 'random', or None


def set_page_config():
    """Set Streamlit page configuration."""
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': f"{GITHUB_REPO_URL}/issues",
            'Report a bug': f"{GITHUB_REPO_URL}/issues/new",
            'About': MENU_ABOUT
        }
    )


def display_header():
    """Display application header."""
    st.title(f"{APP_ICON} {TITLE}")
    st.info(SUBTITLE)
    st.divider()


def display_data_source_info():
    """Display information about the current data source."""
    if st.session_state.data_source:
        source_text = {
            'upload': SOURCE_UPLOAD_TEXT,
            'random': SOURCE_RANDOM_TEXT
        }
        st.caption(source_text.get(st.session_state.data_source, ""))


def clear_data_state():
    """Clear data-related session state."""
    st.session_state.df = None
    st.session_state.upload_valid = True
    st.session_state.missing_columns = []
    st.session_state.data_source = None
