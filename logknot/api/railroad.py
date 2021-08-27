from rest_framework.viewsets import GenericViewSet
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
from dashboard.models import SearchSortByPref
from home.management.commands.railroad import MAP_REGION


class RailRoadViewSet(GenericViewSet):
    def get_region(self, request, region):
        data = []
        if region in MAP_REGION:
            data = MAP_REGION.get(region, [])
        return JsonResponse(
            data,
            safe=False,
            json_dumps_params={'ensure_ascii': False},
            content_type='application/json',
            status=status.HTTP_200_OK
        )

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
        search_sort = SearchSortByPref.objects.filter(pref=pref).first()
        with open('data/railroad.json', 'r', encoding='utf8') as f:
            data = eval(f.read())
            if pref and pref in data:
                transport_company_all = list(data[pref].keys())
                if search_sort:
                    transport_company = search_sort.transport_company
                else:
                    transport_company = []
                for st in transport_company_all:
                    if st not in transport_company:
                        transport_company.append(st)
                return JsonResponse(
                    transport_company,
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
            path('region/<region>/', cls.as_view({'get': 'get_region'}), name='region'),
            path('<pref>/', cls.as_view({'get': 'railroad_pref'}), name='railroad_pref'),
            path('<pref>/<line>/', cls.as_view({'get': 'railroad_line'}), name='railroad_line'),
        ]
