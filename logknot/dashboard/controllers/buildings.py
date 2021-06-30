from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings, media_path
from mongoengine.queryset.visitor import Q
from django.shortcuts import redirect
from django.http import Http404
import datetime


def index(request):
    q = Q(removed=False)
    building_name = request.GET.get('building_name', None)
    if building_name:
        q &= Q(building_name=building_name)
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


def show(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=False).first()
    if not building_detail:
        raise Http404

    if request.method == 'POST':
        _id = request.POST.get('remove', None)
        if _id and str(building_detail.id) == _id:
            building_detail.removed = True
            building_detail.last_time_remove = datetime.datetime.now
            building_detail.remove_by = str(request.user)
            building_detail.save()
            return redirect('buildings')
        building_detail.building_name = request.POST.get('building_name', None)
        building_detail.last_time_update = datetime.datetime.now
        building_detail.update_by = str(request.user)
        building_detail.save()

    media = media_path(building_detail.id)
    template = loader.get_template('wagtailadmin/buildings/show.html')

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'media': media
    }
    return HttpResponse(template.render(context, request))


def add(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name', None)
        if building_name:
            building_add = Buildings(building_name=building_name)
            building_add.create_by = str(request.user)
            building_add.save()
            return redirect('buildings_show', building_add.id)
        raise Http404

    template = loader.get_template('wagtailadmin/buildings/show.html')
    context = {
        'action': '/dashboard/buildings/add/'
    }
    return HttpResponse(template.render(context, request))


def removed(request):
    q = Q(removed=True)
    building_name = request.GET.get('building_name', None)
    if building_name:
        q &= Q(building_name=building_name)
    buildings = Buildings.objects().filter(q)

    media = {}
    for building in buildings:
        media[building.id] = media_path(building.id)
    template = loader.get_template('wagtailadmin/buildings/buildings_removed.html')

    context = {
        'buildings': buildings,
        'media': media
    }
    return HttpResponse(template.render(context, request))


def removed_show(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=True).first()
    if not building_detail:
        raise Http404

    if request.method == 'POST':
        if request.POST.get('rollback', None):
            building_detail.removed = False
            building_detail.last_time_rollback = datetime.datetime.now
            building_detail.rollback_by = str(request.user)
            building_detail.save()
            return redirect('buildings')

    media = media_path(building_detail.id)
    template = loader.get_template('wagtailadmin/buildings/removed_detail.html')

    context = {
        'action': '/dashboard/removed/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'media': media
    }
    return HttpResponse(template.render(context, request))
