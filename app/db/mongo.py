from pymongo import MongoClient
from app.core.config import MONGO_URL, DB_NAME

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
tabelas_collection = db["schemas"]