from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração dos gráficos
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

@dataclass
class Visualizer:
    """Visualizador para análise de dados de acidentes de trânsito."""
    
    # Gráficos básicos com matplotlib/seaborn
    def histograma(self, dados: pd.DataFrame, coluna: str):
        """Cria histograma de uma variável."""
        ax = sns.histplot(dados[coluna].dropna(), kde=True)
        ax.set_title(f"Distribuição de {coluna}")
        ax.set_xlabel(coluna.replace('_', ' ').title())
        ax.set_ylabel("Frequência")
        plt.tight_layout()
        return ax

    def boxplot(self, dados: pd.DataFrame, coluna: str, por: str | None = None):
        """Cria boxplot de uma variável, opcionalmente agrupado."""
        if por:
            ax = sns.boxplot(data=dados, x=por, y=coluna)
            ax.set_title(f"Distribuição de {coluna} por {por}")
        else:
            ax = sns.boxplot(y=dados[coluna])
            ax.set_title(f"Distribuição de {coluna}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return ax

    def dispersao(self, dados: pd.DataFrame, x: str, y: str, cor: str | None = None):
        """Cria gráfico de dispersão entre duas variáveis."""
        ax = sns.scatterplot(data=dados, x=x, y=y, hue=cor)
        ax.set_title(f"Relação entre {x} e {y}")
        ax.set_xlabel(x.replace('_', ' ').title())
        ax.set_ylabel(y.replace('_', ' ').title())
        plt.tight_layout()
        return ax

    def mapa_calor_correlacao(self, correlacao: pd.DataFrame):
        """Cria mapa de calor das correlações."""
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(correlacao, ax=ax, cmap="RdBu_r", center=0, 
                   annot=True, fmt='.2f', square=True)
        ax.set_title("Matriz de Correlação - Variáveis Numéricas")
        plt.tight_layout()
        return ax

    
    # Gráficos interativos com Plotly
    def linha_temporal(self, dados: pd.DataFrame, x: str, y: str, cor: str | None = None):
        """Cria gráfico de linha temporal interativo."""
        fig = px.line(dados, x=x, y=y, color=cor, 
                     title=f"Evolução Temporal de {y.replace('_', ' ').title()}")
        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title(),
            hovermode='x unified'
        )
        return fig

    def barras(self, dados: pd.DataFrame, x: str, y: str, cor: str | None = None):
        """Cria gráfico de barras interativo."""
        fig = px.bar(dados, x=x, y=y, color=cor, 
                    title=f"{y.replace('_', ' ').title()} por {x.replace('_', ' ').title()}")
        fig.update_layout(
            xaxis_title=x.replace('_', ' ').title(),
            yaxis_title=y.replace('_', ' ').title()
        )
        return fig

    def mapa_acidentes(self, dados: pd.DataFrame, lat: str = "latitude", lon: str = "longitude", 
                      cor: str | None = None, zoom: int = 5):
        """Cria mapa interativo dos acidentes."""
        dados_validos = dados.dropna(subset=[lat, lon])
        fig = px.scatter_mapbox(
            dados_validos,
            lat=lat, lon=lon, color=cor, zoom=zoom,
            height=600, title="Localização dos Acidentes",
            hover_data=['uf'] if 'uf' in dados_validos.columns else None
        )
        fig.update_layout(mapbox_style="open-street-map")
        return fig

    def acidentes_por_hora(self, dados: pd.DataFrame):
        """Gráfico da distribuição dos acidentes por hora."""
        if 'hora' not in dados.columns:
            print("⚠️ Coluna 'hora' não encontrada. Tentando criar a partir de 'data_hora_completa'...")
            if 'data_hora_completa' in dados.columns:
                dados = dados.copy()
                dados['hora'] = pd.to_datetime(dados['data_hora_completa']).dt.hour
            elif 'data_inversa' in dados.columns:
                dados = dados.copy()
                dados['hora'] = pd.to_datetime(dados['data_inversa']).dt.hour
            else:
                return px.bar(title="❌ Nenhum dado temporal disponível")
        
        acidentes_por_hora = dados.groupby('hora').size().reset_index(name='quantidade')
        fig = px.bar(
            acidentes_por_hora, 
            x='hora', 
            y='quantidade',
            title="Distribuição dos Acidentes por Hora do Dia",
            labels={'hora': 'Hora do Dia', 'quantidade': 'Número de Acidentes'}
        )
        fig.update_layout(
            xaxis=dict(tickmode='linear', dtick=1),
            showlegend=False
        )
        fig.update_traces(marker_color='steelblue')
        return fig
    
    def acidentes_por_ano(self, dados: pd.DataFrame):
        """Gráfico da evolução dos acidentes por ano."""
        if 'ano' not in dados.columns:
            print("⚠️ Coluna 'ano' não encontrada.")
            return px.bar(title="❌ Dados de ano não disponíveis")
        
        acidentes_por_ano = dados.groupby('ano').size().reset_index(name='quantidade')
        fig = px.bar(
            acidentes_por_ano,
            x='ano',
            y='quantidade',
            title="Evolução dos Acidentes por Ano (2021-2025)",
            labels={'ano': 'Ano', 'quantidade': 'Número de Acidentes'}
        )
        fig.update_traces(marker_color='lightcoral')
        return fig
    
    def heatmap_uf_ano(self, dados: pd.DataFrame):
        """Mapa de calor: acidentes por UF e ano."""
        if not {'uf', 'ano'}.issubset(dados.columns):
            return px.imshow([[0]], title="❌ Colunas 'uf' e 'ano' necessárias")
        
        pivot = dados.groupby(['uf', 'ano']).size().unstack(fill_value=0)
        fig = px.imshow(
            pivot,
            title="Acidentes por Estado e Ano",
            labels=dict(x="Ano", y="Estado", color="Acidentes"),
            aspect="auto"
        )
        return fig
    
    def top_causas(self, dados: pd.DataFrame, top_n: int = 10):
        """Gráfico das principais causas de acidentes."""
        if 'causa_acidente' not in dados.columns:
            return px.bar(title="❌ Coluna 'causa_acidente' não encontrada")
        
        causas = dados['causa_acidente'].value_counts().head(top_n)
        fig = px.bar(
            x=causas.values,
            y=causas.index,
            orientation='h',
            title=f"Top {top_n} Causas de Acidentes",
            labels={'x': 'Número de Acidentes', 'y': 'Causa'}
        )
        fig.update_layout(height=400 + top_n * 20)
        return fig
    
    # Métodos de compatibilidade com nomes antigos
    def hist(self, df: pd.DataFrame, col: str):
        """Compatibilidade: use 'histograma()' ao invés."""
        return self.histograma(df, col)
    
    def box(self, df: pd.DataFrame, col: str, by: str | None = None):
        """Compatibilidade: use 'boxplot()' ao invés."""
        return self.boxplot(df, col, by)
    
    def scatter(self, df: pd.DataFrame, x: str, y: str, color: str | None = None):
        """Compatibilidade: use 'dispersao()' ao invés."""
        return self.dispersao(df, x, y, color)
    
    def heatmap_corr(self, corr: pd.DataFrame):
        """Compatibilidade: use 'mapa_calor_correlacao()' ao invés."""
        return self.mapa_calor_correlacao(corr)
    
    def line_time(self, df: pd.DataFrame, x: str, y: str, color: str | None = None):
        """Compatibilidade: use 'linha_temporal()' ao invés."""
        return self.linha_temporal(df, x, y, color)
    
    def bar(self, df: pd.DataFrame, x: str, y: str, color: str | None = None):
        """Compatibilidade: use 'barras()' ao invés."""
        return self.barras(df, x, y, color)
    
    def geo_scatter(self, df: pd.DataFrame, lat: str, lon: str, color: str | None = None, zoom: int = 10):
        """Compatibilidade: use 'mapa_acidentes()' ao invés."""
        return self.mapa_acidentes(df, lat, lon, color, zoom)
    
    def plot_accidents_by_hour(self, df: pd.DataFrame):
        """Compatibilidade: use 'acidentes_por_hora()' ao invés."""
        return self.acidentes_por_hora(df)
