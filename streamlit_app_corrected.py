import os
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from src.traffic_analysis import DataLoader, DataCleaner, DataExplorer, StatisticalAnalyzer, Visualizer, InsightGenerator

st.set_page_config(page_title="Análise de Acidentes de Trânsito 2021-2025", layout="wide", page_icon="🚗")

st.title("🚗 Análise de Acidentes de Trânsito - Brasil 2021-2025")
st.markdown("---")

# Configuração dos anos disponíveis
AVAILABLE_YEARS = [2021, 2022, 2023, 2024, 2025]

# Détection automatique du chemin de base (même logique que le notebook)
BASE_PATH = Path(__file__).parent if '__file__' in globals() else Path.cwd()
DATA_PATH = BASE_PATH / "data" / "raw_data"

print(f"📁 Chemin de base détecté: {BASE_PATH}")
print(f"📂 Dossier des données: {DATA_PATH}")

# Barra lateral para configurações
st.sidebar.header("⚙️ Configurações")

# Seleção dos anos para análise
selected_years = st.sidebar.multiselect(
    "📅 Selecione os anos para análise:",
    options=AVAILABLE_YEARS,
    default=AVAILABLE_YEARS,
    help="Escolha um ou vários anos para análise"
)

# Opção de upload de arquivo
uploaded = st.sidebar.file_uploader("📁 Ou carregue um CSV personalizado", type=["csv"]) 

@st.cache_data
def carregar_dados_multiplos_anos(anos):
    """Carrega dados para os anos selecionados"""
    if not anos:
        return None
    
    try:
        # Criar um loader temporário para usar o método multi-anos
        # Utiliser le chemin vers le dossier des données
        caminho_arquivo = DATA_PATH / "datatran2025.csv"
        loader = DataLoader(caminho=caminho_arquivo, separador=";", codificacao="utf-8")
        df = loader.carregar_multiplos_anos(anos, caminho_base=DATA_PATH)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

@st.cache_data
def carregar_arquivo_unico():
    """Carrega arquivo único enviado"""
    if uploaded is not None:
        try:
            return pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {e}")
            return None
    return None

# Carregamento dos dados
with st.spinner("🔄 Carregando e processando dados..."):
    if uploaded is not None:
        df_raw = carregar_arquivo_unico()
        modo_analise = "arquivo_unico"
    elif selected_years:
        df_raw = carregar_dados_multiplos_anos(selected_years)
        modo_analise = "multi_anos"
    else:
        st.warning("Por favor selecione pelo menos um ano ou faça upload de um arquivo.")
        df_raw = None
        modo_analise = None

