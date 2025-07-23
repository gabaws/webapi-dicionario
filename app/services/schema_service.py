from app.utils.json_validator import validar_schema
from typing import Dict, Any
import logging

SCHEMA_EXEMPLO = {"type": "object", "properties": {"nome_schema": {"type": "string"}}}

def validar_schema_json(dados: Dict[str, Any]) -> bool:
    logger = logging.getLogger("schema_service")
    valido = validar_schema(dados, SCHEMA_EXEMPLO)
    if not valido:
        logger.warning(f"Schema inválido: {dados}")
    return valido