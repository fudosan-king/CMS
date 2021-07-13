from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status


class RailRoadViewSet(GenericViewSet):
    def railroad(self, request):
        with open('data/railroad.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            return JsonResponse(
                list(data.keys()),
                safe=False,
                json_dumps_params={'ensure_ascii': False},
                content_type='application/json',
                status=status.HTTP_200_OK
            )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    def railroad_pref(self, request, pref):
        with open('data/railroad.json', 'r', encoding='utf8') as f:
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

    def railroad_line(self, request, pref, line):
        with open('data/railroad.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data and line in data[pref]:
                return JsonResponse(
                    data[pref][line],
                    safe=False,
                    json_dumps_params={'ensure_ascii': False},
                    content_type='application/json',
                    status=status.HTTP_200_OK
                )
        return JsonResponse({}, status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view({'get': 'railroad'}), name='railroad'),
            path('<pref>/', cls.as_view({'get': 'railroad_pref'}), name='railroad_pref'),
            path('<pref>/<line>/', cls.as_view({'get': 'railroad_line'}), name='railroad_line'),
        ]
