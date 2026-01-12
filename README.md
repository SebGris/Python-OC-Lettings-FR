## Résumé

Site web d'OC Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.13 ou supérieure
- Poetry (gestionnaire de dépendances Python)

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### Installation de Poetry

#### Windows (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

#### macOS / Linux
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Après l'installation, redémarrez votre terminal.

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Installer les dépendances avec Poetry

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry install`
- Confirmer que la version de l'interpréteur Python est la version 3.13 ou supérieure `poetry run python --version`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `poetry run pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement Poetry, les commandes sont préfixées par `poetry run`
- Exemple : `poetry run python manage.py runserver`

### Commandes Poetry courantes

| Ancienne commande (pip) | Nouvelle commande (Poetry) |
|------------------------|---------------------------|
| `pip install package` | `poetry add package` |
| `pip install -r requirements.txt` | `poetry install` |
| `pip install package --dev` | `poetry add package --group dev` |
| `python script.py` | `poetry run python script.py` |
| `pytest` | `poetry run pytest` |
| `flake8` | `poetry run flake8` |

---

## Déploiement avec Docker

### Prérequis

- Docker et Docker Desktop installés et en cours d'exécution
- Compte Docker Hub (pour télécharger l'image)

### Télécharger et exécuter l'image Docker

L'application est disponible sous forme d'image Docker sur Docker Hub. Vous pouvez la télécharger et l'exécuter localement avec les commandes suivantes :

#### 1. Télécharger l'image depuis Docker Hub

```bash
docker pull <votre-username>/oc-lettings:latest
```

Remplacez `<votre-username>` par le nom d'utilisateur Docker Hub du projet.

#### 2. Exécuter le conteneur

```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key-here" \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  --name oc-lettings \
  <votre-username>/oc-lettings:latest
```

**Explications des options :**
- `-d` : Exécute le conteneur en arrière-plan (mode détaché)
- `-p 8000:8000` : Mappe le port 8000 du conteneur vers le port 8000 de votre machine
- `-e` : Définit les variables d'environnement nécessaires
  - `SECRET_KEY` : Clé secrète Django (utilisez une valeur aléatoire et sécurisée)
  - `DEBUG` : Mode debug (False en production)
  - `ALLOWED_HOSTS` : Hôtes autorisés (ajoutez votre domaine en production)
- `--name` : Nom du conteneur pour faciliter la gestion

#### 3. Vérifier que le conteneur fonctionne

```bash
# Voir les conteneurs en cours d'exécution
docker ps

# Voir les logs du conteneur
docker logs oc-lettings
```

#### 4. Accéder à l'application

Ouvrez votre navigateur et allez sur `http://localhost:8000`

#### 5. Arrêter et supprimer le conteneur

```bash
# Arrêter le conteneur
docker stop oc-lettings

# Supprimer le conteneur
docker rm oc-lettings

# (Optionnel) Supprimer l'image
docker rmi <votre-username>/oc-lettings:latest
```

### Construire l'image Docker localement

Si vous souhaitez construire l'image vous-même au lieu de la télécharger depuis Docker Hub :

```bash
# Construire l'image
docker build -t oc-lettings:local .

# Exécuter le conteneur avec l'image locale
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY="your-secret-key-here" \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  --name oc-lettings \
  oc-lettings:local
```

---

## Pipeline CI/CD

Le projet utilise GitHub Actions pour l'intégration et le déploiement continus. Le pipeline se compose de 3 jobs :

1. **Tests & Linting** : Exécute flake8 et pytest avec une couverture minimale de 80%
2. **Build & Push Docker** : Construit l'image Docker et la pousse sur Docker Hub
3. **Deploy to Render** : Déploie l'application sur Render

Le pipeline se déclenche automatiquement à chaque push sur la branche `master`.

### Configuration requise

Les secrets suivants doivent être configurés dans les GitHub Secrets :

- `DOCKER_USERNAME` : Nom d'utilisateur Docker Hub
- `DOCKER_PASSWORD` : Token d'accès Docker Hub
- `RENDER_DEPLOY_HOOK_URL` : URL du webhook de déploiement Render

---

## Documentation complète

La documentation complète du projet est disponible sur Read The Docs (le lien sera fourni une fois la documentation publiée).

Elle comprend :
- Guide d'installation détaillé
- Architecture de l'application
- Documentation de l'API
- Guide de déploiement
- Structure de la base de données

---

## Monitoring avec Sentry

L'application utilise Sentry pour le monitoring des erreurs en production. Pour activer Sentry :

1. Créez un compte sur [sentry.io](https://sentry.io)
2. Créez un nouveau projet Django
3. Copiez le DSN (Data Source Name)
4. Ajoutez-le comme variable d'environnement :

```bash
# En local (.env)
SENTRY_DSN=your-sentry-dsn-here
SENTRY_ENVIRONMENT=development

# En production (variables d'environnement Render/Docker)
SENTRY_DSN=your-sentry-dsn-here
SENTRY_ENVIRONMENT=production
```
