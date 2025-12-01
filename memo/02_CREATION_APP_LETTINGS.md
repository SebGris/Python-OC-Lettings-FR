# Création de l'application Lettings

## Commande utilisée

```bash
python manage.py startapp lettings
```

Cette commande Django crée automatiquement la structure de base d'une application :

```
lettings/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

## Ajout des modèles

Dans `lettings/models.py`, j'ai copié les modèles `Address` et `Letting` depuis `oc_lettings_site/models.py` :

```python
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self):
        return f'{self.number} {self.street}'


class Letting(models.Model):
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
```

## Enregistrement de l'application

Dans `oc_lettings_site/settings.py`, j'ai ajouté l'application dans `INSTALLED_APPS` :

```python
INSTALLED_APPS = [
    'lettings',  # Nouvelle application
    'oc_lettings_site.apps.OCLettingsSiteConfig',
    'django.contrib.admin',
    # ...
]
```

## Vérification

```bash
python manage.py check
```

Cette commande vérifie que la configuration Django est correcte et que les modèles sont valides.

## Notes importantes

- Les modèles sont **copiés** (pas déplacés) pour l'instant
- Les anciennes tables dans `oc_lettings_site` existent toujours
- La prochaine étape sera de **migrer les données** vers les nouvelles tables
- Puis de **supprimer** les anciens modèles de `oc_lettings_site`
