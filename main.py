import logging
import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI(title="Project Invoice API")


@app.get("/")
def home():
    return {"message": "서버가 동작 중입니다"}


@app.get("/db-check")
def db_check():
    """Check the configured PostgreSQL connection."""
    try:
        with psycopg.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "seoul_chemtech_db"),
            user=os.getenv("DB_USER", "invoice_app"),
            password=os.getenv("DB_PASSWORD", ""),
            connect_timeout=5,
        ) as connection:
            database, username = connection.execute(
                "SELECT current_database(), current_user"
            ).fetchone()

        return {"connected": True, "database": database, "user": username}
    except Exception as error:
        logging.exception("PostgreSQL connection check failed")
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 터미널 오류와 .env 설정을 확인하세요.",
        ) from error

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
