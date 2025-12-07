"""
Pytest fixtures for the lettings application tests.

This module provides fixtures for creating test data used in lettings tests.
"""
import pytest

from lettings.models import Address, Letting


@pytest.fixture
def address():
    """
    Create a test Address instance.

    Returns:
        Address: A test address object.
    """
    return Address.objects.create(
        number=123,
        street="Main Street",
        city="Springfield",
        state="IL",
        zip_code=62701,
        country_iso_code="USA",
    )


@pytest.fixture
def letting(address):
    """
    Create a test Letting instance.

    Args:
        address: The address fixture to associate with the letting.

    Returns:
        Letting: A test letting object.
    """
    return Letting.objects.create(title="Test Letting", address=address)
