from django.utils.safestring import mark_safe
from dashboard.models import Buildings, LogsImport

from wagtail.core import hooks


class WelcomePanel:
    order = 99

    def render(self):
        buildings = Buildings.objects(removed=False).count()
        buildings_removed = Buildings.objects(removed=True).count()
        logs = LogsImport.objects().count()
        return mark_safe("""
        <section class="panel summary nice-padding">
            <h2 class="visuallyhidden">Site summary</h2>
            <ul class="stats">
                <li class="icon icon-doc-full-inverse">
                    <a href="/dashboard/buildings/">
                        <span>{}</span> 建物 <span class="visuallyhidden">created in logknot</span>
                    </a>
                </li>
                <li class="icon icon-doc-full-inverse">
                    <a href="/dashboard/removed/">
                        <span>{}</span> 削除する<span class="visuallyhidden">created in logknot</span>
                    </a>
                </li>
                <li class="icon icon-folder-open-1">
                    <a href="/dashboard/reports/logs/">
                        <span>{}</span> データログ<span class="visuallyhidden">created in logknot</span>
                    </a>
                </li>
            </ul>
        </section>
        """.format(buildings, buildings_removed, logs))


@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(request, panels):
    panels.append(WelcomePanel())
