from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property


@receiver(post_save, sender=Property)
@receiver(post_delete, sender=Property)
def invalidate_property_cache(sender, instance, **kwargs):
    """
    Invalidates the 'all_properties' cache whenever a Property
    is created, updated, or deleted.
    """
    cache.delete("all_properties")
