from django.urls import path
from .views import search, page, result, search_all

urlpatterns = [
    path('', search, name='search'),
    path('all/', search_all, name='search_all'),
    path('result/', result, name='result'),
    path('page/', page, name='page'),
]
