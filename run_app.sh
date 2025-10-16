#!/bin/bash

# Script automatizado para instalar dependências e executar a aplicação Streamlit
# Projet d'Analyse des Accidents de Trafic 2021-2025

echo "🚗 === Iniciando Aplicação de Análise de Acidentes de Trânsito ==="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado. Por favor, instale Python 3.8 ou superior.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION encontrado${NC}"
echo ""

# Criar diretório do projeto se não existir
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Verificar se ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
else
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe${NC}"
fi
echo ""

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualizar pip
echo "📦 Atualizando pip..."
python -m pip install --upgrade pip -q

# Instalar dependências
echo ""
echo "📥 Instalando dependências..."
echo "⏳ Isso pode levar alguns minutos na primeira execução..."
echo ""

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt -q
    echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
else
    echo -e "${RED}❌ Arquivo requirements.txt não encontrado${NC}"
    exit 1
fi

# Verificar se os dados existem
echo ""
echo "🔍 Verificando dados..."
if [ ! -d "data/raw_data" ] || [ -z "$(ls -A data/raw_data/*.csv 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠️  ATENÇÃO: Arquivos CSV não encontrados em data/raw_data/${NC}"
    echo -e "${YELLOW}   Você pode fazer upload de dados personalizados na aplicação${NC}"
    echo ""
    read -p "Deseja continuar mesmo assim? (s/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Saindo..."
        exit 1
    fi
else
    CSV_COUNT=$(ls -1 data/raw_data/*.csv 2>/dev/null | wc -l)
    echo -e "${GREEN}✅ $CSV_COUNT arquivo(s) CSV encontrado(s)${NC}"
fi

# Verificar se streamlit_app_corrected.py existe
echo ""
if [ ! -f "streamlit_app_corrected.py" ]; then
    echo -e "${RED}❌ streamlit_app_corrected.py não encontrado${NC}"
    exit 1
fi

# Executar aplicação Streamlit
echo ""
echo "🚀 Iniciando aplicação Streamlit..."
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   A aplicação será aberta automaticamente no navegador    ${NC}"
echo -e "${GREEN}   URL: http://localhost:8501                               ${NC}"
echo -e "${GREEN}                                                            ${NC}"
echo -e "${GREEN}   Para parar a aplicação: Pressione Ctrl+C                ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
sleep 2

# Executar Streamlit
streamlit run streamlit_app_corrected.py --server.port 8501 --server.headless true

# Desativar ambiente virtual ao sair
deactivate
