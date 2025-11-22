# Machine Learning - Classificação de Gravidade de Acidentes

Módulo de Machine Learning para prever a gravidade de acidentes de trânsito usando classificação multiclasse.

## Estrutura dos Arquivos

```
src/traffic_analysis/
├── ml_classifier.py      # Classe principal do classificador
└── ml_visualizer.py      # Visualizações para análise de resultados

notebooks/
└── ml_accident_severity.ipynb  # Notebook com exemplo completo

scripts/
├── train_model.py        # Script para treinar o modelo
└── test_model.py         # Script para testar predições

models/
└── accident_severity_classifier/
    ├── model.pkl
    ├── label_encoders.pkl
    ├── target_encoder.pkl
    ├── scaler.pkl
    └── metadata.pkl
```

## Uso Rápido

### 1. Treinamento do Modelo

**Via Script:**
```bash
python scripts/train_model.py
```

**Via Python:**
```python
from traffic_analysis import AccidentSeverityClassifier
import pandas as pd

df = pd.read_csv('data/processed/datatran_2021_2025_clean.csv')

classifier = AccidentSeverityClassifier(random_state=42)
results = classifier.train(df, model_type='random_forest')

print(f"Acurácia: {results['accuracy']:.4f}")

classifier.save_model('models/accident_severity_classifier')
```

### 2. Fazer Predições

**Via Script:**
```bash
python scripts/test_model.py
```

**Via Python:**
```python
from traffic_analysis import AccidentSeverityClassifier
import pandas as pd

classifier = AccidentSeverityClassifier()
classifier.load_model('models/accident_severity_classifier')

new_data = pd.read_csv('data/processed/datatran_2021_2025_clean.csv').sample(5)
predictions, probabilities = classifier.predict(new_data)

for pred, prob in zip(predictions, probabilities):
    print(f"Predição: {pred} (Confiança: {prob.max():.2%})")
```

### 3. Visualizações

```python
from traffic_analysis import MLVisualizer

visualizer = MLVisualizer(figsize=(12, 8))

# Matriz de confusão
fig = visualizer.plot_confusion_matrix(
    results['confusion_matrix'],
    classifier.target_encoder.classes_
)

# Importância das features
fig = visualizer.plot_feature_importance(
    results['feature_importance'],
    top_n=15
)

# Métricas por classe
fig = visualizer.plot_classification_metrics(
    results['classification_report']
)
```

## Features Utilizadas

### Features Categóricas:
- `uf`: Estado onde ocorreu o acidente
- `tipo_acidente`: Tipo do acidente
- `causa_acidente`: Causa do acidente
- `tipo_pista`: Tipo da pista
- `tracado_via`: Traçado da via
- `condicao_metereologica`: Condição meteorológica
- `fase_dia`: Fase do dia
- `sentido_via`: Sentido da via
- `dia_semana_nome`: Nome do dia da semana
- `periodo_dia`: Período do dia (criada)

### Features Numéricas:
- `hora`: Hora do acidente
- `mes`: Mês do acidente
- `ano`: Ano do acidente
- `dia_semana_num`: Número do dia da semana
- `km`: Quilômetro da rodovia
- `veiculos`: Número de veículos envolvidos
- `pessoas`: Número de pessoas envolvidas
- `eh_fim_semana`: Flag de fim de semana (criada)
- `eh_noite`: Flag de período noturno (criada)

## Modelos Disponíveis

### Random Forest
```python
classifier.train(
    df,
    model_type='random_forest',
    n_estimators=100,
    max_depth=20,
    min_samples_split=10
)
```

### Gradient Boosting
```python
classifier.train(
    df,
    model_type='gradient_boosting',
    n_estimators=100,
    max_depth=10,
    learning_rate=0.1
)
```

## Métricas de Avaliação

O modelo retorna:
- **Accuracy**: Acurácia geral
- **Classification Report**: Precision, Recall, F1-Score por classe
- **Confusion Matrix**: Matriz de confusão
- **Feature Importance**: Importância de cada feature

## Classes Previstas

- Com Vítimas Fatais
- Com Vítimas Feridas
- Sem Vítimas
- (outras classificações presentes nos dados)

## Exemplo Completo no Notebook

Para ver um exemplo completo com todas as visualizações e análises:

```bash
jupyter notebook notebooks/ml_accident_severity.ipynb
```

## API do Classificador

### Métodos Principais

**`train(df, model_type='random_forest', test_size=0.2, **model_params)`**
- Treina o modelo com os dados fornecidos
- Retorna dicionário com resultados e métricas

**`predict(df)`**
- Faz predições em novos dados
- Retorna predições e probabilidades

**`save_model(path)`**
- Salva o modelo treinado e artefatos

**`load_model(path)`**
- Carrega modelo previamente salvo

## Requisitos

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
```
