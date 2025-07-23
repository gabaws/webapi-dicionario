from fastapi import APIRouter, HTTPException, UploadFile, File, Body, Form, Depends
from typing import List, Dict, Any
from app.models.domain.schemas import Column
from app.models.responses import MessageResponse
from app.db.mongo import tabelas_collection
from app.db.crud import schemas as crud
from app.services.schema_service import validar_schema_json
import json
import logging

router = APIRouter()
logger = logging.getLogger("schemas")

SCHEMA_NAO_ENCONTRADO = "Schema não encontrado"


def get_collection():
    return tabelas_collection

def _parse_upload_file(file: UploadFile) -> dict:
    try:
        conteudo_bytes = file.file.read()
        return json.loads(conteudo_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {str(e)}")

def _validar_e_inserir_schema(conteudo: dict, nome_schema: str, collection):
    conteudo["nome_schema"] = nome_schema
    if not validar_schema_json(conteudo):
        raise HTTPException(status_code=400, detail="JSON inválido")
    crud.insert_schema(conteudo, collection)

@router.post("/schemas/upload", response_model=MessageResponse)
def cadastrar_schema_upload(
    nome_schema: str = Form(...),
    file: UploadFile = File(...),
    collection=Depends(get_collection)
):
    """
    Faz upload e cadastro de um novo schema JSON.
    """
    conteudo = _parse_upload_file(file)
    _validar_e_inserir_schema(conteudo, nome_schema, collection)
    logger.info(f"Schema '{nome_schema}' cadastrado com sucesso.")
    return {"message": "Schema enviado com sucesso"}

@router.put("/schemas/{nome_schema}", response_model=MessageResponse)
def atualizar_schema(
    nome_schema: str,
    file: UploadFile = File(...),
    collection=Depends(get_collection)
):
    """
    Atualiza um schema existente via upload de arquivo JSON.
    """
    conteudo = _parse_upload_file(file)
    conteudo["nome_schema"] = nome_schema
    if not validar_schema_json(conteudo):
        raise HTTPException(status_code=400, detail="JSON inválido")
    atualizado = crud.update_schema(nome_schema, conteudo, collection)
    if not atualizado:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    logger.info(f"Schema '{nome_schema}' atualizado com sucesso.")
    return {"message": "Schema atualizado com sucesso"}

@router.delete("/schemas/{nome_schema}", response_model=MessageResponse)
def remover_schema(nome_schema: str, collection=Depends(get_collection)):
    """
    Remove um schema pelo nome.
    """
    removido = crud.delete_schema(nome_schema, collection)
    if not removido:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    logger.info(f"Schema '{nome_schema}' removido com sucesso.")
    return {"message": "Schema removido com sucesso"}

@router.patch("/schemas/{nome_schema}/tabelas/{tabela}", response_model=MessageResponse)
def atualizar_tabela_schema(
    nome_schema: str,
    tabela: str,
    colunas: List[Column] = Body(...),
    collection=Depends(get_collection)
):
    """
    Atualiza as colunas de uma tabela específica dentro de um schema.
    """
    atualizado = crud.patch_tabela(nome_schema, tabela, [c.dict() for c in colunas], collection)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Tabela ou schema não encontrado")
    logger.info(f"Tabela '{tabela}' do schema '{nome_schema}' atualizada.")
    return {"message": "Tabela atualizada com sucesso"}

@router.get("/schemas/", response_model=List[Dict[str, Any]])
def listar_schemas(collection=Depends(get_collection)):
    """
    Lista todos os schemas cadastrados.
    """
    return crud.get_schemas(collection)

@router.get("/schemas/{nome_schema}", response_model=Dict[str, Any])
def obter_schema(nome_schema: str, collection=Depends(get_collection)):
    """
    Obtém um schema específico pelo nome.
    """
    schema = crud.get_schema_por_nome(nome_schema, collection)
    if not schema:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    return schema
