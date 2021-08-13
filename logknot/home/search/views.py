from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.response import TemplateResponse
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from wagtail.core.models import Page
from wagtail.search.models import Query
from home.management.commands.locations import PREF_MAP
from home.management.commands.railroad import MAP_PREF_STATION


def search(request):
    q = Q(removed=False)
    if request.GET.get('building_name', None):
        q &= Q(building_name=request.GET.get('building_name', None))

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

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
        'pref': PREF_MAP,
        'map_pref': list(MAP_PREF_STATION.values())
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

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings
    }

    return TemplateResponse(request, 'search/result.html', context)


def result(request):
    q = Q(removed=False)
    if request.GET.get('building_name', None):
        q &= Q(building_name=request.GET.get('building_name', None))
    if request.GET.get('pref', []):
        q &= Q(address__pref=request.GET.get('pref'))
    if request.GET.getlist('city', []):
        q &= Q(address__city__in=request.GET.getlist('city'))
    if request.GET.getlist('station_name', []):
        q &= Q(transports__station_name__in=request.GET.getlist('station_name'))

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

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
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
