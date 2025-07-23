import pytest
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.test'))

from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

CONNECTORS_BASE = "/dicionariodados/connectors/"
CONNECTOR_TESTE = "conector_teste"
CONNECTOR_TESTE_ENDPOINT = f"{CONNECTORS_BASE}{CONNECTOR_TESTE}"
CON_NAO_ENCONTRADO = "Conector não encontrado"

def connector_payload(nome="conector_teste"):
    with open(os.path.join(os.path.dirname(__file__), "payloads", "connector.json"), encoding="utf-8") as f:
        payload = json.load(f)
    payload["nome"] = nome
    return payload

@pytest.fixture(scope="module")
def setup_connector():
    # Garante que o conector não existe antes do teste
    client.delete(f"{CONNECTORS_BASE}{CONNECTOR_TESTE}")
    yield
    # Limpa após os testes
    client.delete(f"{CONNECTORS_BASE}{CONNECTOR_TESTE}")

class TestConnectors:
    def test_create_connector_success(self, setup_connector):
        response = client.post(CONNECTORS_BASE, json=connector_payload())
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["connector_name"] == CONNECTOR_TESTE
        assert data["connection_tested"] is True

    def test_create_connector_duplicate(self, setup_connector):
        # Cria o conector
        client.post(CONNECTORS_BASE, json=connector_payload())
        # Tenta criar novamente
        response = client.post(CONNECTORS_BASE, json=connector_payload())
        assert response.status_code == 400
        assert "Já existe um conector" in response.json()["detail"]

    def test_list_connectors(self, setup_connector):
        # Garante que pelo menos um conector existe
        client.post(CONNECTORS_BASE, json=connector_payload())
        response = client.get(CONNECTORS_BASE)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any(c["nome"] == CONNECTOR_TESTE for c in data)

    def test_get_connector_success(self, setup_connector):
        client.post(CONNECTORS_BASE, json=connector_payload())
        response = client.get(CONNECTOR_TESTE_ENDPOINT)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == CONNECTOR_TESTE
        assert "senha" not in data
        assert "_id" not in data

    def test_get_connector_not_found(self, setup_connector):
        response = client.get(f"{CONNECTORS_BASE}inexistente")
        assert response.status_code == 404
        assert response.json()["detail"] == CON_NAO_ENCONTRADO

    def test_update_connector_success(self, setup_connector):
        client.post(CONNECTORS_BASE, json=connector_payload())
        updated_payload = connector_payload()
        updated_payload["host"] = "127.0.0.1"
        response = client.put(CONNECTOR_TESTE_ENDPOINT, json=updated_payload)
        assert response.status_code == 200
        assert "Conector atualizado com sucesso" in response.json()["message"]

    def test_update_connector_not_found(self, setup_connector):
        payload = connector_payload(nome="nao_existe")
        response = client.put(f"{CONNECTORS_BASE}nao_existe", json=payload)
        assert response.status_code == 404
        assert response.json()["detail"] == CON_NAO_ENCONTRADO

    def test_delete_connector_success(self, setup_connector):
        client.post(CONNECTORS_BASE, json=connector_payload())
        response = client.delete(CONNECTOR_TESTE_ENDPOINT)
        assert response.status_code == 200
        assert "Conector removido com sucesso" in response.json()["message"]

    def test_delete_connector_not_found(self, setup_connector):
        response = client.delete(f"{CONNECTORS_BASE}inexistente")
        assert response.status_code == 404
        assert response.json()["detail"] == CON_NAO_ENCONTRADO

    def test_create_connector_invalid(self, setup_connector):
        # Payload faltando campos obrigatórios
        payload = {"nome": "", "host": "", "porta": 0, "banco": "", "usuario": "", "senha": ""}
        response = client.post(CONNECTORS_BASE, json=payload)
        assert response.status_code == 422 