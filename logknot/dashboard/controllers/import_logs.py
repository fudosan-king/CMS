from django.http import HttpResponse
from django.template import loader
from dashboard.models import Buildings
from dashboard.forms.removed import RemovedBuildingsForm
from django.shortcuts import redirect
from django.http import Http404
import datetime
from django.core.paginator import Paginator


def index(request):
    template = loader.get_template('wagtailadmin/import_logs/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def show(request, log_id):
    template = loader.get_template('wagtailadmin/import_logs/show.html')
    context = {
    }
    return HttpResponse(template.render(context, request))
