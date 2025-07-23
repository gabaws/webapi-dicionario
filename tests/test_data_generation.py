import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.services import data_generation
import os
import json

client = TestClient(app)

PSYCOPG2_CONNECT_PATH = "psycopg2.connect"

def load_payload(filename):
    with open(os.path.join(os.path.dirname(__file__), "payloads", filename), encoding="utf-8") as f:
        return json.load(f)

def test_extract_check_values_array():
    expr = "ARRAY['A','B','C']"
    assert data_generation.extract_check_values(expr) == ['A', 'B', 'C']

def test_extract_check_values_in():
    expr = "IN ('X','Y')"
    assert data_generation.extract_check_values(expr) == ['X', 'Y']

def test_extract_check_values_none():
    expr = "SOMETHING ELSE"
    assert data_generation.extract_check_values(expr) is None

def test_extract_numeric_constraint_gt():
    assert data_generation.extract_numeric_constraint("col > 10") == 11

def test_extract_numeric_constraint_lt():
    assert data_generation.extract_numeric_constraint("col < 5") == 4

def test_extract_numeric_constraint_none():
    assert data_generation.extract_numeric_constraint("col = 5") is None

def test_extract_boolean_constraint_in():
    assert data_generation.extract_boolean_constraint("IN ('t','f')") == ['t', 'f']

def test_extract_boolean_constraint_eq():
    assert data_generation.extract_boolean_constraint("= 't'") == ['t']

def test_extract_boolean_constraint_none():
    assert data_generation.extract_boolean_constraint("col = 1") is None

def test_extract_length_equals_constraint_eq():
    assert data_generation.extract_length_equals_constraint("length(col) = 16") == 16

def test_extract_length_equals_constraint_spaces():
    assert data_generation.extract_length_equals_constraint("length(col)    =    8") == 8

def test_extract_length_equals_constraint_none():
    assert data_generation.extract_length_equals_constraint("col = 5") is None

def test_topological_sort_tables():
    schema = {
        "t1": {"depends_on": ["t2"]},
        "t2": {"depends_on": []}
    }
    order = data_generation.topological_sort_tables(schema)
    assert order == ["t2", "t1"]

def test_get_fake_value_integer():
    col = {"type": "integer"}
    val = data_generation.get_fake_value(col)
    assert isinstance(val, int)

def test_get_fake_value_character_varying():
    col = {"type": data_generation.CHARACTER_VARYING, "length": 5}
    val = data_generation.get_fake_value(col)
    assert isinstance(val, str) and len(val) == 5

def test_get_fake_value_check_constraint_array():
    col = {"type": "text", "check_constraint": {"expression": "ARRAY['A','B']"}}
    val = data_generation.get_fake_value(col)
    assert val in ['A', 'B']

def test_get_fake_value_check_constraint_in():
    col = {"type": "text", "check_constraint": {"expression": "IN ('X','Y')"}}
    val = data_generation.get_fake_value(col)
    assert val in ['X', 'Y']

def test_get_fake_value_check_constraint_bool():
    col = {"type": "boolean", "check_constraint": {"expression": "IN ('t','f')"}}
    val = data_generation.get_fake_value(col)
    assert val in ['t', 'f']

def test_get_fake_value_check_constraint_numeric():
    col = {"type": "integer", "check_constraint": {"expression": "col > 5"}}
    val = data_generation.get_fake_value(col)
    assert isinstance(val, int) and val >= 6

def test_get_fake_value_check_constraint_length():
    col = {"type": data_generation.CHARACTER_VARYING, "column": "cartao", "check_constraint": {"expression": "length(col) = 8"}}
    val = data_generation.get_fake_value(col)
    assert isinstance(val, str) and len(val) == 8

def test_generate_insert_sql():
    schema = {
        "nome_schema": "public",
        "tabela1": {
            "columns": [
                {"column": "id", "type": "integer"},
                {"column": "nome", "type": "text"}
            ]
        }
    }
    fake_data = {
        "tabela1": [
            {"id": 1, "nome": "Alice"},
            {"id": 2, "nome": "Bob"}
        ]
    }
    sql = data_generation.generate_insert_sql(schema, fake_data)
    assert "INSERT INTO public.tabela1" in sql
    assert "Alice" in sql and "Bob" in sql

