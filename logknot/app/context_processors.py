from django.conf import settings
from home.models import HomePage


def extra_context(request):
    home_page = HomePage.objects.get(id=3)
    return {
        'base_url': settings.BASE_URL,
        'home_page': home_page
    }
