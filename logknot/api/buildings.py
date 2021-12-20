from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
from dashboard.models import Buildings, BuildingUpdated
from mongoengine.queryset.visitor import Q
from django.urls import reverse
from bson import ObjectId
import json
from dashboard.views import railroad_to_fdk

# http://cms.localhost:5000/api/buildings/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E6%B8%AF%E5%8C%BA/%E9%BA%BB%E5%B8%83%E5%8F%B0/1%E4%B8%81%E7%9B%AE/
# http://cms.localhost:5000/api/buildings/new/61286244507f04c714bd4be1/
# http://cms.localhost:5000/api/buildings/search/


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
        try:
            building = Buildings.objects().filter(id=ObjectId(building_id), removed=False).first()
            if building:
                with open('data/estate.json', 'r', encoding='utf8') as f:
                    estate = eval(f.read())

                building = json.loads(building.to_json())
                for k, v in estate.items():
                    if k in building:
                        estate[k] = building[k]
                estate['estate_name'] = building.get('building_name')
                estate['estate_name_kana'] = building.get('building_name_kana')
                estate['built_date'] = '{}-{:02d}-01 00:00:00'.format(
                    building.get('built_date_year'), building.get('built_date_month'))
                transports = []
                for transport in building['transports']:
                    data = {}
                    data['bus_company'] = transport.get('bus_company')
                    data['bus_mins'] = transport.get('bus_mins')
                    data['bus_station'] = transport.get('bus_station')
                    data['bus_walk_mins'] = transport.get('bus_walk_mins')
                    data['car_distance'] = transport.get('car_distance')
                    data['car_mins'] = transport.get('car_mins')
                    data['station_name'] = transport.get('station_name')
                    data['station_to'] = transport.get('station_to')
                    if transport.get('transport_company'):
                        data['transport_company'] = railroad_to_fdk(transport.get('transport_company'))
                    data['walk_mins'] = transport.get('walk_mins')
                    transports.append(data)
                if 'zipcode_1' in building and 'zipcode_2' in building:
                    estate['address']['zipcode'] = '{}-{}'.format(building.get('zipcode_1'), building.get('zipcode_2'))
                estate['transports'] = transports
                estate['mansion_id'] = str(building.get('_id').get('$oid'))

                land_rights = building.get('land_rights', '')
                lr = ''
                if land_rights:
                    if land_rights == '所有権':
                        lr = '所有権のみ'
                    else:
                        lr = '借地権のみ'
                estate['land_rights'] = lr
        except:
            print('Create new building id have problem: {} '.format(building_id))

        return JsonResponse(
            estate,
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

    def search_buildings(self, request):
        data = []
        if request.method == 'POST':
            q = Q(removed=False)
            address = request.data.get('address', None)
            building_name = request.data.get('building_name', None)
            mansion_id = request.data.get('mansion_id', None)
            if address:
                q &= Q(cache__address__icontains=address)
            if building_name:
                q &= Q(building_name__icontains=building_name)
            if mansion_id:
                q &= Q(id=ObjectId(mansion_id))
            try:
                buildings = Buildings.objects().filter(q).order_by('-created_at')[:10]
                if buildings:
                    for building in buildings:
                        bd = {}
                        bd['mansion_id'] = str(building.id)
                        bd['building_name'] = building.building_name
                        bd['address'] = '{}{}{}{}{}'.format(
                            building.address.get('pref', ''),
                            building.address.get('city', ''),
                            building.address.get('ooaza', ''),
                            building.address.get('tyoume', ''),
                            building.address.get('hidden', ''))
                        data.append(bd)
            except:
                data = []

        return JsonResponse(
            data,
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

    def update_building(self, request):
        building_update = BuildingUpdated.objects().filter(updated=False).first()
        data = []

        if building_update and building_update.building_id:
            data = building_update.building_id
            building_update.updated = True
            building_update.save()

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
            path('new/<building_id>/', cls.as_view({'get': 'new_building'}), name='new_building'),
            path('search/', cls.as_view({'post': 'search_buildings'}), name='search_buildings'),
            path('updated/', cls.as_view({'get': 'update_building'}), name='update_building'),
        ]
