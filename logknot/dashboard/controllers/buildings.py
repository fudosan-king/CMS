from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm, PhotosForm
from wagtail.images import get_image_model


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
            building_detail = building_detail.remove(request)
            if building_detail:
                if building_detail.validate():
                    building_detail.save()
                return redirect('buildings')
            return Http404

        building_detail = building_detail.update(request)
        if building_detail and building_detail.validate():
            building_detail.save()

    template = loader.get_template('wagtailadmin/buildings/show.html')
    photos = get_image_model().objects.filter(building_id=building_id)

    forms = BuildingsForm(instance=building_detail)
    photos_form = PhotosForm(parent_document=building_detail)

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms,
        'photos_form': photos_form
    }
    return HttpResponse(template.render(context, request))


def add(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name', None)
        if building_name:
            building = Buildings(building_name=building_name)
            building = building.add(request)
            if building:
                building.save()
                return redirect('buildings_show', building.id)
        else:
            raise Http404

    forms = BuildingsForm()

    template = loader.get_template('wagtailadmin/buildings/show.html')
    context = {
        'action': '/dashboard/buildings/add/',
        'forms': forms
    }
    return HttpResponse(template.render(context, request))
