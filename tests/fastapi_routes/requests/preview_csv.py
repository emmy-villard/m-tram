import asyncio
import os

import pandas as pd

from db_connection.test_engine import engine
from etl.classes.Ligne import Ligne
from orm.base import Base
from fastapi_routes.requests import raw

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..", "etl", "etl_test_data"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "preview_ligne.csv"
)

"""
For manual testing: writes a real CSV file to disk.
"""


def load_ligne_data():
    dataframe = pd.read_csv(os.path.join(TEST_DATA_DIR, "ligne.csv"))
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Ligne.load_table(dataframe, engine, Ligne.orm_class(), Ligne.data_validator())


async def read_csv_response(response):
    chunks = []
    async for chunk in response.body_iterator:
        if isinstance(chunk, str):
            chunks.append(chunk.encode("utf-8"))
        else:
            chunks.append(chunk)
    return b"".join(chunks)


async def main():
    load_ligne_data()
    response = raw.stream_csv(raw._get_model("ligne"))
    csv_bytes = await read_csv_response(response)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(csv_bytes)
    print(f"CSV écrit dans: {OUTPUT_PATH}")
    print(f"Taille: {len(csv_bytes)} octets")


if __name__ == "__main__":
    asyncio.run(main())
