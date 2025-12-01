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

    for old_letting in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old_letting.id,
            title=old_letting.title,
            address_id=old_letting.address_id,
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

Cette ligne retourne un modèle Django qui permet d'accéder à la table SQLite3 correspondante :

| Code Python | Table SQLite3 |
|-------------|---------------|
| `apps.get_model('oc_lettings_site', 'Address')` | `oc_lettings_site_address` |
| `apps.get_model('lettings', 'Address')` | `lettings_address` |

**Convention de nommage Django** : `<nom_app>_<nom_modèle_en_minuscule>`

Ensuite, on utilise l'ORM Django normalement :

```python
OldAddress.objects.all()        # SELECT * FROM oc_lettings_site_address
NewAddress.objects.create(...)  # INSERT INTO lettings_address ...
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

**Dans notre cas** : non utilisé car on ne fait que copier des données, pas modifier la structure. Mais le paramètre est **obligatoire** car Django appelle toujours la fonction avec ces deux arguments.

Exemple d'utilisation (pour modifier une table) :
```python
def add_column(apps, schema_editor):
    schema_editor.execute("ALTER TABLE my_table ADD COLUMN new_field VARCHAR(100)")
```

Source : [RunPython - Django Documentation](https://docs.djangoproject.com/en/5.2/ref/migration-operations/#runpython)

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
]
```

Cela signifie : **"Cette migration ne peut s'exécuter QU'APRÈS `lettings.0001_initial`"**.

#### Pourquoi cette dépendance ?

La migration `0001_initial` de `lettings` **crée la table `lettings_address`**.
→ On doit créer la table AVANT d'y copier des données.

#### Et `oc_lettings_site` ?

On n'a **pas** besoin de dépendance vers `oc_lettings_site` car :
1. Le `try/except LookupError` gère le cas où les anciens modèles n'existent plus
2. Cela permet à pytest de fonctionner (il crée une base de données vierge sans les anciennes tables)

#### Visualisation

```
lettings.0001_initial
   (crée la nouvelle table)
            ↓
lettings.0002_migrate_data
   (copie les données SI les anciennes tables existent)
```

#### Sans cette dépendance ?

Django pourrait exécuter `0002_migrate_data` **avant** que la table existe → erreur !

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

### Utilisation de `address_id` au lieu de `address`

```python
NewLetting.objects.create(
    id=old_letting.id,
    title=old_letting.title,
    address_id=old_letting.address_id,  # Utilise directement l'ID
)
```

Django permet d'assigner directement l'ID d'une clé étrangère via `<field>_id` au lieu de passer l'objet. Cela évite une requête supplémentaire en base de données :

```python
# ❌ Moins efficace : fait une requête SELECT pour récupérer l'objet Address
new_address = NewAddress.objects.get(id=old_letting.address_id)
NewLetting.objects.create(address=new_address)

# ✅ Plus efficace : assigne directement l'ID sans requête supplémentaire
NewLetting.objects.create(address_id=old_letting.address_id)
```

Cela fonctionne car on préserve les mêmes IDs lors de la migration des `Address`.

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

- [Opérations de migration - Documentation Django](https://docs.djangoproject.com/fr/5.2/ref/migration-operations/)
- [RunPython - Documentation Django](https://docs.djangoproject.com/fr/5.2/ref/migration-operations/#runpython)
- [Écriture de migrations - Documentation Django](https://docs.djangoproject.com/fr/5.2/howto/writing-migrations/)
- [Migration de données entre applications tierces - Documentation Django](https://docs.djangoproject.com/fr/5.2/howto/writing-migrations/#migrating-data-between-third-party-apps)
