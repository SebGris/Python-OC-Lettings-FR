# Création de l'application Profiles et migration des données

## Vue d'ensemble

Ce document explique comment créer l'application `profiles` et migrer le modèle `Profile` depuis `oc_lettings_site`.

## Étape 1 : Créer l'application

```bash
python manage.py startapp profiles
```

## Étape 2 : Ajouter le modèle Profile

Dans `profiles/models.py` :

```python
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
```

## Étape 3 : Enregistrer l'application

Dans `oc_lettings_site/settings.py` :

```python
INSTALLED_APPS = [
    'lettings',
    'profiles',  # Nouvelle application
    'oc_lettings_site.apps.OCLettingsSiteConfig',
    # ...
]
```

## Étape 4 : Créer la migration initiale

```bash
python manage.py makemigrations profiles
```

Génère `profiles/migrations/0001_initial.py`.

## Étape 5 : Créer la migration de transfert des données

Fichier `profiles/migrations/0002_migrate_data.py` :

```python
from django.db import migrations


def migrate_profile_data(apps, schema_editor):
    """Transfère les données de oc_lettings_site.Profile vers profiles.Profile.

    Cette migration a été exécutée lors de la refactorisation initiale.
    Elle ne fait rien si les anciens modèles n'existent plus.
    """
    try:
        OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    except LookupError:
        # Les anciens modèles n'existent plus, migration déjà effectuée
        return

    NewProfile = apps.get_model('profiles', 'Profile')
    for old_profile in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old_profile.id,
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


def reverse_profile_data(apps, schema_editor):
    """Supprime les données de profiles.Profile (pour rollback)"""
    NewProfile = apps.get_model('profiles', 'Profile')
    NewProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_profile_data, reverse_profile_data),
    ]
```

### Note : `user_id` vs `user`

On utilise `user_id=old_profile.user_id` au lieu de `user=old_profile.user` car c'est plus performant (pas de requête supplémentaire pour charger l'objet User).

## Étape 6 : Appliquer les migrations

```bash
python manage.py migrate
```

Résultat :
```
Applying profiles.0001_initial... OK
Applying profiles.0002_migrate_data... OK
```

## Vérification

```bash
python manage.py shell
```

```python
from profiles.models import Profile
print(f"Profile: {Profile.objects.count()} enregistrements")
for p in Profile.objects.all():
    print(f"  - {p} (ville favorite: {p.favorite_city})")
```

Résultat :
```
Profile: 4 enregistrements
  - HeadlinesGazer (ville favorite: Buenos Aires)
  - DavWin (ville favorite: Barcelona)
  - AirWow (ville favorite: Budapest)
  - 4meRomance (ville favorite: Berlin)
```

## Récapitulatif des fichiers créés/modifiés

| Fichier | Action |
|---------|--------|
| `profiles/` | Nouveau dossier (application) |
| `profiles/models.py` | Modèle Profile |
| `profiles/migrations/0001_initial.py` | Migration auto-générée |
| `profiles/migrations/0002_migrate_data.py` | Migration manuelle (transfert données) |
| `oc_lettings_site/settings.py` | Ajout de 'profiles' dans INSTALLED_APPS |

## Prochaines étapes

1. Supprimer les anciens modèles de `oc_lettings_site/models.py`
2. Créer les migrations pour supprimer les anciennes tables
3. Déplacer les vues et URLs vers les nouvelles applications

## Sources

- [Migration Operations - Django Documentation](https://docs.djangoproject.com/fr/5.2/ref/migration-operations/#runpython)
- [ForeignKey.related_name - Django Documentation](https://docs.djangoproject.com/fr/5.2/ref/models/fields/#django.db.models.ForeignKey.related_name)
