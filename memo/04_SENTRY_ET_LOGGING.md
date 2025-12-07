# Configuration de Sentry et du Logging

## Vue d'ensemble

Ce document explique la mise en place de la surveillance des erreurs avec Sentry et la configuration du système de logging Django.

## 1. Installation des dépendances

### Commandes d'installation

```bash
pip install sentry-sdk python-dotenv
```

### Ajout aux dépendances

Dans `requirements.txt` :
```
sentry-sdk==2.19.2
python-dotenv==1.0.1
```

## 2. Configuration des variables d'environnement avec python-dotenv

### Pourquoi utiliser python-dotenv ?

Les variables d'environnement définies avec `set` (Windows) ou `export` (Linux) ne persistent que dans la session terminal actuelle. Si vous fermez le terminal ou ouvrez une nouvelle fenêtre, la variable est perdue.

`python-dotenv` résout ce problème en chargeant automatiquement les variables depuis un fichier `.env`.

### Étape 1 : Créer le fichier .env

Copier le fichier `.env.example` vers `.env` et remplir les valeurs :

```bash
cp .env.example .env
```

Contenu du fichier `.env` :

```
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Sentry configuration
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
SENTRY_ENVIRONMENT=development
```

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `SECRET_KEY` | Clé secrète Django pour la cryptographie | Oui |
| `DEBUG` | Mode debug (True/False) | Non (défaut: False) |
| `ALLOWED_HOSTS` | Domaines autorisés, séparés par des virgules | Non (défaut: localhost,127.0.0.1) |
| `SENTRY_DSN` | URL du projet Sentry | Non (Sentry désactivé si absent) |
| `SENTRY_ENVIRONMENT` | Environnement Sentry (development/production) | Non (défaut: development) |

### Étape 2 : Ajouter .env au .gitignore

**Important** : Le fichier `.env` contient des secrets et ne doit **jamais** être commité :

```gitignore
.env
debug.log
```

### Étape 3 : Charger les variables dans settings.py

Au début de `settings.py` :

```python
import os

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")
```

`load_dotenv()` lit le fichier `.env` et injecte les variables dans `os.environ`. Ensuite, `os.environ.get("SENTRY_DSN")` fonctionne normalement.

## 3. Configuration de Sentry dans settings.py

```python
import sentry_sdk

# Sentry configuration
# Get DSN from environment variable for security
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        send_default_pii=True,
        environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    )
```

### Explication des paramètres

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `dsn` | Variable d'environnement | URL unique fournie par Sentry pour identifier le projet |
| `traces_sample_rate` | `1.0` (100%) | Pourcentage de transactions à tracer pour le monitoring de performance |
| `profiles_sample_rate` | `1.0` (100%) | Pourcentage de transactions à profiler (analyse détaillée) |
| `send_default_pii` | `True` | Envoie les informations utilisateur (IP, email) - mettre à `False` en production si nécessaire |
| `environment` | `"development"` | Tag pour distinguer les environnements (development, staging, production) |

### Pourquoi utiliser une variable d'environnement ?

Le DSN est une clé sensible qui ne doit **jamais** être commitée dans le code :

```python
# ❌ MAUVAIS - clé en dur dans le code
sentry_sdk.init(dsn="https://abc123@sentry.io/123456")

# ✅ BON - clé dans variable d'environnement
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
```

## 4. Configuration du Logging Django

### Structure complète

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "oc_lettings_site": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "lettings": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "profiles": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
```

### Explication des composants

#### Formatters (Formateurs)

Les formatters définissent le format des messages de log :

```python
"formatters": {
    "verbose": {
        "format": "{levelname} {asctime} {module} {message}",
        "style": "{",
    },
}
```

Exemple de sortie :
```
INFO 2024-01-15 10:30:45,123 views Home page accessed
ERROR 2024-01-15 10:31:02,456 views Letting with ID 999 not found
```

| Variable | Description |
|----------|-------------|
| `{levelname}` | Niveau du log (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `{asctime}` | Date et heure |
| `{module}` | Nom du module Python |
| `{message}` | Le message de log |

#### Handlers (Gestionnaires)

Les handlers définissent où les logs sont envoyés :

```python
"handlers": {
    "console": {
        "class": "logging.StreamHandler",  # Sortie vers la console
        "formatter": "verbose",
    },
    "file": {
        "class": "logging.FileHandler",    # Sortie vers un fichier
        "filename": BASE_DIR / "debug.log",
        "formatter": "verbose",
    },
},
```

#### Loggers

Les loggers définissent les règles pour chaque module :

```python
"loggers": {
    "lettings": {
        "handlers": ["console", "file"],  # Envoie aux deux handlers
        "level": "DEBUG",                  # Niveau minimum
        "propagate": False,                # Ne pas propager au logger parent
    },
},
```

### Niveaux de log

| Niveau | Valeur | Usage |
|--------|--------|-------|
| `DEBUG` | 10 | Informations détaillées pour le débogage |
| `INFO` | 20 | Confirmation que tout fonctionne normalement |
| `WARNING` | 30 | Indication d'un problème potentiel |
| `ERROR` | 40 | Erreur qui empêche une fonctionnalité |
| `CRITICAL` | 50 | Erreur grave qui empêche l'application de fonctionner |

Un logger avec `level: "INFO"` affichera INFO, WARNING, ERROR et CRITICAL, mais pas DEBUG.

## 5. Ajout des logs dans les vues

### Pattern utilisé

```python
import logging