def test_get_max_pk_value_success():
    with patch(PSYCOPG2_CONNECT_PATH) as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [42]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn
        val = data_generation.get_max_pk_value({'host': 'x'}, 'schema', 'table', 'pk')
        assert val == 42

def test_get_max_pk_value_none():
    with patch(PSYCOPG2_CONNECT_PATH) as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [None]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn
        val = data_generation.get_max_pk_value({'host': 'x'}, 'schema', 'table', 'pk')
        assert val == 0

def test_get_max_pk_value_exception():
    with patch(PSYCOPG2_CONNECT_PATH, side_effect=Exception("fail")):
        val = data_generation.get_max_pk_value({}, "schema", "table", "pk")
        assert val == 0

def test_generate_fake_data_no_conn_params():
    schema = load_payload("schema_simple.json")
    data = data_generation.generate_fake_data(schema, 2)
    assert "tabela1" in data
    assert len(data["tabela1"]) == 2
    assert "id" in data["tabela1"][0]
    assert "nome" in data["tabela1"][0]

def test_generate_fake_data_with_conn_params():
    schema = load_payload("schema_simple.json")
    schema["tabela1"]["columns"][0]["is_primary_key"] = True
    schema["tabela1"]["columns"][0]["type"] = "integer"
    with patch("app.services.data_generation.get_max_pk_value", return_value=100):
        data = data_generation.generate_fake_data(schema, 1, conn_params={})
        assert data["tabela1"][0]["id"] in (1, 101)

def test_generate_fake_data_not_null_fallback():
    schema = load_payload("schema_notnull.json")
    data = data_generation.generate_fake_data(schema, 1)
    assert data["tabela1"][0]["id"] is not None
    assert data["tabela1"][0]["nome"] is not None

def test_execute_inserts_success():
    with patch(PSYCOPG2_CONNECT_PATH):
        data_generation.execute_inserts({'host': 'x'}, "INSERT INTO t (a) VALUES (1);INSERT INTO t (a) VALUES (2)")

def test_generate_data_schema_not_found():
    response = client.post("/dicionariodados/gerar-dados/inexistente", params={"conector_nome": "fake"})
    assert response.status_code == 404
    assert "Schema não encontrado" in response.text

def test_generate_data_conector_not_found(monkeypatch):
    # Mocka o schema existente
    with patch("app.db.crud.schemas.get_schema_por_nome", return_value={"nome_schema": "schema_teste"}):
        with patch("app.db.crud.connectors.get_conector_por_nome", return_value=None):
            response = client.post("/dicionariodados/gerar-dados/schema_teste", params={"conector_nome": "fake"})
            assert response.status_code == 404
            assert "Conector não encontrado" in response.text

def test_generate_data_success(monkeypatch):
    schema = {"nome_schema": "schema_teste"}
    conector = {"host": "localhost", "porta": 5432, "banco": "test", "usuario": "user", "senha": "token_fake"}
    fake_data = {"tabela": [{"id": 1}]}
    with patch("app.db.crud.schemas.get_schema_por_nome", return_value=schema):
        with patch("app.db.crud.connectors.get_conector_por_nome", return_value=conector):
            with patch("app.api.v1.endpoints.generate_data.decrypt_password", return_value="senha"):
                with patch("app.services.data_generation.generate_fake_data", return_value=fake_data):
                    with patch("app.services.data_generation.generate_insert_sql", return_value="INSERT;"):
                        with patch("app.services.data_generation.execute_inserts") as mock_exec:
                            response = client.post("/dicionariodados/gerar-dados/schema_teste", params={"conector_nome": "fake"})
                            assert response.status_code == 200
                            assert "Dados gerados e inseridos com sucesso" in response.text
                            mock_exec.assert_called()

def test_get_dados_gerados_not_found():
    response = client.get("/dicionariodados/gerar-dados/inexistente")
    assert response.status_code == 404
    assert "Nenhum dado sintético encontrado" in response.text 