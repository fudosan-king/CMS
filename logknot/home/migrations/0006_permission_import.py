from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


def add_import_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    import_content_type, _created = ContentType.objects.get_or_create(
        model='import',
        app_label='importgroup'
    )

    add_import_permission, _created = Permission.objects.get_or_create(
        content_type=import_content_type,
        codename='add_import',
        defaults={'name': 'Can add import'}
    )
    change_import_permission, _created = Permission.objects.get_or_create(
        content_type=import_content_type,
        codename='change_import',
        defaults={'name': 'Can change import'}
    )
    delete_import_permission, _created = Permission.objects.get_or_create(
        content_type=import_content_type,
        codename='delete_import',
        defaults={'name': 'Can delete import'}
    )


def remove_import_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    import_content_type = ContentType.objects.get(
        model='import',
        app_label='importgroup',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=import_content_type,
        codename__in=('add_import', 'change_import', 'delete_import')
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0005_permission_removed'),
    ]

    operations = [
        migrations.RunPython(add_import_permissions_to_admin_groups, remove_import_permissions),
    ]
