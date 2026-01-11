from django.core.cache import cache
from .models import Property


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
