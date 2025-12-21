Interfaces de programmation
===========================

Cette section décrit les points d'accès et les interfaces du projet.

URLs et endpoints
-----------------

Pages publiques
^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - URL
     - Nom
     - Description
   * - ``/``
     - ``index``
     - Page d'accueil
   * - ``/lettings/``
     - ``lettings:index``
     - Liste des locations
   * - ``/lettings/<id>/``
     - ``lettings:letting``
     - Détail d'une location
   * - ``/profiles/``
     - ``profiles:index``
     - Liste des profils
   * - ``/profiles/<username>/``
     - ``profiles:profile``
     - Détail d'un profil

Administration
^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - URL
     - Description
   * - ``/admin/``
     - Interface d'administration Django
   * - ``/admin/lettings/``
     - Gestion des locations
   * - ``/admin/profiles/``
     - Gestion des profils

Vues
----

oc_lettings_site.views
^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: index(request)

   Affiche la page d'accueil de l'application.

   :param request: Objet HttpRequest Django
   :return: Rendu du template ``index.html``

lettings.views
^^^^^^^^^^^^^^

.. py:function:: lettings_index(request)
   :noindex:

   Affiche la liste de toutes les locations.

   :param request: Objet HttpRequest Django
   :return: Rendu du template ``lettings/index.html`` avec la liste des locations

.. py:function:: letting(request, letting_id)

   Affiche les détails d'une location spécifique.

   :param request: Objet HttpRequest Django
   :param letting_id: ID de la location
   :return: Rendu du template ``lettings/letting.html``
   :raises Http404: Si la location n'existe pas

profiles.views
^^^^^^^^^^^^^^

.. py:function:: profiles_index(request)
   :noindex:

   Affiche la liste de tous les profils.

   :param request: Objet HttpRequest Django
   :return: Rendu du template ``profiles/index.html`` avec la liste des profils

.. py:function:: profile(request, username)

   Affiche les détails d'un profil spécifique.

   :param request: Objet HttpRequest Django
   :param username: Nom d'utilisateur
   :return: Rendu du template ``profiles/profile.html``
   :raises Http404: Si le profil n'existe pas

Modèles
-------

lettings.models
^^^^^^^^^^^^^^^

.. py:class:: Address

   Représente une adresse postale.

   .. py:attribute:: number
      :type: PositiveIntegerField

      Numéro de rue

   .. py:attribute:: street
      :type: CharField

      Nom de la rue

   .. py:attribute:: city
      :type: CharField

      Ville

   .. py:attribute:: state
      :type: CharField

      Code état (2 caractères)

   .. py:attribute:: zip_code
      :type: PositiveIntegerField

      Code postal

   .. py:attribute:: country_iso_code
      :type: CharField

      Code ISO du pays (3 caractères)

.. py:class:: Letting

   Représente une location immobilière.

   .. py:attribute:: title
      :type: CharField

      Titre de la location

   .. py:attribute:: address
      :type: OneToOneField

      Adresse de la location (relation 1:1 avec Address)

profiles.models
^^^^^^^^^^^^^^^

.. py:class:: Profile

   Représente un profil utilisateur.

   .. py:attribute:: user
      :type: OneToOneField

      Utilisateur Django associé

   .. py:attribute:: favorite_city
      :type: CharField

      Ville favorite (optionnel)
