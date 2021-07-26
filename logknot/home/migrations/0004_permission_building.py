from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


def add_building_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    building_content_type, _created = ContentType.objects.get_or_create(
        model='building',
        app_label='buildinggroup'
    )

    add_building_permission, _created = Permission.objects.get_or_create(
        content_type=building_content_type,
        codename='add_building',
        defaults={'name': 'Can add building'}
    )
    change_building_permission, _created = Permission.objects.get_or_create(
        content_type=building_content_type,
        codename='change_building',
        defaults={'name': 'Can change building'}
    )
    delete_building_permission, _created = Permission.objects.get_or_create(
        content_type=building_content_type,
        codename='delete_building',
        defaults={'name': 'Can delete building'}
    )


def remove_building_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    building_content_type = ContentType.objects.get(
        model='building',
        app_label='buildinggroup',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=building_content_type,
        codename__in=('add_building', 'change_building', 'delete_building')
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0003_buildingimage_buildingrendition'),
    ]

    operations = [
        migrations.RunPython(add_building_permissions_to_admin_groups, remove_building_permissions),
    ]
