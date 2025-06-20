"""
Quake-Grade: Intelligent Seismic Severity Classification System
Main application entry point using modular architecture.
"""

import streamlit as st

from src.ui.components.data_loader import (
    display_data_info,
    generate_random_dataset,
    handle_file_upload,
    load_base_dataset,
)
from src.ui.components.llm_insights import display_prediction_insights
from src.ui.components.predictions import (
    display_prediction_results,
    display_severity_distribution,
    run_prediction_pipeline,
)
from src.ui.components.visualizations import (
    display_correlation_heatmap,
    display_distribution_analysis,
    display_severity_map,
    display_statistics,
)
from src.ui.utils.constants import (
    BUTTON_RANDOM_DATASET,
    ERROR_MODEL_LOAD,
    HEADER_CSV_FORMAT,
    HEADER_PREVIEW,
    INFO_UPLOAD_FILE,
    SUCCESS_RANDOM_DATASET,
    TAB_AI_ANALYSIS,
    TAB_DESCRIPTIVE,
    TAB_PREDICTIVE,
)
from src.ui.utils.helpers import (
    display_data_source_info,
    display_header,
    initialize_session_state,
    set_page_config,
)


def main():
    """Main application function."""
    # Initial setup
    set_page_config()
    initialize_session_state()
    display_header()

    # Data source selection
    col1, col2 = st.columns([1, 3], vertical_alignment="center")

    with col1:
        if st.button(BUTTON_RANDOM_DATASET, use_container_width=True):
            base_df = load_base_dataset()
            st.session_state.df = generate_random_dataset(base_df)
            st.session_state.data_source = "random"
            st.success(SUCCESS_RANDOM_DATASET)
            st.rerun()

    with col2:
        uploaded_df = handle_file_upload()
        if uploaded_df is not None:
            st.session_state.df = uploaded_df
            st.session_state.data_source = "upload"
            st.rerun()

    # Display data source info
    display_data_source_info()

    # Main content area
    if st.session_state.df is not None:
        df = st.session_state.df

        # Data preview section
        with st.expander(HEADER_PREVIEW, expanded=False):
            display_data_info(df)
            st.dataframe(df.head(10), use_container_width=True)

        # Create tabs for analysis types
        tab_descriptive, tab_predictive, tab_ai_analysis = st.tabs(
            [TAB_DESCRIPTIVE, TAB_PREDICTIVE, TAB_AI_ANALYSIS]
        )

        # Descriptive Analysis Tab
        with tab_descriptive:
            # Statistics section
            display_statistics(df)

            st.divider()

            # Distribution analysis
            display_distribution_analysis(df)

            st.divider()

            # Correlation analysis
            display_correlation_heatmap(df)

        # Predictive Analysis Tab
        with tab_predictive:
            # Run prediction pipeline
            success, predictions, error = run_prediction_pipeline(df)

            if success and predictions is not None:
                # Display results
                display_prediction_results(predictions)

                st.divider()

                # Severity distribution
                display_severity_distribution(predictions)

                st.divider()

                # Map visualization
                display_severity_map(predictions)

            elif error:
                st.error(ERROR_MODEL_LOAD.format(error))

        # AI Analysis Tab
        with tab_ai_analysis:
            # LLM-powered insights on user's dataset
            display_prediction_insights()

    else:
        # No data loaded
        st.info(INFO_UPLOAD_FILE)

        # Show example data structure
        with st.expander(HEADER_CSV_FORMAT):
            st.markdown("""
            O arquivo CSV deve conter as seguintes colunas:
            - **Magnitud**: Magnitude do terremoto (escala Richter)
            - **Latitud**: Latitude do epicentro
            - **Longitud**: Longitude do epicentro
            - **Profundidad**: Profundidade do terremoto em km

            Exemplo:
            | Magnitud | Latitud | Longitud | Profundidad |
            |----------|---------|----------|-------------|
            | 5.2      | 19.42   | -99.13   | 10.5        |
            | 6.1      | 17.98   | -101.45  | 25.3        |
            """)


if __name__ == "__main__":
    main()
