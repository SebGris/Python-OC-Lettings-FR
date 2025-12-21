# Documentation Sphinx et Read The Docs - OC Lettings

## Table des matières
1. [Qu'est-ce que Sphinx ?](#1-quest-ce-que-sphinx-)
2. [Qu'est-ce que Read The Docs ?](#2-quest-ce-que-read-the-docs-)
3. [Structure de la documentation](#3-structure-de-la-documentation)
4. [Configuration Sphinx](#4-configuration-sphinx)
5. [Configuration Read The Docs](#5-configuration-read-the-docs)
6. [Génération locale](#6-génération-locale)
7. [Mise à jour automatique](#7-mise-à-jour-automatique)

---

## 1. Qu'est-ce que Sphinx ?

**Sphinx** est un générateur de documentation Python. Il convertit des fichiers texte (reStructuredText) en documentation HTML, PDF, ou autres formats.

### Pourquoi Sphinx ?

| Avantage | Description |
|----------|-------------|
| **Standard Python** | Utilisé par Django, Python, NumPy, etc. |
| **reStructuredText** | Format de balisage simple et puissant |
| **Thèmes** | Nombreux thèmes disponibles (Read The Docs, etc.) |
| **Extensions** | Support autodoc, viewcode, intersphinx, etc. |

### reStructuredText vs Markdown

| reStructuredText | Markdown |
|------------------|----------|
| Plus puissant (directives, rôles) | Plus simple |
| Standard pour Python | Standard pour GitHub |
| Extension `.rst` | Extension `.md` |

---

## 2. Qu'est-ce que Read The Docs ?

**Read The Docs** (RTD) est une plateforme gratuite d'hébergement de documentation. Elle :

- Construit automatiquement la documentation à chaque push
- Héberge la documentation en ligne
- Gère les versions (branches, tags)
- Fournit une URL publique

### URL du projet

- **Documentation** : https://python-oc-lettings-fr-sg.readthedocs.io
- **Dashboard RTD** : https://readthedocs.org/projects/python-oc-lettings-fr-sg/

---

## 3. Structure de la documentation

```
docs/
├── conf.py              # Configuration Sphinx
├── index.rst            # Page d'accueil (table des matières)
├── introduction.rst     # Description du projet
├── installation.rst     # Guide d'installation
├── quickstart.rst       # Démarrage rapide
├── database.rst         # Modèles de données
├── deployment.rst       # Déploiement CI/CD
├── api.rst              # URLs, vues, modèles
├── technologies.rst     # Stack technique
├── requirements.txt     # Dépendances pour RTD
├── Makefile             # Commandes de build (Linux/Mac)
├── make.bat             # Commandes de build (Windows)
└── _static/             # Fichiers statiques (CSS, images)
```

### Contenu des fichiers .rst

| Fichier | Contenu |
|---------|---------|
| `index.rst` | Page d'accueil avec `toctree` (table des matières) |
| `introduction.rst` | Objectifs, fonctionnalités, structure des apps |
| `installation.rst` | Prérequis, installation Poetry, configuration |
| `quickstart.rst` | Démarrage en 5 min, commandes utiles |
| `database.rst` | Configuration SQLite/PostgreSQL, modèles, diagramme |
| `deployment.rst` | Pipeline CI/CD, Docker, Render, Sentry |
| `api.rst` | Endpoints, vues, modèles documentés |
| `technologies.rst` | Dépendances, versions, infrastructure |

---

## 4. Configuration Sphinx

### Fichier conf.py

```python
# Configuration de base
project = 'OC Lettings'
copyright = '2025, OpenClassrooms'
author = 'Sebastien'
release = '1.4.0'

# Extensions Sphinx
extensions = [
    'sphinx.ext.autodoc',    # Documentation auto depuis docstrings
    'sphinx.ext.viewcode',   # Liens vers le code source
    'sphinx.ext.napoleon',   # Support Google/NumPy docstrings
]

# Langue française
language = 'fr'

# Thème Read The Docs
html_theme = 'sphinx_rtd_theme'
```

### Dépendances (pyproject.toml)

```toml
[tool.poetry.group.docs.dependencies]
sphinx = "^9.0.4"
sphinx-rtd-theme = "^3.0.2"
```

Les dépendances docs sont dans un groupe séparé pour ne pas les installer en production.

---

## 5. Configuration Read The Docs

### Fichier .readthedocs.yaml

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.12"

sphinx:
  configuration: docs/conf.py

python:
  install:
    - requirements: docs/requirements.txt
```

### Fichier docs/requirements.txt

```
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
django>=4.2
python-dotenv>=1.0.0
```

Ce fichier liste les dépendances nécessaires pour construire la documentation sur Read The Docs.

---

## 6. Génération locale

### Construire la documentation

```bash
cd docs
poetry run sphinx-build -b html . _build/html
```

Ou avec Make (Linux/Mac) :

```bash
cd docs
poetry run make html
```

Ou avec make.bat (Windows) :

```bash
cd docs
.\make.bat html
```

### Visualiser la documentation

Ouvrir `docs/_build/html/index.html` dans un navigateur.

### Nettoyer le build

```bash
cd docs
poetry run sphinx-build -M clean . _build
```

---

## 7. Mise à jour automatique

### Fonctionnement

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  git push   │────▶│   GitHub    │────▶│ Read The    │
│  (master)   │     │  Webhook    │     │ Docs Build  │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
                                        Documentation
                                        mise à jour
```

### Étapes automatiques

1. Vous faites un `git push` sur `master`
2. GitHub envoie un webhook à Read The Docs
3. RTD clone le repository
4. RTD installe les dépendances (`docs/requirements.txt`)
5. RTD exécute Sphinx pour générer le HTML
6. La documentation est mise à jour en ligne

### Vérifier le build

1. Aller sur https://readthedocs.org/projects/python-oc-lettings-fr-sg/
2. Cliquer sur **Builds**
3. Vérifier que le dernier build est "Passed"

---

## Syntaxe reStructuredText

### Titres

```rst
Titre principal
===============

Sous-titre
----------

Sous-sous-titre
^^^^^^^^^^^^^^^
```

### Listes

```rst
* Item 1
* Item 2
* Item 3

1. Premier
2. Deuxième
3. Troisième
```

### Code

```rst
Code inline : ``poetry run python manage.py runserver``

Bloc de code :

.. code-block:: python

   def hello():
       print("Hello, World!")
```

### Tableaux

```rst
.. list-table::
   :header-rows: 1

   * - Colonne 1
     - Colonne 2
   * - Valeur 1
     - Valeur 2
```

### Liens

```rst
`Texte du lien <https://example.com>`_
```

### Table des matières

```rst
.. toctree::
   :maxdepth: 2
   :caption: Table des matières

   introduction
   installation
   quickstart
```

---

## Résumé

| Élément | Fichier/Emplacement |
|---------|---------------------|
| Configuration Sphinx | `docs/conf.py` |
| Page d'accueil | `docs/index.rst` |
| Configuration RTD | `.readthedocs.yaml` |
| Dépendances RTD | `docs/requirements.txt` |
| Build local | `docs/_build/html/` |
| URL en ligne | https://python-oc-lettings-fr-sg.readthedocs.io |
