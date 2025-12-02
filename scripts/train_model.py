from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from traffic_analysis import AccidentSeverityClassifier, MLVisualizer


def main():
    base_path = Path(__file__).parent.parent
    data_path = base_path / 'data' / 'processed' / 'datatran_2021_2025_clean.csv'
    model_path = base_path / 'models' / 'accident_severity_classifier'
    
    print("="*60)
    print("TREINAMENTO DO MODELO DE CLASSIFICAÇÃO DE GRAVIDADE")
    print("="*60)
    
    print("\n[1/6] Carregando dados...")
    df = pd.read_csv(data_path)
    print(f"  Total de registros: {len(df):,}")
    print(f"  Distribuição do target:")
    for cls, count in df['classificacao_acidente'].value_counts().items():
        print(f"    - {cls}: {count:,}")
    
    print("\n[2/6] Inicializando classificador...")
    classifier = AccidentSeverityClassifier(random_state=42)
    
    print("\n[3/6] Treinando modelo Random Forest...")
    results_rf = classifier.train(
        df,
        model_type='random_forest',
        test_size=0.2,
        n_estimators=100,
        max_depth=20,
        min_samples_split=10
    )
    print(f"  Acurácia: {results_rf['accuracy']:.4f}")
    
    print("\n[4/6] Treinando modelo Gradient Boosting...")
    classifier_gb = AccidentSeverityClassifier(random_state=42)
    results_gb = classifier_gb.train(
        df,
        model_type='gradient_boosting',
        test_size=0.2,
        n_estimators=100,
        max_depth=10,
        learning_rate=0.1
    )
    print(f"  Acurácia: {results_gb['accuracy']:.4f}")
    
    print("\n[5/6] Comparando modelos...")
    best_classifier = classifier if results_rf['accuracy'] >= results_gb['accuracy'] else classifier_gb
    best_results = results_rf if results_rf['accuracy'] >= results_gb['accuracy'] else results_gb
    best_model_name = 'Random Forest' if results_rf['accuracy'] >= results_gb['accuracy'] else 'Gradient Boosting'
    
    print(f"  Melhor modelo: {best_model_name}")
    print(f"  Acurácia final: {best_results['accuracy']:.4f}")
    
    print("\n[6/6] Salvando modelo...")
    best_classifier.save_model(model_path)
    print(f"  Modelo salvo em: {model_path}")
    
    print("\n" + "="*60)
    print("RESUMO DO TREINAMENTO")
    print("="*60)
    print(f"Modelo: {best_model_name}")
    print(f"Acurácia: {best_results['accuracy']:.4f}")
    print(f"\nTop 5 Features Mais Importantes:")
    for idx, row in best_results['feature_importance'].head(5).iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")
    
    print("\nMétricas por Classe:")
    report = best_results['classification_report']
    for cls in best_classifier.target_encoder.classes_:
        if cls in report:
            metrics = report[cls]
            print(f"  {cls}:")
            print(f"    Precision: {metrics['precision']:.4f}")
            print(f"    Recall: {metrics['recall']:.4f}")
            print(f"    F1-Score: {metrics['f1-score']:.4f}")
    
    print("\n" + "="*60)
    print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*60)


if __name__ == '__main__':
    main()
