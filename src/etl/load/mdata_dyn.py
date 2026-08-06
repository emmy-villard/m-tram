from sqlalchemy import MetaData, PrimaryKeyConstraint
from sqlalchemy import Table, Column, Integer, Text, select, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from db_connection.engine import engine

def load_table(dataframe, table_name):
    with engine.connect() as conn:
        table, new_table_data = getTables(table_name)
        dataframe.to_sql(f"new_{table_name}_data", conn, if_exists="replace")
        lines_with_data = select(new_table_data).where(new_table_data.c[f"{table_name}_nsv_id"] != 0)
        insert_new_lines = insert(table).from_select(
            [f"{table_name}_id", f"{table_name}_time", f"{table_name}_nsv_id"], lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        conn.execute(upsert_new_lines)
        conn.commit()

def getTables(table_name):
    table = Table(
        table_name,
        MetaData(),
        Column(f"{table_name}_id", Text),
        Column(f"{table_name}_time", TIMESTAMP),
        Column(f"{table_name}_nsv_id", Integer),
        PrimaryKeyConstraint(f"{table_name}_id", f"{table_name}_time"),
    )
    new_table_data = Table(
        f"new_{table_name}_data",
        MetaData(),
        Column(f"{table_name}_id", Text),
        Column(f"{table_name}_time", TIMESTAMP),
        Column(f"{table_name}_nsv_id", Integer),
        PrimaryKeyConstraint(f"{table_name}_id", f"{table_name}_time"),
    )
    return table, new_table_data