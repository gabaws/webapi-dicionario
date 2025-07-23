import psycopg2
from app.models.domain.connectors import ConnectorIn
import logging
from typing import Any

def testar_conexao_postgres(conector: ConnectorIn) -> bool:

    logger = logging.getLogger("connector_service")
    try:
        with psycopg2.connect(
            host=conector.host,
            port=conector.porta,
            dbname=conector.banco,
            user=conector.usuario,
            password=conector.senha,
            connect_timeout=5
        ) as conn:
            pass
        logger.info(f"Conexão bem-sucedida com banco {conector.banco} em {conector.host}:{conector.porta}")
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar: {e}")
        raise ConnectionError(f"Erro ao conectar: {e}")