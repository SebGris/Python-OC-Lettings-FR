# Documentation Docker - OC Lettings

## Table des matières
1. [Introduction à Docker](#1-introduction-à-docker)
2. [Concepts clés](#2-concepts-clés)
3. [Notre Dockerfile expliqué](#3-notre-dockerfile-expliqué)
4. [Docker Compose](#4-docker-compose)
5. [Bonnes pratiques appliquées](#5-bonnes-pratiques-appliquées)

> **Commandes Docker** : Voir [docker-commands.md](docker-commands.md) pour la référence complète des commandes.

---

## 1. Introduction à Docker

### Qu'est-ce que Docker ?
Docker est une plateforme de **conteneurisation** qui permet d'empaqueter une application avec toutes ses dépendances dans un conteneur isolé.

### Pourquoi utiliser Docker ?
- **Reproductibilité** : "Ça marche sur ma machine" devient "Ça marche partout"
- **Isolation** : Chaque conteneur est indépendant
- **Portabilité** : Un conteneur fonctionne sur n'importe quel système avec Docker
- **Scalabilité** : Facile de dupliquer des conteneurs

### Différence entre conteneur et machine virtuelle
```
┌─────────────────────────────────────┐    ┌─────────────────────────────────────┐
│         Machine Virtuelle           │    │           Conteneur Docker          │
├─────────────────────────────────────┤    ├─────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐           │    │  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │App 1│ │App 2│ │App 3│           │    │  │App 1│ │App 2│ │App 3│           │
│  └─────┘ └─────┘ └─────┘           │    │  └─────┘ └─────┘ └─────┘           │
│  ┌─────┐ ┌─────┐ ┌─────┐           │    │  └──────────────────────────────────┤
│  │OS   │ │OS   │ │OS   │           │    │            Docker Engine            │
│  └─────┘ └─────┘ └─────┘           │    ├─────────────────────────────────────┤
│        Hyperviseur                  │    │           Système d'exploitation    │
├─────────────────────────────────────┤    └─────────────────────────────────────┘
│     Système d'exploitation          │
└─────────────────────────────────────┘

→ VM : Chaque app a son propre OS complet (lourd)
→ Docker : Les apps partagent le kernel de l'hôte (léger)
```

---

## 2. Concepts clés

### Image Docker
Une **image** est un template en lecture seule qui contient :
- Le système de fichiers
- Le code de l'application
- Les dépendances
- Les variables d'environnement
- La commande de démarrage

### Conteneur
Un **conteneur** est une instance en cours d'exécution d'une image.

### Dockerfile
Un **Dockerfile** est un fichier texte contenant les instructions pour construire une image.

### Docker Hub
**Docker Hub** est un registre public d'images Docker (comme GitHub pour le code).

---

## 3. Notre Dockerfile expliqué

### Structure multi-stage

Notre Dockerfile utilise une approche **multi-stage** pour optimiser la taille de l'image finale :

```dockerfile
# =============================================================================
# STAGE 1: Builder
# =============================================================================
FROM python:3.13-slim as builder
```

**Pourquoi `python:3.13-slim` ?**
- `slim` : Version allégée sans packages superflus (~150MB vs ~1GB pour la version complète)
- `3.13` : Version de Python compatible avec notre projet

### Comment savoir sur quel OS est basée une image Docker ?

L'image `python:3.13-slim` est basée sur **Debian Linux**. Plusieurs méthodes pour le vérifier :

**1. Sur Docker Hub** : https://hub.docker.com/_/python
   - La documentation indique que les images `slim` sont basées sur Debian

**2. Via la ligne de commande** :
```bash
docker run --rm python:3.13-slim cat /etc/os-release
```
Résultat :
```
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
```

**3. Sur GitHub** : https://github.com/docker-library/python
   - Les Dockerfiles officiels montrent `debian:bookworm-slim` comme base

### Variantes d'images Python disponibles

| Tag | Base OS | Taille | Usage | Gestionnaire paquets |
|-----|---------|--------|-------|---------------------|
| `python:3.13` | Debian (full) | ~1 GB | Développement | `apt-get` |
| `python:3.13-slim` | Debian (minimal) | ~150 MB | **Production** ✓ | `apt-get` |
| `python:3.13-alpine` | Alpine Linux | ~50 MB | Ultra-léger | `apk` |
| `python:3.13-bookworm` | Debian 12 | ~1 GB | Debian spécifique | `apt-get` |

**Notre choix : `python:3.13-slim`** car c'est le meilleur compromis taille/compatibilité pour la production

```dockerfile
WORKDIR /app
```
**WORKDIR** : Définit le répertoire de travail dans le conteneur. Toutes les commandes suivantes s'exécuteront depuis ce dossier.

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```
**Variables d'environnement Python** :
- `PYTHONDONTWRITEBYTECODE=1` : Ne crée pas de fichiers `.pyc` (cache bytecode) → réduit la taille
- `PYTHONUNBUFFERED=1` : Les logs Python s'affichent immédiatement (important pour Docker)

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
```

### Explication détaillée de la commande apt-get

`apt-get` est le gestionnaire de paquets de **Debian/Ubuntu**. Comme notre image Docker est basée sur Debian, on utilise `apt-get` pour installer des logiciels système.

**Décomposition de la commande :**

| Partie | Explication |
|--------|-------------|
| `apt-get update` | Met à jour la liste des paquets disponibles depuis les dépôts Debian |
| `&&` | Opérateur ET : exécute la commande suivante seulement si la précédente réussit |
| `apt-get install -y` | Installe des paquets. `-y` = accepte automatiquement (pas de prompt interactif) |
| `--no-install-recommends` | N'installe pas les paquets "recommandés" (garde l'image légère) |
| `gcc` | Le compilateur C GNU, nécessaire pour compiler des extensions Python en C |
| `rm -rf /var/lib/apt/lists/*` | Supprime le cache apt pour réduire la taille de l'image |

**Pourquoi GCC est nécessaire ?**
Certains packages Python (comme des parties de `gunicorn` ou `sentry-sdk`) contiennent du code C qui doit être compilé lors du `pip install`. Sans `gcc`, l'installation échouerait.

**Pourquoi tout en une seule ligne `RUN` ?**
Docker crée une "couche" (layer) pour chaque instruction `RUN`. En combinant les commandes avec `&&`, on crée une seule couche qui inclut l'installation ET le nettoyage, ce qui réduit la taille finale de l'image.

**Gestionnaires de paquets selon l'OS :**

| Système | Commande | Exemple |
|---------|----------|---------|
| Debian/Ubuntu | `apt-get` | `apt-get install gcc` |
| Alpine Linux | `apk` | `apk add gcc` |
| Red Hat/CentOS | `yum` ou `dnf` | `yum install gcc` |
| macOS | `brew` | `brew install gcc` |
| Windows | `choco` | `choco install gcc` |

**Liens pour approfondir :**
- Documentation apt : https://wiki.debian.org/AptCLI
- Best practices Dockerfile : https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#run

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

### Explication détaillée de la commande pip install

`pip` est le gestionnaire de paquets de **Python**. Il permet d'installer des bibliothèques Python depuis PyPI (Python Package Index).

**Décomposition de la commande :**

| Partie | Explication |
|--------|-------------|
| `pip install` | Commande pour installer des packages Python |
| `--no-cache-dir` | N'utilise pas le cache pip (réduit la taille de l'image Docker) |
| `--prefix=/install` | Installe les packages dans `/install` au lieu du dossier par défaut |
| `-r` | **Read** : lire la liste des packages depuis un fichier |
| `requirements.txt` | Fichier contenant la liste des packages à installer |

**Pourquoi `-r requirements.txt` ?**

Le `-r` est un raccourci pour installer tous les packages d'un projet en une seule commande :

```bash
# Avec -r (lit le fichier)
pip install -r requirements.txt

# Équivalent à installer chaque package manuellement
pip install django==4.2.16
pip install flake8==7.3.0
pip install pytest-django==4.11.1
pip install pytest-cov==6.0.0
pip install sentry-sdk==2.47.0
pip install python-dotenv==1.2.1
pip install gunicorn==23.0.0
pip install whitenoise==6.11.0
```

**Pourquoi `--prefix=/install` ?**

Dans un build multi-stage, on installe les packages dans un dossier séparé (`/install`) pour pouvoir les copier facilement vers l'image de production :

```dockerfile
# Stage 1 : Installation dans /install
RUN pip install --prefix=/install -r requirements.txt

# Stage 2 : Copie depuis /install vers /usr/local
COPY --from=builder /install /usr/local
```

Cela permet de ne copier que les packages Python, sans les outils de build (gcc, etc.).

### Stage 2: Production

```dockerfile
FROM python:3.13-slim AS production
```
**Nouvelle image propre** : On repart d'une image vierge pour n'inclure que le nécessaire.

```dockerfile
WORKDIR /app
```
**Répertoire de travail** : Même répertoire que dans le stage builder.

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
```
**Variables d'environnement** : On redéfinit les variables Python + le port par défaut.

```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
```
**Utilisateur non-root** : Pour la sécurité, on ne lance jamais une app en tant que root en production.

```dockerfile
COPY --from=builder /install /usr/local
```
**Copie depuis le builder** : On récupère uniquement les packages Python installés (pas gcc ni le cache apt).

```dockerfile
COPY --chown=appuser:appuser . .
```
**Copie du code** : `--chown` change le propriétaire pour notre utilisateur non-root.

```dockerfile
RUN DEBUG=True python manage.py collectstatic --noinput
```
**Fichiers statiques** : Collecte tous les fichiers CSS/JS/images dans `STATIC_ROOT`.
- `DEBUG=True` est utilisé temporairement pour éviter les erreurs de WhiteNoise sur les fichiers CSS référençant des assets manquants (fonts, images du template).

```dockerfile
USER appuser
```
**Changement d'utilisateur** : Toutes les commandes suivantes s'exécutent en tant que `appuser` (non-root).

```dockerfile
EXPOSE ${PORT}
```
**Exposition du port** : Indique que le conteneur écoute sur le port défini par `$PORT` (8000 par défaut).

```dockerfile
CMD ["sh", "-c", "gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --access-logfile - --error-logfile -"]
```
**Commande de démarrage** avec Gunicorn :
- `sh -c` : Permet d'utiliser la variable d'environnement `$PORT`
- `--bind 0.0.0.0:$PORT` : Écoute sur toutes les interfaces réseau
- `--workers 2` : 2 processus workers (ajuster selon les ressources du serveur)
- `--threads 4` : 4 threads par worker
- `--access-logfile -` : Logs d'accès vers stdout (capturés par Docker)
- `--error-logfile -` : Logs d'erreur vers stderr (capturés par Docker)

---

## 4. Docker Compose

### Qu'est-ce que Docker Compose ?
Docker Compose permet de définir et gérer des applications multi-conteneurs avec un simple fichier YAML.

### Notre fichier docker-compose.yml expliqué

**Note** : L'attribut `version` n'est plus nécessaire dans les versions récentes de Docker Compose et a été supprimé.

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
```
**Build** :
- `context: .` : Le contexte de build est le dossier courant
- `dockerfile: Dockerfile` : Utilise le Dockerfile à la racine
- `target: production` : Utilise le stage "production" du Dockerfile multi-stage

```yaml
    container_name: oc-lettings-web
```
**Nom du conteneur** : Facilite l'identification dans `docker ps` et les commandes `docker logs`.

```yaml
    ports:
      - "8000:8000"
```
**Mapping des ports** : `port_hôte:port_conteneur`
- Le port 8000 de votre machine → port 8000 du conteneur
- Accès via http://localhost:8000

```yaml
    environment:
      - SECRET_KEY=${SECRET_KEY:-change-me-in-production}
      - DEBUG=${DEBUG:-False}
      - ALLOWED_HOSTS=${ALLOWED_HOSTS:-localhost,127.0.0.1}
      - SENTRY_DSN=${SENTRY_DSN:-}
      - SENTRY_ENVIRONMENT=${SENTRY_ENVIRONMENT:-development}
      - PORT=8000
```
**Variables d'environnement** :
- `${VARIABLE:-valeur_defaut}` : Utilise la variable d'env ou une valeur par défaut si non définie
- Ces variables sont lues depuis le fichier `.env` à la racine du projet
- `PORT=8000` : Port fixe utilisé par Gunicorn dans le conteneur

```yaml
    volumes:
      - ./oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3
```
**Volumes** : Monte la base de données SQLite depuis l'hôte pour persister les données.
- Format : `chemin_hôte:chemin_conteneur`
- Permet de conserver les données même si le conteneur est supprimé

```yaml
    restart: unless-stopped
```
**Politique de redémarrage** : Le conteneur redémarre automatiquement sauf s'il est arrêté manuellement.

```yaml
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```
**Healthcheck** : Vérifie que l'application fonctionne correctement.
- `test` : Commande pour tester la santé (requête HTTP vers la page d'accueil)
- `interval` : Temps entre chaque vérification (30 secondes)
- `timeout` : Temps maximum pour la réponse (10 secondes)
- `retries` : Nombre de tentatives avant de marquer comme "unhealthy" (3)
- `start_period` : Délai avant la première vérification (10 secondes)

### Lancer sans Docker Compose (avec docker run)

Si vous ne souhaitez pas utiliser `docker-compose.yml`, vous pouvez lancer l'image directement avec `docker run` :

```bash
docker run -d -p 8000:8000 --name oc-lettings-app -e SECRET_KEY=votre-cle-secrete -e DEBUG=False -e ALLOWED_HOSTS=localhost,127.0.0.1 sebgris/oc-lettings:latest
# Ajoutez l'option -v pour monter un volume
docker run -d -p 8000:8000 --name oc-lettings-app -e SECRET_KEY=votre-cle-secrete -e DEBUG=False -e ALLOWED_HOSTS=localhost,127.0.0.1 -v ./oc-lettings-site.sqlite3:/app/oc-lettings-site.sqlite3 sebgris/oc-lettings:latest
```

**Explication des options :**

| Option | Explication |
|--------|-------------|
| `-d` | Mode détaché (arrière-plan) |
| `-p 8000:8000` | Mapping port hôte:conteneur |
| `--name oc-lettings-app` | Nom du conteneur |
| `-e SECRET_KEY=...` | Variable d'environnement |
| `sebgris/oc-lettings:latest` | Nom de l'image à lancer |

**Différence entre docker-compose et docker run :**

| docker-compose | docker run |
|----------------|------------|
| Lit les variables depuis `.env` automatiquement | Variables passées en `-e` manuellement |
| Configure volumes, healthcheck, restart | Tout doit être ajouté manuellement |
| `docker-compose up --build` | `docker build` + `docker run` séparément |
| Plus simple pour le développement | Plus de contrôle, mais plus verbeux |

---

## 5. Bonnes pratiques appliquées

### 1. Multi-stage build
**Pourquoi ?** Réduit la taille de l'image finale en ne gardant que le nécessaire.

```dockerfile
# Stage 1 : Compile et installe (avec gcc, etc.)
FROM python:3.13-slim as builder
# ... installation ...

# Stage 2 : Image finale légère
FROM python:3.13-slim as production
COPY --from=builder /install /usr/local
```

### 2. Utilisateur non-root
**Pourquoi ?** Sécurité - si le conteneur est compromis, l'attaquant n'a pas les droits root.

```dockerfile
RUN useradd --create-home appuser
USER appuser
```

### 3. .dockerignore
**Pourquoi ?** Accélère le build et réduit la taille en excluant les fichiers inutiles.

```
venv/
__pycache__/
.git/
*.md
```

### 4. Layer caching
**Pourquoi ?** Accélère les builds en réutilisant les layers inchangés.

```dockerfile
# On copie d'abord requirements.txt seul
COPY requirements.txt .
RUN pip install -r requirements.txt

# Puis le reste du code
COPY . .
```
→ Si le code change mais pas requirements.txt, pip install n'est pas réexécuté.

### 5. Variables d'environnement
**Pourquoi ?** Configuration flexible sans modifier l'image.

```dockerfile
ENV PORT=8000
CMD gunicorn --bind 0.0.0.0:$PORT
```

### 6. Healthcheck (dans docker-compose)
**Pourquoi ?** Permet à Docker de vérifier si l'application fonctionne.

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/')"]
  interval: 30s
  timeout: 10s
  retries: 3
```
