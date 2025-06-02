from pymongo.collection import Collection
from typing import Dict, List
from app.db.mongo import tabelas_collection

def insert_schema(schema: Dict[str, List[dict]], collection: Collection = tabelas_collection):
    documents = [{"table_name": table_name, "columns": columns} for table_name, columns in schema.items()]
    result = collection.insert_many(documents)
    return result.inserted_ids
