from sqlalchemy import MetaData, PrimaryKeyConstraint
from sqlalchemy import Table, Column, Integer, Text, select
from sqlalchemy.dialects.postgresql import insert
from .engine import engine

def load_ligne(dataframe):
    with engine.connect() as conn:
        ligne, new_ligne_data = getTables()
        dataframe.to_sql("new_ligne_data", conn, if_exists="replace")
        lines_with_data = select(new_ligne_data).where(new_ligne_data.c.ligne_nsv_id != 0)
        insert_new_lines = insert(ligne).from_select(
            ["ligne_id", "ligne_time", "ligne_nsv_id"], lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        conn.execute(upsert_new_lines)
        conn.commit()

def getTables():
    ligne = Table(
        "ligne",
        MetaData(),
        Column("ligne_id", Integer),
        Column("ligne_time", Text),
        Column("ligne_nsv_id", Integer),
        PrimaryKeyConstraint("ligne_id", "ligne_time"),
    )
    new_ligne_data = Table(
        "new_ligne_data",
        MetaData(),
        Column("ligne_id", Integer),
        Column("ligne_time", Text),
        Column("ligne_nsv_id", Integer),
        PrimaryKeyConstraint("ligne_id", "ligne_time"),
    )
    return ligne, new_ligne_data