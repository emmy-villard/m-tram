from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi_routes.requests import raw, count, markdown, aggregate

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def get_api_doc():
    return markdown.get_doc("api.md")

@app.get("/schema.md", response_class=HTMLResponse)
def get_schema_doc():
    return markdown.get_doc("schema.md")

@app.get("/source.md", response_class=HTMLResponse)
def get_source_doc():
    return markdown.get_doc("source.md")

@app.get("/count")
def get_count():
    return count.get_data()

@app.get("/raw/{table_name}")
def get_raw_data(table_name: str):
    return raw.get_data(table_name)

@app.get("/aggregate/{aggregate_period}")
def get_aggregate(aggregate_period: str):
    return aggregate.get_data(aggregate_period)
