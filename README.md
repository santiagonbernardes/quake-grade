# Quake-Grade

Sistema inteligente de classificação de severidade sísmica que combina análise de dados e Machine Learning para prever níveis de impacto de terremotos, apoiando a tomada de decisões para prevenção de desastres naturais.

## Dependências

O projeto usa **Python 3.11+** e separa as dependências em dois ambientes:

### Dependências de Produção
- `streamlit` - Framework web (inclui pandas & numpy)
- `pycaret` - Automação de workflow de ML
  - O `pycaret` vem com várias dependências utilizadas no projeto, como:
    - `scikit-learn` - Biblioteca de aprendizado de máquina
    - `jupyter` - Notebooks interativos
    - `matplotlib` - Visualização de dados
    - `pandas` - Manipulação de dados
- `seaborn` - Visualização estatística
- `plotly` - Mapas interativos

### Dependências de Desenvolvimento
- `notebook` - Extensão para notebooks no jupyter

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
uv run jupyter notebook
```