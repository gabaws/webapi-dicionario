from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import connectors, schemas, generate_data
from app.db.mongo import client
from app.core.logging import logger

DICIONARIO_PREFIX = "/dicionariodados"

app = FastAPI(
    title="API Dicionário de Dados 🚀",
    description="✨Gerenciamento de conectores, schemas e geração de dados.✨",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/hc", tags=["Health"])
def health():
    """
    Health check endpoint para verificar status da aplicação e banco
    """
    try:
        
        client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503, 
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )

app.include_router(connectors.router, prefix=DICIONARIO_PREFIX, tags=["Conectores"])
app.include_router(schemas.router, prefix=DICIONARIO_PREFIX, tags=["Schemas"])
app.include_router(generate_data.router, prefix=DICIONARIO_PREFIX, tags=["Geração de Dados"])