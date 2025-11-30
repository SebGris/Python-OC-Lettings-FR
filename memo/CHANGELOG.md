# Changelog

---

## Résumé des versions

| Date | Version | Description |
|------|---------|-------------|
| 2025-11-30 | 1.3.0 | Corrections tests et migrations après refactorisation |
| 2025-11-30 | 1.2.0 | Suite de tests complète (96% couverture) |
| 2025-11-24 | 1.1.1 | Suppression setting USE_L10N dépréciée |
| 2025-11-24 | 1.1.0 | Mise à jour Django 4.2.16 pour Python 3.13 |

---

## [1.3.0] - 2025-11-30 - Corrections tests et migrations

### Résumé
Corrections nécessaires après la refactorisation pour que pytest et flake8 fonctionnent correctement avec les nouvelles applications `lettings` et `profiles`.

### Fixed

#### Migrations de données robustes
- **Problème** : `LookupError: No installed app with label 'oc_lettings_site'` lors de pytest
- **Cause** : Les migrations référençaient des modèles supprimés
- **Solution** : Encapsulation dans `try/except LookupError` pour ignorer si les anciens modèles n'existent plus
- **Fichiers** : `lettings/migrations/0002_migrate_data.py`, `profiles/migrations/0002_migrate_data.py`

#### Imports des tests mis à jour
- **Problème** : `ImportError: cannot import name 'Address' from 'oc_lettings_site.models'`
- **Solution** : Mise à jour des imports vers les nouvelles applications
  ```python
  from lettings.models import Address, Letting
  from profiles.models import Profile
  ```

#### URLs avec namespaces dans les tests
- **Avant** : `reverse("lettings_index")`, `reverse("profiles_index")`
- **Après** : `reverse("lettings:index")`, `reverse("profiles:index")`

#### Templates dans les tests
- **Avant** : `"lettings_index.html"`
- **Après** : `"lettings/index.html"`

#### Corrections flake8
- Suppression imports inutilisés dans `lettings/tests.py`, `profiles/tests.py`, `oc_lettings_site/admin.py`
- Correction espacement dans `settings.py` (E231)

### Changed

#### Templates mis à jour
- `templates/base.html` : URLs avec namespaces (`profiles:index`, `lettings:index`)
- `templates/index.html` : URLs avec namespaces

### Vérifications

```bash
pytest    # 26 tests passent, couverture 100%
flake8    # Aucune erreur
```

### Files Modified
- `lettings/migrations/0002_migrate_data.py`
- `profiles/migrations/0002_migrate_data.py`
- `oc_lettings_site/tests.py`
- `oc_lettings_site/admin.py`
- `oc_lettings_site/settings.py`
- `lettings/tests.py`
- `profiles/tests.py`
- `templates/base.html`

---

## [1.2.0] - 2025-11-30 - Suite de tests complète

### Résumé
Ajout d'une suite de tests complète avec 26 tests couvrant les modèles, vues et URLs. Configuration de pytest-cov pour le rapport de couverture avec un seuil minimum de 80%.

### Added

#### Tests (oc_lettings_site/tests.py)
- **Tests des modèles** (7 tests)
  - `TestAddressModel`: Validation de `__str__` et création d'adresse
  - `TestLettingModel`: Validation de `__str__` et relation avec Address
  - `TestProfileModel`: Validation de `__str__`, création et champ optionnel `favorite_city`

- **Tests des vues** (14 tests)
  - `TestIndexView`: Status code 200 et template `index.html`
  - `TestLettingsIndexView`: Status code, template et contenu de la liste
  - `TestLettingDetailView`: Status code, template et données du contexte
  - `TestProfilesIndexView`: Status code, template et contenu de la liste
  - `TestProfileDetailView`: Status code, template et données du profil

- **Tests des URLs** (5 tests)
  - Validation du routage : `/`, `/lettings/`, `/lettings/<id>/`, `/profiles/`, `/profiles/<username>/`

#### Configuration (setup.cfg)
- **Section `[tool:pytest]`**: Ajout des options de couverture
  - `--cov=oc_lettings_site`: Module à mesurer
  - `--cov-report=term-missing`: Affiche les lignes non couvertes
  - `--cov-fail-under=80`: Échec si couverture < 80%

