"""
App configuration for the profiles application.
"""
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Django application configuration for the profiles app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
