from django.utils.translation import gettext as _  # noqa
from django.template.response import TemplateResponse
from home.management.commands.locations import PREF_MAP
from home.management.commands.railroad import MAP_PREF_STATION
from django.http import Http404
from dashboard.models import SearchSortByPref
from dashboard.views import MenuSearchItem
from wagtail.admin import messages


def index(request):
    if not MenuSearchItem.is_shown(MenuSearchItem, request):
        raise Http404
    context = {
        'pref': PREF_MAP,
        'map_pref': list(MAP_PREF_STATION.values()),
    }
    return TemplateResponse(request, 'wagtailadmin/search_sort/index.html', context)


def show(request, pref, kind):
    if not MenuSearchItem.is_shown(MenuSearchItem, request):
        raise Http404
    search_sort = SearchSortByPref.objects.filter(pref=pref).first()
    if not search_sort:
        search_sort = SearchSortByPref(pref=pref)
        search_sort.save()

    if request.POST:
        user = request.user
        if user and user.has_perms(['searchgroup.change_search']):
            if kind == 'city':
                city = request.POST.getlist('city')
                city = list(dict.fromkeys(city))
                search_sort.city = city
            if kind == 'station':
                station = request.POST.getlist('station')
                station = list(dict.fromkeys(station))
                search_sort.station_name = station
            search_sort.save()
        else:
            messages.error(request, _('Sorry, you do not have permission to access this area.'))

    city = None
    station = None
    context = {}
    if kind == 'city':
        with open('data/locations.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref in data:
                city = list(data[pref].keys())
    elif kind == 'station':
        with open('data/railroad.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref in data:
                station = list(data[pref].keys())
    else:
        raise Http404

    context['city'] = city
    context['station'] = station
    context['search_sort'] = search_sort
    context['kind'] = kind
    context['pref'] = pref
    return TemplateResponse(request, 'wagtailadmin/search_sort/show.html', context)
