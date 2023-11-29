# Data Api

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
data-api # or python -m src
```
<br>

### Running with Docker

```
docker network create my-network
```
```
docker build -t data-api .
```
```
docker run --name data-api -dp 8080:8080 --network my-network --network-alias data-api data-api
```
<br>

## Database

**Postgres**
```
docker run --name data-api-db -dp 5436:5432 --network my-network --network-alias my-db -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=data-api postgis/postgis:16-3.4
```
<br>

**Migrations**
```
alembic upgrade head
```
<br>

## Keycloak
```
docker run --name keycloak -dp 8081:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:22.0.5 start-dev
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
docker run --name test-db -dp 5437:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=test postgis/postgis:16-3.4
```
