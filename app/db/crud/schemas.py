from pymongo.collection import Collection
from typing import Dict, List, Optional

def insert_schema(schema_doc: Dict, collection: Collection) -> str:
    result = collection.insert_one(schema_doc)
    return str(result.inserted_id)

def get_schemas(collection: Collection) -> List[Dict]:
    schemas = list(collection.find({}))
    for schema in schemas:
        schema.pop("_id", None)
    return schemas

def get_schema_por_nome(nome_schema: str, collection: Collection) -> Optional[Dict]:
    schema = collection.find_one({"nome_schema": nome_schema})
    if schema:
        schema.pop("_id", None)
    return schema

def update_schema(nome_schema: str, novos_dados: Dict, collection: Collection) -> bool:
    result = collection.update_one({"nome_schema": nome_schema}, {"$set": novos_dados})
    return result.modified_count > 0

def delete_schema(nome_schema: str, collection: Collection) -> bool:
    result = collection.delete_one({"nome_schema": nome_schema})
    return result.deleted_count > 0

def patch_tabela(nome_schema: str, tabela: str, colunas: List[Dict], collection: Collection) -> bool:
    filtro = {"nome_schema": nome_schema}
    update = {"$set": {f"tabelas.{tabela}": colunas}}
    result = collection.update_one(filtro, update)
    return result.modified_count > 0
