from sqlalchemy import MetaData, PrimaryKeyConstraint
from sqlalchemy import Table, Column, Integer, Text, select, TIMESTAMP
from sqlalchemy.dialects.postgresql import insert
from db_connection.engine import engine
from sqlalchemy.orm import Session

def load_table(dataframe, orm_class, new_data_orm_class):
    table = orm_class.__table__
    new_table_data = new_data_orm_class.__table__
    with Session(engine) as session:
        dataframe.to_sql(f"new_{table.name}_data", engine, if_exists="replace")
        cols = [c.name for c in orm_class.__table__.columns]
        lines_with_data = select(new_table_data).where(new_table_data.c[f"{table.name}_nsv_id"] != 0)
        insert_new_lines = insert(table).from_select(cols, lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        session.execute(upsert_new_lines)
        session.commit()
