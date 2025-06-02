from pymongo.collection import Collection
from typing import Dict, List, Optional
from app.db.mongo import tabelas_collection, conectores_collection

# --------------------
# Schemas CRUD
# --------------------

def insert_schema(schema_doc: Dict, collection: Collection = tabelas_collection) -> str:
    result = collection.insert_one(schema_doc)
    return str(result.inserted_id)

def get_schemas(collection: Collection = tabelas_collection) -> List[Dict]:
    return list(collection.find({}))

def get_schema_por_nome(nome_schema: str, collection: Collection = tabelas_collection) -> Optional[Dict]:
    return collection.find_one({"nome_schema": nome_schema})

def update_schema(nome_schema: str, novos_dados: Dict, collection: Collection = tabelas_collection) -> bool:
    result = collection.update_one({"nome_schema": nome_schema}, {"$set": novos_dados})
    return result.modified_count > 0

def delete_schema(nome_schema: str, collection: Collection = tabelas_collection) -> bool:
    result = collection.delete_one({"nome_schema": nome_schema})
    return result.deleted_count > 0

def update_coluna_schema(nome_schema: str, nome_tabela: str, nome_coluna: str, nova_coluna: Dict, collection: Collection = tabelas_collection) -> bool:
    schema = collection.find_one({"nome_schema": nome_schema})
    if not schema:
        return False

    tabelas = schema.get("tabelas", {})
    colunas = tabelas.get(nome_tabela, [])

    for i, col in enumerate(colunas):
        if col.get("column") == nome_coluna:
            colunas[i] = nova_coluna
            break
    else:
        return False

    result = collection.update_one(
        {"nome_schema": nome_schema},
        {"$set": {f"tabelas.{nome_tabela}": colunas}}
    )
    return result.modified_count > 0

# --------------------
# Conectores CRUD
# --------------------

def insert_conector(conector: Dict, collection: Collection = conectores_collection) -> str:
    result = collection.insert_one(conector)
    return str(result.inserted_id)

def get_conectores(collection: Collection = conectores_collection) -> List[Dict]:
    return list(collection.find({}))

def get_conector_por_nome(nome: str, collection: Collection = conectores_collection) -> Optional[Dict]:
    return collection.find_one({"nome": nome})

def update_conector(nome: str, novos_dados: Dict, collection: Collection = conectores_collection) -> bool:
    result = collection.update_one({"nome": nome}, {"$set": novos_dados})
    return result.modified_count > 0

def delete_conector(nome: str, collection: Collection = conectores_collection) -> bool:
    result = collection.delete_one({"nome": nome})
    return result.deleted_count > 0
