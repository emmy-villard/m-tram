# Modules
This document compiles the main building blocks of the project and their responsibilities.

## db_connection
This package centralizes the database connection and engine management used by the ETL and ORM layers. It exposes the SQLAlchemy engine used to connect to the PostgreSQL instance and is the main entry point for all persistence operations.

## etl
The ETL package contains the extraction, transformation, validation, and loading logic for each source. It is split into subpackages that reflect the lifecycle of the data:

- `etl.extract`: endpoint URL construction, API-key retrieval, and source-specific fetch helpers.
- `etl.transform`: normalization of raw JSON payloads into pandas DataFrames ready for database insertion.
- `etl.validation_schemas`: Pydantic models used to validate the structure and ranges of each dataset before insertion.
- `etl.classes`: source-oriented wrappers implementing the common `Data` interface for each dataset.

The current sources handled by this layer are:
- `trr` and `ligne` from MData
- `openmeteo` from Open-Meteo
- `atmo` from ATMO Auvergne-Rhône-Alpes

## orm
The ORM package defines the SQLAlchemy models representing each table in PostgreSQL. These classes are used by the ETL loaders to insert validated rows with typed columns and primary keys.

Current model classes include:
- `Trr`
- `Ligne`
- `OpenMeto`
- `Atmo`

## airflow
The `airflow/dags` directory contains deployment-ready DAGs used to orchestrate periodic ETL runs. The project includes DAGs for:
- `etl_trr.py`
- `etl_ligne.py`
- `etl_meteo.py`
- `etl_atmo.py`

Each DAG follows the same pattern: extract the raw payload, transform it, validate it, and then load the prepared DataFrame into the database.

## util
Utilities for date parsing, environment configuration, and URL management. These helpers are used in the ETL and configuration layers to keep the ingestion code reusable and environment-independent.

## tests
Although not a runtime module, the test suite validates the transformation and integration logic for each workflow. It covers ingestion contracts, schema validation, and database-level behavior across the ETL pipeline.