from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import connectors, schemas, generate_data

app = FastAPI(
    title="API Dicionário de Dados 🚀",
    description="✨Gerenciamento de conectores e schemas.✨",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

app.include_router(connectors.router, prefix="/dicionariodados", tags=["Conectores"])
app.include_router(schemas.router, prefix="/dicionariodados", tags=["Schemas"])
app.include_router(generate_data.router, prefix="/dicionariodados", tags=["Geração de Dados"])