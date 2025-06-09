from fastapi import APIRouter, HTTPException
from app.models.domain.connectors import ConnectorIn, ConnectorOut
from app.models.responses import MessageResponse
from app.db.mongo import conectores_collection
from app.db.crud import connectors as crud
from app.services.connector_service import testar_conexao_postgres
from app.utils.crypto import encrypt_password, decrypt_password
from app.core.logging import logger

router = APIRouter()

@router.post("/connectors/test")
def testar_conexao(conector: ConnectorIn):
    try:
        if testar_conexao_postgres(conector):
            return {"mensagem": "Conexão bem sucedida"}
    except Exception as e:
        logger.error(f"Erro na conexão: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/connectors/", response_model=ConnectorOut)
def cadastrar_conector(conector: ConnectorIn):
    if not testar_conexao_postgres(conector):
        raise HTTPException(status_code=400, detail="Não foi possível conectar com os dados fornecidos")

    doc = conector.dict()
    doc["senha"] = encrypt_password(doc["senha"])
    crud.insert_conector(doc, conectores_collection)
    logger.info(f"Conector '{conector.nome}' cadastrado com sucesso")
    return conector

@router.get("/connectors/", response_model=list[ConnectorOut])
def listar_conectores():
    conectores = crud.get_conectores(conectores_collection)
    for c in conectores:
        c.pop("_id", None)
        c.pop("senha", None)
    return conectores

@router.get("/connectors/{nome}", response_model=ConnectorOut)
def buscar_conector(nome: str):
    conector = crud.get_conector_por_nome(nome, conectores_collection)
    if not conector:
        raise HTTPException(status_code=404, detail="Conector não encontrado")
    conector.pop("_id", None)
    conector.pop("senha", None)
    return conector

@router.put("/connectors/{nome}", response_model=MessageResponse)
def atualizar_conector(nome: str, conector: ConnectorIn):
    doc = conector.dict()
    doc["senha"] = encrypt_password(doc["senha"])
    atualizado = crud.update_conector(nome, doc, conectores_collection)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Conector não encontrado")
    return {"message": "Conector atualizado com sucesso"}

@router.delete("/connectors/{nome}", response_model=MessageResponse)
def remover_conector(nome: str):
    removido = crud.delete_conector(nome, conectores_collection)
    if not removido:
        raise HTTPException(status_code=404, detail="Conector não encontrado")
    return {"message": "Conector removido com sucesso"}
