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

Le fichier `docs/conf.py` est le fichier de configuration principal de Sphinx. Voici son contenu complet avec explications détaillées :

```python
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath('..'))

# Set Django settings module for autodoc (optional - for local builds)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
os.environ.setdefault('SECRET_KEY', 'docs-build-secret-key')

# Try to setup Django for autodoc (skip if not available)
try:
    import django
    django.setup()
except Exception:
    pass  # Skip Django setup for Read The Docs

# -- Project information -----------------------------------------------------
project = 'OC Lettings'
copyright = '2025, OpenClassrooms'
author = 'Sébastien Grison'
release = '1.4.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'navigation_depth': 3,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
```

### Explication détaillée ligne par ligne

#### 1. Imports et configuration du path Python

| Code | Description |
|------|-------------|
| `import os` | Module pour interagir avec le système d'exploitation |
| `import sys` | Module pour accéder aux paramètres de l'interpréteur Python |
| `sys.path.insert(0, os.path.abspath('..'))` | Ajoute le répertoire parent (racine du projet) au path Python. Nécessaire pour que `autodoc` puisse importer les modules Django |

#### 2. Configuration Django pour autodoc

| Code | Description |
|------|-------------|
| `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')` | Définit le module de settings Django à utiliser |
| `os.environ.setdefault('SECRET_KEY', 'docs-build-secret-key')` | Fournit une clé secrète pour éviter les erreurs lors du build |
| `django.setup()` | Initialise Django pour permettre l'import des modèles |
| `try/except` | Encapsule le setup Django pour éviter les erreurs sur Read The Docs |

#### 3. Informations du projet

| Variable | Valeur | Description |
|----------|--------|-------------|
| `project` | 'OC Lettings' | Nom du projet affiché dans la documentation |
| `copyright` | '2025, OpenClassrooms' | Notice de copyright |
| `author` | 'Sébastien Grison' | Auteur du projet |
| `release` | '1.4.0' | Version actuelle du projet |

#### 4. Extensions Sphinx

| Extension | Description |
|-----------|-------------|
| `sphinx.ext.autodoc` | Génère automatiquement la documentation depuis les docstrings Python |
| `sphinx.ext.viewcode` | Ajoute des liens vers le code source dans la documentation |
| `sphinx.ext.napoleon` | Permet d'utiliser les formats Google ou NumPy pour les docstrings |

#### 5. Configuration générale

| Variable | Valeur | Description |
|----------|--------|-------------|
| `templates_path` | `['_templates']` | Dossier contenant les templates Jinja2 personnalisés |
| `exclude_patterns` | `['_build', 'Thumbs.db', '.DS_Store']` | Fichiers/dossiers à ignorer lors du build |
| `language` | `'fr'` | Langue de la documentation (français) |

#### 6. Options de sortie HTML

| Variable | Valeur | Description |
|----------|--------|-------------|
| `html_theme` | `'sphinx_rtd_theme'` | Thème Read The Docs (responsive, moderne) |
| `html_static_path` | `['_static']` | Dossier pour les fichiers statiques (CSS, JS, images) |

#### 7. Options du thème

| Option | Valeur | Description |
|--------|--------|-------------|
| `navigation_depth` | `3` | Profondeur de la table des matières (3 niveaux) |
| `collapse_navigation` | `False` | Ne pas replier les sections dans le menu |
| `sticky_navigation` | `True` | Menu de navigation fixe lors du scroll |

#### 8. Options autodoc

| Option | Valeur | Description |
|--------|--------|-------------|
| `autodoc_member_order` | `'bysource'` | Ordre des membres : par ordre d'apparition dans le code source |
| `members` | `True` | Documenter tous les membres (fonctions, classes, etc.) |
| `undoc-members` | `True` | Inclure les membres sans docstring |
| `show-inheritance` | `True` | Afficher l'héritage des classes |

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

Ce fichier est le fichier de configuration pour **Read the Docs**. Il indique comment la plateforme doit construire et héberger votre documentation Sphinx.

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

### Explication des paramètres

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `version` | 2 | Version du format de configuration Read The Docs |
| `build.os` | ubuntu-22.04 | Système d'exploitation utilisé pour la build |
| `build.tools.python` | 3.12 | Version de Python utilisée pour générer la doc |
| `sphinx.configuration` | docs/conf.py | Chemin vers le fichier de configuration Sphinx |
| `python.install` | docs/requirements.txt | Fichier des dépendances Python à installer |

### Fonctionnement du fichier

1. Quand vous poussez du code sur GitHub, Read the Docs détecte les changements
2. Il lit ce fichier `.readthedocs.yaml` à la racine du projet
3. Il crée un environnement Ubuntu 22.04 avec Python 3.12
4. Il installe les dépendances listées dans `docs/requirements.txt`
5. Il exécute Sphinx avec la configuration `docs/conf.py` pour générer le HTML
6. La documentation est publiée automatiquement sur l'URL du projet

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

### Fichiers Makefile et make.bat

Ces deux fichiers servent à **simplifier les commandes de build Sphinx** en fournissant des raccourcis.

| Fichier | Système | Commande |
|---------|---------|----------|
| `Makefile` | Linux / macOS | `make html` |
| `make.bat` | Windows | `.\make.bat html` |

#### Contenu de make.bat (Windows)

```batch
@ECHO OFF
pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
popd
```

#### Contenu de Makefile (Linux/Mac)

```makefile
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

help:
    @$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

%: Makefile
    @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

#### Variables définies

| Variable | Valeur | Description |
|----------|--------|-------------|
| `SPHINXBUILD` | `sphinx-build` | Commande Sphinx à utiliser |
| `SOURCEDIR` | `.` | Dossier source (docs/) |
| `BUILDDIR` | `_build` | Dossier de sortie |

#### Fonctionnement

Ces fichiers transforment la commande longue :
```bash
sphinx-build -M html . _build
```

En commande courte :
```bash
make html          # Linux/Mac
.\make.bat html    # Windows
```

#### Commandes disponibles

| Commande | Format généré |
|----------|---------------|
| `make html` / `.\make.bat html` | Site web HTML |
| `make clean` / `.\make.bat clean` | Nettoie le dossier _build |
| `make help` / `.\make.bat help` | Affiche toutes les options |
| `make latex` | Document LaTeX |
| `make epub` | E-book EPUB |
| `make text` | Texte brut |

#### Documentation officielle

Ces fichiers sont **générés automatiquement** par Sphinx lors de l'initialisation d'un projet avec la commande `sphinx-quickstart`.

| Ressource | Lien |
|-----------|------|
| Commande sphinx-build | [sphinx-doc.org/en/master/man/sphinx-build.html](https://www.sphinx-doc.org/en/master/man/sphinx-build.html) |
| Commande sphinx-quickstart | [sphinx-doc.org/en/master/man/sphinx-quickstart.html](https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html) |
| Tutorial Sphinx complet | [sphinx-doc.org/en/master/tutorial/index.html](https://www.sphinx-doc.org/en/master/tutorial/index.html) |

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
# Avec sphinx-build
cd docs
poetry run sphinx-build -M clean . _build

# Ou avec make/make.bat
make clean          # Linux/Mac
.\make.bat clean    # Windows
```

---

## 7. Mise à jour automatique

### Fonctionnement

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  git push   │ ────► │   GitHub    │ ────► │ Read The    │
│  (master)   │       │  Webhook    │       │ Docs Build  │
└─────────────┘       └─────────────┘       └─────────────┘
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
