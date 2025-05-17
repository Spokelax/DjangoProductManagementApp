from django.apps import AppConfig
from django_asgi_lifespan.register import register_lifespan_manager

from .context import httpx_lifespan_manager


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "DjangoProductManagementApp.inventory"

    def ready(self):
        register_lifespan_manager(context_manager=httpx_lifespan_manager)
