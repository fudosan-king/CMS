from django.template.response import TemplateResponse
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from bson import ObjectId
from content.models import ContentDetailPage
import urllib3
import json
from django.conf import settings


http = urllib3.PoolManager()


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

    try:
        page_content = ContentDetailPage.objects.get(building_id=building_id)
    except:
        page_content = None

    if settings.BUILDING_ID:
        building_id = settings.BUILDING_ID

    url = '{}/api/{}/list?token={}&building_id={}'.format(
        settings.FDK_URL,
        settings.COMPANY_ID_FDK,
        settings.TOKEN_FDK,
        building_id
    )
    estates = http.request('GET', url)
    estates = json.loads(estates.data)

    context = {
        'building': building,
        'page_content': page_content,
        'estates': estates
    }

    return TemplateResponse(request, 'building/index.html', context)
