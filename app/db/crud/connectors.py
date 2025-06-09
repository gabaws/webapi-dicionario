from pymongo.collection import Collection
from typing import Dict, List, Optional

def insert_conector(conector: Dict, collection: Collection) -> str:
    result = collection.insert_one(conector)
    return str(result.inserted_id)

def get_conectores(collection: Collection) -> List[Dict]:
    return list(collection.find({}))

def get_conector_por_nome(nome: str, collection: Collection) -> Optional[Dict]:
    return collection.find_one({"nome": nome})

def update_conector(nome: str, novos_dados: Dict, collection: Collection) -> bool:
    result = collection.update_one({"nome": nome}, {"$set": novos_dados})
    return result.modified_count > 0

def delete_conector(nome: str, collection: Collection) -> bool:
    result = collection.delete_one({"nome": nome})
    return result.deleted_count > 0