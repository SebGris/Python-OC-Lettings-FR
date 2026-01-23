OC Lettings - Documentation
============================

Bienvenue dans la documentation du projet **OC Lettings**, une application Django de gestion de locations immobilières.

.. toctree::
   :maxdepth: 2
   :caption: Table des matières

   introduction
   installation
   quickstart
   database
   deployment
   api
   technologies

Introduction rapide
-------------------

OC Lettings est une application web permettant de :

* Consulter la liste des locations disponibles
* Voir les détails de chaque location (adresse, prix)
* Consulter les profils utilisateurs
* Gérer les données via l'interface d'administration Django

Architecture
------------

.. code-block:: text

   oc-lettings-site/
   ├── lettings/          # Application des locations
   ├── profiles/          # Application des profils
   ├── oc_lettings_site/  # Configuration Django
   ├── templates/         # Templates HTML
   ├── static/            # Fichiers statiques
   └── docs/              # Documentation Sphinx

Liens utiles
------------

* **Application en ligne** : https://oc-lettings-latest-vu8j.onrender.com/
* **Code source** : https://github.com/SebGris/Python-OC-Lettings-FR
* **Docker Hub** : https://hub.docker.com/r/sebgris/oc-lettings

Index
-----

* :ref:`genindex`
* :ref:`modindex`
