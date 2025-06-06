"""Constants and configuration for the Quake-Grade application."""

# Project Information
GITHUB_REPO_URL = "https://github.com/santiago-albornoz/quake-grade"
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

# Column names (internal use in English, display in Portuguese)
EXPECTED_COLUMNS = ["Magnitud", "Latitud", "Longitud", "Profundidad"]
COLUMN_MAPPING = {
    "Magnitud": "magnitude",
    "Latitud": "latitude",
    "Longitud": "longitude",
    "Profundidad": "depth",
    "Gravedad": "severity"
}

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
CACHE_MAX_ENTRIES = 100

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
