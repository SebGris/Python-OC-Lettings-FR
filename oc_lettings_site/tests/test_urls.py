"""
Tests for the oc_lettings_site application URLs.

This module contains tests for URL resolution in the main site.
"""
import pytest
from django.urls import reverse, resolve

from oc_lettings_site import views


@pytest.mark.django_db
class TestMainUrls:
    """Tests for the main site URL configuration."""

    def test_index_url_resolves(self):
        """Test that the index URL resolves to the correct view."""
        url = reverse("index")
        assert resolve(url).func == views.index

    def test_index_url_path(self):
        """Test that the index URL has the correct path."""
        url = reverse("index")
        assert url == "/"
