"""
URL configuration for the Orange County Lettings project.

This module defines the URL patterns for the main application,
including routes to the home page, lettings, profiles, and admin interface.
"""
from django.contrib import admin
from django.urls import path, include

from . import views


def test_500(request):
    """
    Test view to trigger a 500 error page.

    Args:
        request: The HTTP request object.

    Raises:
        Exception: Always raises an exception to test error handling.
    """
    raise Exception("Test 500 error")


urlpatterns = [
    path("", views.index, name="index"),
    path("lettings/", include("lettings.urls")),
    path("profiles/", include("profiles.urls")),
    path("admin/", admin.site.urls),
    path("test-500/", test_500),
]
