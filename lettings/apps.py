"""
App configuration for the lettings application.
"""
from django.apps import AppConfig


class LettingsConfig(AppConfig):
    """Django application configuration for the lettings app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lettings'
