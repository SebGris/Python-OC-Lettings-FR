# Déploiement sur Render - OC Lettings

## Table des matières
1. [Qu'est-ce que Render ?](#1-quest-ce-que-render-)
2. [Pourquoi Render ?](#2-pourquoi-render-)
3. [Créer un compte Render](#3-créer-un-compte-render)
4. [Créer un Web Service](#4-créer-un-web-service)
5. [Configurer PostgreSQL](#5-configurer-postgresql)
6. [Configuration des variables d'environnement](#6-configuration-des-variables-denvironnement)
7. [Deploy Hook (Webhook)](#7-deploy-hook-webhook)
8. [Monitoring et Logs](#8-monitoring-et-logs)
9. [Dépannage](#9-dépannage)

---

## 1. Qu'est-ce que Render ?

**Render** est une plateforme cloud de type **PaaS (Platform as a Service)** qui permet de déployer des applications web facilement.

### Comparaison avec d'autres plateformes

| Plateforme | Type | Avantages | Inconvénients |
|------------|------|-----------|---------------|
| **Render** | PaaS | Simple, gratuit, Docker natif | Serveurs partagés (tier gratuit) |
| **Heroku** | PaaS | Mature, écosystème riche | Plus cher, plus complexe |
| **AWS** | IaaS | Très puissant, flexible | Complexe, courbe d'apprentissage |
| **DigitalOcean** | IaaS/PaaS | Bon rapport qualité/prix | Configuration manuelle |

### Comment Render fonctionne ?

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RENDER CLOUD                                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Votre Web Service                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │    │
│  │  │   Docker    │  │  Variables  │  │    SSL/HTTPS        │  │    │
│  │  │   Image     │  │   d'env     │  │   (automatique)     │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                              ▲                                       │
│                              │                                       │
│                     ┌────────┴────────┐                             │
│                     │  Deploy Hook    │                             │
│                     │  (Webhook URL)  │                             │
│                     └────────┬────────┘                             │
└─────────────────────────────│───────────────────────────────────────┘
                              │
                              │ curl POST
                              │
┌─────────────────────────────┴───────────────────────────────────────┐
│                      GITHUB ACTIONS                                  │
│                    (après build Docker)                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Pourquoi Render ?

### Avantages pour notre projet

| Fonctionnalité | Détail |
|----------------|--------|
| **Gratuit** | Tier gratuit suffisant pour les projets personnels/éducatifs |
| **Docker natif** | Supporte les images Docker directement |
| **Déploiement simple** | Via webhook ou git push |
| **SSL automatique** | HTTPS configuré automatiquement |
| **Logs intégrés** | Visualisation des logs en temps réel |
| **Variables d'env** | Interface simple pour gérer les secrets |

### Limitations du tier gratuit

- Le service "dort" après 15 minutes d'inactivité
- Premier accès après inactivité = ~30 secondes de délai (cold start)
- 750 heures/mois de runtime
- Pas de scaling automatique

---

## 3. Créer un compte Render

### Étapes

1. Aller sur **https://render.com**

2. Cliquer sur **"Get Started for Free"**

3. S'inscrire avec :
   - GitHub (recommandé - facilite l'intégration)
   - GitLab
   - Email

4. Confirmer l'email si nécessaire

### Interface Render

Après connexion, vous arrivez sur le **Dashboard** :

```
┌─────────────────────────────────────────────────────────────────────┐
│  RENDER DASHBOARD                                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  + New                     ← Bouton pour créer un nouveau service   │
│                                                                      │
│  Services                                                            │
│  ├── oc-lettings-web      [Web Service]   ● Live                    │
│  └── ma-base-de-donnees   [PostgreSQL]    ● Running                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 4. Créer un Web Service

### Étape 1 : Nouveau service

1. Cliquer sur **"+ New"** dans le Dashboard
2. Sélectionner **"Web Service"**

### Étape 2 : Choisir la source

Deux options possibles :

| Option | Description | Notre choix |
|--------|-------------|-------------|
| **Connect a repository** | Render build depuis le code source | Non |
| **Deploy an existing image** | Render utilise une image Docker existante | **Oui ✓** |

Choisir **"Deploy an existing image from a registry"**

### Étape 3 : Configurer l'image Docker

```
┌─────────────────────────────────────────────────────────────────────┐
│  Image URL                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ docker.io/sebgris/oc-lettings:latest                            ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  💡 Format : docker.io/USERNAME/IMAGE:TAG                           │
└─────────────────────────────────────────────────────────────────────┘
```

**Explication du format** :
- `docker.io` : Registre Docker Hub
- `sebgris` : Votre nom d'utilisateur Docker Hub
- `oc-lettings` : Nom de l'image
- `latest` : Tag de l'image (version)

### Étape 4 : Paramètres du service

| Paramètre | Valeur | Explication |
|-----------|--------|-------------|
| **Name** | `oc-lettings` | Nom affiché dans Render |
| **Region** | `Frankfurt (EU Central)` | Région la plus proche |
| **Instance Type** | `Free` | Tier gratuit |
| **Root Directory** | _(vide)_ | Laisser vide pour Docker |

### Étape 5 : Créer le service

Cliquer sur **"Create Web Service"**

Render va :
1. Télécharger l'image depuis Docker Hub
2. Démarrer le conteneur
3. Configurer le SSL
4. Fournir une URL publique

---

## 5. Configurer PostgreSQL

### Pourquoi PostgreSQL plutôt que SQLite ?

| SQLite | PostgreSQL |
|--------|------------|
| Fichier local | Base de données serveur |
| Pas adapté à la production | Adapté à la production |
| Un seul utilisateur à la fois | Multi-utilisateurs |
| Pas de persistance sur Render | Données persistantes |

### Options pour PostgreSQL

Deux options principales pour héberger PostgreSQL :

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **Render PostgreSQL** | Intégration native, URL interne | Expire après 90 jours (tier gratuit) |
| **Supabase** | Gratuit sans expiration, interface web SQL | Service externe, URL externe |

---

### Option A : Render PostgreSQL (intégré)

1. Dashboard → **"+ New"** → **"PostgreSQL"**

2. Configurer la base de données :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `oc-lettings-db` |
| **Database** | `oc_lettings` |
| **User** | _(généré automatiquement)_ |
| **Region** | `Frankfurt (EU Central)` |
| **PostgreSQL Version** | `16` (ou dernière version) |
| **Instance Type** | `Free` |

3. Cliquer sur **"Create Database"**

#### Récupérer l'URL de connexion Render

1. Dashboard → Votre base de données → **"Info"**
2. Copier **"Internal Database URL"** (pour les services Render)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Connections                                                         │
├─────────────────────────────────────────────────────────────────────┤
│  Internal Database URL                                               │
│  postgres://user:password@dpg-xxx.frankfurt-postgres.render.com/db  │
│                                                                      │
│  External Database URL                                               │
│  postgres://user:password@dpg-xxx.frankfurt-postgres.render.com/db  │
└─────────────────────────────────────────────────────────────────────┘
```

> **Note** : Le tier gratuit Render PostgreSQL expire après 90 jours. Pour un projet long terme, considérez Supabase.

---

### Option B : Supabase (recommandé pour projets long terme)

**Supabase** est une alternative open-source à Firebase qui offre PostgreSQL gratuit sans limite de temps.

#### Créer un projet Supabase

1. Aller sur **https://supabase.com** et créer un compte
2. Créer un nouveau projet :
   - **Organization** : Créer ou sélectionner
   - **Project name** : `oc-lettings`
   - **Database Password** : Générer et **sauvegarder** ce mot de passe
   - **Region** : `West EU (Ireland)` ou plus proche

3. Attendre la création (~2 minutes)

#### Récupérer l'URL de connexion Supabase

1. Dashboard → **Project Settings** (icône engrenage) → **Database**
2. Section **"Connection string"** → Onglet **"URI"**
3. Choisir **"Session Pooler"** (recommandé pour applications web)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Connection string                                                   │
├─────────────────────────────────────────────────────────────────────┤
│  Mode: Session (recommandé)                                         │
│                                                                      │
│  postgresql://postgres.[project-ref]:[YOUR-PASSWORD]@              │
│  aws-0-eu-west-1.pooler.supabase.com:5432/postgres                  │
└─────────────────────────────────────────────────────────────────────┘
```

4. Remplacer `[YOUR-PASSWORD]` par le mot de passe créé à l'étape 2

#### Pourquoi Session Pooler ?

| Mode | Description | Usage |
|------|-------------|-------|
| **Session** | Connexion dédiée par session | Applications web (Django) ✓ |
| **Transaction** | Connexion partagée par transaction | Serverless, haute charge |
| **Direct** | Connexion directe sans pooler | Migrations, outils d'admin |

#### Interface SQL Supabase

Supabase offre un éditeur SQL intégré pour vérifier vos données :
1. Dashboard → **SQL Editor**
2. Exécuter des requêtes : `SELECT * FROM profiles_profile;`

---

### Lier la base au Web Service

1. Dashboard → Votre Web Service → **"Environment"**
2. Ajouter une variable :
   - **Key** : `DATABASE_URL`
   - **Value** : L'URL interne copiée

### Initialiser la base de données

Après le premier déploiement, vous devez créer les tables :

1. Dashboard → Votre Web Service → **"Shell"**
2. Exécuter :

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Fonctionnement dans le code

Le fichier `settings.py` détecte automatiquement `DATABASE_URL` :

```python
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Production: PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            ...
        }
    }
else:
    # Développement local: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            ...
        }
    }
```

---

## 6. Configuration des variables d'environnement

### Accéder aux variables

1. Dashboard → Votre service → **"Environment"**

### Variables à configurer

```
┌─────────────────────────────────────────────────────────────────────┐
│  Environment Variables                                               │
├─────────────────────────────────────────────────────────────────────┤
│  Key                    Value                                        │
│  ─────────────────────  ────────────────────────────────────────────│
│  DATABASE_URL           postgres://user:pass@host/db                 │
│  SECRET_KEY             votre-cle-secrete-tres-longue-et-complexe   │
│  DEBUG                  False                                        │
│  ALLOWED_HOSTS          python-oc-lettings-fr-vu8j.onrender.com     │
│  SENTRY_DSN             https://xxx@sentry.io/xxx                   │
│  SENTRY_ENVIRONMENT     production                                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Explication de chaque variable

| Variable | Description | Valeur en production |
|----------|-------------|---------------------|
| `DATABASE_URL` | URL de connexion PostgreSQL | Depuis Render PostgreSQL (voir section 5) |
| `SECRET_KEY` | Clé cryptographique Django pour les sessions, CSRF, etc. | Une clé unique et secrète (50+ caractères) |
| `DEBUG` | Mode debug Django | **False** (JAMAIS True en production) |
| `ALLOWED_HOSTS` | Domaines autorisés à accéder à l'app | L'URL Render de votre app |
| `SENTRY_DSN` | URL de connexion à Sentry pour le monitoring | Depuis votre projet Sentry |
| `SENTRY_ENVIRONMENT` | Identifie l'environnement dans Sentry | `production` |

### Générer une SECRET_KEY sécurisée

> Voir [docker-local-setup.md](docker-local-setup.md#2-générer-une-secret_key) pour les méthodes de génération.

### Différence Local vs Production

| Variable | Local (.env) | Production (Render) |
|----------|--------------|---------------------|
| `SECRET_KEY` | N'importe quelle valeur | Clé unique et secrète |
| `DEBUG` | `True` | **`False`** |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `votre-app.onrender.com` |
| `SENTRY_DSN` | _(vide ou test)_ | DSN de production |
| `SENTRY_ENVIRONMENT` | `development` | `production` |

---

## 7. Deploy Hook (Webhook)

### Qu'est-ce qu'un Deploy Hook ?

Un **Deploy Hook** est une URL secrète qui, lorsqu'elle reçoit une requête HTTP POST, déclenche un redéploiement du service.

```
GitHub Actions                              Render
     │                                         │
     │  curl -X POST "https://..."             │
     │────────────────────────────────────────▶│
     │                                         │
     │                          ┌──────────────┤
     │                          │ Pull image   │
     │                          │ from Docker  │
     │                          │ Hub          │
     │                          ├──────────────┤
     │                          │ Restart      │
     │                          │ container    │
     │                          └──────────────┤
     │                                         │
     │◀────────────────────────────────────────│
     │         Déploiement terminé             │
```

### Obtenir le Deploy Hook

1. Dashboard → Votre service → **"Settings"**
2. Descendre jusqu'à **"Deploy Hook"**
3. Copier l'URL

```
┌─────────────────────────────────────────────────────────────────────┐
│  Deploy Hook                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ https://api.render.com/deploy/srv-xxx?key=yyy                   ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ⚠️  Gardez cette URL secrète !                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Configurer le Deploy Hook dans GitHub

1. GitHub → Votre repo → **Settings** → **Secrets and variables** → **Actions**
2. Cliquer sur **"New repository secret"**
3. Nom : `RENDER_DEPLOY_HOOK_URL`
4. Valeur : L'URL copiée depuis Render
5. Cliquer sur **"Add secret"**

### Comment le webhook est utilisé

Dans notre fichier `.github/workflows/ci-cd.yml` :

```yaml
deploy:
  name: Deploy to Render
  runs-on: ubuntu-latest
  needs: build
  steps:
    - name: Deploy to Render
      run: curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

---

## 8. Monitoring et Logs

### Accéder aux logs

1. Dashboard → Votre service → **"Logs"**

### Types de logs

```
┌─────────────────────────────────────────────────────────────────────┐
│  Logs                                                  [Live] [All] │
├─────────────────────────────────────────────────────────────────────┤
│  Dec 16 10:30:15  Starting gunicorn                                 │
│  Dec 16 10:30:16  [INFO] Starting server on 0.0.0.0:8000           │
│  Dec 16 10:30:17  [INFO] Using worker: sync                         │
│  Dec 16 10:30:20  "GET / HTTP/1.1" 200 1523                        │
│  Dec 16 10:30:25  "GET /lettings/ HTTP/1.1" 200 2341               │
└─────────────────────────────────────────────────────────────────────┘
```

| Type | Description |
|------|-------------|
| **Build logs** | Logs lors du téléchargement/démarrage de l'image |
| **Runtime logs** | Logs de l'application en cours d'exécution |
| **Deploy logs** | Logs des déploiements (succès/échec) |

### Métriques disponibles

- **CPU** : Utilisation processeur
- **Memory** : Utilisation mémoire
- **Bandwidth** : Trafic réseau

---

## 9. Dépannage

### Erreur 502 Bad Gateway

**Cause** : L'application ne démarre pas correctement.

**Solutions** :
1. Vérifier les logs Render
2. Vérifier que `SECRET_KEY` est définie
3. Vérifier que `ALLOWED_HOSTS` contient l'URL Render

### Erreur "Service unavailable" après inactivité

**Cause** : Le tier gratuit met le service en veille après 15 min.

**Solution** : C'est normal. Le premier accès prend ~30 secondes pour "réveiller" le service.

### Les fichiers statiques ne s'affichent pas (CSS manquant)

**Cause** : WhiteNoise ou collectstatic non configuré.

**Solutions** :
1. Vérifier que `whitenoise` est dans `requirements.txt`
2. Vérifier que le Dockerfile exécute `collectstatic`
3. Reconstruire et redéployer l'image

### Erreur 500 sur certaines pages

**Cause** : Erreur dans l'application Django.

**Solutions** :
1. Consulter les logs Render
2. Consulter Sentry si configuré
3. Vérifier les variables d'environnement

### Le déploiement via webhook ne fonctionne pas

**Causes possibles** :
1. URL du webhook incorrecte
2. Secret GitHub mal configuré
3. Image Docker Hub non accessible

**Vérifications** :
- Tester le webhook manuellement avec `curl -X POST "VOTRE_URL_WEBHOOK"`
- Vérifier les logs Render après le déclenchement

---

## URLs de référence pour ce projet

| Service | URL |
|---------|-----|
| **Application** | https://python-oc-lettings-fr-vu8j.onrender.com |
| **Dashboard Render** | https://dashboard.render.com/web/srv-d50jl275r7bs739gbd60 |
| **Docker Hub** | https://hub.docker.com/r/sebgris/oc-lettings |

---

## Résumé des étapes

1. Créer un compte Render
2. Créer un Web Service "Deploy from Docker Registry"
3. Image URL : `docker.io/sebgris/oc-lettings:latest`
4. Configurer les variables d'environnement
5. Copier le Deploy Hook URL
6. Ajouter le Deploy Hook comme secret GitHub
7. Pousser du code pour déclencher le déploiement
