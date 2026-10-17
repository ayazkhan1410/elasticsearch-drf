# SearchLab

Beginner-friendly Django REST Framework starter for learning Elasticsearch step by step.

This stage sets up a clean flat project with Docker (PostgreSQL + Redis), a `Product` model, admin, and a CSV loader. Elasticsearch is **not** installed yet.

## Folder structure

```
searchlab/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml      # Services: searchlab, db, redis
├── MOCK_DATA.csv
├── .env.example
├── .gitignore
├── README.md
├── searchlab/              # Django project settings / URLs
├── product/                # Product app (models, admin, API)
├── utils/                  # Helpers + CSV load script
└── venv/                   # Local virtual environment (gitignored)
```

## Prerequisites

- Python 3.12+ (local venv; Docker image uses 3.12)
- Docker Desktop

## Local setup (virtual environment)

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Without Docker, Django uses **SQLite** when `DB_HOST` is unset. For local SQLite, temporarily comment out or remove `DB_HOST` from `.env`, or rename `.env` while developing locally.

### Migrations

```powershell
python manage.py migrate
```

### Load mock products + create superuser

```powershell
python utils/load_mock_data.py
```

This will:

- Create/update superuser: username `admin`, password `1234`
- Insert rows from `MOCK_DATA.csv` into the `Product` table

### Run the development server

```powershell
python manage.py runserver
```

- Admin: http://127.0.0.1:8000/admin/ (`admin` / `1234`)
- Health: http://127.0.0.1:8000/api/product/health/

## Docker setup (recommended)

1. Start **Docker Desktop** and wait until it is ready.
2. From the project root:

```powershell
copy .env.example .env
docker compose up --build
```

| Service     | Role                         | Port |
|-------------|------------------------------|------|
| `searchlab`     | Django REST API           | 8000 |
| `db`            | PostgreSQL 16             | 5432 |
| `redis`         | Redis 7                   | 6379 |
| `elasticsearch` | Elasticsearch 8.15        | 9200 |

3. In another terminal, load data into the Docker database:

```powershell
docker compose exec searchlab python utils/load_mock_data.py
```

4. Open http://127.0.0.1:8000/api/product/health/

Useful commands:

```powershell
docker compose down
docker compose logs -f searchlab
docker compose exec searchlab python manage.py migrate
```

## Product model fields

| Field          | Type           | CSV column     |
|----------------|----------------|----------------|
| `product_name` | CharField      | product_name   |
| `price`        | DecimalField   | price          |
| `description`  | TextField      | description    |

## What’s next

Elasticsearch packages, indexing, and search endpoints will be added later.
