from django.core.management.base import BaseCommand
import numpy
import json
import codecs
from .locations import PREF_MAP


# Example:
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/lines
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/%EF%BC%AA%EF%BC%B2%E5%B1%B1%E9%99%B0%E6%9C%AC%E7%B7%9A/stations


class Command(BaseCommand):
    help = 'Load railroad'

    def handle(self, *args, **kwargs):
        railroad = {}
        try:
            data = numpy.genfromtxt(
                'data/SUUMO_ENSEN.dat',
                skip_header=1,
                skip_footer=1,
                names=True,
                dtype=None,
                encoding='cp932',
                delimiter='\t'
            )
            # line[2] ~ line name
            # line[3] ~ station name
            # line[4] ~ pref
            for line in data:
                if line[4] in PREF_MAP:
                    if line[4] not in railroad:
                        railroad[line[4]] = {}
                    if line[2] not in railroad[line[4]]:
                        railroad[line[4]][line[2]] = []
                    railroad[line[4]][line[2]].append(line[3])
        except:
            self.stdout.write(self.style.ERROR(
                'Please check file SUUMO_ENSEN.dat')
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
            self.stdout.write(self.style.SUCCESS('SUCCESS'))
