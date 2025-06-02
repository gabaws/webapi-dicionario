from fastapi import APIRouter, HTTPException, UploadFile, Form, Body, File
from typing import Dict, List
from app.models.schemas import Column
from app.db.mongo import tabelas_collection
import json
from pydantic import parse_obj_as

router = APIRouter()

SCHEMA_NAO_ENCONTRADO = "Schema não encontrado"
COLUNA_NAO_ENCONTRADA = "Coluna não encontrada"
ARQUIVO_INVALIDO = "Apenas arquivos .json são permitidos"
JSON_INVALIDO = "JSON inválido"

def serialize_tables(tables: Dict[str, List[Column]]) -> Dict[str, List[dict]]:
    return {
        table_name: [col.dict() for col in columns]
        for table_name, columns in tables.items()
    }

@router.post("/", summary="Criar novo schema completo via upload JSON")
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de validação do schema: {str(e)}")

    serialized_tables = serialize_tables(tables)

    doc = {
        "nome_schema": nome_schema,
        "tabelas": serialized_tables
    }

    result = tabelas_collection.insert_one(doc)
    return {"id": str(result.inserted_id)}

@router.get("/{nome_schema}", summary="Obter schema completo pelo nome do schema")
def obter_schema(nome_schema: str):
    schema = tabelas_collection.find_one({"nome_schema": nome_schema})
    if not schema:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    schema["_id"] = str(schema["_id"])
    return schema

@router.put("/{nome_schema}", summary="Atualizar schema completo via Upload JSON")
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
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=JSON_INVALIDO)

    try:
        tables = parse_obj_as(Dict[str, List[Column]], json_data)
        serialized_tables = serialize_tables(tables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(e)}")

    update_doc = {"tabelas": serialized_tables}
    if novo_nome_schema:
        update_doc["nome_schema"] = novo_nome_schema

    result = tabelas_collection.update_one(
        {"nome_schema": nome_schema},
        {"$set": update_doc}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)

    return {"message": "Atualizado com sucesso"}

@router.delete("/{nome_schema}", summary="Deletar schema pelo nome")
def deletar_schema(nome_schema: str):
    result = tabelas_collection.delete_one({"nome_schema": nome_schema})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)
    return {"message": "Schema deletado com sucesso"}

@router.patch("/{nome_schema}/{nome_tabela}/{nome_coluna}", summary="Atualizar uma coluna específica de uma tabela")
async def atualizar_coluna(
    nome_schema: str,
    nome_tabela: str,
    nome_coluna: str,
    nova_coluna: Column = Body(...)
):
    schema = tabelas_collection.find_one({"nome_schema": nome_schema})
    if not schema:
        raise HTTPException(status_code=404, detail=SCHEMA_NAO_ENCONTRADO)

    tabelas = schema.get("tabelas", {})
    colunas = tabelas.get(nome_tabela, [])

    for i, col in enumerate(colunas):
        if col["column"] == nome_coluna:
            colunas[i] = nova_coluna.dict()
            break
    else:
        raise HTTPException(status_code=404, detail=COLUNA_NAO_ENCONTRADA)

    tabelas_collection.update_one(
        {"nome_schema": nome_schema},
        {"$set": {f"tabelas.{nome_tabela}": colunas}}
    )

    return {"message": f"Coluna '{nome_coluna}' atualizada com sucesso na tabela '{nome_tabela}'"}