from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
from dashboard.models import Buildings
from mongoengine.queryset.visitor import Q
from django.urls import reverse
from bson import ObjectId
import json
from dashboard.views import railroad_to_fdk

# http://cms.localhost:5000/api/buildings/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E6%B8%AF%E5%8C%BA/%E9%BA%BB%E5%B8%83%E5%8F%B0/1%E4%B8%81%E7%9B%AE/
# http://cms.localhost:5000/api/buildings/new/61286244507f04c714bd4be1/


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

    def new_building(self, request, building_id):
        estate = {}
        with open('data/estate.json', 'r', encoding='utf8') as f:
            estate = eval(f.read())
        try:
            building = Buildings.objects().filter(id=ObjectId(building_id)).first()
            building = json.loads(building.to_json())
            for k, v in estate.items():
                if k in building:
                    estate[k] = building[k]
            estate['estate_name'] = building['building_name']
            estate['estate_name_kana'] = building['building_name_kana']
            estate['built_date'] = '{}-{:02d}-01T00:00:00'.format(
                building['built_date_year'], building['built_date_month'])
            transports = []
            for transport in building['transports']:
                data = {}
                data['bus_company'] = transport['bus_company']
                data['bus_mins'] = transport['bus_mins']
                data['bus_station'] = transport['bus_station']
                data['bus_walk_mins'] = transport['bus_walk_mins']
                data['car_distance'] = transport['car_distance']
                data['car_mins'] = transport['car_mins']
                data['station_name'] = transport['station_name']
                data['station_to'] = transport['station_to']
                data['transport_company'] = railroad_to_fdk(transport['transport_company'])
                data['walk_mins'] = transport['walk_mins']
                transports.append(data)
            estate['transports'] = transports
            estate['mansion_id'] = str(building['_id']['$oid'])
        except:
            print('Create new building id have problem: {} '.format(building_id))
        return JsonResponse(
            estate,
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
            path('new/<building_id>/', cls.as_view({'get': 'new_building'}), name='new_building'),
        ]
