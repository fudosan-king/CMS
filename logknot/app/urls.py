from django.conf import settings
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from home.search import urls as search_urls
from home.building import urls as building_urls
from .upload import UploadImages
from .api import api_router
from django.views.static import serve
from django.conf.urls import url


urlpatterns = [
    path('dashboard/', include(wagtailadmin_urls)),
    path('search/', include(search_urls)),
    path('building/', include(building_urls)),
    path('api/', api_router.urls),
    path('images/upload/', UploadImages.as_view(), name='upload'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
