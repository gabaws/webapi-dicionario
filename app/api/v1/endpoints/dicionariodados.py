from fastapi import APIRouter, HTTPException, UploadFile, Form, Body, File
from typing import Dict, List
from app.models.schemas import Column
from app.models.connectors import Connector
from app.db import crud
import json
from pydantic import parse_obj_as

router = APIRouter()

SCHEMA_NAO_ENCONTRADO = "Schema não encontrado"
COLUNA_NAO_ENCONTRADA = "Coluna não encontrada"
ARQUIVO_INVALIDO = "Apenas arquivos .json são permitidos"
JSON_INVALIDO = "JSON inválido"
CONECTOR_INVALIDO = "Conector inválido ou falha ao testar conexão"

def serialize_tables(tables: Dict[str, List[Column]]) -> Dict[str, List[dict]]:
    return {
        table_name: [col.dict() for col in columns]
        for table_name, columns in tables.items()
    }

# --- SCHEMAS ---

@router.post("/schemas/", summary="Criar novo schema completo via upload JSON")
async def criar_schema(
    arquivo_dicionario: UploadFile,
    nome_schema: str = Form(...)
):
    if not arquivo_dicionario.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail=ARQUIVO_INVALIDO)

    conteudo = await arquivo_dicionario.read()
    try:
        json_data = json.loads(conteudo)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=JSON_INVALIDO)

    try:
        tables = parse_obj_as(Dict[str, List[Column]], json_data)
        serialized_tables = serialize_tables(tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de validação do schema: {str(e)}")

    doc = {
        "nome_schema": nome_schema,
        "tabelas": serialized_tables
    }

    inserted_id = crud.insert_schema(doc)
    return {"id": inserted_id}

@router.get("/schemas/{nome_schema}", summary="Obter schema completo pelo nome")
def obter_schema(nome_schema: str):
    schema = crud.get_schema_por_nome(nome_schema)
    if not schema:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    schema["_id"] = str(schema["_id"])
    return schema

@router.put("/schemas/{nome_schema}", summary="Atualizar schema completo via Upload JSON")
async def atualizar_schema_por_upload(
    nome_schema: str,
    arquivo_dicionario: UploadFile = File(...),
    novo_nome_schema: str = Form(None)
):
    if not arquivo_dicionario.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail=ARQUIVO_INVALIDO)

    conteudo = await arquivo_dicionario.read()
    try:
        json_data = json.loads(conteudo)
        tables = parse_obj_as(Dict[str, List[Column]], json_data)
        serialized_tables = serialize_tables(tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(e)}")

    update_doc = {"tabelas": serialized_tables}
    if novo_nome_schema:
        update_doc["nome_schema"] = novo_nome_schema

    atualizado = crud.update_schema(nome_schema, update_doc)
    if not atualizado:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)

    return {"message": "Atualizado com sucesso"}

@router.delete("/schemas/{nome_schema}", summary="Deletar schema pelo nome")
def deletar_schema(nome_schema: str):
    deletado = crud.delete_schema(nome_schema)
    if not deletado:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    return {"message": "Schema deletado com sucesso"}

@router.patch("/schemas/{nome_schema}/{nome_tabela}/{nome_coluna}", summary="Atualizar coluna de tabela")
async def atualizar_coluna(
    nome_schema: str,
    nome_tabela: str,
    nome_coluna: str,
    nova_coluna: Column = Body(...)
):
    atualizado = crud.update_coluna_schema(nome_schema, nome_tabela, nome_coluna, nova_coluna.dict())
    if not atualizado:
        raise HTTPException(status_code=404, detail=COLUNA_NAO_ENCONTRADA)
    return {"message": f"Coluna '{nome_coluna}' atualizada com sucesso na tabela '{nome_tabela}'"}

# --- CONNECTORS ---

@router.post("/connectors/", summary="Cadastrar novo conector de banco de dados")
def criar_conector(conector: Connector):
    if not conector.testa_conexao():
        raise HTTPException(status_code=400, detail=CONECTOR_INVALIDO)
    
    inserted_id = crud.insert_conector(conector.dict())
    return {"id": inserted_id}

@router.get("/connectors/", summary="Listar conectores existentes")
def listar_conectores():
    return crud.get_conectores()

@router.get("/connectors/{nome}", summary="Buscar conector pelo nome")
def obter_conector_por_nome(nome: str):
    conector = crud.get_conector_por_nome(nome)
    if not conector:
        raise HTTPException(status_code=404, detail="Conector não encontrado")
    conector["_id"] = str(conector["_id"])
    return conector
