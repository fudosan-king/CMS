from dashboard.models import Buildings, CountInfoBuildings, BuildingUpdated
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator
from dashboard.forms.buildings import BuildingsForm, PhotosForm, CATEGORY
from wagtail.images import get_image_model
from wagtail.admin import messages
from django.utils.translation import gettext as _  # noqa
from home.management.commands.locations import PREF_MAP
from home.management.commands.railroad import MAP_REGION
from django.template.response import TemplateResponse
from django.conf import settings
from dashboard.views import fetch_url_to_json
from content.models import ContentDetailPage, ContentPage
from dashboard.views import MenuBuildingItem
from dashboard.forms.features import features


def index(request):
    if not MenuBuildingItem.is_shown(MenuBuildingItem, request):
        raise Http404
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
    if not MenuBuildingItem.is_shown(MenuBuildingItem, request):
        raise Http404
    building_detail = Buildings.objects(id=building_id, removed=False).first()
    if not building_detail:
        raise Http404

    city = building_detail.address.get('city')
    station = []
    for transport in building_detail.transports:
        if transport.transport_company and transport.transport_company not in station:
            station.append([transport.map_pref, transport.transport_company])

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
                    update_count(building_detail, removed=True, city=city, station=station)
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
                        update_count(building_detail, city=city, station=station)
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
    try:
        page_content = ContentDetailPage.objects.get(building_id=building_id)
    except:
        page_content = ContentPage.objects.filter(id=4).first()

    context = {
        'action': '/dashboard/buildings/edit/{}/'.format(building_detail.id),
        'building_detail': building_detail,
        'photos': photos,
        'forms': forms,
        'photos_form': photos_form,
        'category': CATEGORY,
        'errors': errors,
        'pref': PREF_MAP,
        'map_pref': list(MAP_REGION.keys()),
        'pref_default': MAP_REGION['関東'],
        'total_room': total_room,
        'active_room': active_room,
        'rooms': data.get('esstates'),
        'page_content': page_content,
        'features': features
    }

    return TemplateResponse(request, 'wagtailadmin/buildings/show.html', context)


def add(request):
    forms = BuildingsForm()
    errors = []
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
                        messages.success(request, '{}{}'.format(_('Created building: '), building.building_name))
                        return redirect('buildings_show', building.id)
                    except:
                        messages.error(request, 'Have problem')
                        forms = BuildingsForm(request.POST)
                        errors = forms.errors.items()
            else:
                messages.error(request, '{}: ({})'.format('物件名', _('required')))
                return redirect('buildings_add')
        else:
            messages.error(request, _('Sorry, you do not have permission to access this area.'))

    context = {
        'action': '/dashboard/buildings/add/',
        'forms': forms,
        'pref': PREF_MAP,
        'map_pref': list(MAP_REGION.keys()),
        'pref_default': MAP_REGION['関東'],
        'features': features,
        'errors': errors
    }

    return TemplateResponse(request, 'wagtailadmin/buildings/show.html', context)


def update_count(building, removed=False, city=None, station=[]):
    building_update = BuildingUpdated.objects().filter(updated=False).first()
    if not building_update:
        building_update = BuildingUpdated()
    if building_update and str(building.id) not in building_update.building_id:
        building_update.building_id.append(str(building.id))
        building_update.save()

    count_info = CountInfoBuildings.objects().first()

    if not count_info:
        count_info = CountInfoBuildings()

    city_dict = count_info.city
    station_dict = count_info.station

    city_in = building.address.get('city')

    transport_company_in = []
    for transport in building.transports:
        if transport.transport_company and transport.transport_company not in transport_company_in:
            transport_company_in.append([transport.map_pref, transport.transport_company])

    if city and city in city_dict and city_dict[city] > 0:
        city_dict[city] = city_dict[city] - 1

    if station:
        for st in station:
            if st[0] and st[1]:
                name_station = '{}-{}'.format(st[0], st[1])
                if name_station in station_dict and station_dict[name_station] > 0:
                    station_dict[name_station] = station_dict[name_station] - 1

    if not removed:
        if city_in not in city_dict:
            city_dict[city_in] = 1
        else:
            city_dict[city_in] = city_dict[city_in] + 1

        for sn in transport_company_in:
            if sn[0] and sn[1]:
                name_station = '{}-{}'.format(sn[0], sn[1])
                if name_station not in station_dict:
                    station_dict[name_station] = 1
                else:
                    station_dict[name_station] = station_dict[name_station] + 1

    count_info.city = city_dict
    count_info.station = station_dict
    count_info.save()
