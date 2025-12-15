"""
WSGI configuration for the OC Lettings project.

This module exposes the WSGI callable as a module-level variable named 'application'.
It is used for deploying the application with WSGI-compatible servers like Gunicorn.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")

application = get_wsgi_application()
