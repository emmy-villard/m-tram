import os
from sqlalchemy import create_engine, select, insert
from sqlalchemy import URL, MetaData, PrimaryKeyConstraint
from sqlalchemy import Table, Column, Integer, Text

def load_trr(dataframe):
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv('POSTGRES_USER'),
        host="localhost",
        port=os.getenv('POSTGRES_PORT'),
        database=os.getenv('POSTGRES_DB'),
        password=os.getenv('POSTGRES_PASSWORD'),
    )
    engine = create_engine(url)

    with engine.connect() as conn:
        trr, trr_tmp = getTables()
        dataframe.to_sql('trr_tmp', conn, if_exists='replace')
        select_new_lines = select(trr_tmp).except_(select(trr))
        insert_new_lines = insert(trr).from_select(
            ["trr_id", "trr_time", "nsv_id"], select_new_lines)
        conn.execute(insert_new_lines)
        conn.commit()

def getTables():
    trr = Table(
        "trr",
        MetaData(),
        Column("trr_id", Integer),
        Column("trr_time", Text),
        Column("nsv_id", Integer),
        PrimaryKeyConstraint("trr_id", "nsv_id"),
    )
    trr_tmp = Table(
        "trr_tmp",
        MetaData(),
        Column("trr_id", Integer),
        Column("trr_time", Text),
        Column("nsv_id", Integer),
        PrimaryKeyConstraint("trr_id", "nsv_id"),
    )
    return trr, trr_tmp