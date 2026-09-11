from orm.trr import Trr
import sqlalchemy

def test_column_types_trr():
    table = Trr.__table__
    assert type(table) == sqlalchemy.Table
    assert type(table.c.trr_id.type) == sqlalchemy.Text
    assert type(table.c.trr_time.type) == sqlalchemy.TIMESTAMP
    assert type(table.c.trr_nsv_id.type) == sqlalchemy.Integer
    pk_names = {c.name for c in table.primary_key}
    assert pk_names == {table.c.trr_id.name, table.c.trr_time.name}