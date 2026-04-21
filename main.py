import os

import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

app = FastAPI(title="E-Shop-CD")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "app"),
    "password": os.getenv("DB_PASSWORD", "app"),
    "dbname": os.getenv("DB_NAME", "eshop"),
}


def get_db():
    return psycopg.connect(**DB_CONFIG, row_factory=dict_row)


@app.get("/products")
async def get_products():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, price, description, created_at
                FROM video_cards
                ORDER BY id
                """
            )
            rows = cur.fetchall()
            return [{**dict(r), "price": float(r["price"])} for r in rows]
    finally:
        conn.close()


@app.get("/product/{pid}")
async def get_product(pid: int):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, price, description, created_at
                FROM video_cards
                WHERE id = %s
                """,
                (pid,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Not found")
            return {**dict(row), "price": float(row["price"])}
    finally:
        conn.close()


@app.get("/health")
async def health():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM video_cards")
            row = cur.fetchone()
            return {"status": "ok", "products": row["total"]}
    finally:
        conn.close()