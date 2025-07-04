from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "dicionario_dados")
COLLECTION_SCHEMAS = os.getenv("MONGO_COLLECTION_SCHEMAS", "schemas")
COLLECTION_CONECTORES = os.getenv("MONGO_COLLECTION_CONECTORES", "conectores")