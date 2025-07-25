import psycopg2
from faker import Faker
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
import random
import re

fake = Faker('pt_BR')

# Mapear tipos SQL para funções do Faker
SQL_TYPE_TO_FAKE = {
    'uuid': lambda: str(fake.uuid4()),
    'integer': lambda: fake.random_int(min=1, max=10000),
    'numeric': lambda: float(fake.pydecimal(left_digits=5, right_digits=2)),
    'text': lambda: fake.text(max_nb_chars=20),
    'character varying': lambda length=20: fake.text(max_nb_chars=length),
    'character': lambda length=1: fake.random_letter(),
    'timestamp without time zone': lambda: fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S'),
    'date': lambda: fake.date(),
    'boolean': lambda: fake.boolean(),
}

CHARACTER_VARYING = 'character varying'
TIMESTAMP_WO_TZ = 'timestamp without time zone'

def extract_check_values(expression: str):
    # ARRAY['A', 'B', ...]
    match = re.search(r"ARRAY\[(.*?)\]", expression)
    if match:
        items = match.group(1)
        values = [item.split("::")[0].strip().strip("'") for item in items.split(",")]
        return values
    # IN ('A', 'B', ...)
    match = re.search(r"IN\s*\((.*?)\)", expression)
    if match:
        items = match.group(1)
        values = [item.strip().strip("'") for item in items.split(",")]
        return values
    return None

def extract_numeric_constraint(expression: str):
    # Exemplo: CHECK (coluna > 0)
    match = re.search(r"> ?(-?\d+)", expression)
    if match:
        return int(match.group(1)) + 1  # Gera acima do valor mínimo
    match = re.search(r"< ?(-?\d+)", expression)
    if match:
        return int(match.group(1)) - 1  # Gera abaixo do valor máximo
    return None

def extract_boolean_constraint(expression: str):
    # Exemplo: CHECK (coluna IN ('t','f'))
    match = re.search(r"IN\s*\((.*?)\)", expression)
    if match:
        items = match.group(1)
        values = [item.strip().strip("'") for item in items.split(",")]
        if set(values) <= {'t', 'f'}:
            return values
    # Exemplo: CHECK (coluna = 't')
    match = re.search(r"= '([tf])'", expression)
    if match:
        return [match.group(1)]
    return None

def extract_length_equals_constraint(expression: str):
    # Exemplo: CHECK ((length((num_cartao)::text) = 16))
    match = re.search(r"length\(.*?\) *= *(\d+)", expression)
    if match:
        return int(match.group(1))
    # Corrigir regex para capturar corretamente
    match = re.search(r"length\(.*?\)\s*=\s*(\d+)", expression)
    if match:
        return int(match.group(1))
    return None

def _fake_value_from_check_constraint(col: dict) -> Any:
    expr = col['check_constraint']['expression']
    allowed = extract_check_values(expr)
    if allowed:
        return random.choice(allowed)
    bool_vals = extract_boolean_constraint(expr)
    if bool_vals:
        return random.choice(bool_vals)
    min_val = extract_numeric_constraint(expr)
    if min_val is not None and col['type'] in ('integer', 'numeric'):
        return random.randint(min_val, min_val + 1000)
    length_eq = extract_length_equals_constraint(expr)
    if length_eq and col['type'] in (CHARACTER_VARYING, 'character'):
        if 'cartao' in col['column']:
            return fake.numerify('#' * length_eq)
        return fake.bothify('?' * length_eq)
    return None

def _fake_value_from_type(col: dict) -> Any:
    t = col['type']
    if t == CHARACTER_VARYING:
        length = col.get('length') or 20
        length = max(1, int(length))
        return fake.pystr(min_chars=length, max_chars=length)
    if t == 'character':
        length = col.get('length') or 1
        length = max(1, int(length))
        return fake.pystr(min_chars=length, max_chars=length)
    if t in (CHARACTER_VARYING, 'character', 'text'):
        length = col.get('length') or 10
        try:
            length = int(length)
        except Exception:
            length = 10
        return fake.pystr(min_chars=length, max_chars=length)
    return SQL_TYPE_TO_FAKE.get(t, lambda: None)()

def get_fake_value(col: dict) -> Any:
    # 1. Tenta gerar valor a partir de check_constraint
    if col.get('check_constraint') and 'expression' in col['check_constraint']:
        value = _fake_value_from_check_constraint(col)
        if value is not None:
            return value
    # 2. Gera valor baseado no tipo
    return _fake_value_from_type(col)


def topological_sort_tables(schema_metadata: Dict[str, Any]) -> List[str]:
    # Ordena as tabelas respeitando dependências de FK
    graph = defaultdict(list)
    indegree = defaultdict(int)
    for table, meta in schema_metadata.items():
        if table == 'nome_schema':
            continue
        for dep in meta.get('depends_on', []):
            graph[dep].append(table)
            indegree[table] += 1
        if table not in indegree:
            indegree[table] = 0
    queue = deque([t for t in indegree if indegree[t] == 0])
    order = []
    while queue:
        t = queue.popleft()
        order.append(t)
        for nei in graph[t]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)
    return order


