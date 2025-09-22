from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from pandas.errors import ParserError
from typing import List, Optional


@dataclass
class DataLoader:
    """Carrega dados CSV/Parquet com esquema opcional."""

    caminho: Path
    separador: str | None = ","
    codificacao: str = "utf-8"
    memoria_baixa: bool = False

    def carregar(self) -> pd.DataFrame:
        """Carrega um único arquivo de dados."""
        caminho_arquivo = Path(self.caminho)
        print(f"📂 Carregando: {caminho_arquivo}")
        if not caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        if caminho_arquivo.suffix.lower() == ".parquet":
            dados = pd.read_parquet(caminho_arquivo)
        else:
            dados = self._carregar_csv_com_fallbacks(caminho_arquivo)
        return dados
    
    def carregar_multiplos_anos(self, anos: List[int], caminho_base: Optional[Path] = None) -> pd.DataFrame:
        """
        Carrega e combina os dados de múltiplos anos.
        
        Args:
            anos: Lista dos anos a carregar (ex: [2021, 2022, 2023, 2024, 2025])
            caminho_base: Caminho base onde estão os arquivos (padrão: diretório pai do caminho)
        
        Returns:
            DataFrame combinado com todos os anos
        """
        if caminho_base is None:
            caminho_base = Path(self.caminho).parent
        
        dataframes_anos = []
        
        for ano in anos:
            caminho_arquivo = caminho_base / f"datatran{ano}.csv"
            if caminho_arquivo.exists():
                print(f"📅 Carregando dados de {ano}...")
                carregador_temporario = DataLoader(
                    caminho=caminho_arquivo,
                    separador=self.separador,
                    codificacao=self.codificacao,
                    memoria_baixa=self.memoria_baixa
                )
                dados_ano = carregador_temporario.carregar()
                dados_ano['ano'] = ano  # Adicionar coluna do ano
                dataframes_anos.append(dados_ano)
                print(f"✓ {ano}: {len(dados_ano):,} registros carregados")
            else:
                print(f"⚠ Arquivo {caminho_arquivo} não encontrado, ignorado")
        
        if not dataframes_anos:
            raise FileNotFoundError(f"Nenhum arquivo de dados encontrado para os anos {anos}")
        
        # Combinar todos os DataFrames
        dados_combinados = pd.concat(dataframes_anos, ignore_index=True)
        print(f"\n✅ Total: {len(dados_combinados):,} registros carregados para {len(dataframes_anos)} anos")
        
        return dados_combinados

    # -- Métodos internos --
    def _carregar_csv_com_fallbacks(self, caminho_arquivo: Path) -> pd.DataFrame:
        """
        Tenta carregar um CSV detectando automaticamente o separador e
        testando várias codificações comuns (utf-8, latin-1). Como último recurso,
        pula linhas problemáticas.
        """

        # Ordem de teste das codificações e separadores
        codificacoes = [self.codificacao, "utf-8", "latin-1"]
        separadores = [self.separador, None, ";", ",", "\t", "|"]

        ultima_excecao: Exception | None = None
        for codif in codificacoes:
            for sep in separadores:
                try:
                    # se sep=None, usar engine='python' para detecção automática
                    motor = "python" if sep is None else "c"
                    kwargs = dict(sep=sep, encoding=codif, engine=motor)
                    if motor == "c":
                        kwargs["low_memory"] = self.memoria_baixa
                    return pd.read_csv(caminho_arquivo, **kwargs)
                except (ParserError, UnicodeDecodeError) as e:
                    ultima_excecao = e
                    continue

        # Último recurso: ignorar linhas corrompidas
        try:
            return pd.read_csv(
                caminho_arquivo,
                sep=self.separador if self.separador is not None else None,
                encoding=self.codificacao,
                engine="python",
                on_bad_lines="skip",
            )
        except Exception as e:
            raise e if ultima_excecao is None else ultima_excecao

    # Métodos de compatibilidade com nomes antigos
    @property
    def path(self) -> Path:
        """Compatibilidade: use 'caminho' ao invés."""
        return self.caminho
    
    @path.setter
    def path(self, value: Path):
        """Compatibilidade: use 'caminho' ao invés."""
        self.caminho = value
    
    def load(self) -> pd.DataFrame:
        """Compatibilidade: use 'carregar()' ao invés."""
        return self.carregar()
    
    def load_multiple_years(self, years: List[int], base_path: Optional[Path] = None) -> pd.DataFrame:
        """Compatibilidade: use 'carregar_multiplos_anos()' ao invés."""
        return self.carregar_multiplos_anos(years, base_path)
