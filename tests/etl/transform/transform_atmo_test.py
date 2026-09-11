from etl.transform.atmo import raw_to_pandas_atmo, \
    _str_to_datetime, _is_value_mesured
import os, json
import pytest

@pytest.fixture
def raw_data():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../etl_test_data/atmo.json") as file:
        return json.load(file)

def test_empty_dataframe_raises():
    with pytest.raises(ValueError):
        raw_to_pandas_atmo({})

def test_failed_fetch_raises():
    with pytest.raises(ValueError):
        raw_to_pandas_atmo({"success": False, "data": []})

def test_unknown_type_valeur():
    unvalid_data = {
        "date_echeance": "2026-01-01",
        "indice": 3,
        "type_valeur": "réelle",
        "sous_indices": [
            {"indice": 1},
            {"indice": 1},
            {"indice": 1},
            {"indice": 1},
            {"indice": 1},
        ],
    }
    unvalid_raw_data = {
        "data": [unvalid_data],
        "success": True
    }
    raw_to_pandas_atmo(unvalid_raw_data) # Assert doesn't throw for now
    unvalid_data["type_valeur"] = "reelle"
    with pytest.raises(ValueError):
        raw_to_pandas_atmo(unvalid_raw_data)

def test_full_dataframe(raw_data):
    dataframe = raw_to_pandas_atmo(raw_data)
    assert len(dataframe.columns) == 8
    for i, day_data in enumerate(raw_data["data"]):
        day_df = dataframe.iloc[i]
        assert day_df["time"] == _str_to_datetime(day_data["date_echeance"])
        assert day_df["pollution_index"] == day_data["indice"]
        assert day_df["is_value_mesured"] == _is_value_mesured(day_data["type_valeur"])
        assert day_df["PM10_index"] == day_data["sous_indices"][0]["indice"]
        assert day_df["PM2_5_index"] == day_data["sous_indices"][1]["indice"]
        assert day_df["O3_index"] == day_data["sous_indices"][2]["indice"]
        assert day_df["NO2_index"] == day_data["sous_indices"][3]["indice"]
        assert day_df["SO2_index"] == day_data["sous_indices"][4]["indice"]
