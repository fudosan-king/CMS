from django.http import HttpResponse
from django.template import loader
from dashboard.models import LogsImport
from django.http import Http404
from django.core.paginator import Paginator
from bson import ObjectId


def index(request):
    logs = LogsImport.objects().all().order_by('-id')
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 20))
    except:
        page = 1
        per_page = 20

    paginator_result = Paginator(logs, per_page)
    try:
        paginator = paginator_result.page(page)
    except:
        raise Http404

    index = (page - 1) * per_page
    limit = index + per_page
    logs = logs[index:limit]

    template = loader.get_template('wagtailadmin/import_logs/index.html')
    context = {
        'logs': logs,
        'paginator': paginator,
        'page': page,
        'limit': per_page,
    }
    return HttpResponse(template.render(context, request))


def show(request, log_id):
    try:
        log_id = ObjectId(log_id)
    except:
        raise Http404

    log = LogsImport.objects().filter(id=log_id).first()
    if not log:
        raise Http404

    total = len(log.import_done.keys()) + len(log.ignore_buildings.keys()) + len(log.import_fail)
    template = loader.get_template('wagtailadmin/import_logs/show.html')
    context = {
        'log': log,
        'total': total
    }
    return HttpResponse(template.render(context, request))
