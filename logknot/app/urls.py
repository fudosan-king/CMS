from django.conf import settings
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from home.search import urls as search_urls
from home.building import urls as building_urls
from .upload import UploadImages
from .api import api_router
# from page import views as search_pages


urlpatterns = [
    path('dashboard/', include(wagtailadmin_urls)),
    path('search/', include(search_urls)),
    path('building/', include(building_urls)),
    path('api/', api_router.urls),
    path('images/upload/', UploadImages.as_view(), name='upload'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
