from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import wagtail.core.models
import wagtail.search.index


def add_search_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    search_content_type, _created = ContentType.objects.get_or_create(
        model='search',
        app_label='searchgroup'
    )
    change_search_permission, _created = Permission.objects.get_or_create(
        content_type=search_content_type,
        codename='change_search',
        defaults={'name': 'Can change search sort'}
    )


def remove_search_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    search_content_type = ContentType.objects.get(
        model='search',
        app_label='searchgroup',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=search_content_type,
        codename__in=('change_search')
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('home', '0008_auto_20210806_0114'),
    ]

    operations = [
        migrations.RunPython(add_search_permissions_to_admin_groups, remove_search_permissions),
    ]
