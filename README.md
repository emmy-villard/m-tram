# M-Tram
A data engineering project from Grenoble's public APIs. The aim of this project is to monitor traffic trends in Grenoble for retrospective analysis.

## Architecture
### Pipeline structure :
Data sources → Airflow → Python ETL → PostgreSQL → FastAPI → dashboard

## Installation

### Complete setup (initial launch)
- ``source scripts/generate_export.env.sh``
- ``./scripts/docker-compose.sh``

### Subsequent launches:
- ``./scripts/docker-compose.sh``
