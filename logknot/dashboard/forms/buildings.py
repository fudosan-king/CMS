from django import forms
from django_mongoengine.forms import DocumentForm, EmbeddedDocumentForm
from dashboard.models import Buildings, Photos
from django.utils.translation import gettext as _  # noqa
from django.utils.translation import gettext_lazy as __  # noqa
import datetime


CATEGORY = [
    ('', ''),
    ('カテゴリー1', 'カテゴリー1'),
    ('カテゴリー2', 'カテゴリー2')
]

DIRECTION = [
    ('', ''),
    ('北', '北'),
    ('北東', '北東'),
    ('東', '東'),
    ('南東', '南東'),
    ('南', '南'),
    ('南西', '南西'),
    ('西', '西'),
    ('北西', '北西'),
]

ROOM_KIND = [
    ('', ''),
    ('K', 'K'),
    ('R', 'R'),
    ('DK', 'DK'),
    ('LK', 'LK'),
    ('SK', 'SK'),
    ('LDK', 'LDK'),
    ('SDK', 'SDK'),
    ('SLDK', 'SLDK'),
    ('間取り最大', '間取り最大')
]

LIMITATIONS = [
    ('文化財保護法', '文化財保護法'),
    ('密集市街地整備法', '密集市街地整備法')
]

STRUCTURE = [
    ('', ''),
    ('PC', 'PC'),
    ('RC', 'RC'),
    ('RC一部SRC', 'RC一部SRC'),
    ('SRC', 'SRC'),
    ('SRC一部RC', 'SRC一部RC'),
    ('SRC一部S', 'SRC一部S'),
    ('軽量鉄骨造', '軽量鉄骨造'),
    ('鉄骨造', '鉄骨造'),
    ('その他', 'その他')
]


MANAGEMENT_SCOPE = [
    ('', ''),
    ('自主管理', '自主管理'),
    ('一部委託', '一部委託'),
    ('全部委託', '全部委託')
]

LAND_RIGHTS = [
    ('借地権', '借地権'),
    ('地上権', '地上権'),
    ('所有権', '所有権'),
    ('定期借地権', '定期借地権')
]

AREA_PURPOSE = [
    ('', ''),
    ('庭', '庭'),
    ('プール', 'プール'),
]


class PhotosForm(EmbeddedDocumentForm):
    class Meta:
        document = Photos
        fields = '__all__'
        embedded_field = 'photos'


class BuildingsForm(DocumentForm):
    building_name = forms.CharField(
        label=__('物件名'),
        max_length=50,
        widget=forms.TextInput()
    )
    recommend = forms.BooleanField(
        label=__('お勧め'),
        required=False,
        widget=forms.CheckboxInput()
    )
    structure = forms.CharField(
        label=__('構造'),
        max_length=254,
        widget=forms.Select(
            choices=STRUCTURE
        ),
        required=True
    )
    ground_floors = forms.IntegerField(
        label=__('階建て'),
        required=True,
        widget=forms.NumberInput()
    )
    underground_floors = forms.IntegerField(
        label=__('階建て (地下)'),
        required=False,
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
        max_length=254,
        widget=forms.Select(
            choices=MANAGEMENT_SCOPE
        ),
        required=False
    )
    land_rights = forms.MultipleChoiceField(
        label=__('土地権利'),
        required=False,
        choices=LAND_RIGHTS,
        initial=[c[0] for c in LAND_RIGHTS],
        widget=forms.CheckboxSelectMultiple()
    )
    area_purpose = forms.CharField(
        label=__('用途地域'),
        max_length=254,
        widget=forms.Select(
            choices=AREA_PURPOSE
        ),
        required=False
    )
    company = forms.CharField(
        label=__('分譲会社'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    constructor_label = forms.CharField(
        label=__('施工会社'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    design_club = forms.CharField(
        label=__('設計会社'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    management_company = forms.CharField(
        label=__('管理会社'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    banners_1 = forms.CharField(
        label=__('物件画像（画像URL1）'),
        max_length=50,
        widget=forms.TextInput(),
        required=False
    )
    banners_2 = forms.CharField(
        label=__('物件画像（画像URL2）'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    banners_3 = forms.CharField(
        label=__('物件画像（画像URL3）'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    banners_4 = forms.CharField(
        label=__('物件画像（画像URL4）'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    google_map = forms.CharField(
        widget=forms.Textarea(),
        required=False,
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
    other_fee = forms.CharField(
        label=__('諸費用'),
        required=False,
        max_length=50,
        widget=forms.TextInput()
    )
    when_to_move_in = forms.DateField(
        label=__('入居時期'),
        required=False,
        initial=datetime.datetime.now,
        widget=forms.DateInput()
    )
    limitations = forms.MultipleChoiceField(
        label=__('その他制限事項'),
        required=False,
        choices=LIMITATIONS,
        initial=[c[0] for c in LIMITATIONS],
        widget=forms.CheckboxSelectMultiple()
    )
    price_full_renovation = forms.IntegerField(
        label=__('フルリノベーション概算価格'),
        required=False,
        widget=forms.NumberInput()
    )
    link_2d = forms.CharField(
        label=__('2D参考プランイメージ'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    link_3d = forms.CharField(
        label=__('3D参考プランイメージ'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    specification_description = forms.CharField(
        label=__('仕様説明'),
        max_length=1000,
        widget=forms.Textarea(),
        required=False
    )

    class Meta:
        document = Buildings
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
