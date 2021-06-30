from django.urls import path
from wagtail.core import hooks
from dashboard.controllers import buildings, import_buildings


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
def buildings_removed():
    return [
        path('removed/', buildings.removed, name='buildings_removed'),
    ]


@hooks.register('register_admin_urls')
def buildings_removed_show():
    return [
        path('removed/edit/<building_id>/', buildings.removed_show, name='buildings_removed_show'),
    ]
