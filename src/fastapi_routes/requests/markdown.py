import os
from markdown import markdown

def get_doc(filename: str):
    PROJECT_PATH = os.getcwd()
    file_doc_path = os.path.join(PROJECT_PATH, "docs", filename)
    template_path = os.path.join(PROJECT_PATH, "templates", "api.html")
    stylesheet_path = os.path.join(PROJECT_PATH, "templates", "api.css")
    with open(file_doc_path) as file:
        documentation = markdown(file.read(), extensions=["fenced_code"])
    with open(template_path) as file:
        template = file.read()
    with open(stylesheet_path) as file:
        stylesheet = file.read()
    html = template.replace("{{ stylesheet }}", stylesheet).replace(
        "{{ documentation }}", documentation
    )
    return html