from django.db import migrations


def migrate_address_data(apps, schema_editor):  # schema_editor non utilisé
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


def migrate_letting_data(apps, schema_editor):  # schema_editor non utilisé
    """Transfère les données de oc_lettings_site.Letting vers lettings.Letting"""
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewLetting = apps.get_model('lettings', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')

    for old_letting in OldLetting.objects.all():
        # Récupère la nouvelle adresse correspondante (même id)
        new_address = NewAddress.objects.get(id=old_letting.address_id)
        NewLetting.objects.create(
            id=old_letting.id,
            title=old_letting.title,
            address=new_address,
        )


def reverse_address_data(apps, schema_editor):  # schema_editor non utilisé
    """Supprime les données de lettings.Address (pour rollback)"""
    NewAddress = apps.get_model('lettings', 'Address')
    NewAddress.objects.all().delete()


def reverse_letting_data(apps, schema_editor):  # schema_editor non utilisé
    """Supprime les données de lettings.Letting (pour rollback)"""
    NewLetting = apps.get_model('lettings', 'Letting')
    NewLetting.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),  # Dépend des anciennes tables
    ]

    operations = [
        migrations.RunPython(migrate_address_data, reverse_address_data),
        migrations.RunPython(migrate_letting_data, reverse_letting_data),
    ]
