from django.core.management.base import BaseCommand
from importer.import_csv import import_csv


class Command(BaseCommand):
    help = 'Import CSV'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--dryrun', type=str, help='Dry run')

    def handle(self, *args, **kwargs):
        dry_run = kwargs['dryrun']

        try:
            if dry_run == 'True':
                done, ignore, fail = import_csv('tests/import', dry_run=True)
                print('Done: {}'.format(len(done.keys())))
                print('ignore: {}'.format(len(ignore.keys())))
                print('Fail: {}'.format(len(fail)))
            elif dry_run == 'False':
                import_csv('test/import', dry_run=False)

            self.stdout.write(self.style.SUCCESS('Import done!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Import fail!: {}'.format(e))
            )
