import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestIndexView:
    def test_index_status_code(self, client):
        response = client.get(reverse("index"))
        assert response.status_code == 200


@pytest.mark.django_db
class TestLettingsIndexView:
    def test_lettings_index_status_code(self, client):
        response = client.get(reverse("lettings:index"))
        assert response.status_code == 200


@pytest.mark.django_db
class TestLettingDetailView:
    def test_letting_status_code(self, client, letting):
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert response.status_code == 200


@pytest.mark.django_db
class TestProfilesIndexView:
    def test_profiles_index_status_code(self, client):
        response = client.get(reverse("profiles:index"))
        assert response.status_code == 200


@pytest.mark.django_db
class TestProfileDetailView:
    def test_profile_status_code(self, client, profile):
        response = client.get(
            reverse("profiles:profile", args=[profile.user.username])
        )
        assert response.status_code == 200
