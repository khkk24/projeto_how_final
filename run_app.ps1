# Script automatizado para instalar dependências e executar a aplicação Streamlit
# Projet d'Analyse des Accidents de Trafic 2021-2025
# Para Windows PowerShell

Write-Host "🚗 === Iniciando Aplicação de Análise de Acidentes de Trânsito ===" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        Write-Host "✅ $pythonVersion encontrado" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python não encontrado. Por favor, instale Python 3.8 ou superior." -ForegroundColor Red
    Write-Host "   Download: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Obter diretório do projeto
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir

# Verificar se ambiente virtual existe
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ambiente virtual já existe" -ForegroundColor Yellow
}
Write-Host ""

# Ativar ambiente virtual
Write-Host "🔄 Ativando ambiente virtual..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Atualizar pip
Write-Host "📦 Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Instalar dependências
Write-Host ""
Write-Host "📥 Instalando dependências..." -ForegroundColor Yellow
Write-Host "⏳ Isso pode levar alguns minutos na primeira execução..." -ForegroundColor Cyan
Write-Host ""

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt --quiet
    Write-Host "✅ Dependências instaladas com sucesso" -ForegroundColor Green
} else {
    Write-Host "❌ Arquivo requirements.txt não encontrado" -ForegroundColor Red
    exit 1
}

# Verificar se os dados existem
Write-Host ""
Write-Host "🔍 Verificando dados..." -ForegroundColor Yellow
if (-not (Test-Path "data\raw_data") -or ((Get-ChildItem "data\raw_data\*.csv" -ErrorAction SilentlyContinue).Count -eq 0)) {
    Write-Host "⚠️  ATENÇÃO: Arquivos CSV não encontrados em data\raw_data\" -ForegroundColor Yellow
    Write-Host "   Você pode fazer upload de dados personalizados na aplicação" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Deseja continuar mesmo assim? (s/n)"
    if ($response -ne "s" -and $response -ne "S") {
        Write-Host "Saindo..." -ForegroundColor Yellow
        exit 1
    }
} else {
    $csvCount = (Get-ChildItem "data\raw_data\*.csv").Count
    Write-Host "✅ $csvCount arquivo(s) CSV encontrado(s)" -ForegroundColor Green
}

# Verificar se streamlit_app_corrected.py existe
Write-Host ""
if (-not (Test-Path "streamlit_app_corrected.py")) {
    Write-Host "❌ streamlit_app_corrected.py não encontrado" -ForegroundColor Red
    exit 1
}

# Executar aplicação Streamlit
Write-Host ""
Write-Host "🚀 Iniciando aplicação Streamlit..." -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   A aplicação será aberta automaticamente no navegador    " -ForegroundColor Green
Write-Host "   URL: http://localhost:8501                               " -ForegroundColor Green
Write-Host "                                                            " -ForegroundColor Green
Write-Host "   Para parar a aplicação: Pressione Ctrl+C                " -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Start-Sleep -Seconds 2

# Executar Streamlit
streamlit run streamlit_app_corrected.py --server.port 8501 --server.headless true
