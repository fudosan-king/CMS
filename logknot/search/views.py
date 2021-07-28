from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q


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

    paginator_result = Paginator(buildings, per_page)
    try:
        paginator = paginator_result.page(page)
    except:
        return TemplateResponse(request, '404.html', {})

    index = (page - 1) * per_page
    limit = index + per_page
    buildings = buildings[index:limit]

    context = {
        'paginator': paginator,
        'page': page,
        'limit': per_page,
        'buildings': buildings,
    }

    return TemplateResponse(request, 'search/search.html', context)
