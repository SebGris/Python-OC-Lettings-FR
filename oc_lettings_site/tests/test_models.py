import pytest
from django.contrib.auth.models import User

from profiles.models import Profile


@pytest.mark.django_db
class TestAddressModel:
    def test_address_str(self, address):
        assert str(address) == "123 Main Street"

    def test_address_creation(self, address):
        assert address.number == 123
        assert address.street == "Main Street"
        assert address.city == "Springfield"
        assert address.state == "IL"
        assert address.zip_code == 62701
        assert address.country_iso_code == "USA"


@pytest.mark.django_db
class TestLettingModel:
    def test_letting_str(self, letting):
        assert str(letting) == "Test Letting"

    def test_letting_creation(self, letting, address):
        assert letting.title == "Test Letting"
        assert letting.address == address


@pytest.mark.django_db
class TestProfileModel:
    def test_profile_str(self, profile):
        assert str(profile) == "testuser"

    def test_profile_creation(self, profile, user):
        assert profile.user == user
        assert profile.favorite_city == "Paris"

    def test_profile_blank_favorite_city(self, user):
        profile = Profile.objects.create(user=user, favorite_city="")
        assert profile.favorite_city == ""
