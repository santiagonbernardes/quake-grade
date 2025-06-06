"""Data validation utilities for the Quake-Grade application."""

import pandas as pd

from ..utils.constants import EXPECTED_COLUMNS


def validate_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate if the DataFrame contains all expected columns.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    is_valid = len(missing_columns) == 0
    return is_valid, missing_columns


def validate_data_ranges(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate if data values are within expected ranges.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    # Define valid ranges for columns
    column_ranges = {
        "Magnitud": (0, 10),  # Magnitude validation (0-10 Richter scale)
        "Latitud": (-90, 90),  # Latitude validation (-90 to 90)
        "Longitud": (-180, 180),  # Longitude validation (-180 to 180)
        "Profundidad": (0, None),  # Depth validation (non-negative)
    }

    # Validate each column based on its range
    for column, (min_val, max_val) in column_ranges.items():
        if column in df.columns:
            if min_val is not None and df[column].min() < min_val:
                errors.append(f"{column} deve ser maior ou igual a {min_val}")
            if max_val is not None and df[column].max() > max_val:
                errors.append(f"{column} deve ser menor ou igual a {max_val}")
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_data_types(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Validate if columns have correct data types.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []

    for col in EXPECTED_COLUMNS:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Coluna '{col}' deve conter valores numéricos")

    is_valid = len(errors) == 0
    return is_valid, errors


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by removing unnecessary columns.

    Args:
        df: DataFrame to clean

    Returns:
        Cleaned DataFrame
    """
    # Remove severity column if present (it will be predicted)
    if "Gravedad" in df.columns:
        df = df.drop(columns=["Gravedad"])

    return df


def validate_file_size(file_size: int, max_size_mb: int = 100) -> tuple[bool, str]:
    """
    Validate uploaded file size.

    Args:
        file_size: Size of file in bytes
        max_size_mb: Maximum allowed size in MB

    Returns:
        Tuple of (is_valid, error_message)
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    if file_size > max_size_bytes:
        return False, f"Arquivo muito grande. Tamanho máximo permitido: {max_size_mb}MB"

    return True, ""
