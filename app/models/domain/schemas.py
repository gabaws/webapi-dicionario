from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict


class Reference(BaseModel):
    table: str
    column: str


class Column(BaseModel):
    column: str
    type: str
    length: Optional[Union[int, None]]
    nullable: str
    is_primary_key: bool
    is_foreign_key: bool
    is_unique: bool
    references: Optional[Reference] = None
    description: Optional[str] = None


class SchemaDoc(BaseModel):
    nome_schema: str = Field(..., example="public")
    tabelas: Dict[str, List[Column]]
