from wagtail.api.v2.router import WagtailAPIRouter
from api.locations import LocationsViewSet
from api.railroad import RailRoadViewSet
from api.count import CountViewSet


api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('locations', LocationsViewSet)
api_router.register_endpoint('railroad', RailRoadViewSet)
api_router.register_endpoint('count', CountViewSet)
