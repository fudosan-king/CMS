from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status


class LocationsViewSet(GenericViewSet):
    def locations(self, request):
        with open('data/locations.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            return JsonResponse(
                list(data.keys()),
                safe=False,
                json_dumps_params={'ensure_ascii': False},
                content_type='application/json',
                status=status.HTTP_200_OK
            )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    def locations_pref(self, request, pref):
        with open('data/locations.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data:
                return JsonResponse(
                    list(data[pref].keys()),
                    safe=False,
                    json_dumps_params={'ensure_ascii': False},
                    content_type='application/json',
                    status=status.HTTP_200_OK
                )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    def locations_city(self, request, pref, city):
        with open('data/locations.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data and city in data[pref]:
                return JsonResponse(
                    list(data[pref][city].keys()),
                    safe=False,
                    json_dumps_params={'ensure_ascii': False},
                    content_type='application/json',
                    status=status.HTTP_200_OK
                )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    def locations_ooaza(self, request, pref, city, ooaza):
        with open('data/locations.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data and city in data[pref] and ooaza in data[pref][city]:
                return JsonResponse(
                    data[pref][city][ooaza],
                    safe=False,
                    json_dumps_params={'ensure_ascii': False},
                    content_type='application/json',
                    status=status.HTTP_200_OK
                )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view({'get': 'locations'}), name='locations'),
            path('<pref>/', cls.as_view({'get': 'locations_pref'}), name='locations_pref'),
            path('<pref>/<city>/', cls.as_view({'get': 'locations_city'}), name='locations_city'),
            path('<pref>/<city>/<ooaza>/', cls.as_view({'get': 'locations_ooaza'}), name='locations_ooaza'),
        ]
