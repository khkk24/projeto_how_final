# 🚀 Scripts de Execução Automatizada

Este diretório contém scripts automatizados para instalar dependências e executar a aplicação Streamlit de análise de acidentes de trânsito.

## 📋 Scripts Disponíveis

### 🐧 Linux / Mac
**Arquivo:** `run_app.sh`

```bash
# Tornar executável (primeira vez apenas)
chmod +x run_app.sh

# Executar
./run_app.sh
```

### 🪟 Windows

#### PowerShell (Recomendado)
**Arquivo:** `run_app.ps1`

```powershell
# Executar no PowerShell
.\run_app.ps1

# Se houver erro de política de execução, execute antes:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Prompt de Comando (CMD)
**Arquivo:** `run_app.bat`

```cmd
# Executar no CMD ou clicar duas vezes no arquivo
run_app.bat
```

## ⚙️ O que os scripts fazem?

1. ✅ **Verificam** se Python está instalado
2. ✅ **Criam** ambiente virtual (`.venv`) se não existir
3. ✅ **Ativam** o ambiente virtual
4. ✅ **Atualizam** o pip para a versão mais recente
5. ✅ **Instalam** todas as dependências do `requirements.txt`
6. ✅ **Verificam** a presença dos arquivos CSV de dados
7. ✅ **Executam** a aplicação Streamlit na porta 8501

## 🌐 Acesso à Aplicação

Após executar o script, a aplicação estará disponível em:
- **URL Local:** http://localhost:8501
- **URL de Rede:** http://[seu-ip]:8501

A aplicação abrirá automaticamente no navegador padrão.

## ⚠️ Requisitos

- **Python 3.8+** instalado no sistema
- **pip** (geralmente incluído com Python)
- Conexão com internet (primeira execução para baixar dependências)

## 📊 Sobre os Dados

Os scripts verificam se existem arquivos CSV em `data/raw_data/`. 

Se não houver dados:
- O script perguntará se deseja continuar
- Você poderá fazer upload de dados diretamente na aplicação Streamlit
- Use a barra lateral: "📁 Ou carregue um CSV personalizado"

## 🛑 Como Parar a Aplicação

Pressione `Ctrl + C` no terminal onde a aplicação está rodando.

## 🐛 Solução de Problemas

### Python não encontrado
```bash
# Linux/Mac
sudo apt install python3 python3-venv  # Debian/Ubuntu
brew install python                     # macOS

# Windows
# Baixe de: https://www.python.org/downloads/
```

### Erro de permissão (Linux/Mac)
```bash
chmod +x run_app.sh
```

### Erro de ExecutionPolicy (Windows PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Porta 8501 já em uso
```bash
# Matar processo na porta 8501
# Linux/Mac:
lsof -ti:8501 | xargs kill -9

# Windows:
netstat -ano | findstr :8501
taskkill /PID [número_do_pid] /F
```

## 📝 Logs e Depuração

Os scripts mostram mensagens coloridas indicando o progresso:
- 🟢 **Verde:** Sucesso
- 🟡 **Amarelo:** Avisos
- 🔴 **Vermelho:** Erros

## 🔄 Atualização de Dependências

Se o arquivo `requirements.txt` for atualizado, simplesmente execute o script novamente. Ele instalará as novas dependências automaticamente.

## 💡 Dicas

1. **Primera execução:** Pode levar alguns minutos para instalar todas as dependências
2. **Execuções seguintes:** Serão muito mais rápidas (apenas ativa o ambiente)
3. **Ambiente virtual:** Mantém as dependências isoladas do sistema
4. **Portabilidade:** Os scripts funcionam em qualquer diretório

## 🤝 Suporte

Para problemas ou dúvidas:
1. Verifique os requisitos acima
2. Consulte a seção de solução de problemas
3. Abra uma issue no GitHub do projeto

---

**Desenvolvido para o Projeto de Análise de Acidentes de Trânsito 2021-2025** 🚗
