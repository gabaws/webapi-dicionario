from fastapi import APIRouter, HTTPException, UploadFile, File, Body, Form
from typing import List, Dict, Any
from app.models.domain.schemas import Column
from app.models.responses import MessageResponse
from app.db.mongo import tabelas_collection
from app.db.crud import schemas as crud
from app.services.schema_service import validar_schema_json
import json

router = APIRouter()

@router.post("/schemas/upload", response_model=MessageResponse)
def cadastrar_schema_upload(nome_schema: str = Form(...), file: UploadFile = File(...)):
    try:
        conteudo_bytes = file.file.read()
        conteudo = json.loads(conteudo_bytes)
        conteudo["nome_schema"] = nome_schema

        if not validar_schema_json(conteudo):
            raise ValueError("JSON inválido")

        crud.insert_schema(conteudo, tabelas_collection)
        return {"message": "Schema enviado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/schemas/{nome_schema}", response_model=MessageResponse)
def atualizar_schema(nome_schema: str, file: UploadFile = File(...)):
    try:
        conteudo_bytes = file.file.read()
        conteudo = json.loads(conteudo_bytes)
        conteudo["nome_schema"] = nome_schema

        if not validar_schema_json(conteudo):
            raise ValueError("JSON inválido")

        atualizado = crud.update_schema(nome_schema, conteudo, tabelas_collection)
        if not atualizado:
            raise HTTPException(status_code=404, detail="Schema não encontrado")

        return {"message": "Schema atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/schemas/{nome_schema}", response_model=MessageResponse)
def remover_schema(nome_schema: str):
    removido = crud.delete_schema(nome_schema, tabelas_collection)
    if not removido:
        raise HTTPException(status_code=404, detail="Schema não encontrado")
    return {"message": "Schema removido com sucesso"}

@router.patch("/schemas/{nome_schema}/tabelas/{tabela}", response_model=MessageResponse)
def atualizar_tabela_schema(nome_schema: str, tabela: str, colunas: List[Column] = Body(...)):
    atualizado = crud.patch_tabela(nome_schema, tabela, [c.dict() for c in colunas], tabelas_collection)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Tabela ou schema não encontrado")
    return {"message": "Tabela atualizada com sucesso"}

@router.get("/schemas/", response_model=List[Dict[str, Any]])
def listar_schemas():
    return crud.get_schemas(tabelas_collection)

@router.get("/schemas/{nome_schema}", response_model=Dict[str, Any])
def obter_schema(nome_schema: str):
    schema = crud.get_schema_por_nome(nome_schema, tabelas_collection)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema não encontrado")
    return schema
