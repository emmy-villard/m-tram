import sqlalchemy

from orm.hourlyagg import HourlyAggregate


def test_column_types_hourly_aggregate():
    table = HourlyAggregate.__table__

    assert type(table) == sqlalchemy.Table
    assert type(table.c.hour_start.type) == sqlalchemy.TIMESTAMP
    assert type(table.c.traffic_type.type) == sqlalchemy.Text
    assert type(table.c.average_congestion_level.type) == sqlalchemy.Float
    assert type(table.c.pollution_index.type) == sqlalchemy.Float
    assert type(table.c.pm10_index.type) == sqlalchemy.Float
    assert type(table.c.pm2_5_index.type) == sqlalchemy.Float
    assert type(table.c.o3_index.type) == sqlalchemy.Float
    assert type(table.c.no2_index.type) == sqlalchemy.Float
    assert type(table.c.so2_index.type) == sqlalchemy.Float
    assert type(table.c.precipitation_total.type) == sqlalchemy.Float
    assert type(table.c.rainfall_total.type) == sqlalchemy.Float
    assert type(table.c.average_temperature.type) == sqlalchemy.Float
    assert type(table.c.average_relative_humidity.type) == sqlalchemy.Float
    assert type(table.c.average_cloud_cover.type) == sqlalchemy.Float
    assert type(table.c.average_wind_speed.type) == sqlalchemy.Float

    pk_names = {column.name for column in table.primary_key}
    assert pk_names == {table.c.hour_start.name, table.c.traffic_type.name}