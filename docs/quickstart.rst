Guide de démarrage rapide
=========================

Ce guide vous permet de démarrer rapidement avec le projet.

Démarrage en 5 minutes
----------------------

1. **Cloner et installer** :

.. code-block:: bash

   git clone https://github.com/SebGris/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR
   poetry install

2. **Configurer l'environnement** :

.. code-block:: bash

   echo "SECRET_KEY=dev-secret-key" > .env
   echo "DEBUG=True" >> .env

3. **Lancer l'application** :

.. code-block:: bash

   poetry run python manage.py runserver

4. **Accéder à l'application** : http://localhost:8000

Lancer les tests
----------------

.. code-block:: bash

   poetry run python -m pytest

Les tests incluent :

* Tests des modèles (Address, Letting, Profile)
* Tests des vues (index, lettings, profiles)
* Tests des URLs
* Couverture de code minimale : 80%

Linter (Flake8)
---------------

.. code-block:: bash

   poetry run python -m flake8

Génération de la documentation
------------------------------

.. code-block:: bash

   cd docs
   poetry run make html

La documentation sera générée dans ``docs/_build/html/``.

Commandes utiles
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Commande
     - Description
   * - ``poetry run python manage.py runserver``
     - Lancer le serveur de développement
   * - ``poetry run python -m pytest``
     - Exécuter les tests
   * - ``poetry run python -m flake8``
     - Vérifier le style de code
   * - ``poetry run python manage.py migrate``
     - Appliquer les migrations
   * - ``poetry run python manage.py createsuperuser``
     - Créer un administrateur
   * - ``docker-compose up --build``
     - Lancer avec Docker
