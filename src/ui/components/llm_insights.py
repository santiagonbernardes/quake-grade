"""LLM-powered insights component for earthquake predictions."""

import hashlib
from typing import Optional

import pandas as pd
import streamlit as st

from src.services.llm_service import create_llm_service
from src.ui.utils.constants import (
    AI_ANALYSIS_DESCRIPTION,
    AI_ANALYSIS_TITLE,
    AI_CLEAR_BUTTON,
    AI_GENERIC_ERROR,
    AI_INSIGHTS_BUTTON,
    AI_INSIGHTS_ERROR,
    AI_INSIGHTS_SPINNER,
    AI_INSIGHTS_TITLE,
    AI_INSIGHTS_UNKNOWN_ERROR,
    AI_QUALITY_BUTTON,
    AI_QUALITY_ERROR,
    AI_QUALITY_SPINNER,
    AI_QUALITY_TITLE,
    AI_QUALITY_UNKNOWN_ERROR,
    AI_RISK_BUTTON,
    AI_RISK_ERROR,
    AI_RISK_SPINNER,
    AI_RISK_TITLE,
    AI_RISK_UNKNOWN_ERROR,
    AI_SERVICE_ERROR,
    AI_UNAVAILABLE_WARNING,
)


@st.cache_data(ttl=1800, max_entries=50)
def _cached_llm_insights(data_hash: str, api_key: str) -> Optional[str]:
    """Generate insights with caching (30-minute TTL)."""
    # Recreate the dataframe from session state for the API call
    predictions = st.session_state.get("df")
    if predictions is None:
        return None

    llm_service = create_llm_service(api_key)
    if not llm_service.is_available():
        return None

    return llm_service.generate_prediction_insights(predictions)


@st.cache_data(ttl=1800, max_entries=50)
def _cached_risk_assessment(data_hash: str, api_key: str) -> Optional[str]:
    """Generate risk assessment with caching (30-minute TTL)."""
    predictions = st.session_state.get("df")
    if predictions is None:
        return None

    llm_service = create_llm_service(api_key)
    if not llm_service.is_available():
        return None

    return llm_service.generate_risk_assessment(predictions)


@st.cache_data(ttl=1800, max_entries=50)
def _cached_quality_analysis(data_hash: str, api_key: str) -> Optional[str]:
    """Generate quality analysis with caching (30-minute TTL)."""
    predictions = st.session_state.get("df")
    if predictions is None:
        return None

    llm_service = create_llm_service(api_key)
    if not llm_service.is_available():
        return None

    return llm_service.analyze_data_quality(predictions)


def _generate_data_hash(df: pd.DataFrame) -> str:
    """Generate a hash of the dataframe for caching purposes."""
    # Create a hash based on the dataframe content
    df_string = df.to_string()
    return hashlib.md5(df_string.encode()).hexdigest()


def _initialize_llm_session_state():
    """Initialize session state variables for LLM results."""
    if "llm_insights" not in st.session_state:
        st.session_state.llm_insights = None
    if "llm_risk_assessment" not in st.session_state:
        st.session_state.llm_risk_assessment = None
    if "llm_quality_analysis" not in st.session_state:
        st.session_state.llm_quality_analysis = None
    if "llm_errors" not in st.session_state:
        st.session_state.llm_errors = {}


def display_prediction_insights(predictions: pd.DataFrame):
    """Display LLM-generated insights for prediction results."""
    # Initialize session state
    _initialize_llm_session_state()

    # Get API key from Streamlit secrets
    api_key = st.secrets.get("OPENAI_API_KEY")

    if not api_key:
        st.warning(AI_UNAVAILABLE_WARNING)
        return

    # Test service availability
    llm_service = create_llm_service(api_key)
    if not llm_service.is_available():
        error_msg = llm_service.get_error_message()
        st.error(AI_SERVICE_ERROR.format(error_msg))
        return

    st.subheader(AI_ANALYSIS_TITLE)
    st.write(AI_ANALYSIS_DESCRIPTION)

    # Generate data hash for caching
    data_hash = _generate_data_hash(predictions)

    # Create columns for buttons and results
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(AI_INSIGHTS_BUTTON, use_container_width=True):
            with st.spinner(AI_INSIGHTS_SPINNER):
                try:
                    insights = _cached_llm_insights(data_hash, api_key)
                    if insights:
                        st.session_state.llm_insights = insights
                        st.session_state.llm_errors.pop("insights", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["insights"] = (
                            error_msg or AI_INSIGHTS_UNKNOWN_ERROR
                        )
                except Exception as e:
                    st.session_state.llm_errors["insights"] = AI_GENERIC_ERROR.format(
                        str(e)
                    )

        # Display insights result in expander
        if st.session_state.llm_insights:
            with st.expander(AI_INSIGHTS_TITLE, expanded=True):
                st.markdown(st.session_state.llm_insights)
        elif "insights" in st.session_state.llm_errors:
            with st.expander(AI_INSIGHTS_ERROR, expanded=True):
                st.error(st.session_state.llm_errors["insights"])

    with col2:
        if st.button(AI_RISK_BUTTON, use_container_width=True):
            with st.spinner(AI_RISK_SPINNER):
                try:
                    risk_assessment = _cached_risk_assessment(data_hash, api_key)
                    if risk_assessment:
                        st.session_state.llm_risk_assessment = risk_assessment
                        st.session_state.llm_errors.pop("risk", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["risk"] = (
                            error_msg or AI_RISK_UNKNOWN_ERROR
                        )
                except Exception as e:
                    st.session_state.llm_errors["risk"] = AI_GENERIC_ERROR.format(
                        str(e)
                    )

        # Display risk assessment result in expander
        if st.session_state.llm_risk_assessment:
            with st.expander(AI_RISK_TITLE, expanded=True):
                st.markdown(st.session_state.llm_risk_assessment)
        elif "risk" in st.session_state.llm_errors:
            with st.expander(AI_RISK_ERROR, expanded=True):
                st.error(st.session_state.llm_errors["risk"])

    with col3:
        if st.button(AI_QUALITY_BUTTON, use_container_width=True):
            with st.spinner(AI_QUALITY_SPINNER):
                try:
                    quality_analysis = _cached_quality_analysis(data_hash, api_key)
                    if quality_analysis:
                        st.session_state.llm_quality_analysis = quality_analysis
                        st.session_state.llm_errors.pop("quality", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["quality"] = (
                            error_msg or AI_QUALITY_UNKNOWN_ERROR
                        )
                except Exception as e:
                    st.session_state.llm_errors["quality"] = AI_GENERIC_ERROR.format(
                        str(e)
                    )

        # Display quality analysis result in expander
        if st.session_state.llm_quality_analysis:
            with st.expander(AI_QUALITY_TITLE, expanded=True):
                st.markdown(st.session_state.llm_quality_analysis)
        elif "quality" in st.session_state.llm_errors:
            with st.expander(AI_QUALITY_ERROR, expanded=True):
                st.error(st.session_state.llm_errors["quality"])

    # Clear results button (only show if there are results)
    if (
        st.session_state.llm_insights
        or st.session_state.llm_risk_assessment
        or st.session_state.llm_quality_analysis
    ):
        st.divider()
        _, button_col, _ = st.columns(3)
        with button_col:
            if st.button(AI_CLEAR_BUTTON, use_container_width=True):
                st.session_state.llm_insights = None
                st.session_state.llm_risk_assessment = None
                st.session_state.llm_quality_analysis = None
                st.session_state.llm_errors = {}
                st.rerun()
