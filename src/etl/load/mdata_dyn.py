from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
def load_table(dataframe, engine, orm_class, new_data_orm_class):
    """
    Load dynamic MData data into the database

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Clean data, ready for insertion
    engine : sqlalchemy.Engine
    orm_class
    new_data_orm_class

    Returns
    -------
    """
    table = orm_class.__table__
    new_table_data = new_data_orm_class.__table__
    with Session(engine) as session:
        dataframe.to_sql(f"new_{table.name}_data", engine, if_exists="replace")
        cols = [c.name for c in orm_class.__table__.columns]
        lines_with_data = select(new_table_data).where(
            new_table_data.c[f"{table.name}_nsv_id"] != 0
        )
        insert_new_lines = insert(table).from_select(cols, lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        result_proxy = session.execute(upsert_new_lines)
        session.commit()
        logger.info(f"Inserted lines: {result_proxy.rowcount}")