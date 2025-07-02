from fastapi import APIRouter, HTTPException, Query, Body
from app.db.mongo import tabelas_collection, conectores_collection, dados_sinteticos_collection
from app.db.crud import schemas as crud_schemas, connectors as crud_connectors, dados_sinteticos as crud_dados_sinteticos
from app.utils.crypto import decrypt_password
from app.services import data_generation
from app.core.logging import logger
from datetime import datetime

router = APIRouter()

@router.post("/gerar-dados/{nome_schema}")
def gerar_dados(
    nome_schema: str,
    conector_nome: str = Query(..., description="Nome do conector de destino"),
    rows_per_table: int = Query(10, description="Linhas por tabela"),
    modo: str = Query('executar', description="executar ou sql"),
    persistir_sql: bool = Query(False, description="Se verdadeiro, persiste o SQL gerado no MongoDB")
):
    try:
        # 1. Buscar metadado do schema
        schema = crud_schemas.get_schema_por_nome(nome_schema, tabelas_collection)
        if not schema:
            raise HTTPException(status_code=404, detail="Schema não encontrado")
        # 2. Buscar conector
        conector = crud_connectors.get_conector_por_nome(conector_nome, conectores_collection)
        if not conector:
            raise HTTPException(status_code=404, detail="Conector não encontrado")
        # 3. Descriptografar senha
        senha = decrypt_password(conector['senha'])
        conn_params = {
            'host': conector['host'],
            'port': conector['porta'],
            'dbname': conector['banco'],
            'user': conector['usuario'],
            'password': senha
        }
        # 4. Gerar dados fake
        fake_data = data_generation.generate_fake_data(schema, rows_per_table, conn_params=conn_params)
        sql = data_generation.generate_insert_sql(schema, fake_data)
        # 5. Persistir SQL se solicitado
        if persistir_sql:
            crud_dados_sinteticos.upsert_sql(nome_schema, sql, dados_sinteticos_collection, rows_per_table=rows_per_table, updated_at=datetime.utcnow())
            logger.info(f"Script SQL persistido para schema {nome_schema} na collection dados_sinteticos")
        if modo == 'sql':
            return {"sql": sql, "persistido": persistir_sql}
        # 6. Executar inserts
        data_generation.execute_inserts(conn_params, sql)
        logger.info(f"Dados gerados e inseridos para schema {nome_schema} usando conector {conector_nome}")
        return {"message": "Dados gerados e inseridos com sucesso!", "persistido": persistir_sql}
    except Exception as e:
        logger.error(f"Erro ao gerar dados: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 