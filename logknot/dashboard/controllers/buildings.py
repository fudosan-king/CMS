from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm, PhotosForm, CATEGORY
from wagtail.images import get_image_model
from wagtail.core import hooks
from wagtail.admin import messages
from django.utils.translation import gettext as _  # noqa


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


@hooks.register('after_edit_page')
def show(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=False).first()
    if not building_detail:
        raise Http404

    template = loader.get_template('wagtailadmin/buildings/show.html')
    photos = get_image_model().objects.filter(building_id=building_id)

    forms = BuildingsForm(instance=building_detail)
    photos_form = PhotosForm(parent_document=building_detail)

    if request.method == 'POST':
        _id = request.POST.get('remove', None)
        if _id and str(building_detail.id) == _id and request.user:
            building_detail = building_detail.remove(request)
            if building_detail:
                building_detail.save()
                return redirect('buildings')
            return Http404

        forms = BuildingsForm(request.POST)
        if forms.is_valid():
            building_detail = building_detail.update(request)
            building_detail.save()
            messages.success(request, _('Updated'))
        else:
            messages.error(request, _('Errors'))

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms,
        'photos_form': photos_form,
        'category': CATEGORY
    }
    return HttpResponse(template.render(context, request))


@hooks.register('after_create_page')
def add(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name', None)
        if building_name:
            building = Buildings(building_name=building_name)
            building = building.add(request)
            if building:
                building.save()
                messages.success(request, '{}{}'.format(_('Created building: '), building.building_name))
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
