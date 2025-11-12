"""App configuration for todoapp."""
from django.apps import AppConfig


class TodoappConfig(AppConfig):
    """Configuration for todoapp."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todoapp'
