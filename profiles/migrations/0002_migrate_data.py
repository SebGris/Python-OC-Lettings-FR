from django.db import migrations


def migrate_profile_data(apps, schema_editor):  # schema_editor non utilisé
    """Transfère les données de oc_lettings_site.Profile vers profiles.Profile"""
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for old_profile in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old_profile.id,
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


def reverse_profile_data(apps, schema_editor):  # schema_editor non utilisé
    """Supprime les données de profiles.Profile (pour rollback)"""
    NewProfile = apps.get_model('profiles', 'Profile')
    NewProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),  # Dépend des anciennes tables
    ]

    operations = [
        migrations.RunPython(migrate_profile_data, reverse_profile_data),
    ]
