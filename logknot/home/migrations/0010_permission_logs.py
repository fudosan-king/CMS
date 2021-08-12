from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


def add_logs_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    logs_content_type, _created = ContentType.objects.get_or_create(
        model='logs',
        app_label='logsgroup'
    )
    change_logs_permission, _created = Permission.objects.get_or_create(
        content_type=logs_content_type,
        codename='change_logs',
        defaults={'name': 'Can change import logs'}
    )


def remove_logs_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    logs_content_type = ContentType.objects.get(
        model='logs',
        app_label='logsgroup',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=logs_content_type,
        codename__in=('change_logs')
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0009_permission_search'),
    ]

    operations = [
        migrations.RunPython(add_logs_permissions_to_admin_groups, remove_logs_permissions),
    ]
