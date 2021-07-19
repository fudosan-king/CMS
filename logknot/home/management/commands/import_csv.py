from django.core.management.base import BaseCommand
from importer.import_csv import import_csv


class Command(BaseCommand):
    help = 'Import CSV'

    def handle(self, *args, **kwargs):
        try:
            import_csv('test/import')
            self.stdout.write(self.style.SUCCESS('Import success'))
        except:
            self.stdout.write(self.style.ERROR(
                'Import fail')
            )
