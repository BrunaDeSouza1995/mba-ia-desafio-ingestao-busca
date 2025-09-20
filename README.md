Este projeto foi desenvolvido como parte do desafio MBA Engenharia de Software com IA - Full Cycle.

---
# Ingestão e Busca Semântica com LangChain e PostgreSQL

## 📋 Objetivo

Este projeto implementa um sistema de **ingestão e busca semântica** que permite:

- **Ingestão**: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector
- **Busca**: Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.8+
- **Framework**: LangChain
- **Banco de Dados**: PostgreSQL + pgVector
- **Containerização**: Docker & Docker Compose
- **Embeddings**: HuggingFace (all-MiniLM-L6-v2)
- **LLM**: Google Gemini (gemini-2.5-flash)

## 💡 Decisões Técnicas

### Escolha do HuggingFace para Embeddings
Foi utilizado o modelo **HuggingFace (all-MiniLM-L6-v2)** para geração de embeddings por dois motivos principais:

1. **Problemas técnicos**: Rate limits encontrados com o Google Gemini durante o desenvolvimento
2. **Conhecimento adquirido**: O HuggingFace foi apresentado na disciplina **Fundamentos de IA Generativa**


Esta solução oferece:

- ✅ **Execução local**: Sem dependência de APIs externas
- ✅ **Sem rate limits**: Processamento ilimitado
- ✅ **Menor latência**: Não há chamadas de rede
- ✅ **Custo zero**: Não consome cota de API

## 📁 Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do PostgreSQL com pgVector
├── requirements.txt        # Dependências Python
├── .env.example           # Template das variáveis de ambiente
├── src/
│   ├── ingest.py          # Script de ingestão do PDF
│   ├── search.py          # Módulo de busca e prompt
│   └── chat.py            # CLI para interação com usuário
├── document.pdf           # PDF para ingestão
└── README.md             # Este arquivo
```

## 🚀 Pré-requisitos

### 1. Software Necessário

- **Python 3.8+**
- **Docker** e **Docker Compose**
- **Git**

### 2. Chave de API

Você precisa apenas da chave de API do Google Gemini:

#### Google Gemini (Obrigatório)
1. Acesse [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Crie uma nova API Key

## ⚙️ Configuração do Ambiente

### 1. Clone o Repositório

```bash
git clone https://github.com/BrunaDeSouza1995/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie e Ative o Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# No macOS/Linux:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas chaves de API
nano .env
```

**Configuração do arquivo `.env`:**

```env
# Chave de API do Google Gemini (obrigatória)
GOOGLE_API_KEY=sua_chave_google_aqui

# Configuração do Banco de Dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=pdf_documents

# Caminho do PDF
PDF_PATH=document.pdf
```

## 🚀 Execução do Projeto

### 1. Inicie o Banco de Dados

```bash
# Subir o PostgreSQL com pgVector
docker compose up -d

# Verificar se os containers estão rodando
docker compose ps
```

**Aguarde alguns segundos** para que o banco de dados seja totalmente inicializado.

### 2. Execute a Ingestão do PDF

```bash
# Processar e armazenar o PDF no banco vetorial
python src/ingest.py
```

**Nota**: Se não houver erros, o script termina sem mensagens. Para verificar se funcionou, execute o chat em seguida.

### 3. Execute o Chat (Perguntas Pré-definidas)

```bash
# Executar perguntas de exemplo
python src/chat.py
```

**Nota**: O chat atual executa perguntas pré-definidas automaticamente.

## 💬 Exemplos de Uso

O chat executa as seguintes perguntas pré-definidas:

### Pergunta 1
```
PERGUNTA: Qual o faturamento da Empresa Prata Energia S.A.?
RESPOSTA: [Resposta baseada no conteúdo do PDF ou "Não tenho informações necessárias para responder sua pergunta."]
```

### Pergunta 2
```
PERGUNTA: Quantos clientes a Empresa Prata Energia S.A. tem em 2025?
RESPOSTA: [Resposta baseada no conteúdo do PDF ou "Não tenho informações necessárias para responder sua pergunta."]
```

## 🔧 Funcionalidades Implementadas

### Ingestão (`src/ingest.py`)
- ✅ Carregamento de PDF usando `PyPDFLoader`
- ✅ Divisão em chunks de 1000 caracteres com overlap de 150
- ✅ Geração de embeddings com HuggingFace (modelo local)
- ✅ Armazenamento no PostgreSQL com pgVector

### Busca (`src/search.py`)
- ✅ Template de prompt estruturado
- ✅ Regras para respostas baseadas apenas no contexto
- ✅ Tratamento de perguntas fora do escopo

### Chat (`src/chat.py`)
- ✅ Execução de perguntas pré-definidas
- ✅ Busca semântica com k=10 resultados mais relevantes
- ✅ Integração com Google Gemini para geração de respostas
- ✅ Formatação clara das respostas