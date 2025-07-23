from fastapi import APIRouter, HTTPException, Depends
from app.models.domain.connectors import ConnectorIn, ConnectorOut
from app.models.responses import MessageResponse, ConnectorCreateResponse
from app.db.mongo import conectores_collection
from app.db.crud import connectors as crud
from app.services.connector_service import testar_conexao_postgres
from app.utils.crypto import encrypt_password
from app.core.logging import logger
from typing import List

router = APIRouter()

CONECTOR_NAO_ENCONTRADO = "Conector não encontrado"


def get_collection():
    return conectores_collection

def _testar_conexao(conector: ConnectorIn, acao: str):
    logger.info(f"🔍 Testando conexão antes de {acao} conector '{conector.nome}'")
    try:
        if not testar_conexao_postgres(conector):
            raise HTTPException(
                status_code=400,
                detail="❌ Falha no teste de conexão. Verifique os dados fornecidos."
            )
        logger.info(f"✅ Teste de conexão bem-sucedido para '{conector.nome}'")
    except Exception as e:
        logger.error(f"❌ Erro no teste de conexão para '{conector.nome}': {e}")
        raise HTTPException(
            status_code=400,
            detail=f"❌ Erro na conexão: {str(e)}"
        )

def _remover_campos_sensiveis(conector: dict) -> dict:
    conector = dict(conector)
    conector.pop("_id", None)
    conector.pop("senha", None)
    return conector

@router.post("/connectors/", response_model=ConnectorCreateResponse)
def cadastrar_conector(conector: ConnectorIn, collection=Depends(get_collection)):
    """
    Cadastra um novo conector PostgreSQL.
    IMPORTANTE: Testa a conexão automaticamente antes de cadastrar.
    Se a conexão falhar, o cadastro não será realizado.
    """
    conector_existente = crud.get_conector_por_nome(conector.nome, collection)
    if conector_existente:
        raise HTTPException(
            status_code=400,
            detail=f"Já existe um conector com o nome '{conector.nome}'"
        )
    _testar_conexao(conector, "cadastrar")
    try:
        doc = conector.dict()
        doc["senha"] = encrypt_password(doc["senha"])
        crud.insert_conector(doc, collection)
        logger.info(f"✅ Conector '{conector.nome}' cadastrado com sucesso")
        return ConnectorCreateResponse(
            success=True,
            message="✅ Conector cadastrado com sucesso!",
            connector_name=conector.nome,
            connection_tested=True
        )
    except Exception as e:
        logger.error(f"❌ Erro ao cadastrar conector '{conector.nome}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao cadastrar conector: {str(e)}"
        )

@router.get("/connectors/", response_model=List[ConnectorOut])
def listar_conectores(collection=Depends(get_collection)):
    """
    Lista todos os conectores cadastrados
    """
    conectores = crud.get_conectores(collection)
    return [_remover_campos_sensiveis(c) for c in conectores]

@router.get("/connectors/{nome}", response_model=ConnectorOut)
def buscar_conector(nome: str, collection=Depends(get_collection)):
    """
    Busca um conector específico pelo nome
    """
    conector = crud.get_conector_por_nome(nome, collection)
    if not conector:
        raise HTTPException(status_code=404, detail=CONECTOR_NAO_ENCONTRADO)
    return _remover_campos_sensiveis(conector)

@router.put("/connectors/{nome}", response_model=MessageResponse)
def atualizar_conector(nome: str, conector: ConnectorIn, collection=Depends(get_collection)):
    """
    Atualiza um conector existente.
    IMPORTANTE: Testa a conexão automaticamente antes de atualizar.
    """
    conector_existente = crud.get_conector_por_nome(nome, collection)
    if not conector_existente:
        raise HTTPException(status_code=404, detail=CONECTOR_NAO_ENCONTRADO)
    _testar_conexao(conector, "atualizar")
    try:
        doc = conector.dict()
        doc["senha"] = encrypt_password(doc["senha"])
        atualizado = crud.update_conector(nome, doc, collection)
        if atualizado:
            logger.info(f"✅ Conector '{nome}' atualizado com sucesso")
            return {"message": "✅ Conector atualizado com sucesso!"}
        else:
            raise HTTPException(status_code=500, detail="Erro ao atualizar conector")
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar conector '{nome}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao atualizar conector: {str(e)}"
        )

@router.delete("/connectors/{nome}", response_model=MessageResponse)
def remover_conector(nome: str, collection=Depends(get_collection)):
    """
    Remove um conector pelo nome
    """
    removido = crud.delete_conector(nome, collection)
    if not removido:
        raise HTTPException(status_code=404, detail=CONECTOR_NAO_ENCONTRADO)
    logger.info(f"✅ Conector '{nome}' removido com sucesso")
    return {"message": "✅ Conector removido com sucesso!"}
