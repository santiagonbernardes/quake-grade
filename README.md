# Quake-Grade

Sistema inteligente de classificação de severidade sísmica que combina análise de dados e Machine Learning para prever níveis de impacto de terremotos, apoiando a tomada de decisões para prevenção de desastres naturais.

## Dependências

O projeto usa **Python 3.11.13** e separa as dependências em dois ambientes:

### Dependências de Produção
- `streamlit` - Framework web (inclui pandas & numpy)
- `pycaret` - Automação de workflow de ML
- `matplotlib` - Plotagem básica  
- `seaborn` - Visualização estatística
- `plotly` - Mapas interativos

### Dependências de Desenvolvimento  
- `jupyter` - Ambiente de notebook para treino de modelos
- `scikit-learn` - Métricas e avaliação de ML

## Configuração

### Instalar UV
Este projeto usa UV como gerenciador de dependências. Instale seguindo as instruções em:
https://docs.astral.sh/uv/getting-started/installation/

### Setup do Projeto
```bash
# Instalar todas as dependências (produção + desenvolvimento)
uv sync

# Instalar apenas dependências de produção
uv sync --no-dev

# Executar a aplicação
uv run python app.py

# Iniciar Jupyter para desenvolvimento de modelos
uv run jupyter lab
```