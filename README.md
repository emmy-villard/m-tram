# M-Tram
A data engineering project from Grenoble's public APIs. The aim of this project is to monitor traffic trends in Grenoble for retrospective analysis.

## Architecture
### Pipeline structure :
Data sources → Airflow → Python ETL → PostgreSQL → FastAPI → dashboard

## Installation

### Complete setup (initial launch)
- ``python3 -m venv .venv``
- ``source .venv/bin/activate``
- ``pip3 install -r requirements/prod.txt``
- ``source scripts/dev/setup.sh``

### Subsequent launches:
- ``source scripts/dev/setup.sh``


