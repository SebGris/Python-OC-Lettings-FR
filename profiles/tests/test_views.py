"""
Tests for the profiles application views.

This module contains integration tests for the profiles views.
"""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestProfilesIndexView:
    """Tests for the profiles index view."""

    def test_index_status_code(self, client):
        """
        Test that the profiles index page returns a 200 status code.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("profiles:index"))
        assert response.status_code == 200

    def test_index_template(self, client):
        """
        Test that the profiles index uses the correct template.

        Args:
            client: The Django test client.
        """
        response = client.get(reverse("profiles:index"))
        assert "profiles/index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestProfileDetailView:
    """Tests for the profile detail view."""

    def test_profile_status_code(self, client, profile):
        """
        Test that a profile detail page returns a 200 status code.

        Args:
            client: The Django test client.
            profile: The profile fixture.
        """
        response = client.get(
            reverse("profiles:profile", args=[profile.user.username])
        )
        assert response.status_code == 200

    def test_profile_template(self, client, profile):
        """
        Test that the profile detail uses the correct template.

        Args:
            client: The Django test client.
            profile: The profile fixture.
        """
        response = client.get(
            reverse("profiles:profile", args=[profile.user.username])
        )
        assert "profiles/profile.html" in [t.name for t in response.templates]

    def test_profile_context(self, client, profile):
        """
        Test that the profile detail context contains the correct data.

        Args:
            client: The Django test client.
            profile: The profile fixture.
        """
        response = client.get(
            reverse("profiles:profile", args=[profile.user.username])
        )
        assert response.context["profile"].user.username == "testuser"
        assert response.context["profile"].favorite_city == "Paris"
