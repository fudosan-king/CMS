from django.contrib.auth.models import Permission
from wagtail.core import hooks
from django.urls import path, reverse  # noqa
from dashboard.controllers import buildings, import_buildings, removed, import_logs, search_sort, admin_3d
from django.utils.translation import gettext as _  # noqa
from dashboard.views import (  # noqa
    MenuBuildingItem, MenuRemovedItem, MenuImportItem, MenuLogsItem,
    MenuSearchItem
)


@hooks.register('register_permissions')
def register_building_permissions():
    return Permission.objects.filter(
        content_type__app_label='buildinggroup',
        codename__in=['add_building', 'change_building', 'delete_building']
    )


@hooks.register('register_permissions')
def register_removed_permissions():
    return Permission.objects.filter(
        content_type__app_label='removedgroup',
        codename__in=['change_removed']
    )


@hooks.register('register_permissions')
def register_import_permissions():
    return Permission.objects.filter(
        content_type__app_label='importgroup',
        codename__in=['add_import']
    )


@hooks.register('register_permissions')
def register_logs_permissions():
    return Permission.objects.filter(
        content_type__app_label='logsgroup',
        codename__in=['change_logs']
    )


@hooks.register('register_permissions')
def register_search_permissions():
    return Permission.objects.filter(
        content_type__app_label='searchgroup',
        codename__in=['change_search']
    )


@hooks.register('register_admin_menu_item')
def register_building_menu_item():
    return MenuBuildingItem(_('Buildings'), reverse('buildings'), icon_name='view', order=2)


@hooks.register('register_admin_menu_item')
def register_removed_menu_item():
    return MenuRemovedItem(_('Remove'), reverse('buildings_removed'), icon_name='cross', order=3)


@hooks.register('register_admin_menu_item')
def register_import_menu_item():
    return MenuImportItem(_('Import'), reverse('buildings_import'), icon_name='download', order=4)


@hooks.register('register_reports_menu_item')
def register_report_import_menu_item():
    return MenuLogsItem(_('Import logs'), reverse('import_logs'), icon_name='list-ul', order=5)


@hooks.register('register_admin_menu_item')
def register_search_sort_menu_item():
    return MenuSearchItem(_('Sort Search'), reverse('search_sort'), icon_name='search', order=6)


@hooks.register('register_admin_menu_item')
def register_3d_menu_item():
    return MenuBuildingItem(_('3D Models'), reverse('3d'), icon_name='code', order=7)


@hooks.register('register_admin_urls')
def admin_3d_index():
    return [
        path('3d/', admin_3d.index, name='3d'),
    ]


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


@hooks.register('register_admin_urls')
def search_sort_index():
    return [
        path('search_sort/', search_sort.index, name='search_sort'),
    ]


@hooks.register('register_admin_urls')
def search_sort_show():
    return [
        path('search_sort/<pref>/<kind>/', search_sort.show, name='search_sort_show'),
    ]
