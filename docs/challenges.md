# Challenges
This file lists the main challenges I encountered while working on this project

## Understanding How APIs Work
The Grenoble traffic API is particularly poorly documented, and I had to do a bit of simple reverse engineering to figure out what data I needed and how to get it.

## Handling Data Loading and Database Integration
I had to progressively move from a simple ETL prototype to a reliable PostgreSQL loading process. This involved reorganizing the project modules, introducing SQLAlchemy ORM models, validating database environment variables, and making sure that inserts were committed correctly.

Running integration tests was also challenging because the application and the tests needed separate database engines and configurations. I created a dedicated test database, added database setup and teardown fixtures, and adjusted the PostgreSQL version, healthcheck, and test port so that the tests could run consistently both locally and in GitHub Actions.

## Managing Installations
I had to ensure that the installations were reproducible—whether they were Python packages or Docker images—so that I could easily deploy my application and run automated tests via GitHub Actions. Airflow made this more complicated because its dependencies are large and version-sensitive. I had to adjust the dependency files, Dockerfiles, and constraints before the application could be built reliably and the DAGs could be imported successfully.

## Docker Compose
I had to adapt the YAML template provided by Airflow by defining variables that I generate automatically in `.env`. Several details required careful adjustment: project paths, internal and external ports, the database connection variable expected by Airflow, and the distinction between the application database and the test database.

I also had to make sure that all volumes were properly mounted and secure the installations to prevent losing my database during application updates. This led to adding a persistent database volume and protecting the generated `.env` file from being overwritten accidentally.

## Orchestrating the ETL with Airflow
Integrating the two ETL pipelines into Airflow required more than just writing the DAGs. I first had to create the Airflow project structure, configure the Docker services, resolve the dependencies needed to parse the DAG files, and make the application available at the expected internal port. Only after these pieces were aligned could I implement the DAGs. I then added airflow dag tests to ensure they actually write in the database, and keep doing it with every push.

## Handling Partial and Invalid API Data
A recurring issue on this branch was that some upstream responses were incomplete, inconsistent, or contained values that had to be rejected rather than loaded as-is. This affected the MData traffic payloads and the newer weather/air-quality sources, where a few rows could be missing a field, contain an unexpected value type, or be structurally incomplete.

I had to refine the transformation logic so that invalid rows were skipped explicitly instead of silently corrupting the database. This required tightening the parsing rules, adding validation checks in the transformation layer, and making sure the resulting DataFrames still remained usable for production loads. The work culminated in a clearer "drop invalid rows gracefully" pattern, which is now reflected in the ETL transform coverage and the validation tests.

## Adding New Environmental Data Sources
The project expanded from the first traffic-only ETL to a richer environmental monitoring pipeline, including OpenMeteo and ATMO. Each of these sources had different response structures, date formats, and validation constraints, which made the ETL more complex than the original MData ingestion.

The main challenge was to normalize these APIs into a consistent relational model while preserving the historical time-series logic used by the traffic tables. This meant designing a reusable transformation and validation structure, handling different scale and units, and ensuring duplicate timestamps were rejected before insertion.

## Strengthening Validation and Test Coverage
Once the project included more sources and more external data, it became critical to validate data before inserting it into PostgreSQL. I added Pydantic schemas for the new datasets, checked that the DataFrames were not empty, verified that timestamps were unique, and filtered out rows that would violate database constraints.

This work was paired with dedicated tests for the transformed DataFrames and the Airflow DAGs. It was especially important to validate the ETL end-to-end because the edge cases were often low-probability but high-impact: a missing pollutant index, a partial weather payload, or an unexpected API response shape could otherwise break the load process.

## Launching the app
A docker-compose that launched with no issues on my local machine started breaking in my VPS. The API server started up slowly, and then the workers eventually failed without completing a single task. I solved this problem by upgrading my VPS server, which didn't have enough capacity to run Airflow properly.