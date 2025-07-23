import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.test'))

import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SCHEMA_TESTE = "schema_teste"
SCHEMA_TESTE_ENDPOINT = f"/dicionariodados/schemas/{SCHEMA_TESTE}"
UPLOAD_ENDPOINT = "/dicionariodados/schemas/upload"
APPLICATION_JSON = "application/json"
SCHEMA_ORIGINAL = "schema_original.json"
SCHEMA_ATUALIZADO = "schema_atualizado.json"
SCHEMA_NAO_ENCONTRADO = "Schema não encontrado"

@pytest.fixture(scope="module")
def cleanup_schema():
    # Remove o schema antes e depois dos testes
    client.delete("/dicionariodados/schemas/schema_teste")
    yield
    client.delete("/dicionariodados/schemas/schema_teste")

def load_payload(filename):
    with open(os.path.join(os.path.dirname(__file__), "payloads", filename), encoding="utf-8") as f:
        return json.load(f)

class TestSchemas:
    def test_create_schema_success(self, cleanup_schema):
        files = {
            'file': (SCHEMA_ORIGINAL, json.dumps(load_payload(SCHEMA_ORIGINAL)), APPLICATION_JSON)
        }
        data = {"nome_schema": SCHEMA_TESTE}
        response = client.post(UPLOAD_ENDPOINT, data=data, files=files)
        assert response.status_code == 200
        assert "Schema enviado com sucesso" in response.json()["message"]

    def test_update_schema_success(self, cleanup_schema):
        # Primeiro cadastra o schema original
        files = {
            'file': (SCHEMA_ORIGINAL, json.dumps(load_payload(SCHEMA_ORIGINAL)), APPLICATION_JSON)
        }
        data = {"nome_schema": SCHEMA_TESTE}
        client.post(UPLOAD_ENDPOINT, data=data, files=files)
        # Atualiza com o schema atualizado
        files = {
            'file': (SCHEMA_ATUALIZADO, json.dumps(load_payload(SCHEMA_ATUALIZADO)), APPLICATION_JSON)
        }
        response = client.put(SCHEMA_TESTE_ENDPOINT, files=files)
        assert response.status_code == 200
        assert "Schema atualizado com sucesso" in response.json()["message"]

    def test_get_schema(self, cleanup_schema):
        # Garante que o schema existe
        files = {
            'file': (SCHEMA_ORIGINAL, json.dumps(load_payload(SCHEMA_ORIGINAL)), APPLICATION_JSON)
        }
        data = {"nome_schema": SCHEMA_TESTE}
        client.post(UPLOAD_ENDPOINT, data=data, files=files)
        response = client.get(SCHEMA_TESTE_ENDPOINT)
        assert response.status_code == 200
        data = response.json()
        assert data["nome_schema"] == SCHEMA_TESTE
        assert any(t["nome"] == "tabela1" for t in data["tabelas"])

    def test_delete_schema(self, cleanup_schema):
        # Garante que o schema existe
        files = {
            'file': (SCHEMA_ORIGINAL, json.dumps(load_payload(SCHEMA_ORIGINAL)), APPLICATION_JSON)
        }
        data = {"nome_schema": SCHEMA_TESTE}
        client.post(UPLOAD_ENDPOINT, data=data, files=files)
        response = client.delete(SCHEMA_TESTE_ENDPOINT)
        assert response.status_code == 200
        assert "Schema removido com sucesso" in response.json()["message"] 