- **Section `[coverage:run]`**: Exclusion des fichiers non pertinents
  - `*/migrations/*`: Fichiers de migration Django
  - `*/tests.py`: Le fichier de tests lui-même
  - `*/__init__.py`: Fichiers d'initialisation
  - `*/asgi.py`, `*/wsgi.py`: Points d'entrée serveur

#### Dépendances (requirements.txt)
- **pytest-cov**: Ajout de `pytest-cov==4.1.0`
  - Plugin pytest pour la mesure de couverture de code
  - Génère des rapports détaillés avec les lignes manquantes

### Métriques de couverture

| Fichier | Couverture | Lignes manquantes |
|---------|------------|-------------------|
| models.py | 100% | - |
| views.py | 100% | - |
| urls.py | 100% | - |
| admin.py | 100% | - |
| settings.py | 100% | - |
| apps.py | 100% | - |
| **TOTAL** | **96%** | asgi.py, wsgi.py (exclus) |

### Fixtures pytest créées

```python
@pytest.fixture
def address()     # Crée une adresse de test
def letting()     # Crée un letting avec adresse
def user()        # Crée un utilisateur Django
def profile()     # Crée un profil avec utilisateur
def client()      # Client HTTP pour les requêtes
```

### Commandes

```bash
# Lancer les tests avec couverture
pytest

# Lancer les tests sans couverture
pytest --no-cov

# Générer un rapport HTML
pytest --cov-report=html
```

### Files Modified
- `oc_lettings_site/tests.py`: Remplacement du test factice par 26 tests complets
- `setup.cfg`: Configuration pytest-cov et exclusions
- `requirements.txt`: Ajout de pytest-cov

---

## [1.1.1] - 2025-11-24 - Django 4.2 Settings Update

### Résumé
Suppression du setting `USE_L10N` dépréciée dans Django 4.2.

### Changed

#### Settings Configuration (oc_lettings_site/settings.py)
- **Removed**: `USE_L10N = True` (line 103)
  - **Reason**: This setting is deprecated in Django 4.2 and will be removed in Django 5.0
  - **What it was**: `USE_L10N` (Localization) controlled whether Django should format dates, numbers, and other data using locale-specific formatting
  - **Why removed**: Starting with Django 4.0, localized formatting is **always enabled by default**. The setting became redundant and was deprecated.
  - **Impact**: No functional change - localization continues to work automatically
  - **Benefit**: Eliminates deprecation warning: `RemovedInDjango50Warning: The USE_L10N setting is deprecated`

#### What USE_L10N Did
When `USE_L10N = True` was set, Django would:
- Format dates according to the current locale (e.g., "11/24/2025" in US, "24/11/2025" in Europe)
- Format numbers with appropriate thousand separators (e.g., "1,000.00" vs "1.000,00")
- Use locale-specific currency symbols and decimal points
- Apply regional formatting to time zones

**In Django 4.0+**, this behavior is the standard and cannot be disabled, making the setting obsolete.

### Files Modified
- `oc_lettings_site/settings.py`: Removed deprecated `USE_L10N` setting

---

## [1.1.0] - 2025-11-24 - Python 3.13 Compatibility Update

### Résumé
Mise à jour de Django 3.0 vers 4.2.16 LTS pour compatibilité avec Python 3.13.7.

### Changed

#### Dependencies (requirements.txt)
- **Django**: Upgraded from `3.0` to `4.2.16` (LTS)
  - **Reason**: Django 3.0 is incompatible with Python 3.13.7 due to removed modules (`distutils`, `cgi`)
  - Django 4.2 LTS provides full Python 3.13 support and extended security updates until April 2026

- **pytest-django**: Upgraded from `3.9.0` to `4.9.0`
  - **Reason**: Required to maintain compatibility with Django 4.2

- **flake8**: Kept at `3.7.0` (no changes required)

### Technical Details

#### Issues Resolved
1. `ModuleNotFoundError: No module named 'distutils'`
   - The `distutils` module was removed from Python 3.12+ standard library
   - Django 3.0 depends on this deprecated module

2. `ModuleNotFoundError: No module named 'cgi'`
   - The `cgi` module was removed from Python 3.13 standard library
   - Django 3.2 and earlier versions depend on this module

#### Environment
- **Python Version**: 3.13.7
- **Platform**: Windows (win32)
- **Django Version**: 4.2.16 LTS

### Files Modified
- `requirements.txt`: Updated dependency versions
- `CHANGELOG.md`: Created to document changes
