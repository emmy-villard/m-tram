from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
def load_table(dataframe, engine, orm_class, new_data_orm_class, data_checker):
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
    data_checker(dataframe)
    with Session(engine) as session:
        dataframe.to_sql(f"new_{table.name}_data", engine, if_exists="replace")
        cols = [c.name for c in orm_class.__table__.columns]
        lines_with_data = select(new_table_data).where(
            new_table_data.c[f"{table.name}_nsv_id"] != 0
        )
        #TODO: should not transform data here! Can remove "new_data" tables?
        insert_new_lines = insert(table).from_select(cols, lines_with_data)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        result_proxy = session.execute(upsert_new_lines)
        session.commit()
        logger.info(f"Inserted lines: {result_proxy.rowcount}")