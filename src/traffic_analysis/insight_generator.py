from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class InsightGenerator:
    """Classe para geração automática de insights sobre dados de acidentes de trânsito."""
    
    def gerar_insights(self, df: pd.DataFrame) -> str:
        """
        Gera insights abrangentes sobre os dados de acidentes.
        
        Args:
            df: DataFrame com dados de acidentes
            
        Returns:
            String com insights formatados
        """
        insights = []
        insights.append("🔍 INSIGHTS AUTOMÁTICOS - ACIDENTES DE TRÂNSITO")
        insights.append("=" * 50)
        
        # Insights básicos
        insights.extend(self._insights_basicos(df))
        
        # Insights temporais
        if 'annee' in df.columns:
            insights.extend(self._insights_temporais(df))
        
        # Insights geográficos
        if 'uf' in df.columns:
            insights.extend(self._insights_geograficos(df))
        
        # Insights sobre causas
        if 'causa_acidente' in df.columns:
            insights.extend(self._insights_causas(df))
        
        # Insights sobre gravidade
        if 'mortos' in df.columns and 'feridos' in df.columns:
            insights.extend(self._insights_gravidade(df))
        
        # Insights sobre padrões temporais
        insights.extend(self._insights_padroes_temporais(df))
        
        return "\n".join(insights)
    
    def _insights_basicos(self, df: pd.DataFrame) -> list:
        """Insights básicos sobre o dataset."""
        insights = ["\n📊 DADOS GERAIS:"]
        
        total_acidentes = len(df)
        insights.append(f"• Total de acidentes analisados: {total_acidentes:,}")
        
        if 'mortos' in df.columns:
            total_mortos = df['mortos'].sum()
            insights.append(f"• Total de mortos: {total_mortos:,}")
            taxa_mortalidade = (total_mortos / total_acidentes * 100)
            insights.append(f"• Taxa de mortalidade: {taxa_mortalidade:.2f}% dos acidentes")
        
        if 'feridos' in df.columns:
            total_feridos = df['feridos'].sum()
            insights.append(f"• Total de feridos: {total_feridos:,}")
        
        if 'pessoas' in df.columns:
            total_pessoas = df['pessoas'].sum()
            insights.append(f"• Total de pessoas envolvidas: {total_pessoas:,}")
            media_pessoas = df['pessoas'].mean()
            insights.append(f"• Média de pessoas por acidente: {media_pessoas:.1f}")
        
        return insights
    
    def _insights_temporais(self, df: pd.DataFrame) -> list:
        """Insights sobre evolução temporal."""
        insights = ["\n📅 EVOLUÇÃO TEMPORAL:"]
        
        anos = sorted(df['annee'].unique())
        primeiro_ano = anos[0]
        ultimo_ano = anos[-1]
        
        acidentes_por_ano = df.groupby('annee').size()
        primeiro_valor = acidentes_por_ano[primeiro_ano]
        ultimo_valor = acidentes_por_ano[ultimo_ano]
        variacao = ((ultimo_valor - primeiro_valor) / primeiro_valor) * 100
        
        insights.append(f"• Período analisado: {primeiro_ano} a {ultimo_ano}")
        insights.append(f"• Acidentes em {primeiro_ano}: {primeiro_valor:,}")
        insights.append(f"• Acidentes em {ultimo_ano}: {ultimo_valor:,}")
        insights.append(f"• Variação: {variacao:+.1f}%")
        
        # Ano com mais acidentes
        ano_pico = acidentes_por_ano.idxmax()
        valor_pico = acidentes_por_ano.max()
        insights.append(f"• Ano com mais acidentes: {ano_pico} ({valor_pico:,} acidentes)")
        
        # Tendência geral
        if variacao > 5:
            tendencia = "crescente"
        elif variacao < -5:
            tendencia = "decrescente"
        else:
            tendencia = "estável"
        insights.append(f"• Tendência geral: {tendencia}")
        
        return insights
    
    def _insights_geograficos(self, df: pd.DataFrame) -> list:
        """Insights sobre distribuição geográfica."""
        insights = ["\n🗺️ DISTRIBUIÇÃO GEOGRÁFICA:"]
        
        acidentes_por_uf = df['uf'].value_counts()
        
        insights.append(f"• Estados com dados: {len(acidentes_por_uf)}")
        insights.append(f"• Estado com mais acidentes: {acidentes_por_uf.index[0]} ({acidentes_por_uf.iloc[0]:,})")
        insights.append(f"• Estado com menos acidentes: {acidentes_por_uf.index[-1]} ({acidentes_por_uf.iloc[-1]:,})")
        
        # Top 3 estados
        top3 = acidentes_por_uf.head(3)
        total_top3 = top3.sum()
        pct_top3 = (total_top3 / len(df)) * 100
        insights.append(f"• Top 3 estados concentram {pct_top3:.1f}% dos acidentes")
        
        # Análise de concentração
        if pct_top3 > 50:
            insights.append("• Concentração ALTA em poucos estados")
        elif pct_top3 > 30:
            insights.append("• Concentração MODERADA em poucos estados")
        else:
            insights.append("• Distribuição mais equilibrada entre estados")
        
        return insights
    
    def _insights_causas(self, df: pd.DataFrame) -> list:
        """Insights sobre principais causas."""
        insights = ["\n⚠️ PRINCIPAIS CAUSAS:"]
        
        causas = df['causa_acidente'].value_counts()
        causa_principal = causas.index[0]
        pct_principal = (causas.iloc[0] / len(df)) * 100
        
        insights.append(f"• Causa mais comum: {causa_principal}")
        insights.append(f"• Representa {pct_principal:.1f}% dos acidentes")
        
        # Top 3 causas
        top3_causas = causas.head(3)
        pct_top3_causas = (top3_causas.sum() / len(df)) * 100
        insights.append(f"• Top 3 causas representam {pct_top3_causas:.1f}% dos casos")
        
        # Análise de padrões nas causas
        causas_humanas = ['reação tardia', 'ineficiente', 'condutor', 'álcool', 'velocidade']
        causas_infra = ['pista', 'sinalização', 'iluminação']
        
        total_humano = 0
        total_infra = 0
        
        for causa, freq in causas.items():
            causa_lower = causa.lower()
            if any(palavra in causa_lower for palavra in causas_humanas):
                total_humano += freq
            elif any(palavra in causa_lower for palavra in causas_infra):
                total_infra += freq
        
        pct_humano = (total_humano / len(df)) * 100
        pct_infra = (total_infra / len(df)) * 100
        
        insights.append(f"• Causas relacionadas ao fator humano: ~{pct_humano:.1f}%")
        insights.append(f"• Causas relacionadas à infraestrutura: ~{pct_infra:.1f}%")
        
        return insights
    
    def _insights_gravidade(self, df: pd.DataFrame) -> list:
        """Insights sobre gravidade dos acidentes."""
        insights = ["\n🚨 GRAVIDADE DOS ACIDENTES:"]
        
        total_mortos = df['mortos'].sum()
        total_feridos = df['feridos'].sum()
        acidentes_com_mortos = (df['mortos'] > 0).sum()
        acidentes_com_feridos = (df['feridos'] > 0).sum()
        
        pct_acidentes_mortos = (acidentes_com_mortos / len(df)) * 100
        pct_acidentes_feridos = (acidentes_com_feridos / len(df)) * 100
        
        insights.append(f"• Acidentes com mortos: {acidentes_com_mortos:,} ({pct_acidentes_mortos:.1f}%)")
        insights.append(f"• Acidentes com feridos: {acidentes_com_feridos:,} ({pct_acidentes_feridos:.1f}%)")
        
        # Média de vítimas por acidente quando há vítimas
        if acidentes_com_mortos > 0:
            media_mortos = total_mortos / acidentes_com_mortos
            insights.append(f"• Média de mortos por acidente fatal: {media_mortos:.1f}")
        
        if acidentes_com_feridos > 0:
            media_feridos = total_feridos / acidentes_com_feridos
            insights.append(f"• Média de feridos por acidente com feridos: {media_feridos:.1f}")
        
        # Classificação de gravidade
        if pct_acidentes_mortos > 10:
            insights.append("• Gravidade ALTA: muitos acidentes fatais")
        elif pct_acidentes_mortos > 5:
            insights.append("• Gravidade MODERADA")
        else:
            insights.append("• Gravidade BAIXA: poucos acidentes fatais")
        
        return insights
    
    def _insights_padroes_temporais(self, df: pd.DataFrame) -> list:
        """Insights sobre padrões temporais."""
        insights = ["\n⏰ PADRÕES TEMPORAIS:"]
        
        # Análise por data se disponível
        if 'data_inversa' in df.columns:
            df_temp = df.copy()
            df_temp['mes'] = df_temp['data_inversa'].dt.month
            df_temp['dia_semana'] = df_temp['data_inversa'].dt.day_name()
            
            # Mês com mais acidentes
            acidentes_por_mes = df_temp['mes'].value_counts().sort_index()
            mes_pico = acidentes_por_mes.idxmax()
            meses_nomes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 
                          5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                          9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
            insights.append(f"• Mês com mais acidentes: {meses_nomes.get(mes_pico, mes_pico)}")
            
            # Dia da semana
            acidentes_por_dia = df_temp['dia_semana'].value_counts()
            dia_pico = acidentes_por_dia.idxmax()
            pct_dia_pico = (acidentes_por_dia.max() / len(df)) * 100
            insights.append(f"• Dia da semana mais perigoso: {dia_pico} ({pct_dia_pico:.1f}%)")
            
            # Padrão fim de semana vs dias úteis
            fins_semana = df_temp[df_temp['dia_semana'].isin(['Saturday', 'Sunday'])]
            pct_fim_semana = (len(fins_semana) / len(df)) * 100
            insights.append(f"• Acidentes em fins de semana: {pct_fim_semana:.1f}%")
        
        # Análise horária se disponível
        if 'hour' in df.columns:
            acidentes_por_hora = df['hour'].value_counts().sort_index()
            hora_pico = acidentes_por_hora.idxmax()
            insights.append(f"• Horário com mais acidentes: {hora_pico}h")
            
            # Períodos do dia
            manha = df[(df['hour'] >= 6) & (df['hour'] < 12)]
            tarde = df[(df['hour'] >= 12) & (df['hour'] < 18)]
            noite = df[(df['hour'] >= 18) & (df['hour'] < 24)]
            madrugada = df[(df['hour'] >= 0) & (df['hour'] < 6)]
            
            periodos = {
                'Manhã': len(manha),
                'Tarde': len(tarde), 
                'Noite': len(noite),
                'Madrugada': len(madrugada)
            }
            periodo_pior = max(periodos, key=periodos.get)
            insights.append(f"• Período mais perigoso: {periodo_pior}")
        
        return insights
    
    def top_horarios(self, df: pd.DataFrame, coluna_hora: str = "hour", top_n: int = 5) -> pd.DataFrame:
        """Retorna os horários com mais acidentes."""
        if coluna_hora not in df.columns:
            return pd.DataFrame()
        contagem = df[coluna_hora].value_counts().sort_values(ascending=False).head(top_n)
        return contagem.rename_axis("hora").reset_index(name="acidentes")

    def top_localizacoes(self, df: pd.DataFrame, lat: str = "latitude", lon: str = "longitude", 
                        precisao: int = 3, top_n: int = 10) -> pd.DataFrame:
        """Identifica localizações com mais acidentes."""
        if not {lat, lon}.issubset(df.columns):
            return pd.DataFrame()
        
        df_temp = df.copy()
        df_temp["lat_arredondada"] = df_temp[lat].round(precisao)
        df_temp["lon_arredondada"] = df_temp[lon].round(precisao)
        
        contagem = df_temp.groupby(["lat_arredondada", "lon_arredondada"]).size().sort_values(ascending=False).head(top_n)
        return contagem.rename_axis(["latitude", "longitude"]).reset_index(name="acidentes")

    def padrao_dias_semana(self, df: pd.DataFrame, coluna_dia: str = "weekday") -> pd.DataFrame:
        """Analisa padrão de acidentes por dia da semana."""
        if coluna_dia not in df.columns:
            return pd.DataFrame()
        
        contagem = df[coluna_dia].value_counts().sort_index()
        return contagem.rename_axis("dia_semana").reset_index(name="acidentes")
    
    def analise_sazonalidade(self, df: pd.DataFrame) -> dict:
        """Analisa padrões sazonais nos dados."""
        if 'data_inversa' not in df.columns:
            return {}
        
        df_temp = df.copy()
        df_temp['mes'] = df_temp['data_inversa'].dt.month
        df_temp['trimestre'] = df_temp['data_inversa'].dt.quarter
        
        acidentes_por_mes = df_temp['mes'].value_counts().sort_index()
        acidentes_por_trimestre = df_temp['trimestre'].value_counts().sort_index()
        
        return {
            'mes_pico': acidentes_por_mes.idxmax(),
            'mes_menor': acidentes_por_mes.idxmin(),
            'variacao_mensal': ((acidentes_por_mes.max() - acidentes_por_mes.min()) / acidentes_por_mes.mean() * 100),
            'trimestre_pico': acidentes_por_trimestre.idxmax(),
            'acidentes_por_mes': acidentes_por_mes.to_dict(),
            'acidentes_por_trimestre': acidentes_por_trimestre.to_dict()
        }

    # Métodos de compatibilidade
    def top_hours(self, df: pd.DataFrame, hour_col: str = "hour", top_n: int = 5) -> pd.DataFrame:
        """Método de compatibilidade - use top_horarios() no lugar."""
        return self.top_horarios(df, hour_col, top_n)

    def top_locations(self, df: pd.DataFrame, lat: str = "latitude", lon: str = "longitude", 
                     precision: int = 3, top_n: int = 10) -> pd.DataFrame:
        """Método de compatibilidade - use top_localizacoes() no lugar."""
        return self.top_localizacoes(df, lat, lon, precision, top_n)

    def weekday_pattern(self, df: pd.DataFrame, weekday_col: str = "weekday") -> pd.DataFrame:
        """Método de compatibilidade - use padrao_dias_semana() no lugar."""
        return self.padrao_dias_semana(df, weekday_col)
    
    def generate_insights(self, df: pd.DataFrame) -> str:
        """Método de compatibilidade - use gerar_insights() no lugar."""
        return self.gerar_insights(df)
