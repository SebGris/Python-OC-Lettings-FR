Déploiement
===========

Pipeline CI/CD
--------------

Le projet utilise **GitHub Actions** pour l'intégration et le déploiement continus.

.. code-block:: text

   ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
   │  Push   │────▶│  Tests  │────▶│  Build  │────▶│ Deploy  │
   │ (Git)   │     │ (pytest)│     │ (Docker)│     │ (Render)│
   └─────────┘     └─────────┘     └─────────┘     └─────────┘

Étapes du pipeline
^^^^^^^^^^^^^^^^^^

1. **Tests & Linting** : Exécute pytest et flake8
2. **Build Docker** : Construit l'image et la pousse sur Docker Hub
3. **Déploiement** : Déclenche le déploiement sur Render via webhook

Conditions de déploiement
^^^^^^^^^^^^^^^^^^^^^^^^^

* Les tests doivent passer (couverture > 80%)
* Le linting doit réussir
* Uniquement sur la branche ``master``

Docker
------

Construction de l'image
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   docker build -t oc-lettings .

L'image utilise un **multi-stage build** :

* **Stage 1 (Builder)** : Installe Poetry et les dépendances
* **Stage 2 (Production)** : Image légère avec le code et les packages

Lancer avec Docker Compose
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   docker-compose up -d

Variables d'environnement requises dans ``.env`` :

* ``SECRET_KEY`` : Clé secrète Django
* ``DEBUG`` : False en production
* ``ALLOWED_HOSTS`` : Domaines autorisés

Render
------

Configuration
^^^^^^^^^^^^^

L'application est déployée sur **Render** comme Web Service Docker.

1. **Image Docker** : ``docker.io/sebgris/oc-lettings:latest``
2. **Region** : Frankfurt (EU Central)
3. **Instance Type** : Free

Variables d'environnement Render
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Description
   * - ``SECRET_KEY``
     - Clé secrète Django (générer une clé unique)
   * - ``DEBUG``
     - ``False`` (toujours en production)
   * - ``ALLOWED_HOSTS``
     - URL Render de l'application
   * - ``DATABASE_URL``
     - URL de connexion PostgreSQL
   * - ``SENTRY_DSN``
     - URL Sentry pour le monitoring
   * - ``SENTRY_ENVIRONMENT``
     - ``production``

PostgreSQL avec Supabase
^^^^^^^^^^^^^^^^^^^^^^^^

Le projet utilise **Supabase** comme base de données PostgreSQL gratuite.

Avantages :

* Gratuit sans limite de temps
* Interface SQL intégrée
* Compatible avec Django via ``DATABASE_URL``

Monitoring avec Sentry
----------------------

Le projet intègre **Sentry** pour le suivi des erreurs.

Configuration dans ``settings.py`` :

.. code-block:: python

   SENTRY_DSN = os.environ.get("SENTRY_DSN", "")

   if SENTRY_DSN:
       sentry_sdk.init(
           dsn=SENTRY_DSN,
           traces_sample_rate=1.0,
           profiles_sample_rate=1.0,
           environment=os.environ.get("SENTRY_ENVIRONMENT", "development"),
       )

URL de l'application
--------------------

* **Production** : https://python-oc-lettings-fr-vu8j.onrender.com
* **Admin** : https://python-oc-lettings-fr-vu8j.onrender.com/admin/
