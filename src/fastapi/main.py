from fastapi import FastAPI
from db_connection.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy import text, func, select
from orm.ligne import Ligne

app = FastAPI()

@app.get("/raw/ligne")
def get_line_number():
    with Session(engine) as session:
        select_stmt = select(Ligne)
        lines = session.execute(select_stmt).scalars().all()
        return {
            "result": [
                {
                    "ligne_id": line.ligne_id,
                    "ligne_time": line.ligne_time,
                    "ligne_nsv_id": line.ligne_nsv_id,
                }
                for line in lines
            ]
        }