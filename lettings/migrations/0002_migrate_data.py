"""
Data migration for the lettings application.

This module migrates Address and Letting data from the old oc_lettings_site
models to the new lettings application models.
"""
from django.db import migrations


def migrate_address_data(apps, _schema_editor):
    """
    Transfer data from oc_lettings_site.Address to lettings.Address.

    This migration was executed during the initial refactoring.
    It does nothing if the old models no longer exist.

    Args:
        apps: The app registry.
        schema_editor: The database schema editor.
    """
    try:
        OldAddress = apps.get_model("oc_lettings_site", "Address")
    except LookupError:
        return

    NewAddress = apps.get_model("lettings", "Address")
    for old_address in OldAddress.objects.iterator():
        NewAddress.objects.create(
            # Preserve ID to maintain FK relationships with Letting
            id=old_address.id,
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code,
        )


def migrate_letting_data(apps, _schema_editor):
    """
    Transfer data from oc_lettings_site.Letting to lettings.Letting.

    This migration was executed during the initial refactoring.
    It does nothing if the old models no longer exist.

    Args:
        apps: The app registry.
        schema_editor: The database schema editor.
    """
    try:
        OldLetting = apps.get_model("oc_lettings_site", "Letting")
    except LookupError:
        return

    NewLetting = apps.get_model("lettings", "Letting")
    for old_letting in OldLetting.objects.all():
        NewLetting.objects.create(
            # Preserve ID for data consistency
            id=old_letting.id,
            title=old_letting.title,
            address=old_letting.address_id,
        )


class Migration(migrations.Migration):
    """Migration to transfer data from oc_lettings_site to lettings app."""

    dependencies = [
        ("lettings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_address_data, migrations.RunPython.noop),
        migrations.RunPython(migrate_letting_data, migrations.RunPython.noop),
    ]
