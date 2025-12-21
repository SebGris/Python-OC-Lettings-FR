Installation
============

Cette section décrit comment installer et configurer le projet en local.

Prérequis
---------

* **Python** : 3.13 ou supérieur
* **Poetry** : Gestionnaire de dépendances Python
* **Git** : Pour cloner le repository
* **Docker** (optionnel) : Pour le déploiement conteneurisé

Cloner le repository
--------------------

.. code-block:: bash

   git clone https://github.com/SebGris/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR

Installation avec Poetry
------------------------

1. **Installer les dépendances** :

.. code-block:: bash

   poetry install

2. **Activer l'environnement virtuel** :

.. code-block:: bash

   poetry shell

Configuration
-------------

1. **Créer un fichier** ``.env`` à la racine du projet :

.. code-block:: bash

   SECRET_KEY=votre-cle-secrete-de-developpement
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

2. **Appliquer les migrations** :

.. code-block:: bash

   poetry run python manage.py migrate

3. **Créer un superutilisateur** (optionnel) :

.. code-block:: bash

   poetry run python manage.py createsuperuser

Lancer l'application
--------------------

.. code-block:: bash

   poetry run python manage.py runserver

L'application sera accessible sur http://localhost:8000

Installation avec Docker
------------------------

Si vous préférez utiliser Docker :

.. code-block:: bash

   docker-compose up --build

L'application sera accessible sur http://localhost:8000

Vérification de l'installation
------------------------------

Pour vérifier que tout fonctionne :

1. Accédez à http://localhost:8000 - Page d'accueil
2. Accédez à http://localhost:8000/admin - Interface admin
3. Accédez à http://localhost:8000/lettings/ - Liste des locations
4. Accédez à http://localhost:8000/profiles/ - Liste des profils
