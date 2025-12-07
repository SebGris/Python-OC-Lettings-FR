"""
Tests for the lettings application views.

This module contains integration tests for the lettings views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLettingsIndexView:
    """Tests for the lettings index view."""

    def test_index_status_code(self, client):
        """
        Test that the lettings index page returns a 200 status code.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("lettings:index"))
        assert response.status_code == 200

    def test_index_template(self, client):
        """
        Test that the lettings index uses the correct template.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("lettings:index"))
        assert "lettings/index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestLettingDetailView:
    """Tests for the letting detail view."""

    def test_letting_status_code(self, client, letting):
        """
        Test that a letting detail page returns a 200 status code.

        Args:
            client: The Django test client.
            letting: The letting fixture.
        """
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert response.status_code == 200

    def test_letting_template(self, client, letting):
        """
        Test that the letting detail uses the correct template.

        Args:
            client: The Django test client.
            letting: The letting fixture.
        """
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert "lettings/letting.html" in [t.name for t in response.templates]

    def test_letting_context(self, client, letting):
        """
        Test that the letting detail context contains the correct data.

        Args:
            client: The Django test client.
            letting: The letting fixture.
        """
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert response.context["title"] == "Test Letting"
        assert response.context["address"].city == "Springfield"
