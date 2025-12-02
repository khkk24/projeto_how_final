"""
Exemplo Rápido: Machine Learning - Classificação de Gravidade de Acidentes
"""

from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from traffic_analysis import AccidentSeverityClassifier

base_path = Path(__file__).parent
data_path = base_path / 'data' / 'processed' / 'datatran_2021_2025_clean.csv'

df = pd.read_csv(data_path)

print("TREINAMENTO RÁPIDO")
print("=" * 50)

classifier = AccidentSeverityClassifier(random_state=42)

results = classifier.train(
    df,
    model_type='random_forest',
    test_size=0.2,
    n_estimators=50
)

print(f"\nAcurácia: {results['accuracy']:.4f}")
print("\nTop 5 Features:")
for _, row in results['feature_importance'].head(5).iterrows():
    print(f"  {row['feature']}: {row['importance']:.4f}")

model_path = base_path / 'models' / 'quick_test'
classifier.save_model(model_path)
print(f"\nModelo salvo em: {model_path}")

print("\nTESTE DE PREDIÇÃO")
print("=" * 50)

sample = df.sample(3, random_state=42)
predictions, probabilities = classifier.predict(sample)

for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    real = sample.iloc[i]['classificacao_acidente']
    print(f"\nAmostra {i+1}:")
    print(f"  Real: {real}")
    print(f"  Previsto: {pred}")
    print(f"  Confiança: {prob.max():.2%}")
    print(f"  Status: {'✓ CORRETO' if real == pred else '✗ INCORRETO'}")
