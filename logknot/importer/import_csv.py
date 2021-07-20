import os
import csv
from formatconverter.converter import FromCSVConverter
from dashboard.models import Buildings
import datetime
from mongoengine.queryset.visitor import Q


def import_csv(dirpath, dry_run=True):
    importer = CSVImporter(dry_run)

    try:
        importer.import_buildings(dirpath)
    except Exception as e:
        print('Import have error: {}'.format(e))


class CSVLoader(object):
    def __init__(self, dirpath):
        self.converter = FromCSVConverter()
        self.dirpath = dirpath

    def __call__(self):
        self.error_count = 0

        with open(os.path.join(self.dirpath, 'import.csv'), 'r', encoding='cp932') as fp:
            it = iter(csv.reader(fp))

            header = next(it)
            if len(header) != 58:
                print('Please check file csv (only 58 column)')
                assert False

            for idx, row in enumerate(it):
                building_name = row[0]
                if not building_name:
                    continue

                try:
                    e, images = self.converter.convert(row)

                except Exception as e:
                    print('CSVLoader have problem: {}'.format(e))
                else:
                    yield idx + 2, e


class CSVImporter(object):
    def __init__(self, dry_run=True):
        self.dry_run = dry_run

    def import_buildings(self, dirpath):
        loader = CSVLoader(dirpath)

        for lineno, building in loader():
            try:
                self.save_building(building)
            except Exception as e:
                print('Import building have error: {}'.format(e))
                continue

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
            import_building.save()
