from django.urls import reverse


class TestUrls:
    def test_index_url(self):
        assert reverse("index") == "/"

    def test_lettings_index_url(self):
        assert reverse("lettings:index") == "/lettings/"

    def test_letting_url(self):
        assert reverse("lettings:letting", args=[1]) == "/lettings/1/"

    def test_profiles_index_url(self):
        assert reverse("profiles:index") == "/profiles/"

    def test_profile_url(self):
        assert reverse("profiles:profile", args=["testuser"]) == "/profiles/testuser/"