logger = logging.getLogger(__name__)
```

`__name__` retourne le nom du module (ex: `lettings.views`), ce qui permet au système de logging de router les messages vers le bon logger configuré dans `settings.py`.

### Exemple : lettings/views.py

```python
import logging

from django.http import Http404
from django.shortcuts import render

from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    logger.info("Lettings index page accessed")
    lettings_list = Letting.objects.all()
    logger.debug("Retrieved %d lettings", lettings_list.count())
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    logger.info("Letting detail page accessed for ID: %s", letting_id)
    try:
        letting = Letting.objects.get(id=letting_id)
        logger.debug("Found letting: %s", letting.title)
    except Letting.DoesNotExist:
        logger.error("Letting with ID %s not found", letting_id)
        raise Http404(f"Letting with ID {letting_id} does not exist")
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
```

### Points critiques identifiés

| Vue | Type de log | Message |
|-----|-------------|---------|
| `index` | INFO | Page accédée |
| `index` | DEBUG | Nombre d'éléments récupérés |
| `letting/profile` | INFO | Détail accédé avec ID/username |
| `letting/profile` | DEBUG | Élément trouvé |
| `letting/profile` | ERROR | Élément non trouvé (dans try/except) |

### Pourquoi utiliser try/except avec Http404 ?

```python
# ❌ Sans try/except - erreur 500 si l'objet n'existe pas
letting = Letting.objects.get(id=letting_id)

# ✅ Avec try/except - erreur 404 propre + log
try:
    letting = Letting.objects.get(id=letting_id)
except Letting.DoesNotExist:
    logger.error("Letting with ID %s not found", letting_id)
    raise Http404(f"Letting with ID {letting_id} does not exist")
```

Avantages :
1. L'utilisateur voit une page 404 au lieu d'une erreur 500
2. L'erreur est loggée pour le monitoring
3. Sentry capture l'événement avec le contexte

## 6. Tester la configuration

### Vérifier que les logs fonctionnent

1. Lancer le serveur :
```bash
python manage.py runserver
```

2. Accéder aux pages et vérifier la console :
```
INFO 2024-01-15 10:30:45,123 views Home page accessed
INFO 2024-01-15 10:30:46,456 views Lettings index page accessed
DEBUG 2024-01-15 10:30:46,789 views Retrieved 3 lettings
```

3. Vérifier le fichier `debug.log` à la racine du projet

### Provoquer une erreur pour tester Sentry

1. Définir le DSN Sentry
2. Accéder à une URL invalide :
   - `/lettings/999/` → log ERROR + page 404
   - `/profiles/unknown/` → log ERROR + page 404
3. Vérifier dans le dashboard Sentry que l'erreur apparaît

### Créer une vue de test (optionnel)

Pour tester Sentry en développement, vous pouvez créer une vue temporaire :

```python
# Dans oc_lettings_site/views.py (temporaire, à supprimer après test)
def trigger_error(request):
    division_by_zero = 1 / 0
```

```python
# Dans oc_lettings_site/urls.py (temporaire)
path('sentry-debug/', trigger_error),
```

Accéder à `/sentry-debug/` provoquera une erreur qui sera capturée par Sentry.

## 7. Bonnes pratiques

### Format des messages de log

```python
# ✅ Utiliser le formatage avec %s (plus performant)
logger.info("User %s logged in", username)

# ❌ Éviter la concaténation ou f-strings dans les logs
logger.info(f"User {username} logged in")
logger.info("User " + username + " logged in")
```

Le formatage avec `%s` est plus performant car le message n'est formaté que si le niveau de log est actif.

### Ne pas logger d'informations sensibles

```python
# ❌ MAUVAIS - mot de passe en clair
logger.debug("User login attempt: %s / %s", username, password)

# ✅ BON - seulement l'information nécessaire
logger.info("User login attempt: %s", username)
```

### Choisir le bon niveau de log

```python
# DEBUG - détails techniques pour le développement
logger.debug("Query executed: SELECT * FROM...")

# INFO - événements normaux
logger.info("User logged in successfully")

# WARNING - situation anormale mais gérée
logger.warning("Rate limit approaching for user %s", user_id)

# ERROR - erreur qui empêche une opération
logger.error("Failed to process payment for order %s", order_id)

