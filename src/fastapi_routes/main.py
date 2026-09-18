from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi_routes.requests import raw, count, markdown

from orm.ligne import Ligne 
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_api_doc():
    return markdown.get_doc("api.md")

@app.get("/schema.md", response_class=HTMLResponse)
def get_schema_doc():
    return markdown.get_doc("schema.md")

@app.get("/count")
def get_count():
    return count.get_data()

@app.get("/raw/ligne")
def get_raw_line():
    return raw.get_data(Ligne)

@app.get("/raw/trr")
def get_raw_trr():
    return raw.get_data(Trr)

@app.get("/raw/atmo")
def get_raw_atmo():
    return raw.get_data(Atmo)

@app.get("/raw/openmeteo")
def get_raw_openmeteo():
    return raw.get_data(OpenMeto)


