"""Constants and configuration for the Quake-Grade application."""

# Project Information
GITHUB_REPO_URL = "https://github.com/santiagonbernardes/quake-grade"
APP_NAME = "Quake-Grade - Monitor Sísmico"
APP_ICON = "🌍"

# UI Text in Portuguese
TITLE = "Monitor Sísmico: Explorando Terremotos no México e Região"
SUBTITLE = (
    "Mergulhe nos dados dos terremotos que cercam o México. Esta ferramenta "
    "analítica permite entender a intensidade dos tremores e prever sua "
    "gravidade com base em características fundamentais."
)

# Tab names
TAB_DESCRIPTIVE = "📊 Análise Descritiva"
TAB_PREDICTIVE = "🤖 Análise Preditiva"

# Section headers
HEADER_PREVIEW = "Prévia dos Dados"
HEADER_STATISTICS = "Estatísticas Gerais"
HEADER_HISTOGRAMS = "Histogramas"
HEADER_BOXPLOTS = "Boxplots"
HEADER_PREDICTIONS = "Predições"
HEADER_MAP = "🗺️ Predições no Mapa"
HEADER_CORRELATION = "📊 Análise de Correlação"
HEADER_SEVERITY_DISTRIBUTION = "📊 Distribuição de Gravidade"
HEADER_CSV_FORMAT = "📋 Formato esperado do arquivo CSV"
HEADER_PREDICTION_DETAILS = "### Detalhes das Predições"

# Buttons and inputs
BUTTON_RANDOM_DATASET = "🔄 Usar Dataset Randômico"
UPLOAD_LABEL = "📂 Envie seu arquivo CSV"
DOWNLOAD_LABEL = "📥 Baixar Resultado como CSV"
SELECT_NUMERIC_COLUMN = "Selecione coluna numérica"

# Messages
SUCCESS_FILE_LOADED = "Arquivo carregado com sucesso!"
SUCCESS_MODEL_LOADED = "Modelo carregado com sucesso!"
SUCCESS_RANDOM_DATASET = "Dataset randômico gerado com sucesso!"
ERROR_FILE_LOAD = "Erro ao carregar arquivo: {}"
ERROR_MODEL_LOAD = "Erro ao carregar o modelo ou fazer predições: {}"
ERROR_MISSING_COLUMNS = (
    "O dataset enviado não possui as seguintes colunas obrigatórias: {}. "
    "Por favor, envie um arquivo no formato correto."
)
INFO_UPLOAD_FILE = "Por favor, envie um arquivo CSV para começar."
ERROR_MAP_CREATION = (
    "Não foi possível criar o mapa. "
    "Verifique se os dados contêm as colunas necessárias."
)

# Tab labels for statistics
TAB_SUMMARY = "📊 Resumo"
TAB_DETAILED = "📈 Detalhado"

# Metric labels
METRIC_TOTAL_RECORDS = "Total de Registros"
METRIC_TOTAL_COLUMNS = "Total de Colunas"
METRIC_MEMORY_USAGE = "Memória Utilizada"

# Severity metric labels
METRIC_LOW_SEVERITY = "Baixa Gravidade"
METRIC_MEDIUM_SEVERITY = "Média Gravidade"
METRIC_HIGH_SEVERITY = "Alta Gravidade"
METRIC_VERY_HIGH_SEVERITY = "Muito Alta Gravidade"

# Help text for metrics
HELP_LOW_SEVERITY = "Terremotos de baixo impacto"
HELP_MEDIUM_SEVERITY = "Terremotos de impacto moderado"
HELP_HIGH_SEVERITY = "Terremotos de alto impacto"
HELP_VERY_HIGH_SEVERITY = "Terremotos de impacto severo"
HELP_STATISTICS = "Média ± Desvio Padrão"

# Loading messages
LOADING_MODEL = "Carregando modelo de predição..."
LOADING_PREDICTIONS = "Realizando predições..."

# Download configuration
DOWNLOAD_FILENAME = "predicoes_terremotos.csv"

# Warning and info messages
WARNING_NO_NUMERIC_COLUMNS = "Nenhuma coluna numérica encontrada no dataset."
INFO_CORRELATION_REQUIREMENT = "Necessário pelo menos 2 colunas numéricas para análise de correlação."

# Chart titles
MAP_TITLE = "Distribuição Geográfica dos Terremotos"
CORRELATION_MATRIX_TITLE = "Matriz de Correlação"

# Data source text
SOURCE_UPLOAD_TEXT = "📂 Dados carregados do arquivo"
SOURCE_RANDOM_TEXT = "🔄 Dados randômicos gerados"

# Column names (internal use in English, display in Portuguese)
EXPECTED_COLUMNS = ["Magnitud", "Latitud", "Longitud", "Profundidad"]

# Severity levels and colors
SEVERITY_LEVELS = {
    "Baja": "Baixa",
    "Media": "Média",
    "Alta": "Alta",
    "Muy Alta": "Muito Alta"
}

SEVERITY_COLORS = {
    "Baja": "#2c7fb8",      # Blue (cold)
    "Media": "#41b6c4",     # Light blue/turquoise
    "Alta": "#fdae61",      # Warm orange
    "Muy Alta": "#d7191c"   # Intense red (hot)
}

# File paths
MODEL_PATH = "src/modelling/model"
BASE_DATASET_PATH = "src/modelling/dataset/df_test.csv"

# Cache configuration
CACHE_TTL_DATA = 3600  # 1 hour

# Map configuration
MAP_ZOOM_LEVEL = 4
MAP_STYLE = "carto-positron"

# Menu configuration
MENU_ABOUT = """
# Quake-Grade 🌍

Sistema inteligente de classificação de severidade sísmica que combina análise 
de dados e Machine Learning para prever níveis de impacto de terremotos.

Desenvolvido para o programa Global Solutions da FIAP.
"""
