from django.core.management.base import BaseCommand
from collections import defaultdict
import json
import codecs

CODE_FIELD = 0
PREF_FIELD = 19
PREF_FIELD_KANA = 10
CITY_FIELD = 20
CITY_FIELD_KANA = 11
TOWN_FIELD = 21
TOWN_FIELD_KANA = 12
AZA_FIELD = 22
AZA_FIELD_KANA = 13
IGNORE_CODE = []

# Example:
# https://fudosan-king.jp/api/area/%E6%9D%B1%E4%BA%AC%E9%83%BD/%E4%B8%89%E9%B7%B9%E5%B8%82/%E4%B8%8A%E9%80%A3%E9%9B%80


class Command(BaseCommand):
    help = 'Load area codes from maf4c'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, help='File path')

    def handle(self, *args, **kwargs):
        codefilename = kwargs['path']

        if not codefilename:
            self.stdout.write(self.style.ERROR(
                'Please add file path. Ex: [python3 manage.py locations -p /home/maf4c.txt]')
            )
            return

        def trim_japan_space(text):
            last = -1
            while len(text) + last > 0 and text[last] in ('', u' ', u'　'):
                last -= 1
            if last == -1:
                return text
            return text[:last + 1]

        data = {}
        try:
            with open(codefilename, 'rb') as fp:
                for ln in fp:
                    line = ln.decode('shift-jis')
                    fields = line.split(u',')
                    code = fields[CODE_FIELD]
                    pref = trim_japan_space(fields[PREF_FIELD])
                    root_code = code[:2]
                    if root_code not in data:
                        data[root_code] = {
                            'pref': pref,
                            'areas': {root_code: pref},
                            'prefdata': {},
                            'prefdata2': defaultdict(list),
                        }
                    while code.endswith('000'):
                        code = code[:-3]

                    if code[:-3] not in data[root_code]['areas']:
                        if len(code) == 11:
                            if code[:-6] not in data[root_code]['areas']:
                                addr = u'{}/{}'.format(
                                    data[root_code]['areas'][code[:-9]],
                                    trim_japan_space(fields[CITY_FIELD])).replace(u'　', '')
                                data[root_code]['areas'][code[:-6]] = addr
                                data[root_code]['areas'][addr] = code[:-6]
                            addr = u'{}/{}'.format(
                                data[root_code]['areas'][code[:-6]],
                                trim_japan_space(fields[TOWN_FIELD])
                            ).replace(u'　', '')
                            data[root_code]['areas'][code[:-3]] = addr
                            data[root_code]['areas'][addr] = code[:-3]
                        if len(code) == 8:
                            if code[:-3] not in data[root_code]['areas']:
                                addr = u'{}/{}'.format(
                                    data[root_code]['areas'][code[:-6]],
                                    trim_japan_space(fields[CITY_FIELD])).replace(u'　', '')
                                data[root_code]['areas'][code[:-3]] = addr
                                data[root_code]['areas'][addr] = code[:-3]

                    if len(code) == 2:
                        continue
                        # name = fields[PREF_FIELD]
                        # furigana = fields[PREF_FIELD_KANA]
                    elif len(code) == 5:
                        name = trim_japan_space(fields[CITY_FIELD]).replace(u'　', '')
                        furigana = trim_japan_space(fields[CITY_FIELD_KANA])
                    elif len(code) == 8:
                        name = trim_japan_space(fields[TOWN_FIELD]).replace(u'　', '')
                        furigana = trim_japan_space(fields[TOWN_FIELD_KANA])
                    elif len(code) == 11:
                        name = trim_japan_space(fields[AZA_FIELD])
                        if name[0] == u'字':
                            name = name[1:]
                        furigana = trim_japan_space(fields[AZA_FIELD_KANA])

                    # update areas
                    addr = u'{}/{}'.format(data[root_code]['areas'][code[:-3]], name)
                    if code not in IGNORE_CODE:
                        data[root_code]['areas'][code] = addr
                        data[root_code]['areas'][addr] = code
                        assert addr.count(u'/') == {2: 0, 5: 1, 8: 2, 11: 3}[len(code)]

                        # update prefdata
                        p = data[root_code]['prefdata']
                        for idx, sub in enumerate(data[root_code]['areas'][code].split('/')):
                            if idx == 0:
                                p = data[root_code]['prefdata']
                            elif idx == 1:
                                p = p.setdefault(sub, {})
                            elif idx == 2:
                                p = p.setdefault(sub, [])
                            elif idx == 3:
                                if sub not in p:
                                    p.append(sub)
                            else:
                                assert 0

                        # update prefdata2
                        data[root_code]['prefdata2'][code[:-3]].append((furigana, name, code))
        except:
            self.stdout.write(self.style.WARNING('No such file or directory: {}'.format(codefilename)))

        if data:
            locations = {}
            for root_code in data:
                locations[data[root_code]['pref']] = data[root_code]['prefdata']

            outfile = open('data/locations.json', 'wb')
            outfile = codecs.lookup('utf-8')[-1](outfile)
            json.dump(
                locations,
                outfile,
                ensure_ascii=False,
                indent=2,
                sort_keys=True
            )
            outfile.close()
            self.stdout.write(self.style.SUCCESS('SUCCESS'))
