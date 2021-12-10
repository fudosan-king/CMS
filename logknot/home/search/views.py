from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from wagtail.core.models import Page
from wagtail.search.models import Query
from home.management.commands.locations import PREF_MAP
from home.management.commands.railroad import MAP_REGION
from dashboard.models import CountInfoBuildings
from dashboard.models import SearchSortByPref
from django.conf import settings
import urllib3
import json

http = urllib3.PoolManager()


def search(request):
    q = Q(removed=False)
    if request.GET.get('building_name', None):
        q &= Q(building_name=request.GET.get('building_name', None))

    active = 'area'
    if request.GET.get('station', None):
        active = 'station'

    buildings = Buildings.objects().filter(q).order_by('-id')

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
            return TemplateResponse(request, '404.html', {})
    else:
        paginator = None

    index = (page - 1) * per_page
    limit = index + per_page
    buildings = buildings[index:limit]

    city_tokyo = []
    pref = '東京都'
    search_sort = SearchSortByPref.objects.filter(pref=pref).first()
    with open('data/locations.json', 'r', encoding='utf8') as f:
        data = eval(f.read())
        if pref and pref in data:
            city_all = list(data[pref].keys())
            if search_sort:
                city_tokyo = search_sort.city
            for ct in city_all:
                if ct not in city_tokyo:
                    city_tokyo.append(ct)

    transport_company_tokyo = []
    with open('data/railroad.json', 'r', encoding='utf8') as f:
        data = eval(f.read())
        if pref and pref in data:
            transport_company_all = list(data[pref].keys())
            if search_sort:
                transport_company_tokyo = search_sort.transport_company
            for st in transport_company_all:
                if st not in transport_company_tokyo:
                    transport_company_tokyo.append(st)

    count_info = CountInfoBuildings.objects().first()
    city_dict = count_info.city
    transport_company_dict = count_info.transport_company
    station_dict = count_info.station

    city_count_tokyo = {}
    for city in city_tokyo:
        if city_dict.get(city):
            city_count_tokyo[city] = city_dict.get(city)

    transport_company_count_tokyo = {}
    for transport in transport_company_tokyo:
        if transport_company_dict.get('{}-{}'.format(pref, transport)):
            transport_company_count_tokyo[transport] = transport_company_dict.get('{}-{}'.format(pref, transport))

    station = {}
    for k, v in transport_company_count_tokyo.items():
        with open('data/railroad.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data and k in data[pref]:
                line = data[pref][k]
                count_station = {}
                for li in line:
                    if li and station_dict.get('{}-{}'.format(pref, li)):
                        count_station[li] = station_dict.get('{}-{}'.format(pref, li))
                station[k] = count_station

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
        'pref': PREF_MAP,
        'map_pref': list(MAP_REGION.keys()),
        'city': city_count_tokyo,
        'station': station,
        'active': active
    }

    return TemplateResponse(request, 'search/search.html', context)


def search_all(request):
    q = Q(removed=False)
    buildings = Buildings.objects().filter(q).order_by('-created_at')

    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 40))
    except:
        page = 1
        per_page = 20
    if buildings:
        paginator_result = Paginator(buildings, per_page)
        try:
            paginator = paginator_result.page(page)
        except:
            return TemplateResponse(request, '404.html', {})
    else:
        paginator = None

    index = (page - 1) * per_page
    limit = index + per_page
    buildings = buildings[index:limit]

    building_estates = {}

    for building in buildings:
        estates = get_estate(building.id)
        building_estates[building.id] = estates

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
        'building_estates': building_estates
    }

    return TemplateResponse(request, 'search/result.html', context)


def result(request):
    q = Q(removed=False)
    if request.GET.get('building_name', None):
        q &= Q(building_name=request.GET.get('building_name', None))
    if request.GET.get('pref', []):
        q &= Q(address__pref=request.GET.get('pref'))
    if request.GET.getlist('area', []):
        q &= Q(address__city__in=request.GET.getlist('area'))
    if request.GET.getlist('transport_company', []):
        q &= Q(transports__transport_company__in=request.GET.getlist('transport_company'))
    if request.GET.getlist('station', []):
        q &= Q(transports__station_name__in=request.GET.getlist('station'))

    buildings = Buildings.objects().filter(q).order_by('-created_at')

    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 40))
    except:
        page = 1
        per_page = 20

    if buildings:
        paginator_result = Paginator(buildings, per_page)
        try:
            paginator = paginator_result.page(page)
        except:
            return TemplateResponse(request, '404.html', {})
    else:
        paginator = None

    index = (page - 1) * per_page
    limit = index + per_page
    buildings = buildings[index:limit]

    building_estates = {}

    for building in buildings:
        estates = get_estate(building.id)
        building_estates[building.id] = estates

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
        'building_estates': building_estates
    }
    return TemplateResponse(request, 'search/result.html', context)


def page(request):
    """Search page live"""
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Search
    if search_query:
        search_results = Page.objects.live().search(search_query)
        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(request, 'page/search.html', {
        'search_query': search_query,
        'search_results': search_results,
        'paginator': paginator
    })


def get_estate(building_id):
    if settings.BUILDING_ID:
        building_id = settings.BUILDING_ID

    url = '{}/api/{}/list?token={}&building_id={}'.format(
        settings.FDK_URL,
        settings.COMPANY_ID_FDK,
        settings.TOKEN_FDK,
        building_id
    )
    estates = http.request('GET', url)
    estates = json.loads(estates.data)

    if 'estates' in estates:
        return estates['estates']
    return []
