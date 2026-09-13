from orm.atmo import Atmo
import sqlalchemy

def test_column_types_Ligne():
    table = Atmo.__table__
    assert type(table) == sqlalchemy.Table
    pk_names = {c.name for c in table.primary_key}
    assert pk_names == {table.c.time.name}