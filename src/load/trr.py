from sqlalchemy import MetaData, PrimaryKeyConstraint
from sqlalchemy import Table, Column, Integer, Text, select
from sqlalchemy.dialects.postgresql import insert
from .engine import engine

def load_trr(dataframe):
    with engine.connect() as conn:
        trr, new_trr_data = getTables()
        dataframe.to_sql("new_trr_data", conn, if_exists="replace")
        lines_with_data = select(new_trr_data).where(new_trr_data.c.nsv_id != 0)
        insert_new_lines = insert(trr).from_select(
            ["trr_id", "trr_time", "nsv_id"], lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        conn.execute(upsert_new_lines)
        conn.commit()

def getTables():
    trr = Table(
        "trr",
        MetaData(),
        Column("trr_id", Integer),
        Column("trr_time", Text),
        Column("nsv_id", Integer),
        PrimaryKeyConstraint("trr_id", "trr_time"),
    )
    trr_tmp = Table(
        "new_trr_data",
        MetaData(),
        Column("trr_id", Integer),
        Column("trr_time", Text),
        Column("nsv_id", Integer),
        PrimaryKeyConstraint("trr_id", "trr_time"),
    )
    return trr, trr_tmp