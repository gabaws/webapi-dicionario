import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, Any
import logging

def validar_schema(
    schema_json: Dict[str, Any],
    schema_regras: Dict[str, Any],
    raise_exception: bool = False
) -> bool:
    
    logger = logging.getLogger("json_validator")
    try:
        validate(instance=schema_json, schema=schema_regras)
        return True
    except ValidationError as e:
        logger.warning(f"Schema inválido: {e.message}")
        if raise_exception:
            raise ValueError(f"Schema inválido: {e.message}")
        return False