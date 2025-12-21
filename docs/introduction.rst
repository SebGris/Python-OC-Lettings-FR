Introduction
============

Description du projet
---------------------

**OC Lettings** est une application web Django développée dans le cadre d'un projet OpenClassrooms. Elle permet la gestion de locations immobilières et de profils utilisateurs.

Objectifs du projet
-------------------

Le projet vise à :

1. Moderniser une application Django existante
2. Implémenter un pipeline CI/CD complet
3. Déployer l'application en production avec Docker
4. Mettre en place un monitoring avec Sentry

Fonctionnalités principales
---------------------------

Locations (Lettings)
^^^^^^^^^^^^^^^^^^^^

* Liste des locations disponibles
* Détails de chaque location avec adresse complète
* Interface d'administration pour la gestion

Profils (Profiles)
^^^^^^^^^^^^^^^^^^

* Liste des profils utilisateurs
* Détails de chaque profil avec ville favorite
* Lien avec les utilisateurs Django

Administration
^^^^^^^^^^^^^^

* Interface Django Admin complète
* Gestion CRUD des locations et profils
* Authentification sécurisée

Structure des applications
--------------------------

Le projet est divisé en trois applications Django :

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Application
     - Description
   * - ``oc_lettings_site``
     - Application principale, configuration et page d'accueil
   * - ``lettings``
     - Gestion des locations et adresses
   * - ``profiles``
     - Gestion des profils utilisateurs
