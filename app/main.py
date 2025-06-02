from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.v1.endpoints import dicionariodados
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Dicionário de Dados",
        description="Esta API tem a finalidade de registrar, editar e deletar schemas e tabelas.",
        version="0.1.0"
    )

    @app.get("/", include_in_schema=False)
    def redirect_root():
        return RedirectResponse(url="/docs")  # ou /dicionariodados

    app.include_router(
        dicionariodados.router,
        prefix="/dicionariodados",
        tags=["Dicionário de Dados"]
    )

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80)