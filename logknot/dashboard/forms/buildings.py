from django import forms
from django_mongoengine.forms import DocumentForm, EmbeddedDocumentForm
from dashboard.models import Buildings, Photos
from django.utils.translation import gettext as _  # noqa
from django.utils.translation import gettext_lazy as __  # noqa
import datetime
from dashboard.forms.core import double


CATEGORY = double('', 'カテゴリー1', 'カテゴリー2')

DIRECTION = [('n', '北'), ('ne', '北東'), ('e', '東'), ('se', '南東'), ('s', '南'), ('sw', '南西'), ('w', '西'), ('nw', '北西')]

ROOM_KIND = double('', 'K', 'R', 'DK', 'LK', 'SK', 'LDK', 'SDK', 'SLDK', '間取り最大')

LIMITATIONS = double(
    '文化財保護法', '古都保存法', '景観法', '密集市街地整備法', '航空法', '河川法', '砂防法', '農地法届出要',
    '安全条例', '宅地造成工事規制区域', '急傾斜地崩壊危険区域', '高度地区', '高度利用地区', '中高層階住居専用地区',
    '高層住宅誘導地区', '防火地域', '準防火地域', '風致地区', '景観地区', '準景観地区', '観光地区', '歴史的風土保存地区',
    '伝統的建造物群保存地区', '特定街区', '特別用途制限地域', '文教地区', '都市再生特別地区', '特別緑地保全地区',
    '高さ最高限度有', '高さ最低限度有', '建ぺい率最低限度有', '容積率最低限度有', '敷地面積最高限度有', '敷地面積最低限度有',
    '建物面積最高限度有', '建物面積最低限度有', '一部都市計画道路', '一部協定通路', '日影制限有', '隅切り有', '接道と段差有',
    '敷地内段差有', '壁面後退有', '建築協定有', '崖下につき建築制限有', '崖上につき建築制限有', '不整形地')

STRUCTURE = double(
    '木造', '鉄骨', 'RC', 'SRC', 'PC', 'HPC', '軽量鉄骨', 'ALC', 'CFT',
    'ブロック', '鉄筋ブロック', 'その他')

STRUCTURE_PART = double(
    '木造', '鉄骨', 'RC', 'SRC', 'PC', 'HPC', '軽量鉄骨', 'ALC', 'CFT',
    'ブロック', '鉄筋ブロック', 'その他')

MANAGEMENT_SCOPE = double('自主管理', '一部委託', '全部委託')

LAND_RIGHTS = double('借地権', '地上権', '所有権', '定期借地権')

ESTATE_SUBTYPE = double('マンション', '公団', '公社', 'タウンハウス', 'リゾートマンション')

SUPER_INTENDENT = double('', '日勤', '巡回', '常駐', '非常駐')

CARPARK_TYPE = double('無', '駐車場', '分譲駐車場(必購入)', '分譲駐車場(任意購入)', '専用使用権付駐車場')

NO_YES = double('無', '有')

CARPARK_PLACE = double('敷地内', '敷地外')

PER_MONTH = [('m', '月'), ('y', '年')]

PARK = double('無', '空無', '有', '近有')

TAX_INC = double('税込み', '税抜き')

CONSTRUCTOR_LABEL = double(
    '無し', '株式会社 - 前', '合名会社 - 前', '合資会社 - 前', '合同会社 - 前',
    '有限会社 - 前', '株式会社 - 後', '合名会社 - 後', '合資会社 - 後', '合同会社 - 後', '有限会社 - 後')

WATERWORKS = double('公営水道', '私設水道', '井戸', 'その他')

SEWER = double('本下水', '集中浄化槽', '個別浄化槽', '汲取', 'その他')

GAS = double('都市ガス', '集中', 'LPG個別', 'LPG', 'オール電化', 'その他')

LAN_LAW_REPORT = double('要', '届出中', '不要')


class PhotosForm(EmbeddedDocumentForm):
    class Meta:
        document = Photos
        fields = '__all__'
        embedded_field = 'photos'


