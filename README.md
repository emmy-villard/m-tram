# M-Tram

**An end-to-end data engineering project for exploring Grenoble traffic alongside weather and air quality.**

M-Tram collects and archives more than 139,000 source records per day from public APIs, validates and stores them as historical time series, and exposes the data through a read-only API and an exploratory dashboard.

[Live API](https://api.m-tram.emmyvillard.fr) · [API documentation](docs/api.md) · [Dashboard documentation](docs/dashboard.md) · [Database schema](docs/schema.md) · [Data sources](docs/source.md)

## At a glance

| Area | Tools |
| --- | --- |
| Orchestration | Apache Airflow with CeleryExecutor |
| Ingestion and transformation | Python, pandas, Pydantic |
| Storage and migrations | PostgreSQL, SQLAlchemy, Alembic |
| Data access and exploration | FastAPI, Streamlit |
| Packaging and delivery | Docker Compose, GitHub Actions, pytest |

## Data pipeline

The pipeline combines three public sources:

- **MData**: Grenoble road (`trr`) and tram-line (`ligne`) traffic snapshots, collected every five minutes.
- **Open-Meteo**: hourly weather observations, loaded daily.
- **ATMO Auvergne-Rhône-Alpes**: daily air-quality and pollutant indices, loaded daily.

Each source follows an extract → transform → validate → load workflow. Airflow DAGs orchestrate the source-specific schedules and retry failed tasks. The pipeline converts API payloads into tabular records, validates them before persistence, and stores the source time series in PostgreSQL. A separate daily job prepares hourly aggregates for the API and dashboard.

![M-Tram data architecture](docs/img/architecture_schema.svg)


## Engineering highlights

- **Data quality:** Pydantic schemas validate required fields, types, allowed values and realistic ranges. Transformations explicitly filter unusable or incomplete source records; validation failures stop the load rather than persisting invalid rows.
- **Relational modeling:** source-specific tables use timestamp-based primary keys; SQLAlchemy defines the models and Alembic tracks schema changes.
- **Orchestration:** separate Airflow DAGs handle traffic, weather, air quality and aggregate refreshes. Source DAGs retry failed tasks, and the aggregate table supports both incremental daily updates and a manual full refresh.
- **Data serving:** the FastAPI API provides record counts, read-only access to source tables and precomputed hourly aggregates. The Streamlit dashboard fetches those aggregates from the API and filters them in memory.
- **Testing and delivery:** GitHub Actions runs unit/integration tests and Airflow DAG tests on pushes. A separate workflow deploys pushes to `main` to a VPS using Docker Compose.

## API and dashboard

The API is read-only and currently provides:

- `GET /count` — row counts by dataset.
- `GET /raw/{table_name}` — raw rows from `ligne`, `trr`, `openmeteo` or `atmo`.
- `GET /aggregate/{period}` — hourly traffic and environmental aggregates for a supported period.

The dashboard compares tram or road congestion with air-quality indices and weather metrics. It supports date-range, weekday and time-of-day filters. Air-quality indices are daily values associated with the corresponding hours; the dashboard is intended for exploration, not causal inference.

See the [API guide](docs/api.md) and [dashboard guide](docs/dashboard.md) for endpoint details and behavior.

## Scope and limitations

This is a portfolio project for collecting, validating and exploring public time-series data, not a production-grade monitoring platform: it does not promise service-level guarantees, operational alerting or complete data-coverage checks. Source and aggregate DAGs run on independent schedules, so the aggregate refresh assumes that source loads have completed; that ordering is not enforced by DAG dependencies. The dashboard is exploratory, and the analysis so far has not shown a significant correlation between congestion and the environmental measures studied.

## Local demo

The demo starts PostgreSQL, the API and the dashboard in Docker, filled with **generated sample hourly aggregates** (60 days of synthetic data). It does not run Airflow or call the public APIs, so no API key is needed. Requirements: Linux, Docker with the Compose plugin, Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
source scripts/tests/run_streamlit.sh
```

Then open the dashboard at <http://localhost:8501>; the API is available at <http://localhost:8081>. The sample data is synthetic: the dashboard's correlations are only meant to show how it works, not real findings.

To stop the demo: `docker compose -f scripts/tests/docker-compose-test.yml --env-file .env.test down -v`.

## Tests

```bash
source .venv/bin/activate
source scripts/tests/setup-test-env.sh
pytest
```

## Deploy on a VPS

This is the full path from a fresh clone to a running instance, using the same setup as the live demo: a Linux VPS running the whole Docker Compose stack, behind a reverse proxy that serves HTTPS, and continuous deployment from GitHub Actions on every push to `main`.

### 1. Prerequisites

- A Linux VPS with **8 GB of RAM recommended** (Airflow warns below 4 GB, and workers failed on an under-sized VPS during development), a few GB of free disk, and a user able to run Docker without `sudo`.
- Three DNS `A` records pointing to the VPS, for example `api.example.com`, `dashboard.example.com` and `airflow.example.com`.
- Ports 80 and 443 open in the VPS firewall, and SSH access.
- A free [ATMO API key](https://api.atmo-aura.fr/register).
- Your own copy of the repository on GitHub (fork it, since you need to add secrets and a deploy key).

### 2. Prepare the VPS

Install Docker Engine with the Compose plugin ([official guide](https://docs.docker.com/engine/install/)), then allow your user to run it:

```bash
sudo usermod -aG docker "$USER"   # log out and back in afterwards
docker compose version
```

**Reverse proxy.** The Compose file does not start a proxy: it joins the external Docker network `proxy_net` and sets `VIRTUAL_HOST` / `ACME_HOST` on the API, dashboard and Airflow UI containers. Run an [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy) stack with its [ACME companion](https://github.com/nginx-proxy/acme-companion) (automatic Let's Encrypt certificates) attached to that network. Check in the companion documentation which variable name your version reads (`ACME_HOST` or `LETSENCRYPT_HOST`) and adjust [`docker-compose.yml`](docker-compose.yml) if needed. The network must exist before the first deployment:

```bash
docker network create proxy_net
```

### 3. Let the VPS pull the repository (deploy key)

The deployment script runs `git pull` on the VPS, so the VPS needs read access to your repository. On the VPS, create a key **without a passphrase** (`ssh-add` runs non-interactively in the workflow):

```bash
ssh-keygen -t ed25519 -N "" -f ~/.ssh/mtram_deploy -C "mtram-vps-deploy"
cat ~/.ssh/mtram_deploy.pub
```

Add the printed public key in GitHub under *your repository → Settings → Deploy keys → Add deploy key* (read-only is enough). Then clone the repository **at the exact location the workflow uses**, `~/projects/m-tram`, over SSH:

```bash
mkdir -p ~/projects && cd ~/projects
GIT_SSH_COMMAND="ssh -i ~/.ssh/mtram_deploy -o IdentitiesOnly=yes" \
  git clone git@github.com:<your-user>/m-tram.git
cd m-tram
git config core.sshCommand "ssh -i ~/.ssh/mtram_deploy -o IdentitiesOnly=yes"
mkdir -p db_backups
```

The absolute path of the private key (for example `/home/<vps-user>/.ssh/mtram_deploy`) is the value of the `SSH_FILE_PATH` secret below.

### 4. Let GitHub Actions connect to the VPS

On **your own machine**, create a second key pair dedicated to the CI, and authorize its public part on the VPS:

```bash
ssh-keygen -t ed25519 -N "" -f ./mtram_ci -C "github-actions-mtram"
ssh-copy-id -i ./mtram_ci.pub <vps-user>@<vps-host>
ssh -i ./mtram_ci <vps-user>@<vps-host> 'echo ok'   # must print "ok"
cat ./mtram_ci                                      # content of the VPS_SSH_KEY secret
```

Store the private key only in the GitHub secret, then delete the local files (`shred -u mtram_ci mtram_ci.pub`).

### 5. Define the GitHub Actions secrets

Go to *Settings → Secrets and variables → Actions → New repository secret*. Use **repository** secrets: the test workflow needs the application secrets too, and secrets stored only in the `production` environment are not visible to it.

| Secret | Value |
| --- | --- |
| `VPS_HOST` | VPS IP address or hostname |
| `VPS_USER` | SSH user on the VPS |
| `VPS_SSH_KEY` | full content of the private key `mtram_ci` |
| `SSH_FILE_PATH` | absolute path of the deploy key on the VPS (`/home/<vps-user>/.ssh/mtram_deploy`) |
| `ATMO_API_KEY` | your ATMO API key |
| `POSTGRES_PASSWORD` | random password of the application database |
| `AIRFLOW_PASSWORD` | random password of the Airflow metadata database |
| `FERNET_KEY` | Airflow Fernet key (see below) |
| `AIRFLOW__API_AUTH__JWT_SECRET` | random secret signing Airflow API tokens |
| `AIRFLOW__API_AUTH__JWT_ISSUER` | any identifier, for example `mtram` |
| `_AIRFLOW_WWW_USER_USERNAME` | Airflow UI admin login |
| `_AIRFLOW_WWW_USER_PASSWORD` | Airflow UI admin password |
| `API_PROD_URL` | API hostname, for example `api.example.com` |
| `DASHBOARD_PROD_URL` | dashboard hostname, for example `dashboard.example.com` |
| `AIRFLOW_APISERVER_PROD_URL` | Airflow UI hostname, for example `airflow.example.com` |

Generate the random values with:

```bash
openssl rand -hex 24                        # passwords and JWT secret
openssl rand -base64 32 | tr '+/' '-_'      # FERNET_KEY
```

Keep a copy of these values in a password manager. Changing `POSTGRES_PASSWORD` or `AIRFLOW_PASSWORD` after the first deployment will not update the existing database volumes.

The deployment job uses the GitHub environment `production` (created on the first run, or manually under *Settings → Environments*). You can add required reviewers there if you want a manual approval before each deployment.

### 6. Deploy

Push to `main`, or run the workflow manually from the *Actions → Deployment → Run workflow* page. The job connects to the VPS and runs `git pull --ff-only`, prunes unused Docker images and containers (`docker system prune -af`, which keeps volumes), regenerates `.env` with [`scripts/generate_env.sh`](scripts/generate_env.sh), then rebuilds and restarts the services with [`scripts/docker-compose.sh`](scripts/docker-compose.sh). The first build takes several minutes.

To deploy by hand instead, export the same variables on the VPS, set `PROXY_NET_EXTERNAL=true`, and run `./scripts/generate_env.sh && ./scripts/docker-compose.sh` from `~/projects/m-tram`.

### 7. Check that it works

On the VPS:

```bash
docker compose ps                # services should be running or healthy
curl https://api.example.com/count
```

- The API returns row counts (zeros at first), and the dashboard and Airflow UI open on their hostnames. Log in to Airflow with `_AIRFLOW_WWW_USER_USERNAME` / `_AIRFLOW_WWW_USER_PASSWORD`.
- DAGs are unpaused at creation. Traffic is collected every 5 minutes; weather and air quality are loaded daily at 12:00, and the hourly aggregates daily at 13:00.
- The dashboard stays empty until aggregates exist, and an hour is only aggregated when traffic, weather and air-quality data all exist for it. Once the first day is collected, run the aggregation manually, or wait for the next 13:00 run:

```bash
docker compose exec airflow-apiserver airflow dags trigger remake_aggregate_table
```

Past weather and air-quality data can be recovered with the commands documented in the DAG docstrings ([`etl_meteo`](airflow/dags/etl_meteo.py), [`etl_atmo`](airflow/dags/etl_atmo.py)), for example:

```bash
docker compose exec airflow-apiserver airflow dags trigger etl_meteo \
  --conf '{"start_date":"2026-01-01", "end_date":"2026-01-07"}'
```

Past traffic data cannot be recovered: MData only exposes the current state, so the history starts when the pipeline starts.

Database backups can be created with [`scripts/make_backup.sh`](scripts/make_backup.sh), which writes a dump into `db_backups/`.

### Troubleshooting

- **The workflow fails at the SSH step:** check `VPS_HOST`, `VPS_USER` and that the public key of `VPS_SSH_KEY` is in `~/.ssh/authorized_keys` on the VPS.
- **`git pull` fails:** the deploy key is missing on the repository, not at `SSH_FILE_PATH`, or protected by a passphrase.
- **`network proxy_net not found`:** create it with `docker network create proxy_net`.
- **Workers crash or the API server is very slow:** the VPS does not have enough memory for Airflow.
- **No HTTPS certificate:** check that the DNS records resolve to the VPS and that ports 80 and 443 are reachable.

## Further documentation

- [Data transformation and validation](docs/data-transformation.md)
- [Hourly aggregate design and refresh behavior](docs/dashboard-aggregate-table.md)
- [Project modules](docs/modules.md)
- [Implementation challenges](docs/challenges.md)
