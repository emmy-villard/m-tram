from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
def load_table(dataframe, engine, orm_class, data_converter):
    """
    Load dynamic MData data into the database

    Parameters
    ----------
    dataframe : pandas.DataFrame
        Clean data, ready for insertion
    engine : sqlalchemy.Engine
    orm_class
    data_converter : callable
        Takes the dataframe and returns a list of Pydantic model
        instances validating/converting the data before insert.

    Returns
    -------
    """
    table = orm_class.__table__
    validated_rows = data_converter(dataframe)
    print(f"ROWS: {validated_rows}")
    rows_to_insert = [row.model_dump() for row in validated_rows]

    if not rows_to_insert:
        logger.info("Inserted lines: 0")
        return

    with Session(engine) as session:
        insert_new_lines = insert(table).values(rows_to_insert)
        upsert_new_lines = insert_new_lines.on_conflict_do_nothing()
        result_proxy = session.execute(upsert_new_lines)
        session.commit()
        logger.info(f"Inserted lines: {result_proxy.rowcount}")