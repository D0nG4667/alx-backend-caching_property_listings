# ALX Backend Caching - Property Listings

A Django-based property listing application featuring integrated caching with Redis and a PostgreSQL database backend, both containerized using Docker.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [uv](https://github.com/astral-sh/uv) (Python package installer and resolver)

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd alx-backend-caching_property_listings
   ```

2. **Start Docker Services:**
   This project uses Docker for PostgreSQL and Redis. To avoid conflicts with local services, PostgreSQL is mapped to host port `5433` and Redis to host port `6380`.
   ```bash
   docker-compose up -d
   ```

3. **Install Dependencies:**
   Using `uv` to install requirements:
   ```bash
   uv sync
   ```

4. **Run Migrations:**
   ```bash
   uv run python manage.py migrate
   ```

5. **Start the Development Server:**
   ```bash
   uv run python manage.py runserver
   ```

## Configuration Details

- **Database:** PostgreSQL (mapped to `localhost:5433` on host)
- **Cache:** Redis (mapped to `localhost:6380` on host)
- **Framework:** Django 6.0+

## Verification

To verify the setup, you can run the following command to test Redis connectivity:
```bash
uv run python manage.py shell -c "from django.core.cache import cache; cache.set('test', 'success'); print('Cache connected:', cache.get('test'))"
```
