"""Visualization components for the Quake-Grade application."""


import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from typing import Optional

from ..utils.constants import (
    HEADER_BOXPLOTS,
    HEADER_HISTOGRAMS,
    HEADER_STATISTICS,
    HEADER_MAP,
    HEADER_CORRELATION,
    MAP_STYLE,
    MAP_ZOOM_LEVEL,
    SELECT_NUMERIC_COLUMN,
    SEVERITY_COLORS,
    TAB_SUMMARY,
    TAB_DETAILED,
    HELP_STATISTICS,
    WARNING_NO_NUMERIC_COLUMNS,
    INFO_CORRELATION_REQUIREMENT,
    MAP_TITLE,
    CORRELATION_MATRIX_TITLE,
    ERROR_MAP_CREATION,
)

# Set the default style for matplotlib plots
sns.set(style="whitegrid")


def display_statistics(df: pd.DataFrame):
    """
    Display descriptive statistics using Streamlit native components.
    
    Args:
        df: DataFrame to analyze
    """
    st.subheader(HEADER_STATISTICS)

    # Use tabs for better organization
    tab1, tab2 = st.tabs([TAB_SUMMARY, TAB_DETAILED])

    with tab1:
        # Display key metrics using st.metric
        numeric_cols = df.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:
            cols = st.columns(len(numeric_cols))
            for i, col in enumerate(numeric_cols):
                with cols[i]:
                    st.metric(
                        label=col,
                        value=f"{df[col].mean():.2f}",
                        delta=f"σ = {df[col].std():.2f}",
                        help=HELP_STATISTICS
                    )

    with tab2:
        # Display full statistics table
        st.dataframe(
            df.describe(include='all'),
            use_container_width=True
        )


@st.cache_data
def create_histogram(df: pd.DataFrame, column: str) -> plt.Figure:
    """
    Create a cached histogram for the specified column.
    
    Args:
        df: DataFrame containing the data
        column: Column name to plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=df, x=column, kde=True, ax=ax)
    ax.set_title(f"Distribuição de {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequência")
    plt.tight_layout()
    return fig


@st.cache_data
def create_boxplot(df: pd.DataFrame, column: str) -> plt.Figure:
    """
    Create a cached boxplot for the specified column.
    
    Args:
        df: DataFrame containing the data
        column: Column name to plot
        
    Returns:
        Matplotlib figure object
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df, x=column, ax=ax)
    ax.set_title(f"Boxplot de {column}")
    ax.set_xlabel(column)
    plt.tight_layout()
    return fig


def display_distribution_analysis(df: pd.DataFrame):
    """
    Display distribution analysis with histograms and boxplots.
    
    Args:
        df: DataFrame to analyze
    """
    numeric_columns = df.select_dtypes(include='number').columns.tolist()

    if not numeric_columns:
        st.warning(WARNING_NO_NUMERIC_COLUMNS)
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(HEADER_HISTOGRAMS)
        selected_hist = st.selectbox(
            SELECT_NUMERIC_COLUMN,
            options=numeric_columns,
            key="histogram_selector"
        )

        if selected_hist:
            fig = create_histogram(df, selected_hist)
            st.pyplot(fig)

    with col2:
        st.subheader(HEADER_BOXPLOTS)
        selected_box = st.selectbox(
            SELECT_NUMERIC_COLUMN,
            options=numeric_columns,
            key="boxplot_selector"
        )

        if selected_box:
            fig = create_boxplot(df, selected_box)
            st.pyplot(fig)


def create_severity_map(
    df: pd.DataFrame,
    lat_col: str = "Latitud",
    lon_col: str = "Longitud",
    severity_col: str = "Gravedad"
) -> Optional[px.scatter_mapbox]:
    """
    Create an interactive map showing earthquake severity.
    
    Args:
        df: DataFrame with location and severity data
        lat_col: Latitude column name
        lon_col: Longitude column name
        severity_col: Severity column name
        
    Returns:
        Plotly figure or None if required columns missing
    """
    required_cols = {lat_col, lon_col, severity_col}
    if not required_cols.issubset(df.columns):
        return None

    # Create hover data
    hover_data = {
        lat_col: ":.4f",
        lon_col: ":.4f"
    }

    # Add magnitude if available
    if "Magnitud" in df.columns:
        hover_data["Magnitud"] = ":.2f"

    fig = px.scatter_mapbox(
        df,
        lat=lat_col,
        lon=lon_col,
        color=severity_col,
        color_discrete_map=SEVERITY_COLORS,
        zoom=MAP_ZOOM_LEVEL,
        mapbox_style=MAP_STYLE,
        hover_data=hover_data,
        title=MAP_TITLE
    )

    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    return fig


def display_correlation_heatmap(df: pd.DataFrame):
    """
    Display correlation heatmap for numeric columns.
    
    Args:
        df: DataFrame to analyze
    """
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.shape[1] < 2:
        st.info(INFO_CORRELATION_REQUIREMENT)
        return

    st.subheader(HEADER_CORRELATION)

    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f",
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Correlação"},
        ax=ax
    )
    ax.set_title(CORRELATION_MATRIX_TITLE)
    plt.tight_layout()

    st.pyplot(fig)


def display_severity_map(predictions: pd.DataFrame):
    """
    Display an interactive map showing earthquake severity predictions.
    
    Args:
        predictions: DataFrame with predictions including location and severity data
    """
    st.subheader(HEADER_MAP)
    
    map_fig = create_severity_map(predictions)
    if map_fig:
        st.plotly_chart(map_fig, use_container_width=True)
    else:
        st.warning(ERROR_MAP_CREATION)
