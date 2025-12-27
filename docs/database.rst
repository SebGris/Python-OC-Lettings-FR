Base de données
===============

Structure et configuration
--------------------------

Le projet supporte deux bases de données selon l'environnement :

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Environnement
     - Base de données
     - Configuration
   * - Développement
     - SQLite
     - Automatique (fichier local)
   * - Production
     - PostgreSQL
     - Via ``DATABASE_URL``

Configuration automatique
-------------------------

Le fichier ``settings.py`` détecte automatiquement la base de données :

.. code-block:: python

   DATABASE_URL = os.environ.get("DATABASE_URL")

   if DATABASE_URL:
       # Production: PostgreSQL
       import urllib.parse
       url = urllib.parse.urlparse(DATABASE_URL)
       DATABASES = {
           "default": {
               "ENGINE": "django.db.backends.postgresql",
               "NAME": url.path[1:],
               "USER": url.username,
               "PASSWORD": url.password,
               "HOST": url.hostname,
               "PORT": url.port or "5432",
           }
       }
   else:
       # Développement: SQLite
       DATABASES = {
           "default": {
               "ENGINE": "django.db.backends.sqlite3",
               "NAME": os.path.join(BASE_DIR, "oc-lettings-site.sqlite3"),
           }
       }

Modèles de données
------------------

Address (Adresse)
^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``number``
     - PositiveIntegerField
     - Numéro de rue (max: 9999)
   * - ``street``
     - CharField(64)
     - Nom de la rue
   * - ``city``
     - CharField(64)
     - Ville
   * - ``state``
     - CharField(2)
     - Code état (ex: CA, NY)
   * - ``zip_code``
     - PositiveIntegerField
     - Code postal (max: 99999)
   * - ``country_iso_code``
     - CharField(3)
     - Code ISO du pays (ex: USA)

Letting (Location)
^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``title``
     - CharField(256)
     - Titre de la location
   * - ``address``
     - OneToOneField
     - Référence vers Address

Profile (Profil)
^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Champ
     - Type
     - Description
   * - ``user``
     - OneToOneField
     - Référence vers User Django
   * - ``favorite_city``
     - CharField(64)
     - Ville favorite (optionnel)

Diagramme des relations
-----------------------

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │                           OC LETTINGS - MODELE DE DONNEES                   │
   └─────────────────────────────────────────────────────────────────────────────┘

   ┌──────────────────────────────────┐      ┌─────────────────────────────────┐
   │           APPLICATION            │      │           APPLICATION           │
   │            PROFILES              │      │            LETTINGS             │
   └──────────────────────────────────┘      └─────────────────────────────────┘

   ┌──────────────────────────────────┐      ┌─────────────────────────────────┐
   │           auth.User              │      │            Letting              │
   │         (Django Auth)            │      │                                 │
   ├──────────────────────────────────┤      ├─────────────────────────────────┤
   │  PK │ id          │ INTEGER      │      │  PK │ id          │ INTEGER     │
   ├──────────────────────────────────┤      ├─────────────────────────────────┤
   │     │ username    │ VARCHAR(150) │      │     │ title       │ VARCHAR(256)│
   │     │ password    │ VARCHAR(128) │      │  FK │ address_id  │ INTEGER     │
   │     │ email       │ VARCHAR(254) │      └───────────────┬─────────────────┘
   │     │ first_name  │ VARCHAR(150) │                      │
   │     │ last_name   │ VARCHAR(150) │                      │ 1:1
   │     │ is_active   │ BOOLEAN      │                      │
   │     │ is_staff    │ BOOLEAN      │                      ▼
   │     │ date_joined │ DATETIME     │      ┌─────────────────────────────────┐
   └────────────────┬─────────────────┘      │            Address              │
                    │                        ├─────────────────────────────────┤
                    │ 1:1                    │  PK │ id               │ INTEGER│
                    │                        ├─────────────────────────────────┤
                    ▼                        │     │ number           │ INTEGER│
   ┌──────────────────────────────────┐      │     │ street           │ VARCHAR│
   │            Profile               │      │     │ city             │ VARCHAR│
   ├──────────────────────────────────┤      │     │ state            │ CHAR(2)│
   │  PK │ id            │ INTEGER    │      │     │ zip_code         │ INTEGER│
   ├──────────────────────────────────┤      │     │ country_iso_code │ CHAR(3)│
   │  FK │ user_id       │ INTEGER    │      └─────────────────────────────────┘
   │     │ favorite_city │ VARCHAR(64)│
   └──────────────────────────────────┘

   ┌─────────────────────────────────────────────────────────────────────────────┐
   │                              LEGENDE                                        │
   ├─────────────────────────────────────────────────────────────────────────────┤
   │  PK = Cle primaire (Primary Key)                                            │
   │  FK = Cle etrangere (Foreign Key)                                           │
   │                                                                             │
   │  Relations:                                                                 │
   │  ─────────────────────────────────────────────────────────────────────────  │
   │  auth.User ───── 1:1 ────► Profile     Un utilisateur a un seul profil      │
   │  Letting   ───── 1:1 ────► Address     Une location a une seule adresse     │
   │                                                                             │
   │  Contraintes:                                                               │
   │  ─────────────────────────────────────────────────────────────────────────  │
   │  - Profile.user_id : UNIQUE, ON DELETE CASCADE                              │
   │  - Letting.address_id : UNIQUE, ON DELETE CASCADE                           │
   │  - Address.number : max 9999                                                │
   │  - Address.zip_code : max 99999                                             │
   └─────────────────────────────────────────────────────────────────────────────┘

Migrations
----------

Appliquer les migrations :

.. code-block:: bash

   poetry run python manage.py migrate

Créer une nouvelle migration après modification d'un modèle :

.. code-block:: bash

   poetry run python manage.py makemigrations
