from dotenv import load_dotenv
import os

load_dotenv()

# Validação de variáveis obrigatórias
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is required")

DB_NAME = os.getenv("DB_NAME", "dicionario_dados")
COLLECTION_SCHEMAS = os.getenv("MONGO_COLLECTION_SCHEMAS", "schemas")
COLLECTION_CONECTORES = os.getenv("MONGO_COLLECTION_CONECTORES", "conectores")
COLLECTION_DADOS_SINTETICOS = os.getenv("MONGO_COLLECTION_DADOS_SINTETICOS", "dados_sinteticos")