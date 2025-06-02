## 🌐 WebAPI Dictionary

Esta Web API permite criar, atualizar, consultar e deletar schemas compostos por múltiplas tabelas e colunas, com persistência em um banco MongoDB. A interface é baseada em FastAPI e aceita uploads de arquivos JSON contendo a estrutura do schema.


🚀 Funcionalidades :

----------------------------------------------------------------------------------------------------------------------------

📥 **POST / – Criar novo schema via JSON**

Cria um schema completo a partir de um arquivo .json contendo o dicionário de dados.

📎 Entrada: Upload de arquivo .json + nome do schema (nome_schema)

✅ Validações: Verifica extensão, valida o JSON e estrutura esperada (Dict[str, List[Column]])

🧾 Persistência: Insere no MongoDB

🔁 Retorno: ID do documento criado

-----------------------------------------------------------------------------------------------------------------------------

🔍 **GET /{nome_schema} – Consultar schema**

Recupera um schema completo salvo no banco, identificado pelo seu nome_schema.

🔎 Busca pelo nome do schema

📤 Retorno: Estrutura do schema com suas tabelas e colunas

-----------------------------------------------------------------------------------------------------------------------------

📝 **PUT /{nome_schema} – Atualizar schema via JSON**

Atualiza um schema existente com um novo arquivo .json, podendo também renomeá-lo.

📎 Entrada: Upload de novo .json + (opcional) novo nome (novo_nome_schema)

🧪 Validação: Estrutura do JSON

🔁 Retorno: Mensagem de sucesso ou erro

-----------------------------------------------------------------------------------------------------------------------------

🗑️ **DELETE /{nome_schema} – Deletar schema**

Remove permanentemente um schema com base no nome_schema.

⚠️ Ação irreversível

✅ Retorno: Mensagem de confirmação

-----------------------------------------------------------------------------------------------------------------------------

🔧 **PATCH /{nome_schema}/{nome_tabela}/{nome_coluna} – Atualizar coluna específica**

Atualiza os dados de uma única coluna dentro de uma tabela específica em um schema.

🎯 Entrada: Objeto Column no body

🧠 Lógica: Substitui a coluna antiga pela nova

✅ Retorno: Confirmação de atualização

-----------------------------------------------------------------------------------------------------------------------------
```
.                                       # Raiz do projeto
├── README.md                           # Documento com instruções e informações do projeto
├── app                                 # Diretório principal da aplicação
│   ├── api                             # Camada de API da aplicação
│   │   ├── __init__.py                 # Torna o diretório um pacote Python
│   │   └── v1                          # Versão 1 da API (permite versionamento da API)
│   │       ├── __init__.py             # Inicializa o pacote da versão
│   │       └── endpoints               # Define os endpoints (rotas) da API
│   │           ├── __init__.py         # Inicializa o pacote de endpoints
│   │           └── dicionariodados.py  # Rotas para manipular o dicionário de dados (CRUD de schemas e colunas)
│   ├── core                            # Configurações centrais e utilitários da aplicação
│   │   ├── __init__.py                 # Inicializa o pacote
│   │   └── config.py                   # Importa as variaveis de ambiente
│   ├── db                              # Camada de acesso ao banco de dados
│   │   ├── __init__.py                 # Inicializa o pacote
│   │   ├── crud.py                     # Controla a inserção do esquema de tabelas (CRUD)
│   │   └── mongo.py                    # Gerencia a conexão com o banco de dados MongoDB
│   ├── main.py                         # Ponto de entrada da aplicação FastAPI
│   └── models                          # Modelos Pydantic usados para validação de dados
│       ├── __init__.py                 # Inicializa o pacote
│       └── schemas.py                  # Estrutura esperada dos dados (colunas de tabelas, etc.)
├── docker-compose.yaml                 # Arquivo de orquestração Docker (define os serviços e dependências)
├── requirements.txt                    # Lista de dependências Python do projeto (instaladas com pip)
├── sonar-project.properties            # Arquivo de configuração para análise de código com o SonarQube
└── tests                               # Testes automatizados para a API
    ├── __init__.py                     # Inicializa o pacote de testes
    ├── schema_atualizado.json          # Schema JSON usado em testes de atualização
    ├── schema_temp.json                # Schema JSON temporário usado em testes
    └── test_dicionariodados.py         # Testes dos endpoints do dicionário de dados

```
-----------------------------------------------------------------------------------------------------------------------------

## 🚀 Bibliotecas utilizadas na WebAPI 

### 1. **fastapi** ⚡  
Framework web moderno, rápido e leve para construir APIs RESTful com Python.  
**Papel na API:** Serve como base para criar rotas, manipular requisições HTTP, validar dados automaticamente com Pydantic e fornecer documentação automática da API.

### 2. **uvicorn[standard]** 🚀  
Servidor ASGI baseado em asyncio para rodar aplicações Python, especialmente FastAPI e Starlette.  
**Papel na API:** Executa a aplicação FastAPI em um servidor web assíncrono, possibilitando alta performance e suporte a operações concorrentes.

### 3. **pymongo** 🍃  
Driver oficial do MongoDB para Python, permitindo conexão e manipulação dos dados armazenados no MongoDB.  
**Papel na API:** Facilita o acesso, consulta, inserção, atualização e exclusão de documentos no banco de dados MongoDB.

### 4. **python-dotenv** 🌿  
Biblioteca para carregar variáveis de ambiente a partir de arquivos `.env`.  
**Papel na API:** Permite a configuração da aplicação via variáveis externas, como strings de conexão, chaves secretas e outras configurações sensíveis, sem expor diretamente no código.

### 5. **python-multipart** 📦  
Biblioteca para lidar com dados de formulários do tipo `multipart/form-data` em requisições HTTP, especialmente uploads de arquivos.  
**Papel na API:** Necessária para processar corretamente uploads de arquivos JSON, usados para criar e atualizar schemas via upload na API.

### 6. **pytest** 🧪  
Framework de testes para Python, utilizado para escrever e rodar testes automatizados.  
**Papel na API:** Utilizado para garantir que os endpoints da API funcionem conforme esperado, ajudando na manutenção e qualidade do código.

### 7. **pytest-asyncio** ⚙️  
Plugin do pytest que adiciona suporte para testar funções assíncronas (`async def`).  
**Papel na API:** Permite testar endpoints assíncronos do FastAPI, que usam async/await para maior desempenho.

### 8. **httpx** 🌐  
Cliente HTTP para Python com suporte a requisições síncronas e assíncronas.  
**Papel na API:** Usado nos testes para simular requisições HTTP contra a API, verificando o comportamento real dos endpoints.