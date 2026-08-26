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

I also had to make sure that all volumes were properly mounted and secure the installations to prevent losing my database during application updates. This led to adding a persistent database volume, ignoring generated Airflow logs, and protecting the generated `.env` file from being overwritten accidentally.

## Orchestrating the ETL with Airflow
Integrating the two ETL pipelines into Airflow required more than just writing the DAGs. I first had to create the Airflow project structure, configure the Docker services, resolve the dependencies needed to parse the DAG files, and make the application available at the expected internal port. Only after these pieces were aligned could I implement the `etl_ligne` and `etl_trr` DAGs.

## Making Pipeline Execution Observable
Once the pipelines were running, it was difficult to tell whether an API request had succeeded or whether data had actually been inserted into PostgreSQL. I added execution logs for API URLs and response codes, as well as the number of rows inserted during loading. This made silent failures, empty responses, and conflicts during database loading easier to investigate.

## Launching the app
A docker-compose that launched with no issues on my local machine started breaking in my VPS. The API server started up slowly, and then the workers eventually failed without completing a single task. I solved this problem by upgrading my VPS server, which didn't have enough capacity to run Airflow properly.