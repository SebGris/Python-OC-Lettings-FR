import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Address, Letting, Profile


# ============== FIXTURES ==============


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


# ============== TESTS MODELS ==============


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


# ============== TESTS VIEWS ==============


@pytest.mark.django_db
class TestIndexView:
    def test_index_status_code(self, client):
        response = client.get(reverse("index"))
        assert response.status_code == 200

    def test_index_template(self, client):
        response = client.get(reverse("index"))
        assert "index.html" in [t.name for t in response.templates]


@pytest.mark.django_db
class TestLettingsIndexView:
    def test_lettings_index_status_code(self, client):
        response = client.get(reverse("lettings_index"))
        assert response.status_code == 200

    def test_lettings_index_template(self, client):
        response = client.get(reverse("lettings_index"))
        assert "lettings_index.html" in [t.name for t in response.templates]

    def test_lettings_index_content(self, client, letting):
        response = client.get(reverse("lettings_index"))
        assert "lettings_list" in response.context
        assert letting in response.context["lettings_list"]


@pytest.mark.django_db
class TestLettingDetailView:
    def test_letting_status_code(self, client, letting):
        response = client.get(reverse("letting", args=[letting.id]))
        assert response.status_code == 200

    def test_letting_template(self, client, letting):
        response = client.get(reverse("letting", args=[letting.id]))
        assert "letting.html" in [t.name for t in response.templates]

    def test_letting_content(self, client, letting):
        response = client.get(reverse("letting", args=[letting.id]))
        assert response.context["title"] == "Test Letting"
        assert response.context["address"] == letting.address


@pytest.mark.django_db
class TestProfilesIndexView:
    def test_profiles_index_status_code(self, client):
        response = client.get(reverse("profiles_index"))
        assert response.status_code == 200

    def test_profiles_index_template(self, client):
        response = client.get(reverse("profiles_index"))
        assert "profiles_index.html" in [t.name for t in response.templates]

    def test_profiles_index_content(self, client, profile):
        response = client.get(reverse("profiles_index"))
        assert "profiles_list" in response.context
        assert profile in response.context["profiles_list"]


@pytest.mark.django_db
class TestProfileDetailView:
    def test_profile_status_code(self, client, profile):
        response = client.get(reverse("profile", args=[profile.user.username]))
        assert response.status_code == 200

    def test_profile_template(self, client, profile):
        response = client.get(reverse("profile", args=[profile.user.username]))
        assert "profile.html" in [t.name for t in response.templates]

    def test_profile_content(self, client, profile):
        response = client.get(reverse("profile", args=[profile.user.username]))
        assert response.context["profile"] == profile


# ============== TESTS URLS ==============


@pytest.mark.django_db
class TestUrls:
    def test_index_url(self):
        assert reverse("index") == "/"

    def test_lettings_index_url(self):
        assert reverse("lettings_index") == "/lettings/"

    def test_letting_url(self):
        assert reverse("letting", args=[1]) == "/lettings/1/"

    def test_profiles_index_url(self):
        assert reverse("profiles_index") == "/profiles/"

    def test_profile_url(self):
        assert reverse("profile", args=["testuser"]) == "/profiles/testuser/"
