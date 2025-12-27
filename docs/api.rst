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

.. automodule:: oc_lettings_site.views
   :members:
   :undoc-members:
   :show-inheritance:

lettings.views
^^^^^^^^^^^^^^

.. automodule:: lettings.views
   :members:
   :undoc-members:
   :show-inheritance:

profiles.views
^^^^^^^^^^^^^^

.. automodule:: profiles.views
   :members:
   :undoc-members:
   :show-inheritance:

Modèles
-------

lettings.models
^^^^^^^^^^^^^^^

.. automodule:: lettings.models
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:

profiles.models
^^^^^^^^^^^^^^^

.. automodule:: profiles.models
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:
