# Soutenance - Environnement de développement local

## Démonstration du site sur localhost

### Lancer l'application

```bash
# Avec Poetry (développement)
poetry run python manage.py runserver

# Ou avec Docker
docker run -d --name oc-lettings-local -p 8001:8000 \
  -e SECRET_KEY="dev-secret-key" \
  -e DEBUG="True" \
  sebgris/oc-lettings:latest
```

### URLs à montrer

| URL | Description |
|-----|-------------|
| http://localhost:8000 | Page d'accueil |
| http://localhost:8000/lettings/ | Liste des locations |
| http://localhost:8000/lettings/1/ | Détail d'une location |
| http://localhost:8000/profiles/ | Liste des profils |
| http://localhost:8000/profiles/HeadlessCross/ | Détail d'un profil |
| http://localhost:8000/admin/ | Interface d'administration |

---

## Problèmes rencontrés et solutions

### 1. Incompatibilité Python 3.13 avec Django 3.0

**Problème :**
```
ModuleNotFoundError: No module named 'distutils'
ModuleNotFoundError: No module named 'cgi'
```

**Cause :**
- Python 3.12+ a supprimé le module `distutils` de la bibliothèque standard
- Python 3.13 a supprimé le module `cgi`
- Django 3.0 dépendait de ces modules obsolètes

**Solution :**
- Mise à jour de Django 3.0 → Django 4.2.16 LTS
- Mise à jour de pytest-django 3.9.0 → 4.9.0

---

### 2. Setting USE_L10N dépréciée

**Problème :**
```
RemovedInDjango50Warning: The USE_L10N setting is deprecated
```

**Cause :**
- `USE_L10N = True` était défini dans `settings.py`
- Cette option est dépréciée depuis Django 4.0 (localisation activée par défaut)

**Solution :**
- Suppression de la ligne `USE_L10N = True` dans `settings.py`

---

### 3. Variables d'environnement Windows

**Problème :**
```bash
# Cette commande ne fonctionne pas sur Windows
set DATABASE_URL=postgresql://... && poetry run python manage.py shell
```

**Cause :**
- Sur Windows, `set VAR=value &&` ne transmet pas correctement les variables d'environnement au processus suivant

**Solution :**
- Utiliser Python pour définir les variables avant l'import Django :

```python
poetry run python -c "
import os
os.environ['DATABASE_URL']='postgresql://...'
os.environ['DJANGO_SETTINGS_MODULE']='oc_lettings_site.settings'
import django
django.setup()
# ... suite du code
"
```

---

### 4. Erreur SQLite en lecture seule avec Docker sur Windows

**Problème :**
```
OperationalError: attempt to write a readonly database
```

**Cause :**
- Montage d'un volume SQLite depuis Windows (NTFS) vers un conteneur Linux
- Différences de permissions entre les systèmes de fichiers

**Solution :**
- Ne pas monter la base SQLite en volume sur Windows
- Utiliser la base de données incluse dans l'image Docker
- En production : utiliser PostgreSQL (Supabase)

---

### 5. Port déjà utilisé avec Docker

**Problème :**
```
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Cause :**
- Un autre conteneur ou processus utilise déjà le port 8000

**Solution :**
```bash
# Option 1 : Arrêter le conteneur existant
docker stop <nom-conteneur>

# Option 2 : Utiliser un port différent
docker run -d -p 8001:8000 ...
```

---

### 6. Nom de conteneur déjà utilisé

**Problème :**
```
Conflict. The container name "/oc-lettings-local" is already in use
```

**Cause :**
- Un conteneur avec ce nom existe déjà (même arrêté)

**Solution :**
```bash
# Supprimer l'ancien conteneur
docker rm oc-lettings-local

# Puis relancer
docker run -d --name oc-lettings-local ...
```

---

### 7. poetry.lock désynchronisé

**Problème :**
```
pyproject.toml changed significantly since poetry.lock was last generated
```

**Cause :**
- Modifications dans `pyproject.toml` sans mise à jour du fichier `poetry.lock`

**Solution :**
```bash
poetry lock
git add poetry.lock
git commit -m "Regenerate poetry.lock"
```

---

## Tableau récapitulatif

| Problème | Cause | Solution |
|----------|-------|----------|
| `ModuleNotFoundError: distutils` | Python 3.13 + Django 3.0 | Upgrade Django 4.2.16 |
| `USE_L10N deprecated` | Setting obsolète | Supprimer USE_L10N |
| Variables env Windows | Syntaxe `set` incompatible | Utiliser Python `os.environ` |
| SQLite readonly Docker | Permissions NTFS/Linux | Ne pas monter en volume |
| Port already allocated | Port 8000 occupé | Utiliser port 8001 |
| Container name in use | Conteneur existant | `docker rm` avant relancer |
| poetry.lock out of sync | pyproject.toml modifié | `poetry lock` |

---

## Points à mentionner lors de la soutenance

1. **Choix de Poetry** : Gestion moderne des dépendances Python avec fichier de verrouillage (`poetry.lock`) pour des builds reproductibles

2. **Configuration flexible** : Le projet détecte automatiquement l'environnement (SQLite en dev, PostgreSQL en prod) via la variable `DATABASE_URL`

3. **Docker multi-stage** : Image optimisée (~150 MB) grâce au build en deux étapes (builder + production)

4. **Compatibilité Windows** : Adaptations spécifiques pour le développement sur Windows (commandes, chemins, permissions)
