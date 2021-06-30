from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings, PhotosBuildings
from django.shortcuts import redirect
from django.http import Http404
import datetime
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm


def index(request):
    query = Buildings().query(request, False)
    buildings = Buildings.objects().filter(query)

    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 10))
    except:
        page = 1
        per_page = 10

    paginator_result = Paginator(buildings, per_page)
    try:
        paginator = paginator_result.page(page)
    except:
        raise Http404

    index = (page - 1) * per_page
    limit = index + per_page
    buildings = buildings[index:limit]

    context = {
        'paginator': paginator,
        'page': page,
        'limit': limit,
        'buildings': buildings,
    }
    template = loader.get_template('wagtailadmin/buildings/index.html')
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

    template = loader.get_template('wagtailadmin/buildings/show.html')
    photos = []
    if 'photos' in building_detail:
        for p in building_detail.photos:
            photos.append(PhotosBuildings().media_path(p.id))

    forms = BuildingsForm(instance=building_detail)

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms
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

    forms = BuildingsForm()

    template = loader.get_template('wagtailadmin/buildings/show.html')
    context = {
        'action': '/dashboard/buildings/add/',
        'forms': forms
    }
    return HttpResponse(template.render(context, request))
