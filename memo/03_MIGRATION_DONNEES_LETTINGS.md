# Migration des données vers l'application Lettings

## Vue d'ensemble

Ce document explique comment transférer les données des modèles `Address` et `Letting` de l'ancienne application `oc_lettings_site` vers la nouvelle application `lettings`.

## Étape 1 : Créer la migration initiale

```bash
python manage.py makemigrations lettings
```

Cette commande génère `lettings/migrations/0001_initial.py` qui crée les nouvelles tables :
- `lettings_address`
- `lettings_letting`

## Étape 2 : Créer la migration de transfert des données

J'ai créé manuellement le fichier `lettings/migrations/0002_migrate_data.py` :

```python
from django.db import migrations


def migrate_address_data(apps, schema_editor):
    """Transfère les données de oc_lettings_site.Address vers lettings.Address"""
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    NewAddress = apps.get_model('lettings', 'Address')

    for old_address in OldAddress.objects.all():
        NewAddress.objects.create(
            id=old_address.id,
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code,
        )


def migrate_letting_data(apps, schema_editor):
    """Transfère les données de oc_lettings_site.Letting vers lettings.Letting"""
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewLetting = apps.get_model('lettings', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')

    for old_letting in OldLetting.objects.all():
        new_address = NewAddress.objects.get(id=old_letting.address_id)
        NewLetting.objects.create(
            id=old_letting.id,
            title=old_letting.title,
            address=new_address,
        )


def reverse_address_data(apps, schema_editor):
    """Supprime les données de lettings.Address (pour rollback)"""
    NewAddress = apps.get_model('lettings', 'Address')
    NewAddress.objects.all().delete()


def reverse_letting_data(apps, schema_editor):
    """Supprime les données de lettings.Letting (pour rollback)"""
    NewLetting = apps.get_model('lettings', 'Letting')
    NewLetting.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_address_data, reverse_address_data),
        migrations.RunPython(migrate_letting_data, reverse_letting_data),
    ]
```

## Concepts clés expliqués

### Signature de la fonction : `def migrate_address_data(apps, schema_editor)`

