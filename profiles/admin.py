"""
Admin configuration for the profiles application.

This module registers the Profile model with the Django admin site.
"""
from django.contrib import admin

from .models import Profile


admin.site.register(Profile)
