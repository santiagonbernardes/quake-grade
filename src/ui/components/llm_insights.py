"""LLM-powered insights component for earthquake predictions."""

import hashlib
from typing import Optional

import pandas as pd
import streamlit as st

from src.services.llm_service import create_llm_service


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
        st.warning(
            "⚠️ OpenAI API key não encontrada. "
            "Funcionalidades de IA não estarão disponíveis."
        )
        return

    # Test service availability
    llm_service = create_llm_service(api_key)
    if not llm_service.is_available():
        error_msg = llm_service.get_error_message()
        st.error(f"❌ Serviço de IA não disponível: {error_msg}")
        return

    st.subheader("🤖 Análise Inteligente")
    st.write(
        "Clique nos botões abaixo para gerar análises específicas usando IA. "
        "Os resultados são armazenados e ficam visíveis até você sair da aplicação."
    )

    # Generate data hash for caching
    data_hash = _generate_data_hash(predictions)

    # Create columns for buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Gerar Insights", use_container_width=True):
            with st.spinner("Gerando insights..."):
                try:
                    insights = _cached_llm_insights(data_hash, api_key)
                    if insights:
                        st.session_state.llm_insights = insights
                        st.session_state.llm_errors.pop("insights", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["insights"] = (
                            error_msg or "Erro desconhecido ao gerar insights"
                        )
                except Exception as e:
                    st.session_state.llm_errors["insights"] = f"Erro: {str(e)}"

    with col2:
        if st.button("⚠️ Avaliar Riscos", use_container_width=True):
            with st.spinner("Analisando riscos..."):
                try:
                    risk_assessment = _cached_risk_assessment(data_hash, api_key)
                    if risk_assessment:
                        st.session_state.llm_risk_assessment = risk_assessment
                        st.session_state.llm_errors.pop("risk", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["risk"] = (
                            error_msg or "Erro desconhecido ao avaliar riscos"
                        )
                except Exception as e:
                    st.session_state.llm_errors["risk"] = f"Erro: {str(e)}"

    with col3:
        if st.button("📊 Analisar Qualidade", use_container_width=True):
            with st.spinner("Analisando qualidade dos dados..."):
                try:
                    quality_analysis = _cached_quality_analysis(data_hash, api_key)
                    if quality_analysis:
                        st.session_state.llm_quality_analysis = quality_analysis
                        st.session_state.llm_errors.pop("quality", None)
                    else:
                        error_msg = llm_service.get_error_message()
                        st.session_state.llm_errors["quality"] = (
                            error_msg or "Erro desconhecido ao analisar qualidade"
                        )
                except Exception as e:
                    st.session_state.llm_errors["quality"] = f"Erro: {str(e)}"

    # Display persistent results
    st.divider()

    # Display insights
    if st.session_state.llm_insights:
        st.markdown("### 💡 Insights Automáticos")
        st.markdown(st.session_state.llm_insights)
        st.divider()
    elif "insights" in st.session_state.llm_errors:
        st.error(f"❌ Insights: {st.session_state.llm_errors['insights']}")

    # Display risk assessment
    if st.session_state.llm_risk_assessment:
        st.markdown("### ⚠️ Avaliação de Riscos")
        st.markdown(st.session_state.llm_risk_assessment)
        st.divider()
    elif "risk" in st.session_state.llm_errors:
        st.error(f"❌ Avaliação de Riscos: {st.session_state.llm_errors['risk']}")

    # Display quality analysis
    if st.session_state.llm_quality_analysis:
        st.markdown("### 📊 Qualidade dos Dados")
        st.markdown(st.session_state.llm_quality_analysis)
        st.divider()
    elif "quality" in st.session_state.llm_errors:
        st.error(f"❌ Qualidade dos Dados: {st.session_state.llm_errors['quality']}")

    # Clear results button
    if (
        st.session_state.llm_insights
        or st.session_state.llm_risk_assessment
        or st.session_state.llm_quality_analysis
    ):
        if st.button("🗑️ Limpar Todas as Análises"):
            st.session_state.llm_insights = None
            st.session_state.llm_risk_assessment = None
            st.session_state.llm_quality_analysis = None
            st.session_state.llm_errors = {}
            st.rerun()
