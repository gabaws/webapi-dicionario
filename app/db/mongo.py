from pymongo import MongoClient
from app.core.config import MONGO_URL, DB_NAME, COLLECTION_SCHEMAS, COLLECTION_CONECTORES, COLLECTION_DADOS_SINTETICOS
from app.core.logging import logger

try:
    client = MongoClient(MONGO_URL)
    # Testa conexão
    client.admin.command('ping')
    logger.info("✅ MongoDB connection established successfully")
except Exception as e:
    logger.error(f"❌ Failed to connect to MongoDB: {e}")
    raise

db = client[DB_NAME]

tabelas_collection = db[COLLECTION_SCHEMAS]
conectores_collection = db[COLLECTION_CONECTORES]

dados_sinteticos_collection = db[COLLECTION_DADOS_SINTETICOS]