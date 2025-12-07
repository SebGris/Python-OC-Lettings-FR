"""
Tests for the oc_lettings_site application views.

This module contains integration tests for the main site views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestIndexView:
    """Tests for the main site index view."""

    def test_index_status_code(self, client):
        """
        Test that the home page returns a 200 status code.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("index"))
        assert response.status_code == 200

    def test_index_template(self, client):
        """
        Test that the home page uses the correct template.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("index"))
        assert "index.html" in [t.name for t in response.templates]
