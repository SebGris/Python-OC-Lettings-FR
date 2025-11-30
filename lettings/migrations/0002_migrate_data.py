from django.db import migrations


def migrate_address_data(apps, schema_editor):
    """Transfère les données de oc_lettings_site.Address vers lettings.Address.

    Cette migration a été exécutée lors de la refactorisation initiale.
    Elle ne fait rien si les anciens modèles n'existent plus.
    """
    try:
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
    except LookupError:
        # Les anciens modèles n'existent plus, migration déjà effectuée
        pass


def migrate_letting_data(apps, schema_editor):
    """Transfère les données de oc_lettings_site.Letting vers lettings.Letting.

    Cette migration a été exécutée lors de la refactorisation initiale.
    Elle ne fait rien si les anciens modèles n'existent plus.
    """
    try:
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
    except LookupError:
        # Les anciens modèles n'existent plus, migration déjà effectuée
        pass


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
