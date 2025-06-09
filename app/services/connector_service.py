import psycopg2
from app.models.domain.connectors import ConnectorIn

def testar_conexao_postgres(conector: ConnectorIn) -> bool:
    try:
        conn = psycopg2.connect(
            host=conector.host,
            port=conector.porta,
            dbname=conector.banco,
            user=conector.usuario,
            password=conector.senha,
            connect_timeout=5
        )
        conn.close()
        return True
    except Exception as e:
        raise ConnectionError(f"Erro ao conectar: {e}")