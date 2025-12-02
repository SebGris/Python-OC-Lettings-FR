import pytest
from django.urls import reverse


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
        response = client.get(reverse("lettings:index"))
        assert response.status_code == 200

    def test_lettings_index_template(self, client):
        response = client.get(reverse("lettings:index"))
        assert "lettings/index.html" in [t.name for t in response.templates]

    def test_lettings_index_content(self, client, letting):
        response = client.get(reverse("lettings:index"))
        assert "lettings_list" in response.context
        assert letting in response.context["lettings_list"]


@pytest.mark.django_db
class TestLettingDetailView:
    def test_letting_status_code(self, client, letting):
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert response.status_code == 200

    def test_letting_template(self, client, letting):
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert "lettings/letting.html" in [t.name for t in response.templates]

    def test_letting_content(self, client, letting):
        response = client.get(reverse("lettings:letting", args=[letting.id]))
        assert response.context["title"] == "Test Letting"
        assert response.context["address"] == letting.address


@pytest.mark.django_db
class TestProfilesIndexView:
    def test_profiles_index_status_code(self, client):
        response = client.get(reverse("profiles:index"))
        assert response.status_code == 200

    def test_profiles_index_template(self, client):
        response = client.get(reverse("profiles:index"))
        assert "profiles/index.html" in [t.name for t in response.templates]

    def test_profiles_index_content(self, client, profile):
        response = client.get(reverse("profiles:index"))
        assert "profiles_list" in response.context
        assert profile in response.context["profiles_list"]


@pytest.mark.django_db
class TestProfileDetailView:
    def test_profile_status_code(self, client, profile):
        response = client.get(reverse("profiles:profile", args=[profile.user.username]))
        assert response.status_code == 200

    def test_profile_template(self, client, profile):
        response = client.get(reverse("profiles:profile", args=[profile.user.username]))
        assert "profiles/profile.html" in [t.name for t in response.templates]

    def test_profile_content(self, client, profile):
        response = client.get(reverse("profiles:profile", args=[profile.user.username]))
        assert response.context["profile"] == profile
