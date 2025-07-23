from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict


class Reference(BaseModel):
    table: str
    column: str


class CheckConstraint(BaseModel):
    expression: str


class Column(BaseModel):
    column: str
    type: str
    length: Optional[Union[int, None]]
    nullable: str
    is_primary_key: bool
    is_foreign_key: bool
    is_unique: bool
    references: Optional[Reference] = None
    check_constraint: Optional[CheckConstraint] = None
    description: Optional[str] = None


class TabelaComDependencias(BaseModel):
    columns: List[Column]
    depends_on: List[str]


class SchemaDoc(BaseModel):
    nome_schema: str = Field(...)
    tabelas: Dict[str, TabelaComDependencias]

    model_config = {
        "json_schema_extra": {
            "example": {
                "nome_schema": "public",
                "tabelas": {}
            }
        }
    }