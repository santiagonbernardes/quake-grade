# Quake-Grade (Monitor Sísmico)

## Descrição

Sistema inteligente de classificação de severidade sísmica que combina análise de dados e Machine Learning para prever níveis de impacto de terremotos com base em magnitude, localização e profundidade. O projeto utiliza modelos pré-treinados para classificar terremotos em quatro níveis de severidade (Baixa, Média, Alta, Muito Alta), apoiando a tomada de decisões para prevenção de desastres naturais.

## Versão em Produção

🔗 [https://gs-quake-grade.streamlit.app](https://gs-quake-grade.streamlit.app)

## Membros do Grupo

| Nome | RM |
|-----|-----|
| [Cristiano Washington Dias](https://github.com/criswd) | RM555992 |
| [Mizael Vieira Bezerra](https://github.com/mizaelvieira1) | RM555796 |
| [Santiago Bernardes](https://github.com/santiagonbernardes) | RM557447 |

## Como Rodar Localmente

### 1. Instale o UV

Siga as instruções de instalação na documentação oficial: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

### 2. Clone o repositório

```bash
git clone https://github.com/santiagonbernardes/quake-grade.git
cd quake-grade
```

### 3. Instale as dependências

```bash
uv sync
```

### 4. Execute a aplicação

```bash
uv run streamlit run app.py
```

A aplicação estará disponível em http://localhost:8501

## Tecnologias Utilizadas

### Frontend e Interface
- **Streamlit**: Framework web Python para criar aplicações de dados interativas com componentes nativos para visualização e análise.

### Machine Learning
- **PyCaret**: Framework AutoML que automatiza o workflow de machine learning, facilitando comparação de modelos e seleção baseada em métricas.
- **scikit-learn**: Biblioteca core para algoritmos de aprendizado de máquina (incluída no PyCaret).

### Análise e Visualização de Dados
- **Pandas & NumPy**: Manipulação e análise de dados estruturados.
- **Plotly**: Criação de mapas interativos para visualização geográfica dos terremotos.
- **Seaborn & Matplotlib**: Visualizações estatísticas e gráficos para análise exploratória.

### Processamento e Validação
- **Jupyter**: Notebooks interativos para desenvolvimento e treinamento de modelos.

### Gerenciamento de Dependências
- **UV**: Gerenciador de dependências moderno e rápido para Python, oferecendo resolução eficiente e melhor experiência de desenvolvimento.

## Estrutura do Projeto

```
├── app.py                         # Aplicação principal Streamlit
├── src/
│   ├── modelling/                 # Modelagem e treinamento
│   │   ├── train.ipynb            # Notebook de treinamento do modelo
│   │   ├── model.pkl              # Modelo ML treinado
│   │   └── dataset/               # Datasets de treino e teste
│   │       ├── balanced_Sismos.csv
│   │       ├── df_train.csv
│   │       └── df_test.csv
│   ├── services/                  # Serviços da aplicação
│   │   ├── llm_service.py         # Integração com LLM (em desenvolvimento)
│   │   └── llm_prompts.py         # Templates de prompts
│   └── ui/                        # Interface do usuário
│       ├── components/            # Componentes modulares da UI
│       │   ├── data_loader.py     # Carregamento e validação de dados
│       │   ├── visualizations.py  # Gráficos e mapas
│       │   ├── predictions.py     # Interface de predições ML
│       │   └── llm_insights.py    # Insights via LLM
│       └── utils/                 # Utilitários
│           ├── constants.py       # Constantes e textos em português
│           ├── validators.py      # Lógica de validação de dados
│           └── helpers.py         # Funções auxiliares
├── pyproject.toml                 # Configuração do projeto e dependências
└── uv.lock                        # Lock file de dependências
```