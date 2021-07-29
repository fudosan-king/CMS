from dashboard.models import Buildings
from dashboard.forms.removed import RemovedBuildingsForm
from django.shortcuts import redirect
from django.http import Http404
import datetime
from django.core.paginator import Paginator
from wagtail.admin import messages
from django.utils.translation import gettext as _  # noqa
from django.template.response import TemplateResponse


def index(request):
    query = Buildings().query(request, True)
    buildings = Buildings.objects().filter(query)

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
        'limit': limit,
        'buildings': buildings
    }

    return TemplateResponse(request, 'wagtailadmin/removed/index.html', context)


def show(request, building_id):
    building_removed = Buildings.objects(id=building_id, removed=True).first()
    if not building_removed:
        raise Http404

    if request.method == 'POST':
        user = request.user
        rollback = request.POST.get('rollback', None)
        if user and user.has_perms(['removedgroup.change_removed']) and rollback:
            building_removed.removed = False
            building_removed.last_time_rollback = datetime.datetime.now
            building_removed.rollback_by = str(request.user)
            building_removed.save()
            return redirect('buildings_removed')
        else:
            messages.error(request, _('Sorry, you do not have permission to access this area.'))

    forms = RemovedBuildingsForm(instance=building_removed)
    context = {
        'action': '/dashboard/removed/{}/'.format(building_removed.id),
        'building_removed': building_removed,
        'forms': forms
    }

    return TemplateResponse(request, 'wagtailadmin/removed/show.html', context)
