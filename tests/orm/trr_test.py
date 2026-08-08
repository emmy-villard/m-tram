from orm.trr import Trr, NewTrrData
import sqlalchemy

def test_column_types_trr():
    table = Trr.__table__
    new_table_data = NewTrrData.__table__
    assert type(table) == sqlalchemy.Table
    assert type(new_table_data) == sqlalchemy.Table
    assert type(table.c.trr_id.type) == sqlalchemy.Text
    assert type(table.c.trr_time.type) == sqlalchemy.TIMESTAMP
    assert type(table.c.trr_nsv_id.type) == sqlalchemy.Integer
    assert type(new_table_data.c.trr_id.type) == sqlalchemy.Text
    assert type(new_table_data.c.trr_time.type) == sqlalchemy.TIMESTAMP
    assert type(new_table_data.c.trr_nsv_id.type) == sqlalchemy.Integer
    pk_names = {c.name for c in table.primary_key}
    assert pk_names == {table.c.trr_id.name, table.c.trr_time.name}
    pk_names_new_data = {c.name for c in new_table_data.primary_key}
    assert pk_names_new_data == {new_table_data.c.trr_id.name, new_table_data.c.trr_time.name}