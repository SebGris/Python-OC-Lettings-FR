# Guide de generation de la documentation Sphinx

Ce guide explique comment creer et regenerer la documentation Sphinx du projet, etape par etape, sans assistance.

---

## Table des matieres

1. [Prerequis](#1-prerequis)
2. [Creer une documentation Sphinx depuis zero](#2-creer-une-documentation-sphinx-depuis-zero)
3. [Regenerer la documentation existante](#3-regenerer-la-documentation-existante)
4. [Ajouter une nouvelle page](#4-ajouter-une-nouvelle-page)
5. [Modifier la configuration](#5-modifier-la-configuration)
6. [Deployer sur Read The Docs](#6-deployer-sur-read-the-docs)
7. [Depannage](#7-depannage)

---

## 1. Prerequis

### Installer les dependances

```bash
# Installer Sphinx et le theme Read The Docs
poetry add sphinx sphinx-rtd-theme --group docs

# Ou avec pip
pip install sphinx sphinx-rtd-theme
```

### Verifier l'installation

```bash
poetry run sphinx-build --version
# Resultat attendu : sphinx-build X.X.X
```

---

## 2. Creer une documentation Sphinx depuis zero

Si vous partez d'un projet sans documentation, suivez ces etapes.

### Etape 1 : Creer le dossier docs

```bash
mkdir docs
cd docs
```

### Etape 2 : Lancer sphinx-quickstart

```bash
poetry run sphinx-quickstart
```

### Etape 3 : Repondre aux questions

Le script pose plusieurs questions. Voici les reponses recommandees :

| Question | Reponse recommandee |
|----------|---------------------|
| Separate source and build directories? | `n` (non) |
| Project name | `OC Lettings` (ou le nom de votre projet) |
| Author name(s) | Votre nom |
| Project release | `1.0.0` (ou votre version) |
| Project language | `fr` (pour francais) |

### Etape 4 : Fichiers generes

Apres `sphinx-quickstart`, vous aurez :

```
docs/
├── conf.py          # Configuration Sphinx
├── index.rst        # Page d'accueil
├── Makefile         # Script de build (Linux/Mac)
├── make.bat         # Script de build (Windows)
├── _static/         # Fichiers statiques (CSS, images)
└── _templates/      # Templates personnalises
```

### Etape 5 : Configurer conf.py pour Django

Ouvrez `docs/conf.py` et ajoutez au debut du fichier :

```python
import os
import sys

# Ajouter le projet au path Python
sys.path.insert(0, os.path.abspath('..'))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
os.environ.setdefault('SECRET_KEY', 'docs-build-secret-key')

try:
    import django
    django.setup()
except Exception:
    pass
```

### Etape 6 : Ajouter les extensions

Dans `conf.py`, modifiez la liste `extensions` :

```python
extensions = [
    'sphinx.ext.autodoc',    # Documentation auto depuis docstrings
    'sphinx.ext.viewcode',   # Liens vers le code source
    'sphinx.ext.napoleon',   # Support Google/NumPy docstrings
]
```

### Etape 7 : Configurer le theme

Dans `conf.py`, modifiez :

```python
html_theme = 'sphinx_rtd_theme'
```

### Etape 8 : Generer la documentation

```bash
# Windows
.\make.bat html

# Linux/Mac
make html
```

### Etape 9 : Visualiser le resultat

Ouvrez `docs/_build/html/index.html` dans un navigateur.

---

## 3. Regenerer la documentation existante

Si la documentation existe deja (comme dans ce projet), utilisez ces commandes.

### Generer le HTML

```bash
cd docs

# Windows
.\make.bat html

# Linux/Mac
make html

# Ou avec poetry (tous systemes)
poetry run sphinx-build -b html . _build/html
```

### Nettoyer avant de regenerer

Si vous avez des problemes ou voulez repartir de zero :

```bash
cd docs

# Windows
.\make.bat clean

# Linux/Mac
make clean

# Puis regenerer
.\make.bat html   # Windows
make html         # Linux/Mac
```

### Regenerer apres modification

Apres avoir modifie un fichier `.rst` ou `conf.py` :

```bash
cd docs
.\make.bat html   # Windows
make html         # Linux/Mac
```

Sphinx ne regenere que les fichiers modifies (build incrementiel).

---

## 4. Ajouter une nouvelle page

### Etape 1 : Creer le fichier .rst

Creez un nouveau fichier dans `docs/`, par exemple `nouvelle_page.rst` :

```rst
Titre de la nouvelle page
=========================

Introduction
------------

Ceci est le contenu de ma nouvelle page.

Sous-section
^^^^^^^^^^^^

Contenu de la sous-section.

Liste a puces
-------------

* Premier element
* Deuxieme element
* Troisieme element

Bloc de code
------------

.. code-block:: python

   def hello():
       print("Hello, World!")
```

### Etape 2 : Ajouter au sommaire

Ouvrez `docs/index.rst` et ajoutez votre page dans le `toctree` :

```rst
.. toctree::
   :maxdepth: 2
   :caption: Table des matieres

   introduction
   installation
   nouvelle_page       <-- Ajouter ici (sans .rst)
   quickstart
```

### Etape 3 : Regenerer

```bash
cd docs
.\make.bat html   # Windows
make html         # Linux/Mac
```

### Etape 4 : Verifier

Ouvrez `docs/_build/html/index.html` et verifiez que votre page apparait dans le menu.

---

## 5. Modifier la configuration

### Changer le nom du projet

Dans `docs/conf.py` :

```python
project = 'Nouveau Nom'
```

### Changer la version

Dans `docs/conf.py` :

```python
release = '2.0.0'
```

### Changer la langue

Dans `docs/conf.py` :

```python
language = 'en'  # Anglais
language = 'fr'  # Francais
```

### Ajouter une extension

Dans `docs/conf.py`, ajoutez a la liste `extensions` :

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',        # Nouvelle extension
]
```

### Modifier les options du theme

Dans `docs/conf.py` :

```python
html_theme_options = {
    'navigation_depth': 4,           # Profondeur du menu (defaut: 3)
    'collapse_navigation': True,     # Replier le menu
    'sticky_navigation': False,      # Menu non fixe
}
```

---

## 6. Deployer sur Read The Docs

### Etape 1 : Creer le fichier .readthedocs.yaml

A la racine du projet (pas dans docs/), creez `.readthedocs.yaml` :

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

### Etape 2 : Creer docs/requirements.txt

Dans le dossier `docs/`, creez `requirements.txt` :

```
sphinx>=7.0.0
sphinx-rtd-theme>=2.0.0
django>=4.2
python-dotenv>=1.0.0
```

### Etape 3 : Pousser sur GitHub

```bash
git add .readthedocs.yaml docs/requirements.txt
git commit -m "Ajout configuration Read The Docs"
git push origin master
```

### Etape 4 : Configurer Read The Docs

1. Aller sur https://readthedocs.org
2. Se connecter avec GitHub
3. Cliquer sur "Import a Project"
4. Selectionner votre repository
5. Cliquer sur "Build Version"

### Etape 5 : Verifier le build

1. Aller sur https://readthedocs.org/projects/votre-projet/
2. Cliquer sur "Builds"
3. Verifier que le build est "Passed"
4. Cliquer sur "View Docs" pour voir le resultat

---

## 7. Depannage

### Erreur : "sphinx-build not found"

**Cause** : Sphinx n'est pas installe ou pas dans le PATH.

**Solution** :
```bash
# Installer Sphinx
poetry add sphinx --group docs

# Utiliser avec poetry
poetry run sphinx-build --version
```

### Erreur : "Could not import Django"

**Cause** : Django n'est pas configure dans conf.py.

**Solution** : Ajoutez au debut de `docs/conf.py` :
```python
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
os.environ.setdefault('SECRET_KEY', 'docs-build-secret-key')
try:
    import django
    django.setup()
except Exception:
    pass
```

### Erreur : "toctree contains reference to nonexisting document"

**Cause** : Un fichier liste dans `toctree` n'existe pas.

**Solution** :
1. Verifiez que le fichier .rst existe dans `docs/`
2. Verifiez l'orthographe dans le `toctree`
3. N'incluez pas l'extension `.rst` dans le `toctree`

### La page n'apparait pas dans le menu

**Cause** : La page n'est pas dans le `toctree`.

**Solution** : Ajoutez le nom du fichier (sans .rst) dans `docs/index.rst` :
```rst
.. toctree::
   :maxdepth: 2

   votre_nouvelle_page
```

### Les modifications ne s'affichent pas

**Cause** : Cache de build.

**Solution** : Nettoyez et regenerez :
```bash
cd docs
.\make.bat clean   # Windows
make clean         # Linux/Mac

.\make.bat html    # Windows
make html          # Linux/Mac
```

### Read The Docs build echoue

**Causes possibles** :
1. `docs/requirements.txt` manquant ou incomplet
2. `.readthedocs.yaml` mal configure
3. Erreur dans `conf.py`

**Solution** :
1. Verifiez les logs sur Read The Docs (onglet "Builds")
2. Assurez-vous que toutes les dependances sont dans `docs/requirements.txt`
3. Testez le build en local avant de pousser

---

## Resume des commandes

| Action | Commande Windows | Commande Linux/Mac |
|--------|------------------|-------------------|
| Initialiser Sphinx | `poetry run sphinx-quickstart` | `poetry run sphinx-quickstart` |
| Generer HTML | `.\make.bat html` | `make html` |
| Nettoyer | `.\make.bat clean` | `make clean` |
| Voir l'aide | `.\make.bat help` | `make help` |
| Generer PDF | `.\make.bat latexpdf` | `make latexpdf` |

---

## Syntaxe reStructuredText rapide

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

1. Premier
2. Deuxieme
```

### Liens

```rst
`Texte du lien <https://example.com>`_
```

### Code inline

```rst
Utilisez ``print("Hello")`` pour afficher du texte.
```

### Bloc de code

```rst
.. code-block:: python

   def hello():
       print("Hello")
```

### Tableaux simples

```rst
.. list-table::
   :header-rows: 1

   * - Colonne 1
     - Colonne 2
   * - Valeur 1
     - Valeur 2
```

### Note et avertissement

```rst
.. note::
   Ceci est une note.

.. warning::
   Ceci est un avertissement.
```

---

## Ressources utiles

| Ressource | URL |
|-----------|-----|
| Documentation Sphinx | https://www.sphinx-doc.org/en/master/ |
| Syntaxe reStructuredText | https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html |
| Theme Read The Docs | https://sphinx-rtd-theme.readthedocs.io/ |
| Read The Docs | https://docs.readthedocs.io/ |
