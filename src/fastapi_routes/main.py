from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi_routes.requests import raw, count

from orm.ligne import Ligne 
from orm.trr import Trr
from orm.openmeteo import OpenMeto
from orm.atmo import Atmo

import os
from markdown import markdown

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_api_doc():
    PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
    api_doc_path = os.path.join(PROJECT_PATH, "docs", "api.md")
    template_path = os.path.join(PROJECT_PATH, "templates", "api.html")
    stylesheet_path = os.path.join(PROJECT_PATH, "templates", "api.css")
    with open(api_doc_path) as file:
        documentation = markdown(file.read(), extensions=["fenced_code"])
    with open(template_path) as file:
        template = file.read()
    with open(stylesheet_path) as file:
        stylesheet = file.read()
    html = template.replace("{{ stylesheet }}", stylesheet).replace(
        "{{ documentation }}", documentation
    )
    return html

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


