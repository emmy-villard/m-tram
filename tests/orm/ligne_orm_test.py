from orm.ligne import Ligne
import sqlalchemy

def test_column_types_Ligne():
    table = Ligne.__table__
    assert type(table) == sqlalchemy.Table
    assert type(table.c.ligne_id.type) == sqlalchemy.Text
    assert type(table.c.ligne_time.type) == sqlalchemy.TIMESTAMP
    assert type(table.c.ligne_nsv_id.type) == sqlalchemy.Integer
    pk_names = {c.name for c in table.primary_key}
    assert pk_names == {table.c.ligne_id.name, table.c.ligne_time.name}