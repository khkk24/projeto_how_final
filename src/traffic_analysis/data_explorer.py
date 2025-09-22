from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class DataExplorer:
    """Classe para exploração descritiva de dados de acidentes de trânsito."""
    
    def formato(self, df: pd.DataFrame) -> tuple[int, int]:
        """Retorna a forma do DataFrame (linhas, colunas)."""
        return df.shape

    def visao_geral(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Gera uma visão geral das colunas do DataFrame.
        
        Returns:
            DataFrame com informações sobre cada coluna (tipo, nulos, únicos)
        """
        info = {
            "coluna": df.columns,
            "tipo_dados": df.dtypes.astype(str).values,
            "qtd_nulos": df.isna().sum().values,
            "pct_nulos": (df.isna().mean() * 100).round(2).values,
            "qtd_unicos": df.nunique(dropna=True).values,
        }
        return pd.DataFrame(info)

    def descrever_numericas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Estatísticas descritivas para variáveis numéricas."""
        return df.select_dtypes(include=["number"]).describe().T

    def descrever_categoricas(self, df: pd.DataFrame, top_n: int = 10) -> dict[str, pd.Series]:
        """
        Frequência das principais categorias para variáveis categóricas.
        
        Args:
            df: DataFrame a ser analisado
            top_n: Número de categorias mais frequentes a retornar
            
        Returns:
            Dicionário com value_counts para cada variável categórica
        """
        resultado = {}
        for coluna in df.select_dtypes(include=["object", "category"]).columns:
            resultado[coluna] = df[coluna].value_counts(dropna=False).head(top_n)
        return resultado
    
    def analise_temporal_anos(self, df: pd.DataFrame, coluna_ano: str = 'annee') -> pd.DataFrame:
        """
        Análise específica para dados multi-anos.
        
        Args:
            df: DataFrame com dados de múltiplos anos
            coluna_ano: Nome da coluna que contém o ano
            
        Returns:
            DataFrame com estatísticas por ano
        """
        if coluna_ano not in df.columns:
            print(f"Coluna '{coluna_ano}' não encontrada. Disponíveis: {list(df.columns)}")
            return pd.DataFrame()
        
        # Estatísticas básicas por ano
        colunas_disponiveis = {}
        colunas_disponiveis[df.columns[0]] = 'count'  # Usar primeira coluna como contagem
        
        if 'mortos' in df.columns:
            colunas_disponiveis['mortos'] = ['sum', 'mean']
        if 'feridos' in df.columns:
            colunas_disponiveis['feridos'] = ['sum', 'mean']
        if 'pessoas' in df.columns:
            colunas_disponiveis['pessoas'] = ['sum', 'mean']
        
        stats_por_ano = df.groupby(coluna_ano).agg(colunas_disponiveis).round(2)
        
        # Renomear colunas para português
        if 'mortos' in df.columns:
            stats_por_ano.columns = [
                'total_acidentes', 'total_mortos', 'media_mortos_por_acidente',
                'total_feridos', 'media_feridos_por_acidente',
                'total_pessoas', 'media_pessoas_por_acidente'
            ]
        
        return stats_por_ano
    
    def tendencias_temporais(self, df: pd.DataFrame, coluna_ano: str = 'annee') -> dict:
        """
        Calcula tendências entre anos.
        
        Returns:
            Dicionário com variações percentuais e tendências
        """
        if coluna_ano not in df.columns:
            return {}
        
        anos = sorted(df[coluna_ano].unique())
        primeiro_ano = anos[0]
        ultimo_ano = anos[-1]
        
        # Acidentes por ano
        acidentes_por_ano = df.groupby(coluna_ano).size()
        
        tendencias = {
            'primeiro_ano': primeiro_ano,
            'ultimo_ano': ultimo_ano,
            'acidentes_primeiro_ano': acidentes_por_ano[primeiro_ano],
            'acidentes_ultimo_ano': acidentes_por_ano[ultimo_ano],
            'variacao_acidentes_pct': round(
                ((acidentes_por_ano[ultimo_ano] - acidentes_por_ano[primeiro_ano]) / 
                 acidentes_por_ano[primeiro_ano]) * 100, 2
            )
        }
        
        # Adicionar tendências para mortos e feridos se disponíveis
        if 'mortos' in df.columns:
            mortos_por_ano = df.groupby(coluna_ano)['mortos'].sum()
            tendencias.update({
                'mortos_primeiro_ano': mortos_por_ano[primeiro_ano],
                'mortos_ultimo_ano': mortos_por_ano[ultimo_ano],
                'variacao_mortos_pct': round(
                    ((mortos_por_ano[ultimo_ano] - mortos_por_ano[primeiro_ano]) / 
                     mortos_por_ano[primeiro_ano]) * 100, 2
                )
            })
        
        if 'feridos' in df.columns:
            feridos_por_ano = df.groupby(coluna_ano)['feridos'].sum()
            tendencias.update({
                'feridos_primeiro_ano': feridos_por_ano[primeiro_ano],
                'feridos_ultimo_ano': feridos_por_ano[ultimo_ano],
                'variacao_feridos_pct': round(
                    ((feridos_por_ano[ultimo_ano] - feridos_por_ano[primeiro_ano]) / 
                     feridos_por_ano[primeiro_ano]) * 100, 2
                )
            })
        
        return tendencias
    
    def top_categorias_por_ano(self, df: pd.DataFrame, coluna: str, coluna_ano: str = 'annee', 
                              top_n: int = 5) -> pd.DataFrame:
        """
        Identifica as principais categorias por ano.
        
        Args:
            df: DataFrame
            coluna: Nome da coluna categórica a analisar
            coluna_ano: Nome da coluna do ano
            top_n: Número de categorias principais
            
        Returns:
            DataFrame com contagem por categoria e ano
        """
        if coluna not in df.columns or coluna_ano not in df.columns:
            return pd.DataFrame()
        
        # Top categorias gerais
        top_categorias = df[coluna].value_counts().head(top_n).index
        
        # Contagem por ano para essas categorias
        resultado = df[df[coluna].isin(top_categorias)].groupby([coluna_ano, coluna]).size().reset_index(name='contagem')
        
        return resultado.pivot(index=coluna, columns=coluna_ano, values='contagem').fillna(0)
    
    def resumo_geografico(self, df: pd.DataFrame, coluna_uf: str = 'uf') -> dict:
        """
        Resumo geográfico dos acidentes.
        
        Returns:
            Dicionário com estatísticas geográficas
        """
        if coluna_uf not in df.columns:
            return {}
        
        # Estatísticas por UF
        acidentes_por_uf = df[coluna_uf].value_counts()
        
        resumo = {
            'total_ufs': df[coluna_uf].nunique(),
            'uf_mais_acidentes': acidentes_por_uf.index[0],
            'acidentes_uf_lider': acidentes_por_uf.iloc[0],
            'top_5_ufs': acidentes_por_uf.head(5).to_dict()
        }
        
        # Adicionar estatísticas de mortos por UF se disponível
        if 'mortos' in df.columns:
            mortos_por_uf = df.groupby(coluna_uf)['mortos'].sum().sort_values(ascending=False)
            resumo.update({
                'uf_mais_mortos': mortos_por_uf.index[0],
                'mortos_uf_lider': mortos_por_uf.iloc[0],
                'taxa_mortalidade_por_uf': (df.groupby(coluna_uf)['mortos'].sum() / 
                                           df[coluna_uf].value_counts() * 100).round(2).to_dict()
            })
        
        return resumo

    # Manter métodos originais para compatibilidade
    def shape(self, df: pd.DataFrame) -> tuple[int, int]:
        """Método de compatibilidade - use formato() no lugar."""
        return self.formato(df)
    
    def overview(self, df: pd.DataFrame) -> pd.DataFrame:
        """Método de compatibilidade - use visao_geral() no lugar."""
        return self.visao_geral(df)
    
    def describe_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Método de compatibilidade - use descrever_numericas() no lugar."""
        return self.descrever_numericas(df)
    
    def describe_categorical(self, df: pd.DataFrame, top_n: int = 10) -> dict[str, pd.Series]:
        """Método de compatibilidade - use descrever_categoricas() no lugar."""
        return self.descrever_categoricas(df, top_n)
