# SearchLab

Django REST Framework + Elasticsearch product search demo. Includes PostgreSQL, Redis, a CSV data loader, a JSON search API, and a browser UI for live testing.

## Folder structure

```
searchlab/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml      # searchlab, db, redis, elasticsearch
├── MOCK_DATA.csv
├── .env.example
├── .gitignore
├── README.md
├── searchlab/              # Django project settings / URLs
├── product/                # Models, documents, API, search UI template
├── utils/                  # CSV loader + Elasticsearch helpers
└── venv/                   # Local virtual environment (gitignored)
```

## Prerequisites

- Python 3.12+ (local venv; Docker image uses 3.12)
- Docker Desktop (or Docker Engine + Compose)

## Environment

```bash
cp .env.example .env
```

| Variable | Purpose |
|----------|---------|
| `DJANGO_SECRET_KEY` | Django secret |
| `DJANGO_DEBUG` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts |
| `DB_*` | Postgres credentials (used when `DB_HOST` is set) |
| `REDIS_URL` | Redis URL (host-mapped default for local tools) |
| `ELASTICSEARCH_HOST` | Elasticsearch URL |

`DB_HOST` is injected by Docker Compose for the app service. Leave it unset for local SQLite.

## Docker setup (recommended)

Host ports are remapped so they do not clash with other local projects:

| Service | Role | Host port |
|---------|------|-----------|
| `searchlab` | Django app + search UI | **8001** |
| `db` | PostgreSQL 16 | **5433** |
| `redis` | Redis 7 | **6380** |
| `elasticsearch` | Elasticsearch 8.15 | **9201** |

```bash
cp .env.example .env
docker compose up --build -d
```

Load products + create superuser:

```bash
docker compose exec searchlab python utils/load_mock_data.py
```

Build / rebuild the Elasticsearch index:

```bash
docker compose exec searchlab python manage.py search_index --rebuild -f
```

Useful commands:

```bash
docker compose logs -f searchlab
docker compose exec searchlab bash
docker compose down
```

**Code changes:** the project root is mounted at `/app`, and Django `runserver` auto-reloads. You do **not** need `docker compose up --build` for normal `.py` / template edits. Rebuild only when `requirements.txt` or the `Dockerfile` change. After changing indexed fields in `product/documents.py`, run `search_index --rebuild -f` again.

## URLs (Docker)

| Page / endpoint | URL |
|-----------------|-----|
| Search UI | http://127.0.0.1:8001/ |
| Search API | http://127.0.0.1:8001/api/products/?search=beef |
| Health | http://127.0.0.1:8001/api/products/health/ |
| Admin | http://127.0.0.1:8001/admin/ (`admin` / `1234`) |

The search UI calls the API as you type (debounced). The API matches whole words, prefixes while typing, and substring contains across `product_name` and `description`.

## Local setup (virtual environment)

```bash
python -m venv venv
source venv/bin/activate          # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Without Docker, Django uses **SQLite** when `DB_HOST` is unset. Point `ELASTICSEARCH_HOST` / `REDIS_URL` at services you have running (or use the Docker host ports above).

```bash
python manage.py migrate
python utils/load_mock_data.py
python manage.py search_index --rebuild -f
python manage.py runserver
```

Local default URLs use port **8000** unless you change them.

## Product model

| Field | Type | CSV column |
|-------|------|------------|
| `product_name` | CharField | product_name |
| `price` | DecimalField | price |
| `description` | TextField | description |

## Elasticsearch document

Defined in `product/documents.py` (index name: `products`). Indexed fields: `product_name`, `description`, `price`.

`django-elasticsearch-dsl` only auto-discovers `documents.py` inside apps listed in `INSTALLED_APPS` — keep documents under `product/`, not a non-app folder.
