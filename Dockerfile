# =============================================================================
# Dockerfile pour OC Lettings - Application Django
# =============================================================================
# Ce fichier définit comment construire l'image Docker de l'application.
# Il utilise Poetry pour la gestion des dépendances et une approche
# multi-stage pour optimiser la taille de l'image finale.
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Builder - Installation des dépendances avec Poetry
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS builder

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Variables d'environnement pour optimiser Python et Poetry dans Docker
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Configuration Poetry
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Ajouter Poetry au PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Installer Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copier les fichiers de configuration Poetry
COPY pyproject.toml poetry.lock* ./

# Installer les dépendances (sans les dépendances de développement)
# --only main : installe uniquement les dépendances de production
RUN poetry install --only main --no-root


# -----------------------------------------------------------------------------
# Stage 2: Production - Image finale légère
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS production

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement pour la production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Port par défaut pour l'application
    PORT=8000

# Créer un utilisateur non-root pour la sécurité
# (ne jamais exécuter une app en tant que root en production)
RUN useradd --create-home --shell /bin/bash appuser

# Copier les packages Python installés depuis le stage builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copier le code source de l'application
COPY --chown=appuser:appuser . .

# Collecter les fichiers statiques pour la production
# Cette commande copie tous les fichiers statiques dans STATIC_ROOT
# On utilise DEBUG=True temporairement pour éviter les erreurs de WhiteNoise
# sur les fichiers CSS référençant des assets manquants (fonts, images du template)
RUN DEBUG=True python manage.py collectstatic --noinput

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port de l'application
EXPOSE ${PORT}

# Commande de démarrage avec Gunicorn (serveur WSGI de production)
# --bind 0.0.0.0:$PORT : Écoute sur toutes les interfaces
# --workers 2 : Nombre de processus workers (ajuster selon les ressources)
# --threads 4 : Nombre de threads par worker
# --access-logfile - : Logs d'accès vers stdout
# --error-logfile - : Logs d'erreur vers stderr
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --access-logfile - --error-logfile -"]
