from django.utils.translation import gettext as _  # noqa
from django.template.response import TemplateResponse


def index(request):
    context = {}

    return TemplateResponse(request, 'wagtailadmin/3d/index.html', context)
