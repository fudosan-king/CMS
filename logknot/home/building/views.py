from django.template.response import TemplateResponse
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from bson import ObjectId


def index(request, building_id):
    try:
        building_id = ObjectId(building_id)
    except:
        return TemplateResponse(request, '404.html', {})

    q = Q(removed=False)
    q &= Q(id=building_id)

    building = Buildings.objects().filter(q).first()
    if not building:
        return TemplateResponse(request, '404.html', {})
    context = {
        'building': building,
    }

    return TemplateResponse(request, 'building/index.html', context)
