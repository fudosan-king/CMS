from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from django.urls import reverse

# http://cms.localhost:5000/api/buildings/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E6%B8%AF%E5%8C%BA/%E9%BA%BB%E5%B8%83%E5%8F%B0/1%E4%B8%81%E7%9B%AE/


class BuildingsViewSet(GenericViewSet):
    def api_buildings(self, request, pref, city, ooaza, tyoume=''):
        q = Q(removed=False)
        if pref and city and ooaza:
            q &= Q(address__pref=pref)
            q &= Q(address__city=city)
            q &= Q(address__ooaza=ooaza)
        if tyoume:
            q &= Q(address__tyoume=tyoume)
        buildings = Buildings.objects().filter(q)
        data = []
        for building in buildings:
            bd = {}
            bd['building_id'] = str(building.id)
            bd['building_name'] = building.building_name
            bd['address'] = '{}{}{}{}{}'.format(
                pref, city, ooaza, building.address.get('tyoume', ''), building.address.get('hidden', ''))
            bd['link'] = reverse('buildings_show', args=(building.id,))
            data.append(bd)

        return JsonResponse(
            data,
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('<pref>/<city>/<ooaza>/', cls.as_view({'get': 'api_buildings'}), name='api_buildings'),
            path('<pref>/<city>/<ooaza>/<tyoume>/', cls.as_view({'get': 'api_buildings'}), name='api_buildings'),
        ]
