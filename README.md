# 🚀 API Dicionário de Dados

> ✨ **Sistema de Gerenciamento de Conectores e Schemas de Banco de Dados**

Uma API REST moderna construída com FastAPI para gerenciar conectores de banco de dados PostgreSQL e schemas de dados de forma segura e eficiente.

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

## 🎯 Sobre o Projeto

Esta aplicação é um **Dicionário de Dados** que permite:

- 🔌 **Gerenciar Conectores**: Cadastrar, testar e gerenciar conexões com bancos PostgreSQL
- 📊 **Gerenciar Schemas**: Upload, validação e gestão de schemas de dados em formato JSON
- 🔒 **Segurança**: Criptografia de senhas e validação de dados
- 📝 **Documentação Automática**: Swagger/OpenAPI integrado
- 🗄️ **Persistência**: Armazenamento em MongoDB

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
└── 📖 README.md                   # Este arquivo
```

## 🚀 Como Executar

### 📋 Pré-requisitos

- Python 3.8 ou superior
- MongoDB instalado e rodando
- PostgreSQL (para testes de conexão)

### 🔧 Instalação

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
MONGO_URL=mongodb://localhost:27017
DB_NAME=dicionario_dados
MONGO_COLLECTION_SCHEMAS=schemas
MONGO_COLLECTION_CONECTORES=conectores
CRYPTO_KEY=sua_chave_secreta_aqui
```

6. **Execute a aplicação**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- 📖 **Swagger UI**: http://localhost:8000/docs
- 📄 **ReDoc**: http://localhost:8000/redoc

### 🔌 Endpoints de Conectores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/dicionariodados/connectors/test` | Testa conexão com PostgreSQL |
| `POST` | `/dicionariodados/connectors/` | Cadastra novo conector |
| `GET` | `/dicionariodados/connectors/` | Lista todos os conectores |
| `GET` | `/dicionariodados/connectors/{nome}` | Busca conector por nome |
| `PUT` | `/dicionariodados/connectors/{nome}` | Atualiza conector |
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

## 🔧 Configuração

### 🔐 Variáveis de Ambiente

```env
# MongoDB
MONGO_URL=mongodb://localhost:27017
DB_NAME=dicionario_dados
MONGO_COLLECTION_SCHEMAS=schemas
MONGO_COLLECTION_CONECTORES=conectores

# Criptografia
CRYPTO_KEY=sua_chave_secreta_aqui
```

## 📁 Estrutura Detalhada do Projeto

### 🚀 **app/main.py**
- Ponto de entrada da aplicação FastAPI
- Configuração de rotas e documentação
- Redirecionamento automático para `/docs`

### 📁 **app/api/v1/endpoints/**
- **connectors.py**: Endpoints para gerenciamento de conectores
- **schemas.py**: Endpoints para gerenciamento de schemas

### 📁 **app/core/**
- **config.py**: Configurações da aplicação
- **logging.py**: Configuração de logs

### 📁 **app/db/**
- **mongo.py**: Conexão com MongoDB
- **crud/**: Operações de banco de dados
  - **connectors.py**: CRUD para conectores
  - **schemas.py**: CRUD para schemas

### 📁 **app/models/**
- **domain/**: Modelos de domínio
  - **connectors.py**: Modelos para conectores
  - **schemas.py**: Modelos para schemas
- **responses.py**: Modelos de resposta da API

### 📁 **app/services/**
- **connector_service.py**: Lógica de teste de conexão PostgreSQL
- **schema_service.py**: Validação de schemas JSON

### 📁 **app/utils/**
- **crypto.py**: Criptografia de senhas
- **json_validator.py**: Validação de JSON

## 🔐 Segurança

### 🔒 Criptografia de Senhas
- Utiliza **Fernet** (cryptography) para criptografia
- Senhas são criptografadas antes de salvar no banco
- Chave de criptografia configurável via variável de ambiente

### ✅ Validação de Dados
- **Pydantic** para validação de entrada
- Validação de formato de host (IP ou domínio)
- Validação de schemas JSON
- Sanitização de dados

## 🧪 Funcionalidades

### 🔌 **Gerenciamento de Conectores**
- ✅ Cadastro de conectores PostgreSQL
- ✅ Teste de conexão em tempo real
- ✅ Validação de credenciais
- ✅ Criptografia de senhas
- ✅ CRUD completo (Create, Read, Update, Delete)

### 📊 **Gerenciamento de Schemas**
- ✅ Upload de schemas via arquivo JSON
- ✅ Validação de estrutura JSON
- ✅ Gerenciamento de tabelas e colunas
- ✅ Suporte a chaves primárias e estrangeiras
- ✅ Constraints e descrições

### 🔍 **Recursos Adicionais**
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Logs estruturados
- ✅ Tratamento de erros
- ✅ Validação de entrada
- ✅ Respostas padronizadas

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
- 📧 Email: [seu-email@exemplo.com]
- 🔗 LinkedIn: [seu-linkedin]
- 🐙 GitHub: [seu-github]

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!** ⭐