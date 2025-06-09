from pydantic import BaseModel, Field, validator
from typing import Optional
import re

class ConnectorIn(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    host: str
    porta: int = Field(default=5432)
    banco: str
    nome_schema: Optional[str] = None
    usuario: str
    senha: Optional[str] = Field(default=None, min_length=8)

    @validator("host")
    def validar_host(cls, v):
        if not re.match(r"^((?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*|(\d{1,3}\.){3}\d{1,3})$", v):
            raise ValueError("Host inválido")
        return v

class ConnectorOut(BaseModel):
    nome: str
    host: str
    porta: int
    banco: str
    nome_schema: Optional[str]
    usuario: str