Selon la [documentation officielle Django](https://docs.djangoproject.com/en/5.2/ref/migration-operations/#runpython) :

> `RunPython` expects a callable as its argument which takes two arguments:
> - the first is an **app registry** that has the historical versions of all your models loaded into it
> - the second is a **SchemaEditor**, which you can use to manually effect database schema changes

#### `apps` - Registre des applications

C'est un registre qui contient les **versions historiques** des modèles. On l'utilise avec `apps.get_model()` :

```python
OldAddress = apps.get_model('oc_lettings_site', 'Address')
```

**Pourquoi ne pas importer directement ?**
```python
# NE PAS FAIRE :
from oc_lettings_site.models import Address
```

Car :
1. Le modèle pourrait avoir changé depuis
2. Le modèle pourrait ne plus exister
3. On veut la version du modèle **au moment de la migration**

#### `schema_editor` - Éditeur de schéma

Permet de modifier le schéma de la base de données (créer/supprimer tables, colonnes, index...).

**Utilisation courante** : accéder à l'alias de connexion pour les bases multiples :
```python
db_alias = schema_editor.connection.alias
Country.objects.using(db_alias).bulk_create([...])
```

**Dans notre cas** : non utilisé car on ne fait que copier des données, pas modifier la structure. Mais le paramètre est **obligatoire** car Django appelle toujours la fonction avec ces deux arguments.

### `operations` - Les opérations à exécuter

```python
operations = [
    migrations.RunPython(migrate_address_data, reverse_address_data),
    migrations.RunPython(migrate_letting_data, reverse_letting_data),
]
```

C'est une **liste d'opérations** que Django exécutera **dans l'ordre** lors de la migration.

#### Ordre d'exécution important !

```python
operations = [
    migrations.RunPython(migrate_address_data, ...),  # 1. D'abord les adresses
    migrations.RunPython(migrate_letting_data, ...),  # 2. Ensuite les lettings
]
```

**Pourquoi cet ordre ?**

Le modèle `Letting` a une clé étrangère vers `Address` :
```python
class Letting(models.Model):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
```

→ On doit copier les `Address` **AVANT** les `Letting`, sinon la clé étrangère pointerait vers une adresse qui n'existe pas encore !

#### Visualisation

```
1. migrate_address_data()
   ┌─────────────────────┐      ┌─────────────────────┐
   │ oc_lettings_site_   │  →   │ lettings_address    │
   │ address             │      │                     │
   │ id=1, "7217 Bedford"│      │ id=1, "7217 Bedford"│
   └─────────────────────┘      └─────────────────────┘

2. migrate_letting_data()
   ┌─────────────────────┐      ┌─────────────────────┐
   │ oc_lettings_site_   │  →   │ lettings_letting    │
   │ letting             │      │                     │
   │ id=1, address_id=1  │      │ id=1, address_id=1  │
   └─────────────────────┘      └─────────────────────┘
                                        ↓
                                (pointe vers lettings_address.id=1 ✓)
```

### `RunPython` - Exécuter du code Python

```python
migrations.RunPython(migrate_address_data, reverse_address_data)
```

- **Premier argument** : fonction à exécuter lors de `migrate` (forward)
- **Second argument** : fonction à exécuter lors de `migrate --reverse` (rollback)

#### Pourquoi deux fonctions ?

Pour rendre la migration **réversible**. Si on doit annuler :

```bash
python manage.py migrate lettings 0001  # Revenir à 0001
```

Django exécutera `reverse_address_data` et `reverse_letting_data` pour supprimer les données copiées.

### `dependencies` - L'ordre d'exécution des migrations

```python
dependencies = [
    ('lettings', '0001_initial'),
    ('oc_lettings_site', '0001_initial'),
]
```

Cela signifie : **"Cette migration ne peut s'exécuter QU'APRÈS ces deux migrations"**.

#### Pourquoi ces deux dépendances ?

**1. `('lettings', '0001_initial')`**

La migration `0001_initial` de `lettings` **crée la table `lettings_address`**.
→ On doit créer la table AVANT d'y copier des données.

**2. `('oc_lettings_site', '0001_initial')`**

La migration `0001_initial` de `oc_lettings_site` **crée la table `oc_lettings_site_address`**.
→ On doit avoir les données sources AVANT de pouvoir les copier.

#### Visualisation

```
oc_lettings_site.0001_initial       lettings.0001_initial
   (crée l'ancienne table)           (crée la nouvelle table)
            ↓                                ↓
            └──────────┬─────────────────────┘
                       ↓
              lettings.0002_migrate_data
              (copie les données de l'une vers l'autre)
```

#### Sans ces dépendances ?

Django pourrait exécuter `0002_migrate_data` **avant** que les tables existent → erreur !

```
django.db.utils.OperationalError: no such table: lettings_address
```

#### Comment Django sait l'ordre ?

Django construit un **graphe de dépendances** et exécute les migrations dans le bon ordre. Tu peux le voir avec :

```bash
python manage.py showmigrations --plan
```

### Préservation des IDs

```python
NewAddress.objects.create(
    id=old_address.id,  # On garde le même ID
    ...
)
```

Important pour :
- Maintenir les relations (ForeignKey)
- Permettre un rollback propre
- Éviter les conflits d'ID

## Étape 3 : Appliquer les migrations

```bash
python manage.py migrate
```

Résultat :
```
Applying lettings.0001_initial... OK
Applying lettings.0002_migrate_data... OK
```

## Vérification

```bash
python manage.py shell
```

```python
from lettings.models import Address, Letting
print(f"Address: {Address.objects.count()} enregistrements")
print(f"Letting: {Letting.objects.count()} enregistrements")
```

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `python manage.py showmigrations` | Voir l'état des migrations |
| `python manage.py migrate lettings 0001` | Revenir à la migration 0001 |
| `python manage.py migrate lettings zero` | Annuler toutes les migrations lettings |
| `python manage.py sqlmigrate lettings 0002` | Voir le SQL généré |

## Prochaines étapes

1. Créer l'application `profiles` et migrer le modèle `Profile`
2. Supprimer les anciens modèles de `oc_lettings_site`
3. Créer les migrations pour supprimer les anciennes tables

## Sources

- [Migration Operations - Django Documentation](https://docs.djangoproject.com/en/5.2/ref/migration-operations/#runpython)
- [How to create database migrations - Django Documentation](https://docs.djangoproject.com/en/5.0/howto/writing-migrations/)
