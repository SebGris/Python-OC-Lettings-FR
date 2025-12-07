"""
Tests for the lettings application URLs.

This module contains tests for URL resolution in the lettings app.
"""
import pytest
from django.urls import reverse, resolve

from lettings import views


@pytest.mark.django_db
class TestLettingsUrls:
    """Tests for the lettings URL configuration."""

    def test_index_url_resolves(self):
        """Test that the lettings index URL resolves to the correct view."""
        url = reverse("lettings:index")
        assert resolve(url).func == views.index

    def test_letting_url_resolves(self):
        """Test that the letting detail URL resolves to the correct view."""
        url = reverse("lettings:letting", args=[1])
        assert resolve(url).func == views.letting

    def test_index_url_path(self):
        """Test that the lettings index URL has the correct path."""
        url = reverse("lettings:index")
        assert url == "/lettings/"

    def test_letting_url_path(self):
        """Test that the letting detail URL has the correct path."""
        url = reverse("lettings:letting", args=[1])
        assert url == "/lettings/1/"
