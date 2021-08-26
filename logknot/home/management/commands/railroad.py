from django.core.management.base import BaseCommand
import json
import codecs
import csv


# Example:
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/lines
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/%EF%BC%AA%EF%BC%B2%E5%B1%B1%E9%99%B0%E6%9C%AC%E7%B7%9A/stations

MAP_PREF_STATION = {
    '1': '北海道',
    '2': '東北',
    '3': '関東',
    '4': '中部',
    '5': '近畿',
    '6': '中国',
    '8': '四国',
    '9': '九州',
}
IGNORE = ['', '#N/A']
COL_CSV_MAP = 16


class Command(BaseCommand):
    help = 'Load map_railroad'

    def handle(self, *args, **kwargs):
        railroad = {}
        try:
            with open('data/veki.csv', 'r', encoding='cp932') as fp:
                it = iter(csv.reader(fp))
                for idx, row in enumerate(it):
                    if MAP_PREF_STATION.get(row[0]) not in railroad:
                        railroad[MAP_PREF_STATION.get(row[0])] = {}
                    if row[3] not in railroad[MAP_PREF_STATION.get(row[0])]:
                        railroad[MAP_PREF_STATION.get(row[0])][row[3]] = []
                    railroad[MAP_PREF_STATION.get(row[0])][row[3]].append(row[5])
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Please check file veki.csv: {}'.format(e))
            )

        if railroad:
            outfile = open('data/railroad.json', 'wb')
            outfile = codecs.lookup('utf-8')[-1](outfile)
            json.dump(
                railroad,
                outfile,
                ensure_ascii=False,
                indent=2,
                sort_keys=True
            )
            outfile.close()
            self.stdout.write(self.style.SUCCESS('SUCCESS: railroad'))

        railroad_from_fdk = {}
        railroad_to_fdk = {}
        try:
            with open('data/map_railroad.csv', 'r', encoding='utf8') as fp:
                it = iter(csv.reader(fp))
                header = next(it)
                if len(header) != COL_CSV_MAP:
                    self.stdout.write(self.style.ERROR(
                        'Pls check file map_railroad.csv: column only {}'.format(COL_CSV_MAP))
                    )
                    assert False
                for idx, row in enumerate(it):
                    if row[11] not in railroad_from_fdk and row[11] not in IGNORE and row[0] and row[0] not in IGNORE:
                        railroad_from_fdk[row[11]] = [row[3], MAP_PREF_STATION.get(row[0])]
                    if row[3] not in railroad_to_fdk and row[3] not in IGNORE:
                        railroad_to_fdk[row[3]] = row[11]
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                'Please check file map_railroad.csv: {}'.format(e))
            )

        if railroad_from_fdk:
            outfile = open('data/railroad_from_fdk.json', 'wb')
            outfile = codecs.lookup('utf-8')[-1](outfile)
            json.dump(
                railroad_from_fdk,
                outfile,
                ensure_ascii=False,
                indent=2,
                sort_keys=True
            )
            outfile.close()
            self.stdout.write(self.style.SUCCESS('SUCCESS: railroad_from_fdk'))

        if railroad_to_fdk:
            outfile = open('data/railroad_to_fdk.json', 'wb')
            outfile = codecs.lookup('utf-8')[-1](outfile)
            json.dump(
                railroad_to_fdk,
                outfile,
                ensure_ascii=False,
                indent=2,
                sort_keys=True
            )
            outfile.close()
            self.stdout.write(self.style.SUCCESS('SUCCESS: railroad_to_fdk'))
