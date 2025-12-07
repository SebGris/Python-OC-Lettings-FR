"""
Tests for the profiles application models.

This module contains unit tests for the Profile model.
"""
import pytest


@pytest.mark.django_db
class TestProfileModel:
    """Tests for the Profile model."""

    def test_profile_str(self, profile):
        """
        Test the string representation of a Profile.

        Args:
            profile: The profile fixture.
        """
        assert str(profile) == "testuser"

    def test_profile_has_user(self, profile):
        """
        Test that a Profile has an associated User.

        Args:
            profile: The profile fixture.
        """
        assert profile.user is not None
        assert profile.user.username == "testuser"

    def test_profile_favorite_city(self, profile):
        """
        Test that a Profile has a favorite city.

        Args:
            profile: The profile fixture.
        """
        assert profile.favorite_city == "Paris"

    def test_profile_favorite_city_blank(self, user):
        """
        Test that favorite_city can be blank.

        Args:
            user: The user fixture.
        """
        from profiles.models import Profile
        profile = Profile.objects.create(user=user, favorite_city="")
        assert profile.favorite_city == ""
