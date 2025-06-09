from pymongo import MongoClient
from app.core.config import MONGO_URL, DB_NAME, COLLECTION_SCHEMAS, COLLECTION_CONECTORES

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

tabelas_collection = db[COLLECTION_SCHEMAS]
conectores_collection = db[COLLECTION_CONECTORES]