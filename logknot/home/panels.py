from django.utils.safestring import mark_safe
from dashboard.models import Buildings, Media

from wagtail.core import hooks


class WelcomePanel:
    order = 99

    def render(self):
        buildings = Buildings.objects(removed=False).count()
        buildings_removed = Buildings.objects(removed=True).count()
        media = Media.objects.count()
        return mark_safe("""
        <section class="panel summary nice-padding">
            <h2 class="visuallyhidden">Site summary</h2>
            <ul class="stats">
                <li class="icon icon-doc-full-inverse">
                    <a href="/dashboard/buildings/">
                        <span>{}</span> Buildings <span class="visuallyhidden">created in logknot</span>
                    </a>
                </li>
                <li class="icon icon-doc-full-inverse">
                    <a href="/dashboard/removed/">
                        <span>{}</span> Removed<span class="visuallyhidden">created in logknot</span>
                    </a>
                </li>
                <li class="icon icon-image">
                    <span>{}</span> Images <span class="visuallyhidden">created in logknot</span>
                </li>
            </ul>
        </section>
        """.format(buildings, buildings_removed, media))


@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(WelcomePanel())