# CRITICAL - erreur système grave
logger.critical("Database connection lost")
```

## 8. Architecture du système de logging

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Django                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ oc_lettings  │  │   lettings   │  │   profiles   │          │
│  │    views     │  │    views     │  │    views     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                      │
│                           ▼                                      │
│                 ┌─────────────────┐                             │
│                 │  Logger Python  │                             │
│                 │  (__name__)     │                             │
│                 └────────┬────────┘                             │
│                          │                                       │
│         ┌────────────────┼────────────────┐                     │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │  Console   │  │   File     │  │   Sentry   │                │
│  │  Handler   │  │  Handler   │  │    SDK     │                │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘                │
│        │               │               │                        │
└────────┼───────────────┼───────────────┼────────────────────────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ Terminal│    │debug.log │    │ Sentry   │
    │         │    │          │    │ Cloud    │
    └─────────┘    └──────────┘    └──────────┘
```

## 9. Sources et références

### Installation et configuration de Sentry

| Code | Source |
|------|--------|
| `pip install sentry-sdk` | [Sentry Python Installation](https://docs.sentry.io/platforms/python/) |
| `sentry_sdk.init(dsn=...)` | [Sentry Django Configuration](https://docs.sentry.io/platforms/python/integrations/django/) |
| `traces_sample_rate=1.0` | [Sentry Performance Monitoring](https://docs.sentry.io/platforms/python/tracing/) |
| `profiles_sample_rate=1.0` | [Sentry Profiling](https://docs.sentry.io/platforms/python/profiling/) |
| `send_default_pii=True` | [Sentry Data Management](https://docs.sentry.io/platforms/python/data-management/sensitive-data/) |
| `environment="development"` | [Sentry Environments](https://docs.sentry.io/platforms/python/configuration/environments/) |

### Configuration de python-dotenv

| Code | Source |
|------|--------|
| `pip install python-dotenv` | [python-dotenv PyPI](https://pypi.org/project/python-dotenv/) |
| `load_dotenv()` | [python-dotenv Documentation](https://saurabh-kumar.com/python-dotenv/) |
| Fichier `.env` | [12 Factor App - Config](https://12factor.net/config) |

### Configuration du Logging Django

| Code | Source |
|------|--------|
| `LOGGING = {...}` | [Django Logging Configuration](https://docs.djangoproject.com/en/4.2/topics/logging/#configuring-logging) |
| `"version": 1` | [Python dictConfig format](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema) |
| `"formatters": {...}` | [Django Logging Formatters](https://docs.djangoproject.com/en/4.2/topics/logging/#formatters) |
| `"handlers": {...}` | [Django Logging Handlers](https://docs.djangoproject.com/en/4.2/topics/logging/#handlers) |
| `"loggers": {...}` | [Django Logging Loggers](https://docs.djangoproject.com/en/4.2/topics/logging/#loggers) |
| `logging.StreamHandler` | [Python StreamHandler](https://docs.python.org/3/library/logging.handlers.html#streamhandler) |
| `logging.FileHandler` | [Python FileHandler](https://docs.python.org/3/library/logging.handlers.html#filehandler) |

### Utilisation du logging dans les vues

| Code | Source |
|------|--------|
| `import logging` | [Python Logging Module](https://docs.python.org/3/library/logging.html) |
| `logger = logging.getLogger(__name__)` | [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html#logging-from-multiple-modules) |
| `logger.info(...)`, `logger.debug(...)` | [Python Logging Levels](https://docs.python.org/3/howto/logging.html#logging-levels) |
| `logger.error(...)` | [Python Logging Tutorial](https://docs.python.org/3/howto/logging.html#a-simple-example) |

### Gestion des erreurs 404

| Code | Source |
|------|--------|
| `from django.http import Http404` | [Django Http404](https://docs.djangoproject.com/en/4.2/topics/http/views/#django.http.Http404) |
| `raise Http404(...)` | [Django Returning Errors](https://docs.djangoproject.com/en/4.2/topics/http/views/#returning-errors) |
| `Model.DoesNotExist` | [Django DoesNotExist Exception](https://docs.djangoproject.com/en/4.2/ref/models/class/#django.db.models.Model.DoesNotExist) |

### Bonnes pratiques

| Concept | Source |
|---------|--------|
| Format `%s` vs f-strings | [Python Logging Performance](https://docs.python.org/3/howto/logging.html#optimization) |
| Ne pas logger de données sensibles | [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) |
| Niveaux de log | [Python Logging Levels](https://docs.python.org/3/howto/logging.html#when-to-use-logging) |

### Tutoriels complémentaires

- [Real Python - Logging in Python](https://realpython.com/python-logging/)
- [Real Python - Python dotenv](https://realpython.com/python-dotenv/)
- [Django Girls - Deploying with Environment Variables](https://tutorial-extensions.djangogirls.org/en/heroku/)
- [TestDriven.io - Django Logging](https://testdriven.io/blog/django-logging/)
