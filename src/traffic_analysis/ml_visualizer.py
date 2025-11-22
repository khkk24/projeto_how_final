import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class MLVisualizer:
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        plt.style.use('default')
        
    def plot_confusion_matrix(self, cm, class_names, title='Matriz de Confusão', cmap='Blues'):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        sns.heatmap(
            cm, annot=True, fmt='d', cmap=cmap,
            xticklabels=class_names,
            yticklabels=class_names,
            ax=ax
        )
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Valor Real', fontsize=12)
        ax.set_xlabel('Valor Previsto', fontsize=12)
        
        plt.tight_layout()
        return fig
    
    def plot_feature_importance(self, feature_importance_df, top_n=15, title='Importância das Features'):
        fig, ax = plt.subplots(figsize=self.figsize)
        
        top_features = feature_importance_df.head(top_n)
        
        ax.barh(top_features['feature'], top_features['importance'], color='steelblue')
        ax.set_xlabel('Importância', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        plt.tight_layout()
        return fig
    
    def plot_classification_metrics(self, report_dict, title='Métricas por Classe'):
        classes = [k for k in report_dict.keys() if k not in ['accuracy', 'macro avg', 'weighted avg']]
        
        metrics = ['precision', 'recall', 'f1-score']
        data = {metric: [report_dict[cls][metric] for cls in classes] for metric in metrics}
        
        df_metrics = pd.DataFrame(data, index=classes)
        
        fig, ax = plt.subplots(figsize=self.figsize)
        df_metrics.plot(kind='bar', ax=ax, rot=45)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Classe', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.legend(title='Métrica')
        ax.set_ylim(0, 1)
        
        plt.tight_layout()
        return fig
    
    def plot_model_comparison(self, models_results, metric='accuracy'):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        model_names = list(models_results.keys())
        scores = [models_results[name][metric] for name in model_names]
        
        bars = ax.bar(model_names, scores, color=['steelblue', 'coral', 'mediumseagreen'])
        
        ax.set_ylabel(metric.capitalize(), fontsize=12)
        ax.set_title(f'Comparação de Modelos - {metric.capitalize()}', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def plot_prediction_distribution(self, y_true, y_pred, class_names):
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        true_counts = pd.Series(y_true).value_counts().sort_index()
        pred_counts = pd.Series(y_pred).value_counts().sort_index()
        
        axes[0].bar(range(len(true_counts)), true_counts.values, color='steelblue', alpha=0.7)
        axes[0].set_xticks(range(len(class_names)))
        axes[0].set_xticklabels(class_names, rotation=45, ha='right')
        axes[0].set_title('Distribuição Real', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Quantidade', fontsize=10)
        
        axes[1].bar(range(len(pred_counts)), pred_counts.values, color='coral', alpha=0.7)
        axes[1].set_xticks(range(len(class_names)))
        axes[1].set_xticklabels(class_names, rotation=45, ha='right')
        axes[1].set_title('Distribuição Prevista', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Quantidade', fontsize=10)
        
        plt.tight_layout()
        return fig
