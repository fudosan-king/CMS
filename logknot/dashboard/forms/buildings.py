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
    ('南向き', '南向き'),
]

ROOM_KIND = [
    ('DK', 'DK'),
    ('LDK', 'LDK')
]

LIMITATIONS = [
    ('文化財保護法', '文化財保護法'),
    ('密集市街地整備法', '密集市街地整備法')
]

STRUCTURE = [
    ('RC', 'RC')
]


MANAGEMENT_SCOPE = [
    ('全部委託', '全部委託')
]

LAND_RIGHTS = [
    ('所有権のみ', '所有権のみ')
]

AREA_PURPOSE = [
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
        max_length=254,
        widget=forms.TextInput()
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
        label=__('階建て（地下）'),
        required=False,
        widget=forms.NumberInput()
    )
    built_date = forms.DateField(
        label=__('築年月'),
        required=True,
        initial=datetime.datetime.now,
        widget=forms.DateInput()
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
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    constructor_label = forms.CharField(
        label=__('施工会社'),
        max_length=254,
        widget=forms.TextInput(),
        required=True
    )
    design_club = forms.CharField(
        label=__('設計会社'),
        max_length=254,
        widget=forms.TextInput(),
        required=True
    )
    management_company = forms.CharField(
        label=__('管理会社'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    banners_1 = forms.CharField(
        label=__('物件画像（画像URL1）'),
        max_length=254,
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
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    junior_high_school_district = forms.CharField(
        label=__('中学校学区'),
        max_length=254,
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
        max_length=254,
        widget=forms.Textarea(),
        required=False
    )
    one_stop_price = forms.IntegerField(
        label=__('ワンストップ価格'),
        required=False,
        widget=forms.NumberInput()
    )
    loan_borrowing = forms.IntegerField(
        label=__('ローン借り入れ金額'),
        required=False,
        widget=forms.NumberInput()
    )
    loan_interest_rate = forms.FloatField(
        label=__('ローン金利'),
        required=False,
        min_value=0,
        max_value=30,
        initial=2.0,
        widget=forms.NumberInput(
            attrs={'step': '0.01'}
        )
    )
    loan_repayment_method = forms.CharField(
        label=__('ローン返済方式'),
        max_length=254,
        widget=forms.TextInput(),
        required=False
    )
    repayment_period = forms.IntegerField(
        label=__('返済期間'),
        required=False,
        min_value=0,
        max_value=100,
        initial=25,
        widget=forms.NumberInput()
    )
    monthly_payment = forms.FloatField(
        label=__('月々支払い'),
        required=False,
        widget=forms.NumberInput()
    )
    bonus_payment = forms.FloatField(
        label=__('ボーナス払い'),
        required=False,
        initial=0,
        widget=forms.NumberInput()
    )

    class Meta:
        document = Buildings
        fields = '__all__'
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
