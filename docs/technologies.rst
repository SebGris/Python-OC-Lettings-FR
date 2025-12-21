Technologies et outils
======================

Langages et frameworks
----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Technologie
     - Version
     - Usage
   * - Python
     - 3.13
     - Langage principal
   * - Django
     - 4.2 LTS
     - Framework web
   * - HTML/CSS
     - 5 / 3
     - Templates et styles

Dépendances Python
------------------

Production
^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Package
     - Version
     - Description
   * - django
     - ^4.2.16
     - Framework web
   * - gunicorn
     - ^23.0.0
     - Serveur WSGI production
   * - whitenoise
     - ^6.11.0
     - Fichiers statiques
   * - psycopg2-binary
     - ^2.9.11
     - Driver PostgreSQL
   * - sentry-sdk
     - ^2.47.0
     - Monitoring erreurs
   * - python-dotenv
     - ^1.2.1
     - Variables d'environnement

Développement
^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Package
     - Version
     - Description
   * - pytest
     - ^8.0.0
     - Framework de tests
   * - pytest-django
     - ^4.11.1
     - Plugin Django pour pytest
   * - pytest-cov
     - ^6.0.0
     - Couverture de code
   * - flake8
     - ^7.3.0
     - Linter Python
   * - sphinx
     - ^9.0.4
     - Générateur de documentation
   * - sphinx-rtd-theme
     - ^3.0.2
     - Thème Read The Docs

Infrastructure
--------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Service
     - Description
   * - **GitHub**
     - Hébergement du code source et CI/CD (GitHub Actions)
   * - **Docker Hub**
     - Registry pour les images Docker
   * - **Render**
     - Hébergement de l'application (PaaS)
   * - **Supabase**
     - Base de données PostgreSQL
   * - **Sentry**
     - Monitoring et suivi des erreurs
   * - **Read The Docs**
     - Hébergement de la documentation

Outils de développement
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Outil
     - Description
   * - **Poetry**
     - Gestionnaire de dépendances Python
   * - **Docker**
     - Conteneurisation de l'application
   * - **Docker Compose**
     - Orchestration des conteneurs
   * - **Git**
     - Versioning du code
   * - **VS Code**
     - IDE recommandé

Versions requises
-----------------

.. code-block:: text

   Python >= 3.13
   Poetry >= 1.8.4
   Docker >= 20.10
   Docker Compose >= 2.0
