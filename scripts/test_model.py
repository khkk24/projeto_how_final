from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from traffic_analysis import AccidentSeverityClassifier


def main():
    base_path = Path(__file__).parent.parent
    model_path = base_path / 'models' / 'accident_severity_classifier'
    
    if not model_path.exists():
        print("Erro: Modelo não encontrado. Execute train_model.py primeiro.")
        return
    
    print("="*60)
    print("TESTE DE PREDIÇÃO DO MODELO")
    print("="*60)
    
    print("\n[1/3] Carregando modelo...")
    classifier = AccidentSeverityClassifier()
    classifier.load_model(model_path)
    print("  Modelo carregado com sucesso!")
    
    print("\n[2/3] Carregando dados de teste...")
    data_path = base_path / 'data' / 'processed' / 'datatran_2021_2025_clean.csv'
    df = pd.read_csv(data_path)
    
    sample_data = df.sample(10, random_state=42)
    print(f"  {len(sample_data)} amostras selecionadas")
    
    print("\n[3/3] Realizando predições...")
    predictions, probabilities = classifier.predict(sample_data)
    
    print("\n" + "="*60)
    print("RESULTADOS DAS PREDIÇÕES")
    print("="*60)
    
    for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
        real = sample_data.iloc[i]['classificacao_acidente']
        uf = sample_data.iloc[i]['uf']
        tipo = sample_data.iloc[i]['tipo_acidente']
        
        print(f"\nAmostra {i+1}:")
        print(f"  UF: {uf} | Tipo: {tipo}")
        print(f"  Real: {real}")
        print(f"  Previsto: {pred}")
        print(f"  Confiança: {prob.max():.2%}")
        print(f"  Correto: {'✓' if real == pred else '✗'}")
    
    accuracy = sum(1 for i, pred in enumerate(predictions) 
                   if pred == sample_data.iloc[i]['classificacao_acidente']) / len(predictions)
    
    print("\n" + "="*60)
    print(f"Acurácia nas amostras: {accuracy:.2%}")
    print("="*60)


if __name__ == '__main__':
    main()
