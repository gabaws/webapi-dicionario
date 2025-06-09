import jsonschema
from jsonschema import validate, ValidationError

def validar_schema(schema_json: dict, schema_regras: dict) -> bool:
    try:
        validate(instance=schema_json, schema=schema_regras)
        return True
    except ValidationError as e:
        raise ValueError(f"Schema inválido: {e.message}")