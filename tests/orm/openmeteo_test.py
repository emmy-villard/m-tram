from orm.openmeteo import OpenMeto
import sqlalchemy

def test_column_types_openmeteo():
    table = OpenMeto.__table__
    assert type(table) == sqlalchemy.Table
    pk_names = {c.name for c in table.primary_key}
    assert pk_names == {table.c.time.name}