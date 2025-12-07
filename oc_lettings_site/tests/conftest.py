"""
Pytest fixtures for the oc_lettings_site application tests.

This module provides fixtures for creating test data used in main site tests.
"""
import pytest
from django.test import Client


@pytest.fixture
def client():
    """
    Create a Django test client.

    Returns:
        Client: A Django test client instance.
    """
    return Client()
