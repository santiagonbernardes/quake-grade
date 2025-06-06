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

    # Magnitude validation (0-10 Richter scale)
    if "Magnitud" in df.columns:
        if df["Magnitud"].min() < 0 or df["Magnitud"].max() > 10:
            errors.append("Magnitude deve estar entre 0 e 10")

    # Latitude validation (-90 to 90)
    if "Latitud" in df.columns:
        if df["Latitud"].min() < -90 or df["Latitud"].max() > 90:
            errors.append("Latitude deve estar entre -90 e 90")

    # Longitude validation (-180 to 180)
    if "Longitud" in df.columns:
        if df["Longitud"].min() < -180 or df["Longitud"].max() > 180:
            errors.append("Longitude deve estar entre -180 e 180")

    # Depth validation (non-negative)
    if "Profundidad" in df.columns:
        if df["Profundidad"].min() < 0:
            errors.append("Profundidade não pode ser negativa")

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
