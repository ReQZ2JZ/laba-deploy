import os
import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

app = FastAPI()

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "app",
    "password": "app",
    "dbname": "eshop",
}


def get_db():
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


@app.get("/products")
async def get_products():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM video_cards")
        rows = cur.fetchall()
        return [{**dict(r), "price": float(r["price"])} for r in rows]


@app.get("/product/{pid}")
async def get_product(pid: int):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM video_cards WHERE id = %s", (pid,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404)
        return dict(row)


@app.get("/health")
async def health():
    return {"status": "ok"}