def get_max_pk_value(conn_params, schema, table, pk_col):
    try:
        with psycopg2.connect(**conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT MAX({pk_col}) FROM {schema}.{table}')
                max_val = cur.fetchone()[0]
                return (max_val or 0)
    except Exception:
        return 0


def _get_pk_value(table, col, idx, pk_start_vals):
    if col['type'] in ('integer', 'bigint'):
        start_val = pk_start_vals.get((table, col['column']), 0)
        return start_val + idx + 1
    return get_fake_value(col)

def _get_fk_value(col, data):
    ref_table = col['references']['table']
    ref_col = col['references']['column']
    ref_vals = [r[ref_col] for r in data.get(ref_table, [])]
    return random.choice(ref_vals) if ref_vals else None

def _get_not_null_fallback(col, idx):
    t = col['type']
    if t in (CHARACTER_VARYING, 'character', 'text'):
        length = col.get('length') or 10
        try:
            length = int(length)
        except Exception:
            length = 10
        return fake.pystr(min_chars=length, max_chars=length)
    elif t in ('integer', 'numeric', 'bigint'):
        return idx + 1
    elif t == 'date':
        return fake.date()
    elif t == TIMESTAMP_WO_TZ:
        return fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
    elif t == 'boolean':
        return True
    return None

def _get_not_null_final_fallback(col, idx):
    t = col['type']
    if t in (CHARACTER_VARYING, 'character', 'text'):
        return 'X'
    elif t in ('integer', 'numeric', 'bigint'):
        return idx + 1
    elif t == 'date':
        return '2000-01-01'
    elif t == TIMESTAMP_WO_TZ:
        return '2000-01-01 00:00:00'
    elif t == 'boolean':
        return True
    return None

def _generate_row(table, table_meta, idx, pk_start_vals, data):
    row = {}
    for col in table_meta['columns']:
        value = None
        if col['is_primary_key']:
            value = _get_pk_value(table, col, idx, pk_start_vals)
            row[col['column']] = value
        elif col['is_foreign_key'] and col['references']:
            value = _get_fk_value(col, data)
            row[col['column']] = value
        else:
            value = get_fake_value(col)
            if col.get('nullable', 'YES') == 'NO' and value is None:
                value = _get_not_null_fallback(col, idx)
            if col.get('nullable', 'YES') == 'NO' and value is None:
                value = _get_not_null_final_fallback(col, idx)
            row[col['column']] = value
    return row

def generate_fake_data(schema_metadata: Dict[str, Any], rows_per_table: int = 10, conn_params: Optional[dict] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Gera dados fake para cada tabela do schema, respeitando FKs e constraints básicas.
    Se conn_params for fornecido, busca o maior valor atual das PKs inteiras para evitar duplicidade.
    """
    data = {}
    table_order = topological_sort_tables(schema_metadata)
    pk_start_vals = {}
    if conn_params:
        nome_schema = schema_metadata.get('nome_schema', 'public')
        for table in table_order:
            if table == 'nome_schema':
                continue
            table_meta = schema_metadata[table]
            for col in table_meta['columns']:
                if col['is_primary_key'] and col['type'] in ('integer', 'bigint'):
                    pk_start_vals[(table, col['column'])] = get_max_pk_value(conn_params, nome_schema, table, col['column'])
    for table in table_order:
        if table == 'nome_schema':
            continue
        table_meta = schema_metadata[table]
        rows = []
        for idx in range(rows_per_table):
            row = _generate_row(table, table_meta, idx, pk_start_vals, data)
            rows.append(row)
        data[table] = rows
    return data


def generate_insert_sql(schema_metadata: Dict[str, Any], fake_data: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Gera comandos INSERT SQL para os dados fake gerados.
    """
    nome_schema = schema_metadata.get('nome_schema', 'public')
    sqls = []
    for table, rows in fake_data.items():
        if table == 'nome_schema':
            continue
        cols = [col['column'] for col in schema_metadata[table]['columns']]
        for row in rows:
            values = []
            for c in cols:
                v = row[c]
                if v is None:
                    values.append('NULL')
                elif isinstance(v, str):
                    values.append("'" + v.replace("'", "''") + "'")
                else:
                    values.append(str(v))
            sql = f"INSERT INTO {nome_schema}.{table} ({', '.join(cols)}) VALUES ({', '.join(values)});"
            sqls.append(sql)
    return '\n'.join(sqls)


def execute_inserts(conn_params: dict, sql: str):
    """
    Executa os comandos INSERT SQL na base de destino.
    """
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    for statement in sql.split(';'):
        stmt = statement.strip()
        if stmt:
            cur.execute(stmt)
    conn.commit()
    cur.close()
    conn.close() 