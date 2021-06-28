from django.urls import path
from wagtail.core import hooks
from django.http import HttpResponse
from django.template import loader


def admin_view(request):
    template = loader.get_template('wagtailadmin/import_buildings/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


@hooks.register('register_admin_urls')
def import_estate():
    return [
        path('import/', admin_view, name='import'),
    ]
