from pydantic import BaseModel, Field, validator
from typing import Optional
import psycopg2
import re

class Connector(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    host: str = Field(..., description="Hostname ou IP do banco de dados")
    porta: int = Field(default=5432, ge=1, le=65535)
    banco: str = Field(..., min_length=1, max_length=100)
    schema: Optional[str] = Field(default=None, max_length=100)
    usuario: str = Field(..., min_length=1, max_length=50)
    senha: Optional[str] = Field(default=None, min_length=8, max_length=100)

    @validator("host")
    def validar_host(cls, v):
        if not re.match(r"^((?!-)[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*|(\d{1,3}\.){3}\d{1,3})$", v):
            raise ValueError("Host inválido. Use um hostname ou IPv4 válido.")
        return v

    def testar_conexao(self) -> bool:
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.porta,
                dbname=self.banco,
                user=self.usuario,
                password=self.senha,
                connect_timeout=5
            )
            conn.close()
            return True
        except Exception as e:
            raise ConnectionError(f"Falha ao conectar: {str(e)}")