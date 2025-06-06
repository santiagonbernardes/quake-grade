"""Data loading and handling components for the Quake-Grade application."""

from typing import Optional

import numpy as np
import pandas as pd
import streamlit as st

from ..utils.constants import (
    BASE_DATASET_PATH,
    CACHE_TTL_DATA,
    ERROR_FILE_LOAD,
    ERROR_MISSING_COLUMNS,
    METRIC_MEMORY_USAGE,
    METRIC_TOTAL_COLUMNS,
    METRIC_TOTAL_RECORDS,
    SUCCESS_FILE_LOADED,
    UPLOAD_LABEL,
)
from ..utils.validators import (
    clean_dataset,
    validate_columns,
    validate_data_ranges,
    validate_data_types,
)


@st.cache_data(ttl=CACHE_TTL_DATA)
def load_base_dataset() -> pd.DataFrame:
    """
    Load and cache the base dataset.

    Returns:
        Base DataFrame for the application
    """
    df = pd.read_csv(BASE_DATASET_PATH)
    df = clean_dataset(df)
    return df


def generate_random_dataset(
    base_df: pd.DataFrame, n_samples: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate a random dataset based on the statistical properties of the base dataset.

    Args:
        base_df: Base DataFrame to use for statistical properties
        n_samples: Number of samples to generate (default: same as base)

    Returns:
        Generated DataFrame with random data
    """
    if n_samples is None:
        n_samples = len(base_df)

    random_df = pd.DataFrame()

    for col in base_df.columns:
        if pd.api.types.is_numeric_dtype(base_df[col]):
            # Generate random numeric data preserving statistical properties
            mean = base_df[col].mean()
            std = base_df[col].std()
            min_val = base_df[col].min()
            max_val = base_df[col].max()

            # Generate normal distribution and clip to original range
            values = np.random.normal(loc=mean, scale=std, size=n_samples)
            values = np.clip(values, min_val, max_val)

            # Preserve integer type if original was integer
            if pd.api.types.is_integer_dtype(base_df[col]):
                values = np.round(values).astype(int)

            random_df[col] = values
        else:
            # For categorical columns, sample from existing values
            probabilities = base_df[col].value_counts(normalize=True)
            categories = probabilities.index.tolist()
            probs = probabilities.values
            random_df[col] = np.random.choice(categories, size=n_samples, p=probs)

    return random_df


def handle_file_upload() -> Optional[pd.DataFrame]:
    """
    Handle file upload with validation.

    Returns:
        Validated DataFrame or None if no valid file uploaded
    """
    uploaded_file = st.file_uploader(UPLOAD_LABEL, type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)

            # Clean the dataset
            df = clean_dataset(df)

            # Validate columns
            columns_valid, missing_columns = validate_columns(df)
            if not columns_valid:
                st.error(ERROR_MISSING_COLUMNS.format(", ".join(missing_columns)))
                return None

            # Validate data types
            types_valid, type_errors = validate_data_types(df)
            if not types_valid:
                for error in type_errors:
                    st.error(error)
                return None

            # Validate data ranges
            ranges_valid, range_errors = validate_data_ranges(df)
            if not ranges_valid:
                for error in range_errors:
                    st.warning(error)

            st.success(SUCCESS_FILE_LOADED)
            return df

        except Exception as e:
            st.error(ERROR_FILE_LOAD.format(e))
            return None

    return None


def display_data_info(df: pd.DataFrame):
    """
    Display basic information about the loaded dataset.

    Args:
        df: DataFrame to display info for
    """
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(METRIC_TOTAL_RECORDS, f"{len(df):,}")

    with col2:
        st.metric(METRIC_TOTAL_COLUMNS, len(df.columns))

    with col3:
        st.metric(METRIC_MEMORY_USAGE, f"{df.memory_usage().sum() / 1024:.1f} KB")
