import logging
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def get_redis_cache_metrics():
    """
    Retrieves and analyzes Redis cache hit/miss metrics.
    Returns a dictionary with hits, misses, and hit ratio.
    """
    try:
        r = get_redis_connection("default")
        info = r.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total_requests = hits + misses
        hit_ratio = (hits / total_requests) if total_requests > 0 else 0

        metrics = {"hits": hits, "misses": misses, "hit_ratio": round(hit_ratio, 4)}

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}


def get_all_properties():
    """
    Fetches all properties from Redis cache if available,
    otherwise fetches from the database and caches the result.
    """
    cache_key = "all_properties"
    properties = cache.get(cache_key)

    if properties is None:
        # Cache miss, fetch from database
        properties = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set(cache_key, properties, 3600)

    return properties
