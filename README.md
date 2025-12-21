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
