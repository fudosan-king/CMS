from django.urls import path
from wagtail.core import hooks
from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings


def admin_import_buildings(request):
    if request.method == 'POST':
        method = 'Insert buildings'
        buildings = Buildings(building_name='Building 1')
        buildings.save()
    elif request.method == 'GET':
        method = 'Form insert buildings'
    else:
        return HttpResponse(status=404)

    template = loader.get_template('wagtailadmin/import_buildings/index.html')
    context = {
        'method': method
    }
    return HttpResponse(template.render(context, request))


@hooks.register('register_admin_urls')
def import_buildings():
    return [
        path('import/', admin_import_buildings, name='import'),
    ]
