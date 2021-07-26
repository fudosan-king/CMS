from django.contrib.auth.models import Permission
from wagtail.core import hooks
from django.urls import path, reverse
from dashboard.controllers import buildings, import_buildings, removed, import_logs
from wagtail.admin.menu import MenuItem
from django.utils.translation import gettext as _  # noqa


@hooks.register('register_permissions')
def register_building_permissions():
    return Permission.objects.filter(
        content_type__app_label='buildinggroup',
        codename__in=['add_building', 'change_building', 'delete_building']
    )


@hooks.register('register_admin_menu_item')
def register_building_menu_item():
    return MenuItem(_('Buildings'), reverse('buildings'), icon_name='view', order=2)


@hooks.register('register_permissions')
def register_removed_permissions():
    return Permission.objects.filter(
        content_type__app_label='removedgroup',
        codename__in=['add_removed', 'change_removed', 'delete_removed']
    )


@hooks.register('register_admin_menu_item')
def register_removed_menu_item():
    return MenuItem(_('Removed'), reverse('buildings_removed'), icon_name='cross', order=3)


@hooks.register('register_permissions')
def register_import_permissions():
    return Permission.objects.filter(
        content_type__app_label='importgroup',
        codename__in=['add_import', 'change_import', 'delete_import']
    )


@hooks.register('register_admin_menu_item')
def register_import_menu_item():
    return MenuItem(_('Import'), reverse('buildings_import'), icon_name='download', order=4)


@hooks.register('register_reports_menu_item')
def register_report_import_menu_item():
    return MenuItem(_('Import Logs'), reverse('import_logs'), icon_name='list-ul', order=5)


@hooks.register('register_admin_urls')
def buildings_index():
    return [
        path('buildings/', buildings.index, name='buildings'),
    ]


@hooks.register('register_admin_urls')
def buildings_add():
    return [
        path('buildings/add/', buildings.add, name='buildings_add'),
    ]


@hooks.register('register_admin_urls')
def buildings_show():
    return [
        path('buildings/edit/<building_id>/', buildings.show, name='buildings_show'),
    ]


@hooks.register('register_admin_urls')
def buildings_import():
    return [
        path('import/', import_buildings.index, name='buildings_import'),
    ]


@hooks.register('register_admin_urls')
def buildings_import_logs():
    return [
        path('reports/logs/', import_logs.index, name='import_logs'),
    ]


@hooks.register('register_admin_urls')
def buildings_import_logs_id():
    return [
        path('import/logs/<log_id>/', import_logs.show, name='import_logs_id'),
    ]


@hooks.register('register_admin_urls')
def buildings_removed():
    return [
        path('removed/', removed.index, name='buildings_removed'),
    ]


@hooks.register('register_admin_urls')
def buildings_removed_show():
    return [
        path('removed/edit/<building_id>/', removed.show, name='buildings_removed_show'),
    ]
