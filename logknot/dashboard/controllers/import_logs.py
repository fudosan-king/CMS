from dashboard.models import LogsImport
from django.http import Http404
from django.core.paginator import Paginator
from bson import ObjectId
from django.template.response import TemplateResponse


def index(request):
    logs = LogsImport.objects().all().order_by('-id')
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('limit', 20))
    except:
        page = 1
        per_page = 20

    if logs:
        paginator_result = Paginator(logs, per_page)
        try:
            paginator = paginator_result.page(page)
        except:
            raise Http404
    else:
        paginator = None

    index = (page - 1) * per_page
    limit = index + per_page
    logs = logs[index:limit]

    context = {
        'logs': logs,
        'paginator': paginator,
        'page': page,
        'limit': per_page,
    }

    return TemplateResponse(request, 'wagtailadmin/import_logs/index.html', context)


def show(request, log_id):
    try:
        log_id = ObjectId(log_id)
    except:
        raise Http404

    log = LogsImport.objects().filter(id=log_id).first()
    if not log:
        raise Http404

    total = len(log.import_done.keys()) + len(log.ignore_buildings.keys()) + len(log.import_fail)
    context = {
        'log': log,
        'total': total
    }

    return TemplateResponse(request, 'wagtailadmin/import_logs/show.html', context)
