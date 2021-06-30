from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings
from django.shortcuts import redirect
from django.http import Http404
import datetime
from django.core.paginator import Paginator


def index(request):
    query = Buildings().query(request, True)
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

    template = loader.get_template('wagtailadmin/removed/index.html')

    context = {
        'paginator': paginator,
        'page': page,
        'limit': limit,
        'buildings': buildings
    }
    return HttpResponse(template.render(context, request))


def show(request, building_id):
    building_detail = Buildings.objects(id=building_id, removed=True).first()
    if not building_detail:
        raise Http404

    if request.method == 'POST':
        if request.POST.get('rollback', None):
            building_detail.removed = False
            building_detail.last_time_rollback = datetime.datetime.now
            building_detail.rollback_by = str(request.user)
            building_detail.save()
            return redirect('buildings_removed')

    template = loader.get_template('wagtailadmin/removed/show.html')

    context = {
        'action': '/dashboard/removed/{}/'.format(building_detail.id),
        'building_detail': building_detail
    }
    return HttpResponse(template.render(context, request))
