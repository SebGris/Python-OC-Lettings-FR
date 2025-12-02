import pytest
from django.test import Client
from django.contrib.auth.models import User

from lettings.models import Address, Letting
from profiles.models import Profile


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def address():
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
    return Letting.objects.create(title="Test Letting", address=address)


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", password="testpass123"
    )


@pytest.fixture
def profile(user):
    return Profile.objects.create(user=user, favorite_city="Paris")
