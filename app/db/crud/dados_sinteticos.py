from datetime import datetime
import psycopg2

def upsert_sql(schema_name, sql, collection, **extra):
    doc = {
        "nome_schema": schema_name,
        "sql": sql,
        "created_at": datetime.utcnow(),
        **extra
    }
    collection.update_one(
        {"nome_schema": schema_name},
        {"$set": doc},
        upsert=True
    )

def get_sql(schema_name, collection):
    return collection.find_one({"nome_schema": schema_name}) 