@echo off
REM Script automatizado para instalar dependências e executar a aplicação Streamlit
REM Projet d'Analyse des Accidents de Trafic 2021-2025

echo.
echo ========================================
echo  Aplicacao de Analise de Acidentes
echo ========================================
echo.

REM Verificar se Python está instalado
echo [ETAPA 1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Ir para o diretório do script
cd /d "%~dp0"

REM Verificar/Criar ambiente virtual
echo [ETAPA 2/5] Configurando ambiente virtual...
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo Ambiente virtual criado com sucesso!
) else (
    echo Ambiente virtual ja existe
)
echo.

REM Ativar ambiente virtual
echo [ETAPA 3/5] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip --quiet

REM Instalar dependências
echo.
echo [ETAPA 4/5] Instalando dependencias...
echo Isso pode levar alguns minutos na primeira execucao...
echo.
if exist requirements.txt (
    pip install -r requirements.txt --quiet
    echo Dependencias instaladas com sucesso!
) else (
    echo [ERRO] Arquivo requirements.txt nao encontrado
    pause
    exit /b 1
)

REM Verificar dados
echo.
echo [ETAPA 5/5] Verificando dados...
if not exist "data\raw_data" (
    echo [AVISO] Pasta data\raw_data nao encontrada
    echo Voce pode fazer upload de dados na aplicacao
) else (
    dir /b "data\raw_data\*.csv" >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] Nenhum arquivo CSV encontrado em data\raw_data
        echo Voce pode fazer upload de dados na aplicacao
    ) else (
        echo Arquivos CSV encontrados
    )
)

REM Verificar se aplicação existe
if not exist "streamlit_app_corrected.py" (
    echo [ERRO] streamlit_app_corrected.py nao encontrado
    pause
    exit /b 1
)

REM Executar aplicação
echo.
echo ========================================
echo  INICIANDO APLICACAO STREAMLIT
echo ========================================
echo.
echo A aplicacao sera aberta no navegador
echo URL: http://localhost:8501
echo.
echo Para parar: Pressione Ctrl+C
echo ========================================
echo.

timeout /t 2 >nul

streamlit run streamlit_app_corrected.py --server.port 8501 --server.headless true

REM Desativar ambiente virtual ao sair
call .venv\Scripts\deactivate.bat
