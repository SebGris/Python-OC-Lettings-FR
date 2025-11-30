# Corrections des tests et migrations après refactorisation

## Vue d'ensemble

Après la refactorisation des applications, plusieurs corrections étaient nécessaires pour que `pytest` et `flake8` fonctionnent correctement.

## Problème 1 : Erreur des migrations de données avec pytest

### Symptôme

```bash
pytest
# LookupError: No installed app with label 'oc_lettings_site'.
```

### Cause

Les migrations de données (`0002_migrate_data.py`) référençaient les anciens modèles de `oc_lettings_site` qui n'existent plus :

```python
# Avant (provoquait l'erreur)
OldAddress = apps.get_model('oc_lettings_site', 'Address')
```

Quand pytest crée une base de données de test, il exécute toutes les migrations depuis le début. Les anciennes tables n'existent plus, donc `apps.get_model()` échoue.

### Solution

Encapsuler le code dans un bloc `try/except LookupError` :

```python
def migrate_address_data(apps, schema_editor):
    """Migration qui ne fait rien si les anciens modèles n'existent plus."""
    try:
        OldAddress = apps.get_model('oc_lettings_site', 'Address')
        NewAddress = apps.get_model('lettings', 'Address')

        for old_address in OldAddress.objects.all():
            NewAddress.objects.create(...)
    except LookupError:
        # Les anciens modèles n'existent plus, migration déjà effectuée
        pass
```

### Fichiers modifiés

- `lettings/migrations/0002_migrate_data.py`
- `profiles/migrations/0002_migrate_data.py`

### Pourquoi ça fonctionne

1. **En production** : Les anciens modèles existaient, la migration a transféré les données
2. **Avec pytest** : Les anciens modèles n'existent plus, le `LookupError` est attrapé et ignoré

---

## Problème 2 : Tests avec imports obsolètes

### Symptôme

```bash
pytest
# ImportError: cannot import name 'Address' from 'oc_lettings_site.models'
```

### Cause

Le fichier `oc_lettings_site/tests.py` importait encore les modèles depuis l'ancien emplacement :

```python
# Avant (erreur)
from .models import Address, Letting, Profile
```

### Solution

Mettre à jour les imports vers les nouvelles applications :

```python
# Après (correct)
from lettings.models import Address, Letting
from profiles.models import Profile
```

---

## Problème 3 : URLs avec namespaces dans les tests

### Symptôme

Les tests échouaient car ils utilisaient les anciens noms d'URL :

```python
# Avant (erreur)
reverse("lettings_index")
reverse("profiles_index")
```

### Solution

Utiliser les noms avec namespace :

```python
# Après (correct)
reverse("lettings:index")
reverse("profiles:index")
reverse("lettings:letting", args=[letting.id])
reverse("profiles:profile", args=[profile.user.username])
```

---

## Problème 4 : Templates dans les assertions de tests

### Symptôme

Les assertions sur les noms de templates échouaient :

```python
# Avant (erreur)
assert "lettings_index.html" in [t.name for t in response.templates]
```

### Solution

Utiliser les nouveaux chemins de templates :

```python
# Après (correct)
assert "lettings/index.html" in [t.name for t in response.templates]
assert "profiles/index.html" in [t.name for t in response.templates]
```

---

## Problème 5 : Erreurs flake8

### Symptômes

```bash
flake8
# F401 'django.test.TestCase' imported but unused (lettings/tests.py)
# F401 'django.test.TestCase' imported but unused (profiles/tests.py)
# F401 'django.contrib.admin' imported but unused (oc_lettings_site/admin.py)
# E231 missing whitespace after ',' (settings.py:114)
```

### Solutions

1. **lettings/tests.py** et **profiles/tests.py** : Remplacer l'import inutilisé par un commentaire
   ```python
   # Tests for lettings app are in oc_lettings_site/tests.py
   ```

2. **oc_lettings_site/admin.py** : Supprimer l'import inutile
   ```python
   # Models have been moved to their respective apps
   ```

3. **settings.py** : Ajouter l'espace après la virgule
   ```python
   STATICFILES_DIRS = [BASE_DIR / "static", ]
   ```

---

## Récapitulatif des fichiers modifiés

| Fichier | Modification |
|---------|--------------|
| `lettings/migrations/0002_migrate_data.py` | Ajout try/except LookupError |
| `profiles/migrations/0002_migrate_data.py` | Ajout try/except LookupError |
| `oc_lettings_site/tests.py` | Mise à jour imports et URLs |
| `templates/base.html` | URLs avec namespaces |
| `lettings/tests.py` | Suppression import inutilisé |
| `profiles/tests.py` | Suppression import inutilisé |
| `oc_lettings_site/admin.py` | Suppression import inutilisé |
| `oc_lettings_site/settings.py` | Correction style flake8 |

---

## Vérification finale

```bash
# Tests : 26 passent, couverture 100%
pytest

# Linting : aucune erreur
flake8

# Vérification Django
python manage.py check
# System check identified no issues (0 silenced).
```

---

## Concepts clés

### try/except dans les migrations

Les migrations Django doivent être **idempotentes** et **robustes**. Une migration de données qui référence des modèles potentiellement absents doit gérer ce cas gracieusement.

### Centralisation des tests

Tous les tests sont dans `oc_lettings_site/tests.py` car :
- Les modèles sont testés ensemble
- Les vues et URLs forment un ensemble cohérent
- La couverture est mesurée sur `oc_lettings_site`

Les fichiers `lettings/tests.py` et `profiles/tests.py` sont vides (commentaire uniquement) pour éviter les erreurs flake8.
