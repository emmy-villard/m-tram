# M-Tram
A data engineering project from Grenoble's public APIs. The aim of this project is to monitor traffic trends in Grenoble for retrospective analysis.

## Architecture
### Pipeline structure :
Data sources → Airflow → Python ETL → PostgreSQL → FastAPI → dashboard

## Config
The script [``scripts/generate_export.env.sh``](scripts/generate_export.env.sh) provides a basic configuration for your .env file, including random passwords. If you want to configure it further, feel free to modify the corresponding variables in the .env file.

Otherwise, the script is all you need to launch a preconfigured project. Refer to the Airflow and PostgreSQL documentation for the variables. 

## Installation
### Requirements
- 8GB RAM
- On a linux machine

### Get api keys
- Register to obtain an api-atmo key (free and without delays): https://api.atmo-aura.fr/register
- Assign this key to the `ATMO_API_KEY` variable in the `.env` file
- Paste the API key in a file named "atmo_apikey.txt" in the api_keys folder
### Launch the app (airflow)
- ``source scripts/generate_export.env.sh`` (won't overwrite an existing .env file)
- ``./scripts/docker-compose.sh``

### Local tests:
- ``python3 -m venv .venv``
- ``source .venv/bin/activate``
- ``pytest``
- ``./scripts/docker-compose.sh``