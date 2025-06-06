import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from pycaret.classification import load_model, predict_model

# Estilo dos gráficos
sns.set(style="whitegrid")

# Configurações da página
st.set_page_config(layout="wide")
st.title("Monitor Sísmico: Explorando Terremotos no México e Região")
st.info(
    "Mergulhe nos dados dos terremotos que cercam o México. Esta ferramenta "
    "analítica permite entender a intensidade dos tremores e prever sua "
    "gravidade com base em características fundamentais."
)
st.write("")


# Define colunas esperadas do dataset
colunas_esperadas = [
    "Magnitud",
    "Latitud",
    "Longitud",
    "Profundidad",
]  # Ajuste para seu dataset


# Carrega dataset base uma vez
@st.cache_data
def carregar_dataset_base():
    df_base = pd.read_csv("src/modelling/dataset/df_test.csv")
    if "Gravedad" in df_base.columns:
        df_base = df_base.drop(columns=["Gravedad"])
    return df_base


app_dataset = carregar_dataset_base()


def validar_dataset(df, colunas_esperadas):
    # Verifica se todas as colunas esperadas estão presentes
    faltando = [c for c in colunas_esperadas if c not in df.columns]
    if faltando:
        return False, faltando
    return True, []


def gerar_dataset_randomico(df, n=None):
    if n is None:
        n = len(df)
    df_random = pd.DataFrame()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean = df[col].mean()
            std = df[col].std()
            min_val = df[col].min()
            max_val = df[col].max()
            vals = np.random.normal(loc=mean, scale=std, size=n)
            vals = np.clip(vals, min_val, max_val)
            if pd.api.types.is_integer_dtype(df[col]):
                vals = np.round(vals).astype(int)
            df_random[col] = vals
        else:
            probs = df[col].value_counts(normalize=True)
            categorias = probs.index.tolist()
            probabilidades = probs.values
            df_random[col] = np.random.choice(categorias, size=n, p=probabilidades)
    return df_random


# Inicializa df e flag de erro na session_state
if "df" not in st.session_state:
    st.session_state["df"] = None
if "upload_valido" not in st.session_state:
    st.session_state["upload_valido"] = True
if "colunas_faltando" not in st.session_state:
    st.session_state["colunas_faltando"] = []

col1, col2 = st.columns([1, 3])
with col1:
    st.write("")
    st.write("")

    usar_dataset_randomico = st.button("🔄 Usar Dataset Randômico Gerado")
with col2:
    uploaded_file = st.file_uploader("📂 Envie seu arquivo CSV", type=["csv"])

# Validação do upload
if uploaded_file is not None:
    try:
        df_uploaded = pd.read_csv(uploaded_file)
        if "Gravedad" in df_uploaded.columns:
            df_uploaded = df_uploaded.drop(columns=["Gravedad"])
        valido, faltando = validar_dataset(df_uploaded, colunas_esperadas)
        if valido:
            st.session_state["df"] = df_uploaded
            st.session_state["upload_valido"] = True
            st.session_state["colunas_faltando"] = []
            st.success("Arquivo carregado com sucesso!")
        else:
            st.session_state["upload_valido"] = False
            st.session_state["colunas_faltando"] = faltando
            st.session_state["df"] = None
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        st.session_state["upload_valido"] = False
        st.session_state["colunas_faltando"] = []
        st.session_state["df"] = None

if usar_dataset_randomico:
    st.session_state["df"] = gerar_dataset_randomico(app_dataset)
    st.session_state["upload_valido"] = True
    st.session_state["colunas_faltando"] = []
    st.success("Dataset randômico gerado com sucesso!")

# Mostrar aviso se upload inválido
if not st.session_state.get("upload_valido", True):
    faltando = st.session_state.get("colunas_faltando", [])
    st.info(
        f"O dataset enviado não possui as seguintes colunas obrigatórias: "
        f"{faltando}. Por favor, envie um arquivo no formato correto."
    )

# Mostrar preview se df existir e upload válido
if st.session_state["df"] is not None and st.session_state.get("upload_valido", True):
    df = st.session_state["df"]
    st.subheader("Prévia dos Dados")
    st.dataframe(df.head())

    opcao = st.sidebar.radio(
        "Escolha a funcionalidade:",
        ["Análise Descritiva", "Análise Preditiva de Gravidade"],
    )

    if opcao == "Análise Descritiva":
        st.header("📊 Análise Descritiva")
        st.subheader("Estatísticas Gerais")
        st.write(df.describe(include="all"))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Histogramas")
            col_num = st.selectbox(
                "Selecione coluna numérica",
                options=df.select_dtypes(include=np.number).columns,
            )
            if col_num:
                fig, ax = plt.subplots()
                sns.histplot(df[col_num], ax=ax, kde=True)
                st.pyplot(fig)
        with col2:
            st.subheader("Boxplots")
            col_num_box = st.selectbox(
                "Selecione coluna numérica",
                options=df.select_dtypes(include=np.number).columns,
                key="box",
            )
            if col_num_box:
                fig, ax = plt.subplots()
                sns.boxplot(x=df[col_num_box], ax=ax)
                st.pyplot(fig)

    elif opcao == "Análise Preditiva de Gravidade":
        st.header("🤖 Análise Preditiva de Gravidade")

        try:
            model = load_model("src/modelling/model")
            st.success("Modelo carregado com sucesso!")

            # Executar predições
            st.subheader("Predições")
            predicoes = predict_model(model, data=df)

            # Renomear a coluna de predição
            predicoes = predicoes.rename(columns={"prediction_label": "Gravedad"})

            # Cores personalizadas por gravidade
            cores_linha = {
                "Baja": "#2c7fb8",  # azul (frio)
                "Media": "#41b6c4",  # azul claro / turquesa
                "Alta": "#fdae61",  # laranja quente
                "Muy Alta": "#d7191c",  # vermelho intenso (quente)
            }

            # Função para aplicar cor na linha
            def colorir_linhas_por_gravedad(row):
                cor = cores_linha.get(row["Gravedad"], "#ffffff")  # branco padrão
                return [f"background-color: {cor}"] * len(row)

            # Aplicar estilo e mostrar
            df_estilizado = predicoes.style.apply(colorir_linhas_por_gravedad, axis=1)
            st.dataframe(df_estilizado)

            # Botão para baixar CSV
            csv = predicoes.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar Resultado como CSV",
                data=csv,
                file_name="predicoes.csv",
                mime="text/csv",
            )

            # Mapa com Plotly
            if {"Latitud", "Longitud", "Gravedad"}.issubset(predicoes.columns):
                import plotly.express as px

                st.subheader("🗺️ Predições no Mapa")

                fig_map = px.scatter_mapbox(
                    predicoes,
                    lat="Latitud",
                    lon="Longitud",
                    color="Gravedad",
                    color_discrete_map=cores_linha,
                    zoom=4,
                    mapbox_style="carto-positron",
                )
                st.plotly_chart(fig_map)

        except Exception as e:
            st.error(f"Erro ao carregar o modelo ou fazer predições: {e}")

    else:
        st.info("Por favor, envie um arquivo CSV para começar.")
