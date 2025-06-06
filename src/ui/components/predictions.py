"""Machine learning prediction components for the Quake-Grade application."""


import pandas as pd
import streamlit as st
from pycaret.classification import load_model, predict_model
from typing import Optional

from ..utils.constants import (
    DOWNLOAD_LABEL,
    DOWNLOAD_FILENAME,
    HEADER_PREDICTIONS,
    HEADER_PREDICTION_DETAILS,
    MODEL_PATH,
    SEVERITY_COLORS,
    SEVERITY_LEVELS,
    SUCCESS_MODEL_LOADED,
    METRIC_LOW_SEVERITY,
    METRIC_MEDIUM_SEVERITY,
    METRIC_HIGH_SEVERITY,
    METRIC_VERY_HIGH_SEVERITY,
    HELP_LOW_SEVERITY,
    HELP_MEDIUM_SEVERITY,
    HELP_HIGH_SEVERITY,
    HELP_VERY_HIGH_SEVERITY,
    LOADING_MODEL,
    LOADING_PREDICTIONS, HEADER_SEVERITY_DISTRIBUTION,
)


@st.cache_resource
def load_ml_model():
    """
    Load and cache the machine learning model.
    Using cache_resource as recommended for ML models in Streamlit docs.
    
    Returns:
        Loaded PyCaret model
    """
    try:
        model = load_model(MODEL_PATH)
        return model, None
    except Exception as e:
        return None, str(e)


def run_predictions(model, df: pd.DataFrame) -> pd.DataFrame:
    """
    Run predictions on the input DataFrame.
    
    Args:
        model: Loaded ML model
        df: Input DataFrame
        
    Returns:
        DataFrame with predictions
    """
    predictions = predict_model(model, data=df)
    # Rename prediction column to match expected name
    predictions = predictions.rename(columns={"prediction_label": "Gravedad"})
    return predictions


def style_predictions_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply color styling to predictions based on severity.
    
    Args:
        df: DataFrame with predictions
        
    Returns:
        Styled DataFrame
    """
    def apply_row_color(row):
        """Apply background color based on severity level."""
        severity = row.get("Gravedad", "")
        color = SEVERITY_COLORS.get(severity, "#ffffff")
        return [f"background-color: {color}"] * len(row)

    # Apply styling
    styled_df = df.style.apply(apply_row_color, axis=1)
    return styled_df


def display_prediction_results(predictions: pd.DataFrame):
    """
    Display prediction results with proper formatting.
    
    Args:
        predictions: DataFrame with predictions
    """
    st.subheader(HEADER_PREDICTIONS)

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    severity_counts = predictions["Gravedad"].value_counts()

    with col1:
        st.metric(
            METRIC_LOW_SEVERITY,
            severity_counts.get("Baja", 0),
            help=HELP_LOW_SEVERITY
        )

    with col2:
        st.metric(
            METRIC_MEDIUM_SEVERITY,
            severity_counts.get("Media", 0),
            help=HELP_MEDIUM_SEVERITY
        )

    with col3:
        st.metric(
            METRIC_HIGH_SEVERITY,
            severity_counts.get("Alta", 0),
            help=HELP_HIGH_SEVERITY
        )

    with col4:
        st.metric(
            METRIC_VERY_HIGH_SEVERITY,
            severity_counts.get("Muy Alta", 0),
            help=HELP_VERY_HIGH_SEVERITY
        )

    # Display styled dataframe
    st.write(HEADER_PREDICTION_DETAILS)
    styled_df = style_predictions_dataframe(predictions)
    st.dataframe(styled_df, use_container_width=True)

    # Download button
    csv_data = predictions.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=DOWNLOAD_LABEL,
        data=csv_data,
        file_name=DOWNLOAD_FILENAME,
        mime="text/csv"
    )


def run_prediction_pipeline(df: pd.DataFrame) -> tuple[bool, Optional[pd.DataFrame], Optional[str]]:
    """
    Run the complete prediction pipeline.
    
    Args:
        df: Input DataFrame
        
    Returns:
        Tuple of (success, predictions_df, error_message)
    """
    # Load model with progress indicator
    with st.spinner(LOADING_MODEL):
        model, error = load_ml_model()

    if error:
        return False, None, error

    st.success(SUCCESS_MODEL_LOADED)

    # Run predictions with progress indicator
    with st.spinner(LOADING_PREDICTIONS):
        try:
            predictions = run_predictions(model, df)
            return True, predictions, None
        except Exception as e:
            return False, None, str(e)


def display_severity_distribution(predictions: pd.DataFrame):
    """
    Display distribution of predicted severities.
    
    Args:
        predictions: DataFrame with predictions
    """
    st.subheader(HEADER_SEVERITY_DISTRIBUTION)
    severity_counts = predictions["Gravedad"].value_counts()

    # Create a bar chart using Streamlit native chart
    chart_data = pd.DataFrame({
        'Gravidade': [SEVERITY_LEVELS.get(k, k) for k in severity_counts.index],
        'Quantidade': severity_counts.values
    })

    st.bar_chart(chart_data.set_index('Gravidade'))
