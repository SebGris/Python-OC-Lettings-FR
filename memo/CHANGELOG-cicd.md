# Changelog - Mise en place CI/CD et Docker

Ce document récapitule toutes les modifications apportées pour implémenter l'étape 4 du projet : pipeline CI/CD et déploiement Docker.

---

## Fichiers créés

### 1. Dockerfile
**Chemin** : `/Dockerfile`

Image Docker multi-stage pour l'application Django :
- **Stage 1 (builder)** : Installe les dépendances Python avec gcc
- **Stage 2 (production)** : Image légère avec uniquement le nécessaire
- Utilise `python:3.13-slim` comme base
- Crée un utilisateur non-root `appuser` pour la sécurité
- Collecte les fichiers statiques avec `DEBUG=True` (évite les erreurs WhiteNoise sur les assets manquants du template CSS)
- Lance Gunicorn avec 2 workers et 4 threads

---

### 2. docker-compose.yml
**Chemin** : `/docker-compose.yml`

Configuration pour le développement local :
- Build depuis le Dockerfile local
- Mapping du port 8000
- Variables d'environnement depuis `.env`
- Volume pour persister la base SQLite
- Healthcheck pour vérifier que l'application fonctionne

---

### 3. .dockerignore
**Chemin** : `/.dockerignore`

Exclusions pour optimiser le build Docker :
- `venv/`, `__pycache__/`, `.git/`
- Fichiers de développement (`.env`, `*.md`, etc.)
- Base de données SQLite (montée en volume)

---

### 4. Pipeline CI/CD GitHub Actions
**Chemin** : `/.github/workflows/ci-cd.yml`

Pipeline automatisé avec 3 jobs :

| Job | Déclencheur | Actions |
|-----|-------------|---------|
| **test** | Push et PR | Linting (flake8), Tests (pytest), Couverture (80% min) |
| **build** | Push sur master (si tests OK) | Build et push image Docker Hub |
| **deploy** | Push sur master (si build OK) | Déploiement sur Render |

**Secrets requis dans GitHub** :
- `DOCKERHUB_USERNAME` - Nom d'utilisateur Docker Hub
- `DOCKERHUB_TOKEN` - Token d'accès Docker Hub
- `RENDER_DEPLOY_HOOK_URL` - URL du webhook Render

---

### 5. Fichiers SVG manquants
**Chemin** : `/static/assets/img/backgrounds/`

Fichiers créés pour résoudre les erreurs de WhiteNoise :
- `bg-waves.svg` - Fond de vagues (référencé ligne 18603 de styles.css)
- `bg-angles.svg` - Fond d'angles (référencé ligne 18607 de styles.css)

Ces fichiers sont référencés par le template CSS Start Bootstrap mais n'étaient pas inclus dans le projet.

---

### 6. Documentation
**Chemin** : `/memo/`

| Fichier | Description |
|---------|-------------|
| `docker.md` | Concepts Docker, explication du Dockerfile, commandes essentielles |
| `docker-local-setup.md` | Guide pas-à-pas pour lancer Docker en local, gestion de la SECRET_KEY |
| `ci-cd.md` | Explication du pipeline GitHub Actions, configuration des secrets |
| `python-django.md` | Architecture Django, settings.py, Gunicorn, WhiteNoise |

---

## Fichiers modifiés

### 1. requirements.txt
**Ajouts** :
```
gunicorn==21.2.0      # Serveur WSGI de production
whitenoise==6.6.0     # Serveur de fichiers statiques
```

---

### 2. oc_lettings_site/settings.py

#### Modification 1 : Configuration WhiteNoise
```python
# Ajout du middleware WhiteNoise (après SecurityMiddleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # AJOUTÉ
    ...
]

# Configuration STORAGES pour WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
            if not DEBUG
            else "django.contrib.staticfiles.storage.StaticFilesStorage"
        ),
    },
}
```

**Pourquoi cette configuration conditionnelle ?**
- En production (`DEBUG=False`) : Utilise `CompressedManifestStaticFilesStorage` qui compresse les fichiers et ajoute un hash pour le cache busting
- En développement (`DEBUG=True`) : Utilise le backend standard pour éviter les erreurs sur les fichiers manquants référencés dans le CSS

---

#### Modification 2 : Suppression de enable_logs dans Sentry
```python
# AVANT
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    send_default_pii=True,
    environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
    enable_logs=True,  # SUPPRIMÉ - non supporté par la version de sentry-sdk
)

# APRÈS
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    send_default_pii=True,
    environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
)
```

**Raison** : L'option `enable_logs=True` n'est pas supportée par la version de sentry-sdk dans requirements.txt et causait une erreur au démarrage de Gunicorn.

---

#### Modification 3 : Simplification de la configuration de logging
```python
# AVANT - Avec handler 'file'
LOGGING = {
    ...
    "handlers": {
        "console": {...},
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "oc_lettings_site": {
            "handlers": ["console", "file"],  # Utilisait 'file'
            ...
        },
    },
}

# APRÈS - Console uniquement
LOGGING = {
    ...
    "handlers": {
        "console": {...},
        # Handler 'file' supprimé
    },
    "loggers": {
        "oc_lettings_site": {
            "handlers": ["console"],  # Console uniquement
            ...
        },
    },
}
```

**Raison** : Dans Docker, l'utilisateur `appuser` n'a pas les permissions d'écriture sur `/app/debug.log` (créé par root lors du build). En production Docker, il est préférable de logger uniquement vers stdout/stderr, qui sont capturés par Docker et peuvent être consultés via `docker logs`.

---

## Résumé des commandes

### Tester localement avec Docker
```bash
# Construire et lancer
docker-compose up --build

# Accéder à l'application
http://localhost:8000

# Arrêter
docker-compose down
```

### Lancer les tests
```bash
python -m pytest --cov=. --cov-fail-under=80
python -m flake8
```

---

## Prochaines étapes

1. **Configurer les secrets GitHub** :
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
   - `RENDER_DEPLOY_HOOK_URL`

2. **Créer le service sur Render** :
   - Connecter le repository GitHub
   - Configurer les variables d'environnement (SECRET_KEY, ALLOWED_HOSTS, etc.)
   - Récupérer l'URL du deploy hook

3. **Pousser sur GitHub** pour déclencher le pipeline CI/CD
