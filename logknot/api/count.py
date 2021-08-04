from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
from dashboard.models import CountInfoBuildings


class CountViewSet(GenericViewSet):
    def count_city(self, request, city):
        count_info = CountInfoBuildings.objects().first()
        city_dict = count_info.city
        return JsonResponse(
            [city, city_dict.get(city)],
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

    def count_station(self, request, station):
        count_info = CountInfoBuildings.objects().first()
        station_dict = count_info.station
        return JsonResponse(
            [station, station_dict.get(station)],
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('city/<city>/', cls.as_view({'get': 'count_city'}), name='count_city'),
            path('station/<station>/', cls.as_view({'get': 'count_station'}), name='count_station'),
        ]
