# 🚗 Projeto Análise de Acidentes de Trânsito (2021-2025)

## 📋 Descrição
Este projeto apresenta uma análise completa dos dados de acidentes de trânsito da Polícia Rodoviária Federal (PRF) cobrindo o período de 2021 a 2025. O objetivo é identificar padrões, tendências e insights que possam contribuir para a melhoria da segurança viária nas rodovias federais brasileiras.

## 🎯 Objetivos da Análise
1. **Evolução Temporal**: Analisar como os acidentes evoluíram ao longo dos 5 anos
2. **Distribuição Geográfica**: Identificar estados e regiões com maior incidência
3. **Padrões Temporais**: Descobrir horários, dias e meses mais críticos
4. **Análise de Causas**: Estudar as principais causas dos acidentes
5. **Gravidade**: Avaliar a evolução da gravidade dos acidentes
6. **Correlações**: Identificar fatores correlacionados com a gravidade

## 🏗️ Estrutura do Projeto

```
projeto_how_final/
├── notebooks/
│   └── analyse_complete_2021_2025.ipynb    # Análise completa em Jupyter
├── data/
│   ├── raw_data/                           # Dados brutos CSV (não versionados)
│   └── processed/                          # Dados processados e resultados
├── src/
│   └── traffic_analysis/                   # Módulos de análise
│       ├── __init__.py
│       ├── data_loader.py                  # Carregamento de dados
│       ├── data_cleaner.py                 # Limpeza de dados
│       ├── data_explorer.py                # Exploração de dados
│       ├── statistical_analyzer.py         # Análises estatísticas
│       ├── visualizer.py                   # Visualizações
│       └── insight_generator.py            # Geração de insights
├── streamlit_app_corrected.py              # Aplicação web interativa
├── environment.yml                         # Dependências do projeto
├── .gitignore                             # Arquivos ignorados pelo Git
└── README.md                              # Este arquivo
```

## 🚀 Como Executar

### 1. Configuração do Ambiente

```bash
# Clonar o repositório
git clone git@github.com:khkk24/projeto_how_final.git
cd projeto_how_final

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
# ou com conda:
conda env create -f environment.yml
conda activate traffic_analysis
```

### 2. Preparação dos Dados

⚠️ **Importante**: Os dados CSV não estão incluídos no repositório por questões de privacidade e tamanho.

Você precisa colocar os arquivos de dados na pasta `data/raw_data/`:
- `datatran2021.csv`
- `datatran2022.csv`  
- `datatran2023.csv`
- `datatran2024.csv`
- `datatran2025.csv`

### 3. Executar a Análise

#### Jupyter Notebook
```bash
jupyter notebook notebooks/analyse_complete_2021_2025.ipynb
```

#### Aplicação Streamlit
```bash
streamlit run streamlit_app_corrected.py
```

## 📊 Funcionalidades

### Jupyter Notebook
- ✅ Análise exploratória completa
- ✅ Visualizações estáticas e interativas
- ✅ Testes estatísticos
- ✅ Insights automáticos
- ✅ Exportação de resultados

### Aplicação Streamlit
- ✅ Interface web interativa
- ✅ Seleção de anos para análise
- ✅ Upload de dados personalizados
- ✅ Dashboards interativos
- ✅ Mapas de localização
- ✅ Análises em tempo real

## 📈 Principais Descobertas

### Dados Gerais (2021-2025)
- **311.029 acidentes** analisados
- **26.039 mortes** registradas
- **355.066 feridos** contabilizados
- Taxa de mortalidade: **8,37%** dos acidentes

### Tendências Temporais
- **Redução de 38,4%** no número de acidentes entre 2021-2025
- **Agosto** é o mês mais perigoso
- **18h** é o horário com mais acidentes (7,5%)
- **Sexta-feira** é o dia mais perigoso

### Distribuição Geográfica
- **Minas Gerais (MG)**: estado com mais acidentes
- **Pará (PA)**: maior taxa de mortalidade (53,86%)
- Concentração em estados do Sul e Sudeste

### Principais Causas
- **Reação tardia do condutor** (13,6% dos casos)
- **Ausência de reação do condutor**
- **Velocidade incompatível**

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Matplotlib/Seaborn** - Visualizações estáticas
- **Plotly** - Visualizações interativas
- **Streamlit** - Interface web
- **Jupyter** - Notebooks interativos
- **Scipy** - Análises estatísticas

## 📝 Metodologia

1. **Carregamento**: Dados de múltiplos anos com validação
2. **Limpeza**: Tratamento de valores ausentes e duplicatas
3. **Exploração**: Análise descritiva e visual
4. **Estatísticas**: Testes de hipóteses e correlações
5. **Insights**: Geração automática de descobertas
6. **Visualização**: Dashboards interativos

## 🔒 Privacidade e Dados

Os dados utilizados são de domínio público da Polícia Rodoviária Federal (PRF). 
Os arquivos CSV não são versionados por questões de:
- Tamanho dos arquivos (>400MB total)
- Privacidade e proteção de dados
- Performance do repositório



## 👥 Autores

- **Kokouvi Hola Kanyi- Kodovi **
- ** Mariano ** - 

## 📞 Contato

- GitHub: [@khkk24](https://github.com/khkk24)
- Projeto: [projeto_how_final](https://github.com/khkk24/projeto_how_final)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
