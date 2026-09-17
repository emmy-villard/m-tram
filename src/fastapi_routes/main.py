from fastapi import FastAPI
from fastapi_routes.requests import trr
from fastapi_routes.requests import atmo, ligne, openmeteo
from fastapi_routes.requests import count

app = FastAPI()


@app.get("/count")
def get_count():
    return count.get_data()

@app.get("/raw/ligne")
def get_raw_line():
    return ligne.get_raw_data()

@app.get("/raw/trr")
def get_raw_trr():
    return trr.get_raw_data()

@app.get("/raw/atmo")
def get_raw_atmo():
    return atmo.get_raw_data()

@app.get("/raw/openmeteo")
def get_raw_openmeteo():
    return openmeteo.get_raw_data()


