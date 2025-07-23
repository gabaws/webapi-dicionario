from pydantic import BaseModel

class MessageResponse(BaseModel):
    message: str

class ConnectorCreateResponse(BaseModel):
    success: bool
    message: str
    connector_name: str
    connection_tested: bool