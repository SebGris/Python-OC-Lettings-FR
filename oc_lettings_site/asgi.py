"""
ASGI configuration for the Orange County Lettings project.

This module exposes the ASGI callable as a module-level variable named 'application'.
It is used for deploying the application with ASGI-compatible servers.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')

application = get_asgi_application()
