from app.utils.json_validator import validar_schema

SCHEMA_EXEMPLO = {"type": "object", "properties": {"nome_schema": {"type": "string"}}}

def validar_schema_json(dados: dict) -> bool:
    return validar_schema(dados, SCHEMA_EXEMPLO)