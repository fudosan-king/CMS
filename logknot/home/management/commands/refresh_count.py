from django.core.management.base import BaseCommand
from dashboard.models import Buildings, CountInfoBuildings
from dashboard.controllers.buildings import update_count


class Command(BaseCommand):
    help = 'Refresh count'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        try:
            buildings = Buildings.objects().order_by('-id')
            count = CountInfoBuildings()
            count.drop_collection()
            for building in buildings:
                update_count(building)

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Refresh fail: {}'.format(e))
            )
