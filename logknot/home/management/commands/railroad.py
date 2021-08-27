from django.core.management.base import BaseCommand
import json
import codecs
import csv


# Example:
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/lines
# https://fudosan-king.jp/api/pref/%E4%BA%AC%E9%83%BD%E5%BA%9C/%EF%BC%AA%EF%BC%B2%E5%B1%B1%E9%99%B0%E6%9C%AC%E7%B7%9A/stations

IGNORE = ['', '#N/A']
COL_CSV_MAP = 15

MAP_REGION = {
    '北海道': ['北海道'],
    '東北': ['青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県'],
    '関東': ['茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県'],
    '中部': ['新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県'],
    '関西': ['三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県'],
    '中国': ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
    '四国': ['徳島県', '香川県', '愛媛県', '高知県'],
    '九州': ['福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']
}


class Command(BaseCommand):
    help = 'Load map_railroad'

    def handle(self, *args, **kwargs):
        railroad = {}
        try:
            with open('data/veki.csv', 'r', encoding='utf8') as fp:
                it = iter(csv.reader(fp))
                for idx, row in enumerate(it):
                    if row[9] not in railroad:
                        railroad[row[9]] = {}
                    if row[3] not in railroad[row[9]]:
                        railroad[row[9]][row[3]] = []
                    railroad[row[9]][row[3]].append(row[5])
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
                        railroad_from_fdk[row[11]] = [row[3], row[13]]
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
