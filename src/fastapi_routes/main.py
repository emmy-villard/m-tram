from fastapi import FastAPI
from fastapi_routes.raw import atmo, ligne, openmeteo, trr

app = FastAPI()

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


