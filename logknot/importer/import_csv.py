import os
import csv
from formatconverter.converter import FromCSVConverter


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
            if len(header) == 9:
                assert header[0] == 'header'
                assert header[1] == '4.1.0'
                assert header[2] == '0'

            for idx, row in enumerate(it):
                building_name = row[9]
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
        print(building)
