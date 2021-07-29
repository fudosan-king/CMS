from django.urls import path
from .views import search, page

urlpatterns = [
    path('', search, name='search'),
    path('page/', page, name='page'),
]
