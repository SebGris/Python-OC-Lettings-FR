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
