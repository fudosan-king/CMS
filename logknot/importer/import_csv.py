import os
import csv
from formatconverter.converter import FromCSVConverter
from dashboard.models import Buildings
from .models import LogsImport
import datetime
from mongoengine.queryset.visitor import Q
from django.urls import reverse

COL_CSV = 58


def import_csv(dirpath, dry_run=True):
    importer = CSVImporter(dry_run)

    try:
        importer.import_buildings(dirpath)
    except Exception as e:
        print('Import have error: {}'.format(e))
    if dry_run:
        return importer.get_log()


class CSVLoader(object):
    def __init__(self, dirpath):
        self.converter = FromCSVConverter()
        self.dirpath = dirpath

    def __call__(self):
        self.error_count = 0

        with open(os.path.join(self.dirpath, 'import.csv'), 'r', encoding='cp932') as fp:
            it = iter(csv.reader(fp))

            header = next(it)
            if len(header) != COL_CSV:
                print('Please check file csv (only 58 column)')
                assert False

            for idx, row in enumerate(it):
                error = None
                building = None
                building_name = row[0]
                if not building_name:
                    continue

                try:
                    building, images = self.converter.convert(row)
                except Exception as e:
                    error = building_name
                    print('CSVLoader have problem: {}'.format(e))

                yield idx + 2, building, error


class CSVImporter(object):
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.import_done = {}
        self.ignore_buildings = {}
        self.import_fail = []

    def import_buildings(self, dirpath):
        loader = CSVLoader(dirpath)

        for lineno, building, error in loader():
            if not error and building:
                try:
                    self.save_building(building)
                except Exception as e:
                    print('Import building have error: {} - {}'.format(building.get('building_name'), e))
                    continue
            else:
                self.import_fail.append(error)

        if not self.dry_run:
            self.save_log()

    def save_log(self):
        logs = LogsImport()
        logs.import_done = self.import_done
        logs.ignore_buildings = self.ignore_buildings
        logs.import_fail = self.import_fail
        logs.save()

    def get_log(self):
        return self.import_done, self.ignore_buildings, self.import_fail

    def save_building(self, building):
        query = Q(building_name=building.get('building_name'))
        query &= Q(address__pref=building.get('address', {}).get('pref'))
        query &= Q(address__city=building.get('address', {}).get('city'))
        query &= Q(address__ooaza=building.get('address', {}).get('ooaza'))
        building_query = Buildings.objects().filter(query).first()

        if not building_query:
            import_building = Buildings(building_name=building.get('building_name'))
            for k, v in building.items():
                if k != 'building_name':
                    import_building[k] = v
            import_building.loan_interest_rate = 2.0
            import_building.import_date = datetime.datetime.now
            if not self.dry_run:
                try:
                    import_building.save()
                except:
                    self.import_fail.append(building.get('building_name'))

            self.import_done[import_building.building_name] = reverse(
                'buildings_show',
                args=(import_building.id,)
            )
        else:
            self.ignore_buildings[building_query.building_name] = reverse('buildings_show', args=(building_query.id,))
