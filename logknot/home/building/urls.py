from django.urls import path
from .views import index

urlpatterns = [
    path('<building_id>/', index, name='building'),
]
