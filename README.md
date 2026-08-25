# M-Tram
A data engineering project from Grenoble's public APIs. The aim of this project is to monitor traffic trends in Grenoble for retrospective analysis.

## Architecture
### Pipeline structure :
Data sources → Airflow → Python ETL → PostgreSQL → FastAPI → dashboard

## Config
The script [``scripts/generate_export.env.sh``](scripts/generate_export.env.sh) provides a basic configuration for your .env file, including random passwords. If you want to configure it further, feel free to modify the corresponding variables in the .env file.

Otherwise, the script is all you need to launch a preconfigured project. Refer to the Airflow and PostgreSQL documentation for the variables. 

## Installation

### Complete setup (initial launch)
- ``source scripts/generate_export.env.sh``
- ``./scripts/docker-compose.sh``

### Subsequent launches:
- ``./scripts/docker-compose.sh``