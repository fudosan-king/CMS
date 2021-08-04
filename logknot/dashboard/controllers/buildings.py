from dashboard.models import Buildings, CountInfoBuildings
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm, PhotosForm, CATEGORY
from wagtail.images import get_image_model
from wagtail.admin import messages
from django.utils.translation import gettext as _  # noqa
from home.management.commands.locations import PREF_MAP
from django.template.response import TemplateResponse
from django.conf import settings
from dashboard.views import fetch_url_to_json


def index(request):
    query = Buildings().query(request, False)
    buildings = Buildings.objects().filter(query).order_by('-id')

    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 20))
    except:
        page = 1
        per_page = 20

    if buildings:
        paginator_result = Paginator(buildings, per_page)
        try:
            paginator = paginator_result.page(page)
        except:
            raise Http404
    else:
        paginator = None

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

    city = building_detail.address.get('city')
    pref = building_detail.address.get('pref')
    station = []
    for transport in building_detail.transports:
        if transport.station_name and transport.station_name not in station:
            station.append(transport.station_name)

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
                    update_count(building_detail, removed=True, pref=pref, city=city, station=station)
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
                        update_count(building_detail, pref=pref, city=city, station=station)
                        messages.success(request, _('Updated'))
                    except Exception as e:
                        print('Update building error: {}'.format(e))
                        errors = forms.errors.items()
                        forms = BuildingsForm(instance=building_detail)
                        messages.error(request, _('Error'))
                else:
                    errors = forms.errors.items()
                    messages.error(request, _('Error'))
            else:
                messages.error(request, _('Sorry, you do not have permission to access this area.'))

    data = fetch_url_to_json(settings.API_DATA_FDK)
    total_room = 0
    active_room = 2
    if data and 'esstates' in data:
        total_room = len(data.get('esstates'))

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms,
        'photos_form': photos_form,
        'category': CATEGORY,
        'errors': errors,
        'pref': PREF_MAP,
        'total_room': total_room,
        'active_room': active_room,
        'rooms': data.get('esstates')
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
                        update_count(building)
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


def update_count(building, removed=False, pref=None, city=None, station=[]):
    count_info = CountInfoBuildings.objects().first()

    if not count_info:
        count_info = CountInfoBuildings()

    city_dict = count_info.city
    station_dict = count_info.station

    city_in = building.address.get('city')
    pref_in = building.address.get('pref')

    station_name_in = []
    for transport in building.transports:
        if transport.station_name and transport.station_name not in station_name_in:
            station_name_in.append(transport.station_name)

    if city and city in city_dict and city_dict[city] > 0:
        city_dict[city] = city_dict[city] - 1

    if pref and station:
        for st in station:
            name_station = '{}-{}'.format(pref, st)
            if name_station in station_dict and station_dict[name_station] > 0:
                station_dict[name_station] = station_dict[name_station] - 1

    if not removed:
        if city_in not in city_dict:
            city_dict[city_in] = 1
        else:
            city_dict[city_in] = city_dict[city_in] + 1

        for sn in station_name_in:
            name_station = '{}-{}'.format(pref_in, sn)
            if name_station not in station_dict:
                station_dict[name_station] = 1
            else:
                station_dict[name_station] = station_dict[name_station] + 1

    count_info.city = city_dict
    count_info.station = station_dict
    count_info.save()
