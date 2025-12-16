# Documentation Python/Django - OC Lettings

## Table des matières
1. [Architecture du projet](#1-architecture-du-projet)
2. [Configuration Django (settings.py)](#2-configuration-django-settingspy)
3. [Les modèles Django](#3-les-modèles-django)
4. [Les vues et URLs](#4-les-vues-et-urls)
5. [Gestion des fichiers statiques](#5-gestion-des-fichiers-statiques)
6. [Serveur de production (Gunicorn)](#6-serveur-de-production-gunicorn)
7. [Gestion des erreurs (Sentry)](#7-gestion-des-erreurs-sentry)
8. [Tests avec Pytest](#8-tests-avec-pytest)

---

## 1. Architecture du projet

### Structure des dossiers

```
project-13 Python-OC-Lettings-FR/
│
├── oc_lettings_site/          # Application principale (configuration)
│   ├── __init__.py
│   ├── settings.py            # Configuration Django
│   ├── urls.py                # Routes principales
│   ├── wsgi.py                # Point d'entrée WSGI (production)
│   ├── asgi.py                # Point d'entrée ASGI (async)
│   └── views.py               # Vues de l'app principale
│
├── lettings/                   # App Django pour les locations
│   ├── models.py              # Modèles Address et Letting
│   ├── views.py               # Vues pour les locations
│   ├── urls.py                # Routes de l'app
│   ├── admin.py               # Configuration admin
│   └── templates/             # Templates HTML
│
├── profiles/                   # App Django pour les profils
│   ├── models.py              # Modèle Profile
│   ├── views.py               # Vues pour les profils
│   ├── urls.py                # Routes de l'app
│   └── templates/             # Templates HTML
│
├── templates/                  # Templates globaux
│   ├── base.html              # Template de base
│   ├── index.html             # Page d'accueil
│   ├── 404.html               # Page d'erreur 404
│   └── 500.html               # Page d'erreur 500
│
├── static/                     # Fichiers statiques sources
│   ├── css/
│   └── js/
│
├── staticfiles/                # Fichiers statiques collectés (production)
│
├── manage.py                   # Script de gestion Django
├── requirements.txt            # Dépendances Python
└── setup.cfg                   # Configuration pytest/flake8
```

### Philosophie Django : MTV (Model-Template-View)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Requête HTTP                               │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          URLs (urls.py)                             │
│         Route la requête vers la bonne vue                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          View (views.py)                            │
│         Logique métier : récupère les données, prépare le contexte  │
└──────────┬────────────────────┴───────────────────────┬─────────────┘
           │                                            │
           ▼                                            ▼
┌──────────────────────┐                  ┌──────────────────────────┐
│   Model (models.py)  │                  │   Template (.html)       │
│   Accès base données │                  │   Rendu HTML             │
└──────────────────────┘                  └──────────────────────────┘
```

---

## 2. Configuration Django (settings.py)

### Variables d'environnement

```python
from dotenv import load_dotenv
import os

# Charge les variables depuis le fichier .env
load_dotenv(BASE_DIR / ".env")

# Récupère les variables
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
```

**Pourquoi ?**
- Les secrets ne sont jamais dans le code source
- Configuration différente par environnement (dev/prod)

### Configuration des hôtes autorisés

```python
ALLOWED_HOSTS = (
    os.environ.get("ALLOWED_HOSTS", "").split(",")
    if os.environ.get("ALLOWED_HOSTS")
    else []
)
if DEBUG:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

**Explication** :
- En production : définir explicitement les domaines autorisés
- En développement : autoriser localhost automatiquement
- Protection contre les attaques HTTP Host header

### Applications installées

```python
INSTALLED_APPS = [
    "lettings",                              # Notre app locations
    "profiles",                              # Notre app profils
    "oc_lettings_site.apps.OCLettingsSiteConfig",  # App principale
    "django.contrib.admin",                  # Interface d'administration
    "django.contrib.auth",                   # Authentification
    "django.contrib.contenttypes",           # Types de contenu
    "django.contrib.sessions",               # Sessions
    "django.contrib.messages",               # Messages flash
    "django.contrib.staticfiles",            # Fichiers statiques
]
```

### Middleware

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Fichiers statiques en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

**Middleware** : Couches qui traitent chaque requête/réponse.

**WhiteNoise** : Sert les fichiers statiques directement depuis Django en production (sans serveur web séparé).

---

## 3. Les modèles Django

### Modèle Address (lettings/models.py)

```python
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator

class Address(models.Model):
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.number} {self.street}"
```

**Explications** :
- `models.Model` : Classe de base pour tous les modèles Django
- `PositiveIntegerField` : Entier positif uniquement
- `CharField(max_length=64)` : Chaîne de caractères limitée
- `validators=[...]` : Validation des données
- `class Meta` : Options du modèle (nom pluriel, etc.)
- `__str__` : Représentation textuelle de l'objet

### Modèle Letting

```python
class Letting(models.Model):
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

**Relations** :
- `OneToOneField` : Relation 1-1 (une location = une adresse unique)
- `on_delete=models.CASCADE` : Si l'adresse est supprimée, la location l'est aussi

### Modèle Profile (profiles/models.py)

```python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
```

**Extension du modèle User** :
- Django fournit un modèle `User` intégré
- `OneToOneField` permet d'ajouter des champs supplémentaires
- `blank=True` : Le champ peut être vide

### Migrations

```bash
# Créer les migrations après modification des modèles
python manage.py makemigrations

# Appliquer les migrations à la base de données
python manage.py migrate

# Voir l'état des migrations
python manage.py showmigrations
```

---

## 4. Les vues et URLs

### Configuration des URLs

**oc_lettings_site/urls.py** (URLs principales) :
```python
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),                    # Page d'accueil
    path("lettings/", include("lettings.urls")),            # Inclut les URLs de lettings
    path("profiles/", include("profiles.urls")),            # Inclut les URLs de profiles
    path("admin/", admin.site.urls),                        # Admin Django
]
```

**lettings/urls.py** (URLs de l'app) :
```python
app_name = "lettings"  # Namespace pour éviter les conflits

urlpatterns = [
    path("", views.index, name="index"),              # /lettings/
    path("<int:letting_id>/", views.letting, name="letting"),  # /lettings/1/
]
```

### Types de vues

#### Vue fonction (Function-Based View)

```python
from django.shortcuts import render

def index(request):
    """Liste toutes les locations."""
    lettings_list = Letting.objects.all()
    context = {"lettings_list": lettings_list}
    return render(request, "lettings/index.html", context)
```

**Explication** :
- `request` : L'objet requête HTTP
- `Letting.objects.all()` : Récupère tous les objets Letting
- `context` : Dictionnaire passé au template
- `render()` : Combine template + contexte → réponse HTML

#### Vue avec paramètre

```python
from django.shortcuts import render, get_object_or_404

def letting(request, letting_id):
    """Affiche les détails d'une location."""
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        "title": letting.title,
        "address": letting.address,
    }
    return render(request, "lettings/letting.html", context)
```

**`get_object_or_404`** : Récupère l'objet ou retourne une erreur 404.

### Templates Django

```html
<!-- templates/lettings/index.html -->
{% extends "base.html" %}

{% block content %}
<h1>Lettings</h1>
<ul>
    {% for letting in lettings_list %}
        <li>
            <a href="{% url 'lettings:letting' letting.id %}">
                {{ letting.title }}
            </a>
        </li>
    {% empty %}
        <li>No lettings available.</li>
    {% endfor %}
</ul>
{% endblock %}
```

**Syntaxe Django Template** :
- `{% extends "base.html" %}` : Hérite du template de base
- `{% block content %}` : Définit un bloc de contenu
- `{% for ... %}` : Boucle
- `{% url 'app:name' %}` : Génère une URL à partir de son nom
- `{{ variable }}` : Affiche une variable

---

## 5. Gestion des fichiers statiques

### Configuration

```python
# settings.py

# URL pour accéder aux fichiers statiques
STATIC_URL = "/static/"

# Dossiers contenant les fichiers sources
STATICFILES_DIRS = [BASE_DIR / "static"]

# Dossier où collectstatic copie tout (production)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Backend de stockage avec compression
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

### Flux des fichiers statiques

```
Développement                           Production
─────────────────                       ─────────────────
static/                                 staticfiles/
├── css/style.css        ────▶         ├── css/style.abc123.css
└── js/script.js          collectstatic └── js/script.def456.js
                                        └── staticfiles.json (manifest)
```

### Commandes

```bash
# Collecte tous les fichiers statiques dans STATIC_ROOT
python manage.py collectstatic

# Avec --noinput pour automatisation (CI/CD)
python manage.py collectstatic --noinput
```

### WhiteNoise

**Qu'est-ce que WhiteNoise ?**
- Middleware qui sert les fichiers statiques directement depuis Django
- Pas besoin de Nginx/Apache pour les fichiers statiques
- Compression automatique (gzip/brotli)
- Cache headers optimisés

**Configuration** :
```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Après SecurityMiddleware
    # ...
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

---

## 6. Serveur de production (Gunicorn)

### Pourquoi pas `runserver` en production ?

Le serveur de développement Django (`manage.py runserver`) :
- N'est pas sécurisé
- Ne gère qu'une requête à la fois
- N'est pas optimisé pour les performances

### Qu'est-ce que Gunicorn ?

**Gunicorn** (Green Unicorn) est un serveur WSGI Python de production :
- Multi-processus (plusieurs requêtes simultanées)
- Robuste et éprouvé
- Facile à configurer

### WSGI expliqué

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Gunicorn  │────▶│   Django    │
│  (Browser)  │◀────│   (WSGI)    │◀────│   (App)     │
└─────────────┘     └─────────────┘     └─────────────┘

WSGI = Web Server Gateway Interface
Interface standard entre serveur web et application Python
```

### Configuration Gunicorn

```bash
gunicorn oc_lettings_site.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --access-logfile - \
    --error-logfile -
```

**Options** :
- `oc_lettings_site.wsgi:application` : Point d'entrée WSGI
- `--bind 0.0.0.0:8000` : Écoute sur le port 8000
- `--workers 2` : 2 processus (règle : 2*CPU + 1)
- `--threads 4` : 4 threads par worker
- `--access-logfile -` : Logs d'accès vers stdout
- `--error-logfile -` : Logs d'erreur vers stderr

### Fichier wsgi.py

```python
# oc_lettings_site/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")

application = get_wsgi_application()
```

---

## 7. Gestion des erreurs (Sentry)

### Qu'est-ce que Sentry ?

Sentry est un service de monitoring d'erreurs qui :
- Capture automatiquement les exceptions
- Fournit le contexte complet (stack trace, requête, user)
- Envoie des alertes
- Groupe les erreurs similaires

### Configuration

```python
# settings.py
import sentry_sdk

SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,      # 100% des transactions tracées
        profiles_sample_rate=1.0,    # 100% des transactions profilées
        send_default_pii=True,       # Envoie les infos utilisateur
        environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
        enable_logs=True,            # Envoie les logs Python
    )
```

### Utilisation

```python
import sentry_sdk

# Capture manuelle d'une exception
try:
    risque_erreur()
except Exception as e:
    sentry_sdk.capture_exception(e)

# Message personnalisé
sentry_sdk.capture_message("Quelque chose s'est passé")

# Contexte additionnel
with sentry_sdk.push_scope() as scope:
    scope.set_tag("page", "lettings")
    scope.set_extra("letting_id", 42)
    sentry_sdk.capture_message("Détail location consultée")
```

---

## 8. Tests avec Pytest

### Configuration (setup.cfg)

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = oc_lettings_site.settings
python_files = tests.py test_*.py
addopts = --cov=oc_lettings_site --cov=lettings --cov=profiles
          --cov-report=term-missing
          --cov-fail-under=80

[coverage:run]
omit = */migrations/*, */tests/*, */wsgi.py, */asgi.py, manage.py
```

**Options** :
- `--cov` : Active la couverture
- `--cov-report=term-missing` : Affiche les lignes non couvertes
- `--cov-fail-under=80` : Échoue si < 80% de couverture

### Structure des tests

```python
# lettings/tests/test_views.py
import pytest
from django.urls import reverse
from lettings.models import Address, Letting

@pytest.mark.django_db
class TestLettingsViews:
    """Tests pour les vues de l'application lettings."""

    def test_index_view(self, client):
        """Vérifie que la page d'index s'affiche correctement."""
        url = reverse("lettings:index")
        response = client.get(url)
        assert response.status_code == 200
        assert b"Lettings" in response.content

    def test_letting_detail_view(self, client):
        """Vérifie qu'une location s'affiche correctement."""
        # Créer les données de test
        address = Address.objects.create(
            number=123, street="Test St", city="Test City",
            state="TS", zip_code=12345, country_iso_code="USA"
        )
        letting = Letting.objects.create(title="Test Letting", address=address)

        # Tester la vue
        url = reverse("lettings:letting", args=[letting.id])
        response = client.get(url)
        assert response.status_code == 200
        assert b"Test Letting" in response.content
```

### Décorateurs et fixtures

```python
@pytest.mark.django_db  # Permet l'accès à la base de données
def test_avec_db():
    pass

@pytest.fixture
def address():
    """Fixture qui crée une adresse de test."""
    return Address.objects.create(
        number=123, street="Test", city="City",
        state="ST", zip_code=12345, country_iso_code="USA"
    )

def test_utilise_fixture(address):
    # address est automatiquement créée et passée
    assert address.number == 123
```

### Commandes de test

```bash
# Lancer tous les tests
python -m pytest

# Tests avec couverture détaillée
python -m pytest --cov --cov-report=html

# Tests d'un fichier spécifique
python -m pytest lettings/tests/test_views.py

# Tests verbeux
python -m pytest -v

# Stopper au premier échec
python -m pytest -x
```

---

## Résumé des commandes Django

```bash
# Développement
python manage.py runserver          # Lancer le serveur de dev
python manage.py shell              # Shell Python avec Django

# Base de données
python manage.py makemigrations     # Créer les migrations
python manage.py migrate            # Appliquer les migrations
python manage.py createsuperuser    # Créer un admin

# Fichiers statiques
python manage.py collectstatic      # Collecter pour la production

# Tests
python -m pytest                    # Lancer les tests
python -m flake8                    # Vérifier le style de code
```
