"""
LLM prompts for earthquake data analysis.
Contains all prompt templates used by the LLM service.
"""

import json


def create_insights_prompt(data_summary: dict) -> str:
    """Create prompt for insights generation."""
    return f"""
    Analise os seguintes dados de predições sísmicas e forneça insights acionáveis:

    Dados:
    {json.dumps(data_summary, indent=2, ensure_ascii=False)}

    Por favor, forneça:
    1. **Principais descobertas**: Padrões importantes nos dados de magnitude, 
       profundidade e localização
    2. **Distribuição de severidade**: Análise das predições de gravidade dos 
       terremotos
    3. **Características geográficas**: Insights sobre a distribuição espacial 
       (latitude/longitude)
    4. **Recomendações**: Ações sugeridas baseadas nos padrões identificados

    Mantenha a resposta concisa e focada em insights práticos para gestores de 
    emergência.
    """


def create_risk_prompt(risk_summary: dict) -> str:
    """Create prompt for risk assessment."""
    return f"""
    Com base nos dados de predição sísmica, crie uma avaliação de risco:

    Dados de Risco:
    {json.dumps(risk_summary, indent=2, ensure_ascii=False)}

    Por favor, forneça:
    1. **Nível de Risco Geral**: Baixo/Médio/Alto com justificativa baseada na 
       distribuição de severidade
    2. **Eventos Críticos**: Análise dos terremotos de alta severidade (Muy Alta)
    3. **Medidas Preventivas**: Ações específicas recomendadas baseadas nos dados
    4. **Monitoramento**: Aspectos que devem ser acompanhados

    Foque em recomendações práticas para autoridades de proteção civil.
    """


def create_quality_prompt(quality_summary: dict) -> str:
    """Create prompt for data quality analysis."""
    return f"""
    Analise a qualidade dos dados sísmicos e sugira melhorias:

    Informações de Qualidade:
    {json.dumps(quality_summary, indent=2, ensure_ascii=False)}

    Por favor, identifique:
    1. **Problemas de Qualidade**: Dados faltantes, duplicados, inconsistências
    2. **Impacto na Análise**: Como os problemas afetam as predições
    3. **Recomendações de Melhoria**: Ações para melhorar a qualidade dos dados
    4. **Prioridades**: Quais problemas resolver primeiro

    Seja específico e técnico nas recomendações.
    """


# System prompts for different analysis types
INSIGHTS_SYSTEM_PROMPT = (
    "Você é um especialista em análise sísmica que gera insights claros e "
    "acionáveis sobre dados de terremotos."
)

RISK_SYSTEM_PROMPT = (
    "Você é um especialista em gestão de riscos sísmicos que cria avaliações de "
    "risco claras para autoridades de proteção civil."
)

QUALITY_SYSTEM_PROMPT = (
    "Você é um especialista em qualidade de dados sísmicos que identifica "
    "problemas e sugere melhorias."
)
