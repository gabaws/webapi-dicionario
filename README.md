# 🚀 API Dicionário de Dados

> ✨ **Sistema de Gerenciamento de Conectores, Schemas e Geração de Dados Sintéticos**

Uma API REST moderna construída com FastAPI para gerenciar conectores de banco de dados PostgreSQL, schemas de dados e gerar dados sintéticos de forma segura e eficiente.

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [🏗️ Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [🚀 Como Executar](#-como-executar)
- [📚 Documentação da API](#-documentação-da-api)
- [🔧 Configuração](#-configuração)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🔐 Segurança](#-segurança)
- [🧪 Funcionalidades](#-funcionalidades)
- [🏥 Monitoramento](#-monitoramento)

## 🎯 Sobre o Projeto

Esta aplicação é um **Dicionário de Dados Avançado** que permite:

- 🔌 **Gerenciar Conectores**: Cadastrar, testar e gerenciar conexões com bancos PostgreSQL
- 📊 **Gerenciar Schemas**: Upload, validação e gestão de schemas de dados em formato JSON
- 🎲 **Gerar Dados Sintéticos**: Criação automática de dados fake baseados nos schemas
- 🔒 **Segurança**: Criptografia de senhas e validação robusta de dados
- 📝 **Documentação Automática**: Swagger/OpenAPI integrado
- 🗄️ **Persistência**: Armazenamento em MongoDB com validação de conexão
- 🏥 **Monitoramento**: Health checks e logs estruturados

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| 🐍 **Python** | 3.8+ | Linguagem principal |
| ⚡ **FastAPI** | Latest | Framework web moderno |
| 🗄️ **MongoDB** | - | Banco de dados NoSQL |
| 🐘 **PostgreSQL** | - | Banco de dados relacional |
| 🔐 **Cryptography** | - | Criptografia de senhas |
| 📋 **Pydantic** | - | Validação de dados |
| 🎨 **Uvicorn** | - | Servidor ASGI |
| 📄 **JSON Schema** | - | Validação de schemas |
| 🎲 **Faker** | - | Geração de dados sintéticos |

## 🏗️ Arquitetura do Projeto

```
webapi-dicionario/
├── 📁 app/
│   ├── 🚀 main.py                 # Ponto de entrada da aplicação
│   ├── 📁 api/                    # Camada de API
│   │   └── 📁 v1/endpoints/       # Endpoints da API
│   ├── 📁 core/                   # Configurações centrais
│   ├── 📁 db/                     # Camada de dados
│   │   └── 📁 crud/               # Operações CRUD
│   ├── 📁 models/                 # Modelos de dados
│   │   └── 📁 domain/             # Modelos de domínio
│   ├── 📁 services/               # Lógica de negócio
│   └── 📁 utils/                  # Utilitários
├── 📄 requirements.txt            # Dependências Python
├── 📄 .env                        # Variáveis de ambiente
├── 📁 logs/                       # Logs da aplicação
└── 📖 README.md                   # Este arquivo
```

## 🚀 Como Executar

### 🐳 **Usando Docker Compose (Recomendado)**

#### 📋 Pré-requisitos
- Docker e Docker Compose instalados
- Git

#### 🔧 Instalação Rápida

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd webapi-dicionario
```

#### 🛠️ Comandos Docker Compose

```bash
# Iniciar aplicação
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Parar aplicação
docker-compose down

# Ver status
docker-compose ps

# Reiniciar
docker-compose restart
```

### 🐍 **Execução Local (Desenvolvimento)**

#### 📋 Pré-requisitos
- Python 3.8 ou superior
- MongoDB instalado e rodando
- PostgreSQL (para testes de conexão)

#### 🔧 Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd webapi-dicionario
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente**
```bash
# Crie um arquivo .env na raiz do projeto
MONGO_URL=mongodb://root:example@localhost:27017/
DB_NAME=dicionario_dados
MONGO_COLLECTION_SCHEMAS=schemas
MONGO_COLLECTION_CONECTORES=conectores
MONGO_COLLECTION_DADOS_SINTETICOS=dados_sinteticos
CRYPTO_KEY=sua_chave_secreta_aqui_minimo_32_caracteres
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- 📖 **Swagger UI**: http://localhost:8000/docs
- 📄 **ReDoc**: http://localhost:8000/redoc

### 🏥 Health Check 

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/hc` | Status da aplicação e conexão com MongoDB |

### 🔌 Endpoints de Conectores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/dicionariodados/connectors/` | Cadastra novo conector (testa conexão automaticamente) |
| `GET` | `/dicionariodados/connectors/` | Lista todos os conectores |
| `GET` | `/dicionariodados/connectors/{nome}` | Busca conector por nome |
| `PUT` | `/dicionariodados/connectors/{nome}` | Atualiza conector (testa conexão automaticamente) |
| `DELETE` | `/dicionariodados/connectors/{nome}` | Remove conector |

### 📊 Endpoints de Schemas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/dicionariodados/schemas/upload` | Upload de schema via arquivo |
| `PUT` | `/dicionariodados/schemas/{nome_schema}` | Atualiza schema |
| `DELETE` | `/dicionariodados/schemas/{nome_schema}` | Remove schema |
| `PATCH` | `/dicionariodados/schemas/{nome_schema}/tabelas/{tabela}` | Atualiza tabela específica |
| `GET` | `/dicionariodados/schemas/` | Lista todos os schemas |
| `GET` | `/dicionariodados/schemas/{nome_schema}` | Obtém schema específico |

### 🎲 Endpoints de Geração de Dados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/dicionariodados/gerar-dados/{nome_schema}` | Gera e insere dados sintéticos |

## 🔧 Configuração

### 🐳 **Docker Compose**

A aplicação inclui configuração completa do Docker Compose com:

- **MongoDB**: Banco de dados principal
- **PostgreSQL**: Para testes de conexão
- **FastAPI**: Aplicação principal
- **Health Checks**: Monitoramento automático
- **Volumes**: Persistência de dados

#### 📁 Arquivos Docker
- `docker-compose.yaml`: Configuração dos serviços
- `Dockerfile`: Build da aplicação
- `.dockerignore`: Otimização da build
- `docker-run.sh`: Script de gerenciamento (Linux/Mac)
- `docker-run.ps1`: Script de gerenciamento (Windows)

### 🔐 Variáveis de Ambiente

```env
# MongoDB
MONGO_URL=mongodb://root:example@localhost:27017/
DB_NAME=dicionario_dados
MONGO_COLLECTION_SCHEMAS=schemas
MONGO_COLLECTION_CONECTORES=conectores
MONGO_COLLECTION_DADOS_SINTETICOS=dados_sinteticos

# Criptografia (OBRIGATÓRIO)
CRYPTO_KEY=sua_chave_secreta_aqui_minimo_32_caracteres
```

### 🔑 Gerando Chave Criptográfica

Para gerar uma chave segura:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 📁 Estrutura Detalhada do Projeto

### 🚀 **app/main.py**
- Ponto de entrada da aplicação FastAPI
- Configuração de rotas e documentação
- Health check endpoint
- Redirecionamento automático para `/docs`

### 📁 **app/api/v1/endpoints/**
- **connectors.py**: Endpoints para gerenciamento de conectores
- **schemas.py**: Endpoints para gerenciamento de schemas
- **generate_data.py**: Endpoints para geração de dados sintéticos

### 📁 **app/core/**
- **config.py**: Configurações da aplicação com validação
- **logging.py**: Configuração de logs com rotação

### 📁 **app/db/**
- **mongo.py**: Conexão com MongoDB com tratamento de erros
- **crud/**: Operações de banco de dados
  - **connectors.py**: CRUD para conectores
  - **schemas.py**: CRUD para schemas
  - **dados_sinteticos.py**: CRUD para dados sintéticos

### 📁 **app/models/**
- **domain/**: Modelos de domínio
  - **connectors.py**: Modelos para conectores
  - **schemas.py**: Modelos para schemas
- **responses.py**: Modelos de resposta da API

### 📁 **app/services/**
- **connector_service.py**: Lógica de teste de conexão PostgreSQL
- **schema_service.py**: Validação de schemas JSON
- **data_generation.py**: Geração de dados sintéticos

### 📁 **app/utils/**
- **crypto.py**: Criptografia de senhas com validação
- **json_validator.py**: Validação de JSON

## 🔐 Segurança

### 🔒 Criptografia de Senhas
- Utiliza **Fernet** (cryptography) para criptografia
- Senhas são criptografadas antes de salvar no banco
- Chave de criptografia obrigatória via variável de ambiente
- Validação de chave na inicialização

### ✅ Validação de Dados
- **Pydantic** para validação de entrada
- Validação de formato de host (IP ou domínio)
- Validação de schemas JSON
- Sanitização de dados

## 🏥 Monitoramento

### 📊 Health Check
- Endpoint `/health` para verificar status da aplicação
- Teste de conexão com MongoDB
- Status detalhado do sistema

### 📝 Logging
- Logs estruturados com rotação automática
- Arquivo de logs em `logs/app.log`
- Tamanho máximo de 5MB por arquivo
- Mantém 3 backups

### ⚠️ Tratamento de Erros
- Validação de configuração na inicialização
- Tratamento robusto de erros de conexão
- Logs informativos para debugging

## 🧪 Funcionalidades

### 🔌 **Gerenciamento de Conectores**
- ✅ Cadastro de conectores PostgreSQL com teste de conexão obrigatório
- ✅ Atualização com validação de conexão automática
- ✅ Validação de credenciais em tempo real
- ✅ Criptografia de senhas
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Verificação de duplicatas por nome
- ✅ Respostas detalhadas com status de conexão

### 📊 **Gerenciamento de Schemas**
- ✅ Upload de schemas via arquivo JSON
- ✅ Validação de estrutura JSON
- ✅ Gerenciamento de tabelas e colunas
- ✅ Suporte a chaves primárias e estrangeiras
- ✅ Constraints e descrições

### 🎲 **Geração de Dados Sintéticos**
- ✅ Geração automática de dados fake
- ✅ Baseado na estrutura dos schemas
- ✅ Inserção direta no PostgreSQL
- ✅ Geração de scripts SQL
- ✅ Persistência de scripts gerados

### 🔍 **Recursos Adicionais**
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Logs estruturados com rotação
- ✅ Health checks
- ✅ Tratamento robusto de erros
- ✅ Validação de entrada
- ✅ Respostas padronizadas

## 🚀 Exemplo de Uso

### 1. Cadastrar um Conector (teste automático obrigatório)
```bash
curl -X POST "http://localhost:8000/dicionariodados/connectors/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "meu_banco",
    "host": "localhost",
    "porta": 5432,
    "banco": "teste",
    "usuario": "postgres",
    "senha": "minha_senha"
  }'
```

### 2. Upload de Schema
```bash
curl -X POST "http://localhost:8000/dicionariodados/schemas/upload" \
  -F "nome_schema=meu_schema" \
  -F "file=@schema.json"
```

### 3. Gerar Dados Sintéticos
```bash
curl -X POST "http://localhost:8000/dicionariodados/gerar-dados/meu_schema?conector_nome=meu_banco&rows_per_table=100"
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Geração de Dados**
- 📧 Email: [gabrielterres199@gmail.com]
- 🐙 GitHub: [https://github.com/gabaws]
