"""
Tests for the lettings application models.

This module contains unit tests for the Address and Letting models.
"""
import pytest


@pytest.mark.django_db
class TestAddressModel:
    """Tests for the Address model."""

    def test_address_str(self, address):
        """
        Test the string representation of an Address.

        Args:
            address: The address fixture.
        """
        assert str(address) == "123 Main Street"

    def test_address_fields(self, address):
        """
        Test that Address fields are correctly set.

        Args:
            address: The address fixture.
        """
        assert address.number == 123
        assert address.street == "Main Street"
        assert address.city == "Springfield"
        assert address.state == "IL"
        assert address.zip_code == 62701
        assert address.country_iso_code == "USA"


@pytest.mark.django_db
class TestLettingModel:
    """Tests for the Letting model."""

    def test_letting_str(self, letting):
        """
        Test the string representation of a Letting.

        Args:
            letting: The letting fixture.
        """
        assert str(letting) == "Test Letting"

    def test_letting_has_address(self, letting):
        """
        Test that a Letting has an associated Address.

        Args:
            letting: The letting fixture.
        """
        assert letting.address is not None
        assert letting.address.city == "Springfield"
