from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import numpy as np
from scipy import stats


@dataclass
class StatisticalAnalyzer:
    """Classe para análises estatísticas de dados de acidentes de trânsito."""
    
    def correlacoes(self, df: pd.DataFrame, colunas: list = None) -> pd.DataFrame:
        """
        Calcula matriz de correlação para variáveis numéricas.
        
        Args:
            df: DataFrame a ser analisado
            colunas: Lista de colunas específicas para análise (opcional)
            
        Returns:
            DataFrame com matriz de correlação
        """
        if colunas:
            # Filtrar apenas colunas que existem e são numéricas
            colunas_disponiveis = [col for col in colunas if col in df.columns]
            df_num = df[colunas_disponiveis].select_dtypes(include=["number"])
        else:
            df_num = df.select_dtypes(include=["number"])
        
        if df_num.shape[1] < 2:
            return pd.DataFrame()
        
        return df_num.corr(numeric_only=True)
    
    def teste_t_dois_grupos(self, df: pd.DataFrame, coluna_valor: str, coluna_grupo: str, 
                           grupo1: str, grupo2: str) -> dict:
        """
        Teste t de Student para comparar dois grupos.
        
        Args:
            df: DataFrame
            coluna_valor: Coluna com valores numéricos
            coluna_grupo: Coluna com grupos
            grupo1, grupo2: Nomes dos grupos a comparar
            
        Returns:
            Dicionário com estatística t e p-valor
        """
        serie1 = df.loc[df[coluna_grupo] == grupo1, coluna_valor].dropna()
        serie2 = df.loc[df[coluna_grupo] == grupo2, coluna_valor].dropna()
        
        if len(serie1) < 2 or len(serie2) < 2:
            return {"estatistica": np.nan, "p_valor": np.nan, "nota": "amostras muito pequenas"}
        
        t_stat, p_val = stats.ttest_ind(serie1, serie2, equal_var=False)
        
        return {
            "estatistica": t_stat, 
            "p_valor": p_val,
            "significativo": p_val < 0.05,
            "interpretacao": "Diferença significativa" if p_val < 0.05 else "Sem diferença significativa"
        }
    
    def anova_multiplos_grupos(self, df: pd.DataFrame, coluna_valor: str, coluna_grupo: str) -> dict:
        """
        ANOVA para comparar múltiplos grupos.
        
        Args:
            df: DataFrame
            coluna_valor: Coluna com valores numéricos
            coluna_grupo: Coluna com grupos
            
        Returns:
            Dicionário com resultado da ANOVA
        """
        grupos = []
        for grupo in df[coluna_grupo].unique():
            grupo_dados = df.loc[df[coluna_grupo] == grupo, coluna_valor].dropna()
            if len(grupo_dados) >= 2:
                grupos.append(grupo_dados)
        
        if len(grupos) < 2:
            return {"f_estatistica": np.nan, "p_valor": np.nan, "nota": "Menos de 2 grupos válidos"}
        
        f_stat, p_val = stats.f_oneway(*grupos)
        
        return {
            "f_estatistica": f_stat,
            "p_valor": p_val,
            "significativo": p_val < 0.05,
            "interpretacao": "Diferença significativa entre grupos" if p_val < 0.05 else "Sem diferença significativa",
            "num_grupos": len(grupos)
        }
    
    def tendencia_temporal(self, df: pd.DataFrame, coluna_tempo: str, coluna_valor: str) -> dict:
        """
        Análise de tendência temporal usando correlação.
        
        Args:
            df: DataFrame
            coluna_tempo: Coluna com tempo (anos, meses, etc.)
            coluna_valor: Coluna com valores a analisar
            
        Returns:
            Dicionário com resultado da análise de tendência
        """
        dados_tempo = df.groupby(coluna_tempo)[coluna_valor].sum().reset_index()
        
        if len(dados_tempo) < 3:
            return {"correlacao": np.nan, "p_valor": np.nan, "nota": "Poucos pontos temporais"}
        
        correlacao, p_val = stats.pearsonr(dados_tempo[coluna_tempo], dados_tempo[coluna_valor])
        
        # Determinar tipo de tendência
        if p_val < 0.05:
            if correlacao > 0:
                tendencia = "Crescente"
            else:
                tendencia = "Decrescente"
        else:
            tendencia = "Sem tendência clara"
        
        return {
            "correlacao": correlacao,
            "p_valor": p_val,
            "significativo": p_val < 0.05,
            "tendencia": tendencia,
            "interpretacao": f"Tendência {tendencia.lower()} {'significativa' if p_val < 0.05 else 'não significativa'}"
        }
    
    def tabela_frequencias(self, df: pd.DataFrame, coluna: str, incluir_nulos: bool = False) -> pd.DataFrame:
        """
        Tabela de frequências com contagem e porcentagem.
        
        Args:
            df: DataFrame
            coluna: Nome da coluna para análise
            incluir_nulos: Se incluir valores nulos na contagem
            
        Returns:
            DataFrame com frequências
        """
        contagem = df[coluna].value_counts(dropna=not incluir_nulos)
        porcentagem = (contagem / contagem.sum() * 100).round(2)
        
        return pd.DataFrame({
            "contagem": contagem, 
            "porcentagem": porcentagem
        })
    
    def estatisticas_descritivas_por_grupo(self, df: pd.DataFrame, coluna_valor: str, 
                                         coluna_grupo: str) -> pd.DataFrame:
        """
        Estatísticas descritivas segmentadas por grupo.
        
        Args:
            df: DataFrame
            coluna_valor: Coluna numérica para estatísticas
            coluna_grupo: Coluna para agrupamento
            
        Returns:
            DataFrame com estatísticas por grupo
        """
        return df.groupby(coluna_grupo)[coluna_valor].describe()
    
    def analise_outliers(self, df: pd.DataFrame, coluna: str, metodo: str = 'iqr') -> dict:
        """
        Detecta outliers em uma variável numérica.
        
        Args:
            df: DataFrame
            coluna: Nome da coluna numérica
            metodo: 'iqr' ou 'zscore'
            
        Returns:
            Dicionário com informações sobre outliers
        """
        dados = df[coluna].dropna()
        
        if metodo == 'iqr':
            Q1 = dados.quantile(0.25)
            Q3 = dados.quantile(0.75)
            IQR = Q3 - Q1
            limite_inferior = Q1 - 1.5 * IQR
            limite_superior = Q3 + 1.5 * IQR
            outliers = dados[(dados < limite_inferior) | (dados > limite_superior)]
        
        elif metodo == 'zscore':
            z_scores = np.abs(stats.zscore(dados))
            outliers = dados[z_scores > 3]
        
        else:
            return {"erro": "Método deve ser 'iqr' ou 'zscore'"}
        
        return {
            "num_outliers": len(outliers),
            "porcentagem_outliers": round(len(outliers) / len(dados) * 100, 2),
            "outliers": outliers.tolist()[:10],  # Máximo 10 exemplos
            "metodo": metodo
        }
    
    def chi_quadrado_independencia(self, df: pd.DataFrame, coluna1: str, coluna2: str) -> dict:
        """
        Teste chi-quadrado de independência entre duas variáveis categóricas.
        
        Args:
            df: DataFrame
            coluna1, coluna2: Nomes das colunas categóricas
            
        Returns:
            Dicionário com resultado do teste
        """
        tabela_contingencia = pd.crosstab(df[coluna1], df[coluna2])
        
        if tabela_contingencia.size == 0:
            return {"erro": "Tabela de contingência vazia"}
        
        chi2, p_val, dof, expected = stats.chi2_contingency(tabela_contingencia)
        
        return {
            "chi2_estatistica": chi2,
            "p_valor": p_val,
            "graus_liberdade": dof,
            "significativo": p_val < 0.05,
            "interpretacao": "Variáveis dependentes" if p_val < 0.05 else "Variáveis independentes",
            "tabela_contingencia": tabela_contingencia
        }

    # Métodos de compatibilidade com versão anterior
    def correlations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Método de compatibilidade - use correlacoes() no lugar."""
        return self.correlacoes(df)
    
    def ttest_two_groups(self, df: pd.DataFrame, value_col: str, group_col: str, g1: str, g2: str) -> dict:
        """Método de compatibilidade - use teste_t_dois_grupos() no lugar."""
        return self.teste_t_dois_grupos(df, value_col, group_col, g1, g2)
    
    def freq_table(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """Método de compatibilidade - use tabela_frequencias() no lugar."""
        return self.tabela_frequencias(df, col)
