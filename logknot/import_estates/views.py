# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
# from wagtail.core.models import Estates


def import_estates(request):
    return TemplateResponse(request, 'import_estates.html', {
    })
