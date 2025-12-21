# Documentation CI/CD - OC Lettings

## Table des matières
1. [Introduction au CI/CD](#1-introduction-au-cicd)
2. [GitHub Actions](#2-github-actions)
3. [Notre Pipeline expliqué](#3-notre-pipeline-expliqué)
4. [Configuration des secrets](#4-configuration-des-secrets)
5. [Déploiement sur Render](#5-déploiement-sur-render)
6. [Dépannage](#6-dépannage)

> **Note** : Ce projet utilise **Poetry** pour la gestion des dépendances Python.

---

## 1. Introduction au CI/CD

### Qu'est-ce que CI/CD ?

**CI (Continuous Integration)** - Intégration Continue :
- Automatise les tests à chaque modification du code
- Détecte les bugs rapidement
- Assure que le code est toujours dans un état fonctionnel

**CD (Continuous Delivery/Deployment)** - Livraison/Déploiement Continu :
- Automatise la mise en production
- Réduit les erreurs humaines
- Permet des déploiements fréquents et fiables

### Flux de travail CI/CD

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Commit    │────▶│    Test     │────▶│    Build    │────▶│   Deploy    │
│   (Push)    │     │  (Pytest)   │     │  (Docker)   │     │  (Render)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │                   │
                          ▼                   ▼                   ▼
                    Si échec: Stop      Si échec: Stop      Application
                    et notifier         et notifier          en ligne
```

---

## 2. GitHub Actions

### Qu'est-ce que GitHub Actions ?
GitHub Actions est un service d'automatisation intégré à GitHub qui permet d'exécuter des workflows (scripts) en réponse à des événements.

### Concepts clés

#### Workflow
Un **workflow** est un processus automatisé défini dans un fichier YAML.
- Emplacement : `.github/workflows/`
- Extension : `.yml` ou `.yaml`

#### Job
Un **job** est un ensemble d'étapes qui s'exécutent sur la même machine virtuelle.

```yaml
jobs:
  test:           # Nom du job
    runs-on: ubuntu-latest
    steps:
      - name: Étape 1
      - name: Étape 2
```

#### Step
Une **step** (étape) est une tâche individuelle dans un job.

```yaml
steps:
  - name: Checkout code
    uses: actions/checkout@v4    # Action pré-construite

  - name: Run tests
    run: pytest                   # Commande shell
```

#### Action
Une **action** est un composant réutilisable (comme une fonction).

```yaml
# Action officielle pour checkout le code
uses: actions/checkout@v4

# Action pour configurer Python
uses: actions/setup-python@v5
```

#### Runner
Un **runner** est la machine qui exécute le job.

```yaml
runs-on: ubuntu-latest    # Machine virtuelle Ubuntu
```

---

## 3. Notre Pipeline expliqué

### Fichier `.github/workflows/ci-cd.yml`

#### Déclencheurs (Triggers)

```yaml
on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master
```

**Explication** :
- `push` sur `master` : Le workflow se lance quand du code est poussé sur master
- `pull_request` vers `master` : Se lance quand une PR cible master

#### Variables globales

```yaml
env:
  DOCKER_IMAGE: ${{ secrets.DOCKER_USERNAME }}/oc-lettings
```

**Explication** :
- `${{ secrets.XXX }}` : Accède aux secrets GitHub (variables sécurisées)
- L'image Docker sera nommée `votre-username/oc-lettings`

---

### Job 1: Tests & Linting

```yaml
test:
  name: Tests & Linting
  runs-on: ubuntu-latest
```

**Objectif** : Vérifier la qualité du code avant tout déploiement.

#### Étapes détaillées

```yaml
- name: Checkout code
  uses: actions/checkout@v4
```
**Checkout** : Clone le repository dans le runner.

```yaml
- name: Set up Python 3.13
  uses: actions/setup-python@v5
  with:
    python-version: '3.13'
```
**Setup Python** : Installe Python 3.13.

```yaml
- name: Install Poetry
  uses: snok/install-poetry@v1
  with:
    version: ${{ env.POETRY_VERSION }}
    virtualenvs-create: true
    virtualenvs-in-project: true
```
**Poetry** : Installe Poetry avec un virtualenv dans le projet (`.venv/`).

```yaml
- name: Load cached venv
  uses: actions/cache@v4
  with:
    path: .venv
    key: venv-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}
```
**Cache** : Réutilise le virtualenv si `poetry.lock` n'a pas changé.

```yaml
- name: Install dependencies
  if: steps.cached-poetry-dependencies.outputs.cache-hit != 'true'
  run: poetry install --no-interaction --no-root
```
**Dépendances** : Installe les packages uniquement si le cache est manquant.

```yaml
- name: Run flake8 linting
  run: poetry run python -m flake8
```
**Linting** : Vérifie le style de code (PEP 8) via Poetry.

```yaml
- name: Run tests with coverage
  env:
    SECRET_KEY: test-secret-key-for-ci
    DEBUG: 'True'
  run: poetry run python -m pytest --cov --cov-fail-under=80
```
**Tests** :
- `poetry run` : Exécute dans le virtualenv Poetry
- `env` : Variables d'environnement pour les tests
- `--cov` : Active la couverture de code
- `--cov-fail-under=80` : Échoue si la couverture est < 80%

---

### Job 2: Build & Push Docker

> **Note** : Le Dockerfile utilise une approche **multi-stage** avec deux images. Voir [docker.md](docker.md#3-notre-dockerfile-expliqué) pour les détails complets.

#### Pourquoi deux images (multi-stage) ?

```
┌─────────────────────────────────────┐     ┌─────────────────────────────────────┐
│         Stage 1: Builder            │     │       Stage 2: Production           │
├─────────────────────────────────────┤     ├─────────────────────────────────────┤
│  - Python 3.13-slim                 │     │  - Python 3.13-slim                 │
│  - gcc, curl (outils de build)      │     │  - Packages Python uniquement       │
│  - Poetry                           │────▶│  - Code source                      │
│  - Installation des dépendances     │     │  - Fichiers statiques               │
│                                     │     │  - Utilisateur non-root             │
│  Taille: ~500 MB                    │     │  Taille: ~200 MB                    │
└─────────────────────────────────────┘     └─────────────────────────────────────┘
         Image temporaire                          Image finale déployée
```

**Avantages** :
- **Sécurité** : Pas d'outils de build (gcc, curl) en production
- **Taille réduite** : L'image finale ne contient que le nécessaire
- **Performance** : Téléchargement et démarrage plus rapides

```yaml
build:
  name: Build & Push Docker Image
  runs-on: ubuntu-latest
  needs: test
  if: github.ref == 'refs/heads/master' && github.event_name == 'push'
```

**Explication** :
- `needs: test` : S'exécute seulement si le job `test` réussit
- `if: ...` : S'exécute seulement sur push vers master (pas sur les PRs)

#### Étapes détaillées

```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3
```
**Buildx** : Outil avancé de build Docker (cache, multi-plateforme).

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```
**Login** : Se connecte à Docker Hub avec les credentials secrets.

```yaml
- name: Extract metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: ${{ env.DOCKER_IMAGE }}
    tags: |
      type=sha,prefix=
      type=raw,value=latest,enable={{is_default_branch}}
```
**Metadata** : Génère les tags de l'image.
- `type=sha` : Tag avec le SHA du commit (ex: `abc1234`)
- `type=raw,value=latest` : Tag `latest` sur master

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```
**Build & Push** :
- `push: true` : Pousse l'image sur Docker Hub
- `cache-from/to` : Utilise le cache GitHub Actions pour accélérer

---

### Job 3: Déploiement

```yaml
deploy:
  name: Deploy to Render
  runs-on: ubuntu-latest
  needs: build
  if: github.ref == 'refs/heads/master' && github.event_name == 'push'
```

**Explication** : S'exécute après le build, uniquement sur master.

```yaml
- name: Deploy to Render
  run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```
**Déploiement** : Déclenche un webhook Render pour déployer la nouvelle image.

---

## 4. Configuration des secrets

### Secrets nécessaires

Dans GitHub → Settings → Secrets and variables → Actions :

| Secret | Description | Exemple |
|--------|-------------|---------|
| `DOCKER_USERNAME` | Votre nom d'utilisateur Docker Hub | `monusername` |
| `DOCKER_PASSWORD` | Token d'accès Docker Hub | `dckr_pat_xxxx` |
| `RENDER_DEPLOY_HOOK_URL` | URL webhook Render | `https://api.render.com/deploy/...` |

### Créer un token Docker Hub

1. Aller sur https://hub.docker.com
2. Account Settings → Security → New Access Token
3. Donner un nom (ex: "github-actions")
4. Copier le token et l'ajouter comme secret GitHub

### Obtenir le webhook Render

1. Aller sur https://dashboard.render.com
2. Sélectionner votre service
3. Settings → Deploy Hook
4. Copier l'URL et l'ajouter comme secret GitHub

---

## 5. Déploiement sur Render

> **Documentation complète** : Voir [render.md](render.md) pour les explications détaillées sur Render.

### Résumé rapide

**Render** est une plateforme PaaS gratuite qui héberge notre application Django via Docker.

### Flux de déploiement

```
Developer                GitHub Actions              Docker Hub              Render
    │                          │                          │                    │
    │  git push master         │                          │                    │
    │─────────────────────────▶│                          │                    │
    │                          │  tests + linting         │                    │
    │                          │──────────────────────────│                    │
    │                          │  build docker            │                    │
    │                          │─────────────────────────▶│                    │
    │                          │                          │  push image        │
    │                          │                          │───────────────────▶│
    │                          │  webhook deploy          │                    │
    │                          │────────────────────────────────────────────────▶
    │                          │                          │                    │
    │                          │                          │  pull image        │
    │                          │                          │◀───────────────────│
    │                          │                          │                    │
    │◀──────────────────────────────────────────────────────────────────────────│
    │                                App déployée et accessible !              │
```

### Configuration minimale

1. Créer un Web Service sur Render
2. Image URL : `docker.io/sebgris/oc-lettings:latest`
3. Configurer les variables d'environnement (voir [render.md](render.md#5-configuration-des-variables-denvironnement))
4. Copier le Deploy Hook et l'ajouter comme secret GitHub

---

## 6. Dépannage

### Problèmes courants

#### Les tests échouent
```bash
# Vérifier localement
poetry run python -m pytest --cov --cov-fail-under=80

# Vérifier le linting
poetry run python -m flake8
```

#### Le build Docker échoue
```bash
# Construire localement pour débuguer
docker build -t oc-lettings .

# Vérifier les logs de build
docker build --progress=plain -t oc-lettings .
```

#### Le push Docker Hub échoue
- Vérifier que `DOCKER_USERNAME` et `DOCKER_PASSWORD` sont corrects
- Le token Docker Hub a-t-il expiré ?
- Le nom de l'image est-il correct ?

#### Le déploiement Render échoue
- Vérifier le webhook URL dans les secrets
- Consulter les logs Render : Dashboard → Service → Logs
- Vérifier les variables d'environnement Render

### Visualiser les workflows

1. GitHub → Onglet "Actions"
2. Cliquer sur un workflow pour voir les détails
3. Chaque job peut être expansé pour voir les logs

### Relancer un workflow

1. GitHub → Actions → Workflow concerné
2. "Re-run all jobs" ou "Re-run failed jobs"

---

## Résumé des étapes de configuration

### 1. Configurer Docker Hub
```bash
# Créer un compte sur hub.docker.com
# Créer un Access Token (Settings → Security)
```

### 2. Configurer les secrets GitHub
```
Settings → Secrets → Actions → New repository secret

DOCKER_USERNAME = votre-username
DOCKER_PASSWORD = votre-token
RENDER_DEPLOY_HOOK_URL = https://api.render.com/deploy/...
```

### 3. Configurer Render

> Voir [render.md](render.md) pour les instructions détaillées.

```
1. Créer un Web Service depuis Docker Registry
2. Image: docker.io/username/oc-lettings:latest
3. Configurer les variables d'environnement
4. Copier le Deploy Hook URL
```

### 4. Tester le pipeline
```bash
# Faire une modification
echo "# test" >> README.md
git add . && git commit -m "Test CI/CD" && git push

# Vérifier sur GitHub Actions que le pipeline passe
```
