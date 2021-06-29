from django.urls import path
from wagtail.core import hooks
from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings, media_path
from mongoengine.queryset.visitor import Q
from django.shortcuts import redirect


def admin_show_buildings(request):
    q = Q(removed=False)
    building_name = request.GET.get('building_name', None)
    if building_name:
        q |= Q(building_name=building_name)

    buildings = Buildings.objects().filter(q)
    media = {}
    for building in buildings:
        media[building.id] = media_path(building.id)
    template = loader.get_template('wagtailadmin/buildings/index.html')
    context = {
        'buildings': buildings,
        'media': media
    }
    return HttpResponse(template.render(context, request))


def admin_building_detail(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=False).first()
    if not building_detail:
        return redirect('/dashboard/buildings/')
    if request.method == 'POST':
        if request.POST.get('delete', None):
            building_detail.removed = True
            building_detail.save()
            return redirect('/dashboard/buildings/')
        building_detail.building_name = request.POST.get('building_name', None)
        building_detail.save()
    media = media_path(building_detail.id)
    template = loader.get_template('wagtailadmin/buildings/building.html')
    context = {
        'action': '/dashboard/buildings/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'media': media
    }
    return HttpResponse(template.render(context, request))


def admin_building_add(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name', None)
        if building_name:
            building_add = Buildings(building_name=building_name)
            building_add.save()
            return redirect('building_detail', building_add.id)
    template = loader.get_template('wagtailadmin/buildings/building.html')
    context = {
        'action': '/dashboard/building/add/'
    }
    return HttpResponse(template.render(context, request))


@hooks.register('register_admin_urls')
def show_buildings():
    return [
        path('buildings/', admin_show_buildings, name='buildings'),
    ]


@hooks.register('register_admin_urls')
def building_detail():
    return [
        path('buildings/<building_id>/', admin_building_detail, name='building_detail'),
    ]


@hooks.register('register_admin_urls')
def building_add():
    return [
        path('building/add/', admin_building_add, name='building_add'),
    ]
