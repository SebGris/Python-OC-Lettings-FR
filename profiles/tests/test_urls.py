"""
Tests for the profiles application URLs.

This module contains tests for URL resolution in the profiles app.
"""
import pytest
from django.urls import reverse, resolve

from profiles import views


@pytest.mark.django_db
class TestProfilesUrls:
    """Tests for the profiles URL configuration."""

    def test_index_url_resolves(self):
        """Test that the profiles index URL resolves to the correct view."""
        url = reverse("profiles:index")
        assert resolve(url).func == views.index

    def test_profile_url_resolves(self):
        """Test that the profile detail URL resolves to the correct view."""
        url = reverse("profiles:profile", args=["testuser"])
        assert resolve(url).func == views.profile

    def test_index_url_path(self):
        """Test that the profiles index URL has the correct path."""
        url = reverse("profiles:index")
        assert url == "/profiles/"

    def test_profile_url_path(self):
        """Test that the profile detail URL has the correct path."""
        url = reverse("profiles:profile", args=["testuser"])
        assert url == "/profiles/testuser/"
