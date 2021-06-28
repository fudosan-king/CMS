from django.urls import path
from wagtail.core import hooks
from django.http import HttpResponse


def admin_view(request):
    return HttpResponse(
        'Import buildings',
        content_type='text/plain')


@hooks.register('register_admin_urls')
def import_estate():
    return [
        path('import/', admin_view, name='import'),
    ]