class BuildingsForm(DocumentForm):
    estate_subtype = forms.CharField(
        label=__('物件種別'),
        max_length=20,
        initial='マンション',
        widget=forms.Select(
            choices=ESTATE_SUBTYPE,
        ),
    )
    building_name = forms.CharField(
        label=__('物件名'),
        max_length=50,
        widget=forms.TextInput()
    )
    building_name_kana = forms.CharField(
        label=__('物件名（フリガナ）'),
        max_length=50,
        required=False,
        widget=forms.TextInput()
    )
    zipcode_1 = forms.CharField(
        label=__('郵便番号'),
        max_length=3,
        required=True,
        widget=forms.NumberInput()
    )
    zipcode_2 = forms.CharField(
        label=__('郵便番号'),
        max_length=4,
        required=True,
        widget=forms.NumberInput()
    )
    recommend = forms.BooleanField(
        label=__('お勧め'),
        required=False,
        widget=forms.CheckboxInput()
    )
    structure = forms.CharField(
        label=__('構造(主要)'),
        max_length=20,
        widget=forms.Select(
            choices=STRUCTURE
        ),
        initial='その他',
        required=True
    )
    structure_part = forms.CharField(
        label=__('構造(一部)'),
        max_length=20,
        widget=forms.Select(
            choices=STRUCTURE_PART
        ),
        initial='その他',
        required=False
    )
    ground_floors = forms.IntegerField(
        label=__('階建て（地上）'),
        required=True,
        widget=forms.NumberInput()
    )
    underground_floors = forms.IntegerField(
        label=__('階建て（地下）'),
        required=True,
        widget=forms.NumberInput()
    )
    built_date_year = forms.IntegerField(
        label=__('築年月'),
        required=True,
        initial=datetime.datetime.now().year,
        widget=forms.NumberInput(),
        min_value=1950,
        max_value=datetime.datetime.now().year
    )
    built_date_month = forms.IntegerField(
        label=__(''),
        required=False,
        initial=datetime.datetime.now().month,
        widget=forms.Select(
            choices=[
                (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)
            ]
        ),
    )
    total_houses = forms.IntegerField(
        label=__('総戸数'),
        required=False,
        widget=forms.NumberInput()
    )
    management_scope = forms.CharField(
        label=__('管理方式'),
        max_length=20,
        widget=forms.Select(
            choices=MANAGEMENT_SCOPE
        ),
        required=True,
        initial='自主管理'
    )
    superintendent = forms.CharField(
        label=__('管理人'),
        max_length=20,
        widget=forms.Select(
            choices=SUPER_INTENDENT
        ),
        required=False
    )
    land_rights = forms.CharField(
        label=__('敷地権利'),
        required=True,
        widget=forms.RadioSelect(
            choices=LAND_RIGHTS,
        )
    )
    waterworks = forms.CharField(
        label=__('上水道'),
        widget=forms.RadioSelect(
            choices=WATERWORKS
        ),
        required=False
    )
    sewer = forms.CharField(
        label=__('下水道'),
        widget=forms.RadioSelect(
            choices=SEWER
        ),
        required=False
    )
    gas = forms.CharField(
        label=__('ガス'),
        widget=forms.RadioSelect(
            choices=GAS
        ),
        required=False
    )
    land_law_report = forms.CharField(
        label=__('国土法'),
        widget=forms.RadioSelect(
            choices=LAN_LAW_REPORT
        ),
        initial='要',
        required=True
    )
    constructor_label = forms.CharField(
        label=__('施工会社'),
        widget=forms.Select(
            choices=CONSTRUCTOR_LABEL
        ),
        required=False
    )
    building_confirmation_number = forms.CharField(
        label=__('建築確認番号'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    constructor = forms.CharField(
        label=__('施工会社'),
        max_length=100,
        widget=forms.TextInput(),
        required=False
    )
    design_club = forms.CharField(
        label=__('施工会社'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    management_company = forms.CharField(
        label=__('管理会社'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    carpark_type = forms.CharField(
        label=__('駐車場'),
        max_length=20,
        widget=forms.Select(
            choices=CARPARK_TYPE
        ),
        required=False
    )
    carpark_space = forms.CharField(
        label=__('空き'),
        max_length=20,
        widget=forms.Select(
            choices=NO_YES
        ),
        required=False
    )
    carpark_space_cars = forms.IntegerField(
        label=__('空き台数'),
        widget=forms.NumberInput(),
        min_value=0,
        required=False
    )
    carpark_place = forms.CharField(
        label=__('場所'),
        max_length=20,
        widget=forms.Select(
            choices=CARPARK_PLACE
        ),
        required=False
    )
    carpark_fee_min = forms.IntegerField(
        label=__('料金金額'),
        widget=forms.NumberInput(),
        min_value=0,
        required=False
    )
    carpark_fee_per = forms.CharField(
        label=__('料金支払方法'),
        max_length=20,
        widget=forms.Select(
            choices=PER_MONTH
        ),
        required=False
    )
    carpark_fee_tax_inc = forms.CharField(
        label=__('料金税抜き・込み'),
        max_length=20,
        widget=forms.Select(
            choices=TAX_INC
        ),
        required=False
    )
    carpark_note = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        max_length=100,
        label=__('備考')
    )
    bike_park = forms.CharField(
        label=__('バイク置場'),
        max_length=20,
        widget=forms.Select(
            choices=PARK
        ),
        required=False
    )
    bike_park_price = forms.IntegerField(
        label=__('バイク置場料金'),
        widget=forms.NumberInput(),
        min_value=0,
        required=False
    )
    bike_park_price_per = forms.CharField(
        label=__('バイク置場料金（期間）'),
        max_length=20,
        widget=forms.Select(
            choices=PER_MONTH
        ),
        required=False
    )
    bicycles_park = forms.CharField(
        label=__('駐輪場'),
        max_length=254,
        widget=forms.Select(
            choices=PARK
        ),
        required=False
    )
    bicycles_park_price = forms.IntegerField(
        label=__('駐輪場料金'),
        widget=forms.NumberInput(),
        min_value=0,
        required=False
    )
    bicycles_park_price_per = forms.CharField(
        label=__('駐輪場料金（期間）'),
        max_length=20,
        widget=forms.Select(
            choices=PER_MONTH
        ),
        required=False
    )
    google_map = forms.CharField(
        widget=forms.Textarea(),
        required=False,
        max_length=1000,
        label=__('Google map 座標')
    )
    google_map_lat = forms.FloatField(
        required=False,
        label=__('ストリートビュー座標（lat）'),
        widget=forms.NumberInput()
    )
    google_map_lng = forms.FloatField(
        required=False,
        label=__('ストリートビュー座標（lng）'),
        widget=forms.NumberInput()
    )
    google_map_yaw = forms.IntegerField(
        label=__('ストリートビュー座標（yaw）'),
        min_value=0,
        max_value=360,
        widget=forms.NumberInput(),
        required=False
    )
    google_map_pitch = forms.IntegerField(
        label=__('ストリートビュー座標（pitch）'),
        min_value=-90,
        max_value=90,
        widget=forms.NumberInput(),
        required=False
    )
    google_map_zoom = forms.IntegerField(
        label=__('ストリートビュー座標（zoom）'),
        min_value=0,
        max_value=2,
        widget=forms.NumberInput(),
        required=False
    )
    elementary_school_district = forms.CharField(
        label=__('小学校学区'),
        max_length=100,
        widget=forms.TextInput(),
        required=False
    )
    junior_high_school_district = forms.CharField(
        label=__('中学校学区'),
        max_length=100,
        widget=forms.TextInput(),
        required=False
    )
    price = forms.FloatField(
        required=False,
        label=__('物件販売価格'),
        widget=forms.NumberInput()
    )
    tatemono_menseki = forms.FloatField(
        required=False,
        label=__('専有面積'),
        widget=forms.NumberInput()
    )
    balcony_space = forms.FloatField(
        required=False,
        label=__('バルコニー面積'),
        initial=0,
        widget=forms.NumberInput()
    )
    room_floor = forms.IntegerField(
        required=False,
        label=__('バルコニー面積'),
        widget=forms.NumberInput()
    )
    direction = forms.CharField(
        label=__('向き（方角）'),
        widget=forms.Select(
            choices=DIRECTION
        ),
        required=False
    )
    room_count = forms.IntegerField(
        label=__('部屋数'),
        required=False,
        widget=forms.NumberInput()
    )
    room_kind = forms.CharField(
        label=__('部屋の種類'),
        required=False,
        widget=forms.Select(
            choices=ROOM_KIND
        )
    )
    management_fee = forms.IntegerField(
        label=__('管理費'),
        required=False,
        widget=forms.NumberInput()
    )
    repair_reserve_fee = forms.IntegerField(
        label=__('修繕積立金'),
        required=False,
        widget=forms.NumberInput()
    )
    when_to_move_in = forms.DateField(
        label=__('入居時期'),
        required=False,
        initial=datetime.datetime.now,
        widget=forms.DateInput()
    )
    limitations = forms.MultipleChoiceField(
        label=__('法令上の制限'),
        required=False,
        choices=LIMITATIONS,
        # initial=[c[0] for c in LIMITATIONS],
        widget=forms.CheckboxSelectMultiple()
    )
    limitations_etc = forms.CharField(
        label=__('その他制限事項'),
        max_length=60,
        widget=forms.TextInput(),
        required=False
    )
    pref = forms.CharField(
        label=__('住所'),
        required=True
    )
    city = forms.CharField(
        label=__('住所'),
        required=True
    )
    ooaza = forms.CharField(
        label=__('住所'),
        required=True
    )

    class Meta:
        document = Buildings
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
