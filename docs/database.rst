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

.. mermaid::

   erDiagram
       User ||--|| Profile : "has one"
       Letting ||--|| Address : "has one"

       User {
           int id PK
           varchar username
           varchar password
           varchar email
           varchar first_name
           varchar last_name
           boolean is_active
           boolean is_staff
           datetime date_joined
       }

       Profile {
           int id PK
           int user_id FK
           varchar favorite_city
       }

       Letting {
           int id PK
           varchar title
           int address_id FK
       }

       Address {
           int id PK
           int number
           varchar street
           varchar city
           char state
           int zip_code
           char country_iso_code
       }

**Légende des relations :**

- **User → Profile** : Relation 1:1 (un utilisateur a un seul profil)
- **Letting → Address** : Relation 1:1 (une location a une seule adresse)

**Contraintes :**

- ``Profile.user_id`` : UNIQUE, ON DELETE CASCADE
- ``Letting.address_id`` : UNIQUE, ON DELETE CASCADE
- ``Address.number`` : max 9999
- ``Address.zip_code`` : max 99999

Migrations
----------

Appliquer les migrations :

.. code-block:: bash

   poetry run python manage.py migrate

Créer une nouvelle migration après modification d'un modèle :

.. code-block:: bash

   poetry run python manage.py makemigrations
