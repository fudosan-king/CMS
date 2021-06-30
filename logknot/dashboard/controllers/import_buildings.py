from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings
from django.http import Http404


def index(request):
    if request.method == 'POST':
        method = 'Insert buildings'
        buildings = Buildings(building_name='Building 1')
        buildings.save()
    elif request.method == 'GET':
        method = 'Form insert buildings'
    else:
        raise Http404

    template = loader.get_template('wagtailadmin/import_buildings/index.html')
    context = {
        'method': method
    }
    return HttpResponse(template.render(context, request))
