from pydantic import BaseModel
from typing import Optional, Union

class Column(BaseModel):
    column: str
    type: str
    length: Optional[Union[int, None]]
    nullable: str
    is_primary_key: bool
    is_foreign_key: bool
    references: Optional[str] = None