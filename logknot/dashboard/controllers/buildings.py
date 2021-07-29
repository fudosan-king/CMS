from dashboard.models import Buildings
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm, PhotosForm, CATEGORY
from wagtail.images import get_image_model
from wagtail.admin import messages
from django.utils.translation import gettext as _  # noqa
from home.management.commands.locations import PREF_MAP
from django.template.response import TemplateResponse


def index(request):
    query = Buildings().query(request, False)
    buildings = Buildings.objects().filter(query).order_by('-id')

    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 20))
    except:
        page = 1
        per_page = 20

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
        'limit': per_page,
        'buildings': buildings,
    }

    return TemplateResponse(request, 'wagtailadmin/buildings/index.html', context)


def show(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=False).first()
    if not building_detail:
        raise Http404

    photos = get_image_model().objects.filter(building_id=building_id)

    forms = BuildingsForm(instance=building_detail)
    photos_form = PhotosForm(parent_document=building_detail)
    errors = []
    if request.method == 'POST':
        user = request.user
        _id = request.POST.get('remove', None)

        if _id and str(building_detail.id) == _id:
            if user and user.has_perms(['buildinggroup.delete_building']):
                building_detail = building_detail.remove(request)
                if building_detail:
                    building_detail.save()
                    return redirect('buildings')
                return Http404
            else:
                messages.error(request, _('Sorry, you do not have permission to access this area.'))
        else:
            if user and user.has_perms(['buildinggroup.change_building']):
                forms = BuildingsForm(request.POST)

                if forms.is_valid():
                    building_detail = building_detail.update(request)
                    try:
                        building_detail.save()
                        messages.success(request, _('Updated'))

                    except:
                        errors = forms.errors.items()
                        forms = BuildingsForm(instance=building_detail)
                        messages.error(request, _('Error'))
                else:
                    errors = forms.errors.items()
                    messages.error(request, _('Error'))
            else:
                messages.error(request, _('Sorry, you do not have permission to access this area.'))

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms,
        'photos_form': photos_form,
        'category': CATEGORY,
        'errors': errors,
        'pref': PREF_MAP
    }

    return TemplateResponse(request, 'wagtailadmin/buildings/show.html', context)


def add(request):
    if request.method == 'POST':
        user = request.user
        if user and user.has_perms(['buildinggroup.add_building']):
            building_name = request.POST.get('building_name', None)
            if building_name:
                building = Buildings(building_name=building_name)
                building = building.add(request)
                if building:
                    try:
                        building.save()
                    except:
                        messages.error(request, 'Have problem')
                    messages.success(request, '{}{}'.format(_('Created building: '), building.building_name))
                    return redirect('buildings_show', building.id)
            else:
                raise Http404
        else:
            messages.error(request, _('Sorry, you do not have permission to access this area.'))

    forms = BuildingsForm()
    context = {
        'action': '/dashboard/buildings/add/',
        'forms': forms,
        'pref': PREF_MAP
    }

    return TemplateResponse(request, 'wagtailadmin/buildings/show.html', context)
