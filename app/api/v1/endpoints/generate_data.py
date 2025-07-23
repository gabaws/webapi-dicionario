from fastapi import APIRouter, HTTPException, Query, Depends
from app.db.mongo import tabelas_collection, conectores_collection, dados_sinteticos_collection
from app.db.crud import schemas as crud_schemas, connectors as crud_connectors, dados_sinteticos as crud_dados_sinteticos
from app.utils.crypto import decrypt_password
from app.services import data_generation
from app.core.logging import logger
from datetime import datetime
from typing import Any, Dict

router = APIRouter()


def get_tabelas_collection():
    return tabelas_collection

def get_conectores_collection():
    return conectores_collection

def get_dados_sinteticos_collection():
    return dados_sinteticos_collection

def _buscar_schema(nome_schema: str, collection) -> Dict[str, Any]:
    schema = crud_schemas.get_schema_por_nome(nome_schema, collection)
    if not schema:
        raise HTTPException(status_code=404, detail="Schema não encontrado")
    return schema

def _buscar_conector(conector_nome: str, collection) -> Dict[str, Any]:
    conector = crud_connectors.get_conector_por_nome(conector_nome, collection)
    if not conector:
        raise HTTPException(status_code=404, detail="Conector não encontrado")
    return conector

def _montar_conn_params(conector: dict) -> dict:
    senha = decrypt_password(conector['senha'])
    return {
        'host': conector['host'],
        'port': conector['porta'],
        'dbname': conector['banco'],
        'user': conector['usuario'],
        'password': senha
    }

@router.post("/gerar-dados/{nome_schema}")
def gerar_dados(
    nome_schema: str,
    conector_nome: str = Query(..., description="Nome do conector de destino"),
    rows_per_table: int = Query(10, description="Linhas por tabela"),
    modo: str = Query('executar', description="executar ou sql"),
    persistir_sql: bool = Query(False, description="Se verdadeiro, persiste o SQL gerado no MongoDB"),
    tabelas_col=Depends(get_tabelas_collection),
    conectores_col=Depends(get_conectores_collection),
    dados_sint_col=Depends(get_dados_sinteticos_collection)
):
    """
    Gera dados sintéticos para um schema e insere ou retorna o SQL.
    """
    try:
        schema = _buscar_schema(nome_schema, tabelas_col)
        conector = _buscar_conector(conector_nome, conectores_col)
        conn_params = _montar_conn_params(conector)
        fake_data = data_generation.generate_fake_data(schema, rows_per_table, conn_params=conn_params)
        sql = data_generation.generate_insert_sql(schema, fake_data)
        if persistir_sql:
            crud_dados_sinteticos.upsert_sql(
                nome_schema, sql, dados_sint_col,
                rows_per_table=rows_per_table, updated_at=datetime.utcnow()
            )
            logger.info(f"Script SQL persistido para schema {nome_schema} na collection dados_sinteticos")
        if modo == 'sql':
            return {"sql": sql, "persistido": persistir_sql}
        data_generation.execute_inserts(conn_params, sql)
        logger.info(f"Dados gerados e inseridos para schema {nome_schema} usando conector {conector_nome}")
        return {"message": "Dados gerados e inseridos com sucesso!", "persistido": persistir_sql}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao gerar dados: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/gerar-dados/{nome_schema}")
def get_dados_gerados(
    nome_schema: str,
    dados_sint_col=Depends(get_dados_sinteticos_collection)
):
    """
    Retorna os dados sintéticos gerados e persistidos para o schema informado.
    """
    doc = crud_dados_sinteticos.get_sql(nome_schema, dados_sint_col)
    if not doc:
        raise HTTPException(status_code=404, detail="Nenhum dado sintético encontrado para este schema.")
    doc.pop("_id", None)
    return doc 