if df_raw is not None and len(df_raw) > 0:
    # Limpeza dos dados
    with st.spinner("🧹 Limpando dados..."):
        limpador = DataCleaner(
            coluna_data="data_inversa",
            coluna_hora="horario", 
            coluna_lat="latitude",
            coluna_lon="longitude"
        )
        df = limpador.executar(df_raw)
    
    # Exibição das informações básicas
    if modo_analise == "multi_anos":
        anos_nos_dados = sorted(df['ano'].unique()) if 'ano' in df.columns else selected_years
        st.success(f"✅ Dados carregados com sucesso!")
        st.info(f"📊 **{df.shape[0]:,}** registros processados para os anos **{', '.join(map(str, anos_nos_dados))}**")
    else:
        st.success(f"✅ Dados carregados com sucesso! **{df.shape[0]:,}** registros processados.")
    
    # Exibição do período dos dados
    if 'data_inversa' in df.columns:
        data_min = df['data_inversa'].min().strftime('%d/%m/%Y')
        data_max = df['data_inversa'].max().strftime('%d/%m/%Y') 
        st.info(f"📅 Período dos dados: **{data_min}** a **{data_max}**")
    
    # Abas para organizar a análise
    if modo_analise == "multi_anos":
        aba1, aba2, aba3, aba4, aba5 = st.tabs([
            "📊 Visão Geral", 
            "📈 Evolução Temporal", 
            "🗺️ Análise Geográfica", 
            "⚠️ Causas e Tipos", 
            "🔍 Análises Avançadas"
        ])
    else:
        aba1, aba2, aba3, aba4 = st.tabs([
            "📊 Visão Geral", 
            "🗺️ Análise Geográfica", 
            "⚠️ Causas e Tipos", 
            "🔍 Análises Avançadas"
        ])
    
    # Primeira aba - Visão Geral
    with aba1:
        st.header("📊 Visão Geral dos Dados")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Acidentes", f"{df.shape[0]:,}")
        with col2:
            total_mortos = df['mortos'].sum() if 'mortos' in df.columns else 0
            st.metric("Total de Mortos", f"{total_mortos:,}")
        with col3:
            total_feridos = df['feridos'].sum() if 'feridos' in df.columns else 0
            st.metric("Total de Feridos", f"{total_feridos:,}")
        with col4:
            if 'ano' in df.columns:
                nb_anos = df['ano'].nunique()
                st.metric("Anos Analisados", nb_anos)
            else:
                st.metric("Variáveis", df.shape[1])
        
        # Distribuição dos acidentes
        if modo_analise == "multi_anos" and 'ano' in df.columns:
            st.subheader("📊 Distribuição de acidentes por ano")
            acidentes_por_ano = df['ano'].value_counts().sort_index()
            fig = px.bar(x=acidentes_por_ano.index, y=acidentes_por_ano.values,
                        labels={'x': 'Ano', 'y': 'Número de Acidentes'},
                        title="Número de acidentes por ano")
            st.plotly_chart(fig, use_container_width=True)
        
        # Visualização dos dados
        st.subheader("🔍 Amostra dos Dados")
        df_display = df.copy()
        # Converter datetime para exibição
        for col in df_display.columns:
            if df_display[col].dtype == 'datetime64[ns]' or 'datetime' in str(df_display[col].dtype):
                df_display[col] = df_display[col].astype(str)
        st.dataframe(df_display.head(10), use_container_width=True)
        
        # Estatísticas descritivas
        with st.expander("📈 Estatísticas Descritivas Detalhadas"):
            try:
                st.dataframe(df.select_dtypes(include=[np.number]).describe(), use_container_width=True)
            except Exception as e:
                st.write("Erro ao exibir estatísticas:", str(e))
    
    # Segunda aba - Evolução temporal (apenas para multi-anos)
    if modo_analise == "multi_anos":
        with aba2:
            st.header("📈 Evolução Temporal dos Acidentes")
            
            if 'ano' in df.columns:
                # Evolução por ano
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Acidentes por ano")
                    acidentes_por_ano = df.groupby('ano').size()
                    fig = px.line(x=acidentes_por_ano.index, y=acidentes_por_ano.values,
                                 markers=True, labels={'x': 'Ano', 'y': 'Número de Acidentes'})
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if 'mortos' in df.columns:
                        st.subheader("Mortos por ano")
                        mortos_por_ano = df.groupby('ano')['mortos'].sum()
                        fig = px.line(x=mortos_por_ano.index, y=mortos_por_ano.values,
                                     markers=True, labels={'x': 'Ano', 'y': 'Número de Mortos'},
                                     line_shape='spline')
                        fig.update_traces(line_color='red')
                        st.plotly_chart(fig, use_container_width=True)
                
                # Evolução mensal
                if 'data_inversa' in df.columns:
                    st.subheader("Evolução mensal por ano")
                    df['mes'] = df['data_inversa'].dt.month
                    dados_mensais = df.groupby(['ano', 'mes']).size().reset_index(name='acidentes')
                    
                    fig = px.line(dados_mensais, x='mes', y='acidentes', color='ano',
                                 markers=True, labels={'mes': 'Mês', 'acidentes': 'Número de Acidentes'},
                                 title="Evolução mensal dos acidentes por ano")
                    
                    labels_meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                    fig.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1,13)), ticktext=labels_meses))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Heatmap dos acidentes por mês e ano
                if 'data_inversa' in df.columns:
                    st.subheader("Heatmap: Acidentes por mês e ano")
                    dados_heatmap = dados_mensais.pivot(index='ano', columns='mes', values='acidentes')
                    
                    fig = px.imshow(dados_heatmap, 
                                   labels=dict(x="Mês", y="Ano", color="Acidentes"),
                                   x=labels_meses,
                                   aspect="auto",
                                   color_continuous_scale="YlOrRd")
                    st.plotly_chart(fig, use_container_width=True)
    
    # Aba Análise geográfica
    aba_geo = aba3 if modo_analise == "multi_anos" else aba2
    with aba_geo:
        st.header("🗺️ Análise Geográfica")
        
        if 'uf' in df.columns:
            # Top dos estados
            st.subheader("Top 10 estados com mais acidentes")
            
            if modo_analise == "multi_anos" and 'ano' in df.columns:
                acidentes_por_estado_ano = df.groupby(['uf', 'ano']).size().reset_index(name='acidentes')
                top_estados = df['uf'].value_counts().head(10).index
                dados_top_estados = acidentes_por_estado_ano[acidentes_por_estado_ano['uf'].isin(top_estados)]
                
                fig = px.bar(dados_top_estados, x='uf', y='acidentes', color='ano',
                           title="Top 10 estados - Acidentes por ano",
                           labels={'uf': 'Estado', 'acidentes': 'Número de Acidentes'})
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            else:
                acidentes_por_estado = df['uf'].value_counts().head(10)
                fig = px.bar(x=acidentes_por_estado.index, y=acidentes_por_estado.values,
                           labels={'x': 'Estado', 'y': 'Número de Acidentes'},
                           title="Top 10 estados com mais acidentes")
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Mapa dos acidentes (se coordenadas disponíveis)
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.subheader("🗺️ Mapa dos Acidentes")
            
            # Filtrar dados com coordenadas válidas
            df_mapa = df.dropna(subset=['latitude', 'longitude'])
            
            if len(df_mapa) > 0:
                # Amostragem se muitos dados
                if len(df_mapa) > 5000:
                    df_mapa = df_mapa.sample(n=5000, random_state=42)
                    st.info(f"Exibindo amostra de 5000 acidentes de {len(df)} para otimizar performance")
                
                # Mapa com plotly
                cor_col = 'ano' if 'ano' in df_mapa.columns else None
                dados_hover = ['uf', 'municipio'] if all(col in df_mapa.columns for col in ['uf', 'municipio']) else None
                
                fig = px.scatter_map(df_mapa, lat="latitude", lon="longitude",
                                   color=cor_col, hover_data=dados_hover,
                                   zoom=4, height=600,
                                   map_style="open-street-map",
                                   title="Localização dos acidentes")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Nenhuma coordenada válida encontrada para exibir o mapa.")
    
    # Aba Causas e tipos
    aba_causas = aba4 if modo_analise == "multi_anos" else aba3
    with aba_causas:
        st.header("⚠️ Análise de Causas e Tipos de Acidentes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'causa_acidente' in df.columns:
                st.subheader("Principais causas de acidentes")
                top_causas = df['causa_acidente'].value_counts().head(10)
                fig = px.pie(values=top_causas.values, names=top_causas.index,
                           title="Top 10 causas de acidentes")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'tipo_acidente' in df.columns:
                st.subheader("Tipos de acidentes mais frequentes")
                top_tipos = df['tipo_acidente'].value_counts().head(10)
                fig = px.bar(x=top_tipos.values, y=top_tipos.index, orientation='h',
                           labels={'x': 'Número de Acidentes', 'y': 'Tipo de Acidente'},
                           title="Top 10 tipos de acidentes")
                st.plotly_chart(fig, use_container_width=True)
        
        # Evolução das causas no tempo (para multi-anos)
        if modo_analise == "multi_anos" and 'ano' in df.columns and 'causa_acidente' in df.columns:
            st.subheader("Evolução das principais causas no tempo")
            lista_top_causas = df['causa_acidente'].value_counts().head(5).index
            evolucao_causas = df[df['causa_acidente'].isin(lista_top_causas)].groupby(['ano', 'causa_acidente']).size().reset_index(name='acidentes')
            
            fig = px.line(evolucao_causas, x='ano', y='acidentes', color='causa_acidente',
                         markers=True, title="Evolução das principais causas por ano")
            st.plotly_chart(fig, use_container_width=True)
    
    # Aba Análises avançadas
    aba_avancada = aba5 if modo_analise == "multi_anos" else aba4
    with aba_avancada:
        st.header("🔍 Análises Avançadas")
        
        # Análise da gravidade
        if 'classificacao_acidente' in df.columns:
            st.subheader("Distribuição por gravidade dos acidentes")
            contagem_gravidade = df['classificacao_acidente'].value_counts()
            fig = px.pie(values=contagem_gravidade.values, names=contagem_gravidade.index,
                       title="Distribuição dos acidentes por gravidade")
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise temporal detalhada
        if 'data_inversa' in df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                # Acidentes por dia da semana
                df['dia_semana'] = df['data_inversa'].dt.day_name()
                ordem_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                acidentes_dia = df['dia_semana'].value_counts().reindex(ordem_dias)
                fig = px.bar(x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'], 
                           y=acidentes_dia.values,
                           labels={'x': 'Dia da Semana', 'y': 'Número de Acidentes'},
                           title="Acidentes por dia da semana")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Distribuição horária
                if 'horario' in df.columns:
                    try:
                        df['hora'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour
                        acidentes_hora = df['hora'].value_counts().sort_index()
                        fig = px.line(x=acidentes_hora.index, y=acidentes_hora.values,
                                     markers=True,
                                     labels={'x': 'Hora', 'y': 'Número de Acidentes'},
                                     title="Distribuição horária dos acidentes")
                        st.plotly_chart(fig, use_container_width=True)
                    except:
                        st.warning("Formato de hora não reconhecido para análise horária")
        
        # Visualizações extras
        st.subheader("📈 Visualizações Avançadas")
        
        viz = Visualizer()

        # Histograma
        st.subheader("📊 Distribuição de Variáveis Numéricas")
        colunas_num = df.select_dtypes(include=['number']).columns.tolist()
        if colunas_num:
            col = st.selectbox("Selecione uma variável numérica para histograma", colunas_num)
            if col:
                try:
                    fig_hist = viz.histograma(df, col)
                    st.pyplot(fig_hist.figure)
                except Exception as e:
                    st.error(f"Erro ao gerar histograma: {e}")

        # Gráficos temporais interativos
        st.subheader("⏰ Análise Temporal")
        opcoes_temporais = []
        for c in ["hora", "dia_semana", "mes"]:
            if c in df.columns:
                opcoes_temporais.append(c)
        
        if opcoes_temporais:
            por = st.selectbox("Agregação temporal", opcoes_temporais)
            if por:
                try:
                    ts = df.groupby(por).size().reset_index(name="count").sort_values(por)
                    fig_temporal = px.bar(ts, x=por, y="count")
                    
                    # Melhorar o gráfico
                    labels = {
                        'hora': 'Distribuição por Hora',
                        'dia_semana': 'Distribuição por Dia da Semana', 
                        'mes': 'Distribuição por Mês'
                    }
                    fig_temporal.update_layout(title=labels.get(por, f"Distribuição por {por}"))
                    st.plotly_chart(fig_temporal, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar gráfico temporal: {e}")

        # Mapa
        st.subheader("🗺️ Localização dos Acidentes")
        if {'latitude','longitude'}.issubset(df.columns):
            df_geo = df[['latitude','longitude']].dropna()
            if len(df_geo) > 0:
                # Limitar para performance
                if len(df_geo) > 10000:
                    df_geo = df_geo.sample(n=10000, random_state=42)
                    st.info(f"Mostrando amostra de 10.000 pontos de {len(df[['latitude','longitude']].dropna())} total para melhor performance.")
                
                st.map(df_geo.rename(columns={"latitude":"lat","longitude":"lon"}))
                
                st.write(f"📍 Total de acidentes com localização: {len(df[['latitude','longitude']].dropna()):,}")
            else:
                st.warning("Nenhuma coordenada válida encontrada.")
        else:
            st.warning("Colunas de latitude/longitude não encontradas.")
        
        # Correlações
        st.subheader("Matriz de correlação")
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(colunas_numericas) > 1:
            # Limitar às colunas mais relevantes
            colunas_relevantes = [col for col in ['pessoas', 'mortos', 'feridos', 'feridos_graves', 'feridos_leves', 'veiculos'] 
                               if col in colunas_numericas]
            if len(colunas_relevantes) > 1:
                matriz_corr = df[colunas_relevantes].corr()
                fig = px.imshow(matriz_corr, 
                               labels=dict(color="Correlação"),
                               color_continuous_scale="RdBu_r",
                               aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Não há variáveis numéricas relevantes suficientes para matriz de correlação")
        else:
            st.info("Não há variáveis numéricas suficientes para calcular correlações")
        
        # Insights automáticos
        with st.expander("🤖 Insights Automáticos"):
            try:
                # Usar o gerador de insights se disponível
                gerador_insights = InsightGenerator()
                insights = gerador_insights.gerar_insights(df)
                st.write(insights)
            except Exception as e:
                # Insights básicos se a ferramenta não funcionar
                st.write("**Insights Básicos:**")
                if 'ano' in df.columns:
                    ano_mais_acidentes = df['ano'].mode()[0]
                    st.write(f"• Ano com mais acidentes: {ano_mais_acidentes}")
                if 'uf' in df.columns:
                    estado_mais_acidentes = df['uf'].mode()[0]
                    st.write(f"• Estado com mais acidentes: {estado_mais_acidentes}")
                if 'causa_acidente' in df.columns:
                    causa_principal = df['causa_acidente'].mode()[0]
                    st.write(f"• Causa principal: {causa_principal}")

    # Resumo Executivo
    st.header("📋 Resumo Executivo")
    
    with st.container():
        st.markdown("**🎯 Principais Descobertas:**")
        
        pontos_resumo = []
        
        # Volume de dados
        pontos_resumo.append(f"• **Volume:** {len(df):,} registros de acidentes de trânsito")
        
        # Qualidade dos dados
        if 'latitude' in df.columns and 'longitude' in df.columns:
            cobertura_geo = df[['latitude', 'longitude']].dropna().shape[0] / len(df) * 100
            pontos_resumo.append(f"• **Qualidade:** {cobertura_geo:.1f}% dos acidentes possuem localização geográfica")
        
        # Padrões temporais
        if 'hora' in df.columns:
            hora_pico = df['hora'].value_counts().idxmax()
            contagem_pico = df['hora'].value_counts().max()
            pontos_resumo.append(f"• **Horário Crítico:** {hora_pico}h concentra {contagem_pico:,} acidentes")
        
        if 'dia_semana' in df.columns:
            dia_pico = df['dia_semana'].value_counts().idxmax()
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            dias_ingles = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            try:
                indice_dia = dias_ingles.index(dia_pico)
                nome_dia = dias_semana[indice_dia]
                pontos_resumo.append(f"• **Dia Crítico:** {nome_dia} é o dia com mais acidentes")
            except:
                pontos_resumo.append(f"• **Dia Crítico:** {dia_pico} é o dia com mais acidentes")
        
        # Período de dados
        if 'data_inversa' in df.columns:
            periodo = (df['data_inversa'].max() - df['data_inversa'].min()).days
            pontos_resumo.append(f"• **Período:** Dados cobrem {periodo} dias de registros")
        
        # Completude
        completude = (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        pontos_resumo.append(f"• **Completude:** {completude:.1f}% dos dados estão preenchidos")
        
        for ponto in pontos_resumo:
            st.write(ponto)
        
        st.markdown("""
        **💼 Recomendações:**
        • Focar políticas de segurança nos horários e dias de pico
        • Implementar medidas preventivas nas regiões com maior concentração
        • Melhorar a coleta de dados nas áreas com baixa cobertura geográfica
        • Monitorar tendências temporais para ações proativas
        """)

    # Informações adicionais
    with st.expander("ℹ️ Informações sobre os Dados"):
        st.write("**Colunas disponíveis:**")
        for col in df.columns:
            st.write(f"- {col}: {df[col].dtype}")

else:
    st.error("❌ Nenhum dado disponível. Verifique os arquivos ou faça upload de um CSV.")
    
    st.markdown("### 📝 Instruções:")
    st.markdown("""
    1. **Para análise multi-anos:** Certifique-se de que os arquivos `datatran2021.csv`, `datatran2022.csv`, etc. estejam presentes no diretório
    2. **Para arquivo personalizado:** Use o botão de upload na barra lateral  
    3. **Formato esperado:** Os arquivos CSV devem conter as colunas padrão dos dados PRF (Polícia Rodoviária Federal)
    """)
