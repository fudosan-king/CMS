from wagtail.api.v2.router import WagtailAPIRouter
from api.locations import LocationsViewSet
from api.railroad import RailRoadViewSet

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('locations', LocationsViewSet)
api_router.register_endpoint('railroad', RailRoadViewSet)
