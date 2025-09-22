from __future__ import annotations
from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class DataCleaner:
    """Limpador de dados para análise de acidentes de trânsito."""
    
    colunas_data: tuple[str, ...] = ("data_inversa", "date", "data_ocorrencia", "data") 
    colunas_hora: tuple[str, ...] = ("hora", "horario", "hora_ocorrencia", "time")
    coluna_latitude: str = "latitude"
    coluna_longitude: str = "longitude"
    
    def __init__(self, coluna_data: str = None, coluna_hora: str = None, 
                 coluna_lat: str = None, coluna_lon: str = None):
        """
        Inicializa o DataCleaner com colunas específicas ou usa os valores padrão.
        
        Args:
            coluna_data: Nome da coluna de data principal (opcional)
            coluna_hora: Nome da coluna de tempo/hora (opcional)
            coluna_lat: Nome da coluna de latitude (opcional)
            coluna_lon: Nome da coluna de longitude (opcional)
        """
        # Usar os valores fornecidos ou manter os valores padrão
        if coluna_data:
            self.colunas_data = (coluna_data,) + self.colunas_data
        if coluna_hora:
            self.colunas_hora = (coluna_hora,) + self.colunas_hora
        if coluna_lat:
            self.coluna_latitude = coluna_lat
        if coluna_lon:
            self.coluna_longitude = coluna_lon

    def padronizar_colunas(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Padroniza os nomes das colunas removendo acentos e espaços."""
        dados = dados.copy()
        dados.columns = (
            dados.columns.str.strip() 
            .str.lower()
            .str.normalize("NFKD") 
            .str.encode("ascii", errors="ignore").str.decode("utf-8")
            .str.replace("\s+", "_", regex=True) 
        )
        return dados

    def processar_datas(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Processa e converte colunas de data para datetime."""
        dados = dados.copy()
        for coluna in self.colunas_data: 
            if coluna in dados.columns:
                dados[coluna] = pd.to_datetime(dados[coluna], errors="coerce", dayfirst=True)
        
        # Heurística: se uma coluna de hora existe, combinar com data
        for coluna_hora in self.colunas_hora:
            if coluna_hora in dados.columns and "data_inversa" in dados.columns:
                # combinar data + hora se possível
                try:
                    dados["data_hora_completa"] = pd.to_datetime(
                        dados["data_inversa"].dt.date.astype(str) + " " + dados[coluna_hora].astype(str),
                        errors="coerce"
                    )
                except Exception:
                    pass
        
        # criar variáveis de tempo se datetime disponível
        for coluna_temporal in ("data_hora_completa", "data", "date", "data_inversa"):
            if coluna_temporal in dados.columns and np.issubdtype(dados[coluna_temporal].dtype, np.datetime64):
                base = coluna_temporal
                dados["ano"] = dados[base].dt.year
                dados["mes"] = dados[base].dt.month
                dados["dia"] = dados[base].dt.day
                dados["hora"] = dados[base].dt.hour
                dados["dia_semana"] = dados[base].dt.weekday
                break
        return dados

    def tratar_valores_ausentes(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Trata valores ausentes através de imputação e remoção de colunas vazias."""
        dados = dados.copy()
        
        # Remover colunas quase vazias (mais de 95% de valores ausentes)
        fracao_nulos = dados.isna().mean()
        colunas_para_remover = fracao_nulos[fracao_nulos > 0.95].index.tolist()
        if colunas_para_remover:
            print(f"🗑️ Removendo {len(colunas_para_remover)} colunas quase vazias")
            dados = dados.drop(columns=colunas_para_remover)
        
        # Imputação simples para variáveis numéricas (mediana)
        colunas_numericas = dados.select_dtypes(include=["number"]).columns
        for coluna in colunas_numericas:
            if dados[coluna].isna().any():
                mediana = dados[coluna].median()
                dados[coluna] = dados[coluna].fillna(mediana)
        
        # Imputação simples para variáveis categóricas
        colunas_categoricas = dados.select_dtypes(include=["object", "category"]).columns
        for coluna in colunas_categoricas:
            if dados[coluna].isna().any():
                dados[coluna] = dados[coluna].fillna("nao_informado")
        
        return dados

    def remover_duplicatas(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Remove registros duplicados do dataset."""
        tamanho_original = len(dados)
        dados_limpos = dados.drop_duplicates()
        duplicatas_removidas = tamanho_original - len(dados_limpos)
        if duplicatas_removidas > 0:
            print(f"🔄 Removidas {duplicatas_removidas} duplicatas")
        return dados_limpos

    def corrigir_coordenadas_geograficas(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Corrige e valida coordenadas geográficas."""
        dados = dados.copy()
        for coluna in (self.coluna_latitude, self.coluna_longitude):
            if coluna in dados.columns:
                # Tratar coordenadas com vírgulas como separadores decimais (formato brasileiro/europeu)
                dados[coluna] = dados[coluna].astype(str).str.replace(',', '.', regex=False)
                dados[coluna] = pd.to_numeric(dados[coluna], errors="coerce")
                
                # Validar coordenadas brasileiras
                if coluna == self.coluna_latitude:
                    # Brasil: latitude entre -35 e 5 graus aproximadamente
                    mascara_valida = (dados[coluna] >= -35) & (dados[coluna] <= 5)
                    dados.loc[~mascara_valida, coluna] = np.nan
                elif coluna == self.coluna_longitude:
                    # Brasil: longitude entre -75 e -30 graus aproximadamente
                    mascara_valida = (dados[coluna] >= -75) & (dados[coluna] <= -30)
                    dados.loc[~mascara_valida, coluna] = np.nan
                    
        return dados

    def executar(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Executa todo o pipeline de limpeza dos dados."""
        print("🧹 Iniciando limpeza dos dados...")
        
        dados = self.padronizar_colunas(dados)
        print("✓ Colunas padronizadas")
        
        dados = self.processar_datas(dados)
        print("✓ Datas processadas")
        
        dados = self.tratar_valores_ausentes(dados)
        print("✓ Valores ausentes tratados")
        
        dados = self.remover_duplicatas(dados)
        print("✓ Duplicatas removidas")
        
        dados = self.corrigir_coordenadas_geograficas(dados)
        print("✓ Coordenadas geográficas corrigidas")
        
        print("✅ Limpeza concluída!")
        return dados
    
    def limpar(self, dados: pd.DataFrame) -> pd.DataFrame:
        """Alias para o método executar() para compatibilidade."""
        return self.executar(dados)
    
    # Métodos de compatibilidade com nomes antigos
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'padronizar_colunas()' ao invés."""
        return self.padronizar_colunas(df)
    
    def parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'processar_datas()' ao invés."""
        return self.processar_datas(df)
    
    def handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'tratar_valores_ausentes()' ao invés."""
        return self.tratar_valores_ausentes(df)
    
    def drop_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'remover_duplicatas()' ao invés."""
        return self.remover_duplicatas(df)
    
    def coerce_geo(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'corrigir_coordenadas_geograficas()' ao invés."""
        return self.corrigir_coordenadas_geograficas(df)
    
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'executar()' ao invés."""
        return self.executar(df)
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compatibilidade: use 'limpar()' ao invés."""
        return self.limpar(df)

# --- Utilitários CLI / teste ---
import argparse
import csv
from pathlib import Path

def _detectar_separador(caminho: Path, codificacao: str = "utf-8") -> str | None:
    """Detecta automaticamente o separador de um arquivo CSV."""
    try:
        amostra = caminho.read_bytes()[:65536]
        try:
            texto = amostra.decode(codificacao)
        except UnicodeDecodeError:
            texto = amostra.decode("latin-1", errors="ignore")
        dialeto = csv.Sniffer().sniff(texto, delimiters=";,|\t,")
        return dialeto.delimiter
    except Exception:
        return None

def _carregar_entrada(caminho: Path, separador: str | None = None, 
                     codificacao: str | None = None, num_linhas: int | None = None) -> pd.DataFrame:
    """Carrega arquivo de entrada com detecção automática de formato."""
    if caminho.suffix.lower() in {".parquet", ".pq"}:
        return pd.read_parquet(caminho)
    
    # CSV
    candidatos_codificacao = [codificacao] if codificacao else ["utf-8", "latin-1"]
    candidatos_separador = [separador] if separador is not None else []
    separador_detectado = _detectar_separador(caminho, candidatos_codificacao[0] if candidatos_codificacao else "utf-8")
    
    for delimitador in [separador_detectado, ";", ",", "\t", "|", None]:
        if delimitador not in candidatos_separador:
            candidatos_separador.append(delimitador)
    
    ultimo_erro = None
    for codif in candidatos_codificacao:
        for delim in candidatos_separador:
            try:
                return pd.read_csv(caminho, sep=delim, encoding=codif, engine="python", nrows=num_linhas)
            except Exception as e:
                ultimo_erro = e
                continue
    
    # último recurso: ignorar linhas problemáticas
    try:
        return pd.read_csv(caminho, sep=candidatos_separador[0], encoding=candidatos_codificacao[-1], 
                          engine="python", on_bad_lines="skip", nrows=num_linhas)
    except Exception as e:
        raise ultimo_erro if ultimo_erro is not None else e

def main():
    """Função principal para testar o DataCleaner via linha de comando."""
    parser = argparse.ArgumentParser(description="Testar DataCleaner em um arquivo CSV/Parquet.")
    parser.add_argument("-i", "--input", required=True, help="Caminho do arquivo de entrada (CSV ou Parquet).")
    parser.add_argument("--sep", default=None, help="Separador CSV (ex: ';' ou ','). Padrão: auto.")
    parser.add_argument("--encoding", default=None, help="Codificação (ex: 'utf-8' ou 'latin-1'). Padrão: auto.")
    parser.add_argument("--nrows", type=int, default=None, help="Número de linhas a carregar (para teste rápido).")
    parser.add_argument("--save-dir", default=None, help="Pasta de saída para salvar o DataFrame limpo (Parquet).")
    args = parser.parse_args()

    caminho = Path(args.input).expanduser().resolve()
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    print(f"📂 Carregando: {caminho}")
    dados_brutos = _carregar_entrada(caminho, sep=args.sep, encoding=args.encoding, nrows=args.nrows)
    print(f"📊 Forma bruta: {dados_brutos.shape}")

    limpador = DataCleaner()
    dados_limpos = limpador.executar(dados_brutos)
    print(f"📋 Forma limpa: {dados_limpos.shape}")
    print("👀 Amostra (5 linhas):")
    print(dados_limpos.head().to_string(index=False))

    if args.save_dir:
        pasta_saida = Path(args.save_dir).expanduser().resolve()
        pasta_saida.mkdir(parents=True, exist_ok=True)
        caminho_saida = pasta_saida / (caminho.stem + "_limpo.parquet")
        dados_limpos.to_parquet(caminho_saida)
        print(f"💾 Salvo em: {caminho_saida}")

if __name__ == "__main__":
    main()
