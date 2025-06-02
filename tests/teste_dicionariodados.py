import pytest
import json
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000/dicionariodados"
TEST_SCHEMA = "teste_schema"

SCHEMA_TEMP_FILE = "schema_temp.json"
SCHEMA_ATUALIZADO_FILE = "schema_atualizado.json"

@pytest.mark.asyncio
async def test_criar_schema():
    dados = {
        "usuarios": [
            {
                "column": "id",
                "type": "int",
                "length": None,
                "nullable": "False",
                "is_primary_key": True,
                "is_foreign_key": False,
                "references": None
            },
            {
                "column": "nome",
                "type": "string",
                "length": 255,
                "nullable": "False",
                "is_primary_key": False,
                "is_foreign_key": False,
                "references": None
            }
        ]
    }

    with open(SCHEMA_TEMP_FILE, "w") as f:
        json.dump(dados, f)

    with open(SCHEMA_TEMP_FILE, "rb") as f:
        files = {"arquivo_dicionario": (SCHEMA_TEMP_FILE, f, "application/json")}
        data = {"nome_schema": TEST_SCHEMA}
        async with AsyncClient() as client:
            response = await client.post(BASE_URL + "/", files=files, data=data)

    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_obter_schema():
    async with AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{TEST_SCHEMA}")
    assert response.status_code == 200
    assert response.json()["nome_schema"] == TEST_SCHEMA

@pytest.mark.asyncio
async def test_atualizar_schema():
    dados_atualizados = {
        "usuarios": [
            {
                "column": "id",
                "type": "int",
                "length": None,
                "nullable": "False",
                "is_primary_key": True,
                "is_foreign_key": False,
                "references": None
            },
            {
                "column": "email",
                "type": "string",
                "length": 320,
                "nullable": "True",
                "is_primary_key": False,
                "is_foreign_key": False,
                "references": None
            }
        ]
    }

    with open(SCHEMA_ATUALIZADO_FILE, "w") as f:
        json.dump(dados_atualizados, f)

    with open(SCHEMA_ATUALIZADO_FILE, "rb") as f:
        files = {"arquivo_dicionario": (SCHEMA_ATUALIZADO_FILE, f, "application/json")}
        data = {"novo_nome_schema": TEST_SCHEMA}
        async with AsyncClient() as client:
            response = await client.put(f"{BASE_URL}/{TEST_SCHEMA}", files=files, data=data)

    assert response.status_code == 200
    assert response.json()["message"] == "Atualizado com sucesso"

@pytest.mark.asyncio
async def test_patch_coluna():
    nova_coluna = {
        "column": "email",
        "type": "varchar",
        "length": 320,
        "nullable": "False",
        "is_primary_key": False,
        "is_foreign_key": False,
        "references": None
    }

    async with AsyncClient() as client:
        response = await client.patch(
            f"{BASE_URL}/{TEST_SCHEMA}/usuarios/email",
            json=nova_coluna
        )

    assert response.status_code == 200
    assert "atualizada com sucesso" in response.json()["message"]

@pytest.mark.asyncio
async def test_deletar_schema():
    async with AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/{TEST_SCHEMA}")
    assert response.status_code == 200
    assert response.json()["message"] == "Schema deletado com sucesso"