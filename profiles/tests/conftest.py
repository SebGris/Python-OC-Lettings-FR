"""
Pytest fixtures for the profiles application tests.

This module provides fixtures for creating test data used in profiles tests.
"""
import pytest
from django.contrib.auth.models import User

from profiles.models import Profile


@pytest.fixture
def user():
    """
    Create a test User instance.

    Returns:
        User: A test user object.
    """
    return User.objects.create_user(
        username="testuser",
        password="testpass123"
    )


@pytest.fixture
def profile(user):
    """
    Create a test Profile instance.

    Args:
        user: The user fixture to associate with the profile.

    Returns:
        Profile: A test profile object.
    """
    return Profile.objects.create(user=user, favorite_city="Paris")
