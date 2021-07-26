from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


def add_removed_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    removed_content_type, _created = ContentType.objects.get_or_create(
        model='removed',
        app_label='removedgroup'
    )

    add_removed_permission, _created = Permission.objects.get_or_create(
        content_type=removed_content_type,
        codename='add_removed',
        defaults={'name': 'Can add removed'}
    )
    change_removed_permission, _created = Permission.objects.get_or_create(
        content_type=removed_content_type,
        codename='change_removed',
        defaults={'name': 'Can change removed'}
    )
    delete_removed_permission, _created = Permission.objects.get_or_create(
        content_type=removed_content_type,
        codename='delete_removed',
        defaults={'name': 'Can delete removed'}
    )


def remove_removed_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    removed_content_type = ContentType.objects.get(
        model='removed',
        app_label='removedgroup',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=removed_content_type,
        codename__in=('add_removed', 'change_removed', 'delete_removed')
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0004_permission_building'),
    ]

    operations = [
        migrations.RunPython(add_removed_permissions_to_admin_groups, remove_removed_permissions),
    ]
