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

## Caching Strategy

This project implements three levels of caching and monitoring:

1.  **Page-Level Caching**: The `/properties/` endpoint is cached for 15 minutes using the `@cache_page` decorator.
2.  **Low-Level Caching**: The property queryset is cached for 1 hour using Django's low-level cache API (`cache.get`/`cache.set`) in `properties/utils.py`.
3.  **Cache Invalidation**: The `all_properties` cache is automatically invalidated whenever a `Property` is created, updated, or deleted using Django signals (`post_save` and `post_delete`).

## API Endpoints

-   `GET /properties/`: Returns a JSON list of all properties.
    -   **Response Format**: `{"data": [...]}`
    -   **Cache Duration**: 15 minutes (Page), 1 hour (Queryset)

## Performance Monitoring

Developers can monitor cache efficiency using the `get_redis_cache_metrics()` utility in `properties/utils.py`. This function provides:
-   **Hits**: Total successful cache lookups.
-   **Misses**: Total failed cache lookups.
-   **Hit Ratio**: Efficiency percentage updated in real-time.

## Verification

To verify the setup and caching, you can run the following commands:

**1. Test Redis Connectivity:**
```bash
uv run python manage.py shell -c "from django.core.cache import cache; cache.set('test', 'success'); print('Cache connected:', cache.get('test'))"
```

**2. Test Low-Level Cache (Queryset):**
```bash
uv run python manage.py shell -c "from properties.utils import get_all_properties; from django.core.cache import cache; cache.delete('all_properties'); props = get_all_properties(); print('Key saved in Redis:', cache.get('all_properties') is not None)"
```

**3. Test Cache Invalidation (Signals):**
```bash
uv run python manage.py shell -c "from django.core.cache import cache; from properties.utils import get_all_properties; from properties.models import Property; cache.delete('all_properties'); get_all_properties(); print('Cache before creation:', cache.get('all_properties') is not None); Property.objects.create(title='Test Signal', description='Testing', price=100.00, location='Test'); print('Cache after creation:', cache.get('all_properties') is None)"
```

**4. Test Cache Metrics Analysis:**
```bash
uv run python manage.py shell -c "from properties.utils import get_redis_cache_metrics; print('Cache Metrics:', get_redis_cache_metrics())"
```
