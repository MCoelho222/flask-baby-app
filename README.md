# Light Data Api

## Developer

**Create virtual environment**
```
python -m venv .venv
```
<br>

**Activate virtual environment**
```
.venv/Scripts/activate (windows)
```
```
.venv\Scripts\activate.bat (linux)
```
<br>

**Install packages for development**
```
pip install -e .[dev]
```
<br>

**Run**
```shell
light-data-api # or python -m src
```
<br>

### Running with Docker

```
docker network create light-network
```
```
docker build -t light-data-api .
```
```
docker run --name light-data-api -dp 8080:8080 --network light-network --network-alias light-data-api light-data-api
```
<br>

## Database

**Postgres**
```
docker run --name light-db -dp 5436:5432 --network light-network --network-alias light-db -e POSTGRES_PASSWORD=mcoelho -e POSTGRES_USER=mcoelho -e POSTGRES_DB=light postgis/postgis:16-3.4
```
<br>

**Migrations**
```
alembic upgrade head
```
<br>

## Keycloak
```
docker run --name light-keycloak -dp 8081:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:22.0.5 start-dev
```
<br>

## Tests
Change in your .env => FLASK_ENV=testing

```
pytest -p no:warnings
```
<br>

**Postgres**
```
docker run --name light-test-db -dp 5437:5432 -e POSTGRES_PASSWORD=mcoelho -e POSTGRES_USER=mcoelho -e POSTGRES_DB=light-test postgis/postgis:16-3.4
```
