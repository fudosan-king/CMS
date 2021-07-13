from django_mongoengine import Document, EmbeddedDocument, fields  # noqa
import datetime
from mongoengine.queryset.visitor import Q
from django.core.validators import *  # noqa
import html

IGNORE = [
    'path',
    'category',
    'comment',
    'pref',
    'city',
    'ooaza',
    'tyoume',
    'hidden',
    'station_name',
    'station_to',
    'walk_mins',
    'csrfmiddlewaretoken',
    'initial-when_to_move_in',
    'built_date',
    'land_rights',
    'limitations',
    'google_map'
]


class Photos(EmbeddedDocument):
    path = fields.StringField(max_length=255, blank=True)
    category = fields.StringField(max_length=255, blank=True)
    comment = fields.StringField(max_length=255, blank=True)


class Address(EmbeddedDocument):
    pref = fields.StringField(max_length=255, blank=True)
    city = fields.StringField(max_length=255, blank=True)
    ooaza = fields.StringField(max_length=255, blank=True)
    tyoume = fields.StringField(max_length=255, blank=True)
    hidden = fields.StringField(max_length=255, blank=True)


class Transports(EmbeddedDocument):
    station_name = fields.StringField(max_length=255, blank=True)
    station_to = fields.StringField(max_length=255, blank=True)
    walk_mins = fields.StringField(max_length=255, blank=True)


class Buildings(Document):
    # Default update by system
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    removed = fields.BooleanField(default=False, blank=True)
    create_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_remove = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    remove_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_update = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    update_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_rollback = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    rollback_by = fields.StringField(max_length=255, default='system', blank=True)

    # Update by form
    building_name = fields.StringField(max_length=50)
    photos = fields.ListField(
        fields.EmbeddedDocumentField('Photos'),
        blank=True,
        default=[]
    )
    address = fields.DictField(blank=True, default={})
    structure = fields.StringField(max_length=255, blank=False, default='')
    ground_floors = fields.IntField(blank=False, default=0)
    underground_floors = fields.StringField(blank=True)
    built_date = fields.DateField(blank=False, default=datetime.datetime.now)
    total_houses = fields.StringField(max_length=255, blank=True)
    management_scope = fields.StringField(max_length=255, blank=True)
    land_rights = fields.ListField(
        fields.StringField(max_length=255, blank=True),
        blank=True,
        default=[]
    )
    area_purpose = fields.StringField(max_length=255, blank=True)
    company = fields.StringField(max_length=50, blank=False, default='')
    constructor_label = fields.StringField(max_length=50, blank=False, default='')
    design_club = fields.StringField(max_length=50, blank=False, default='')
    management_company = fields.StringField(max_length=50, blank=True, defaul='')
    banners_1 = fields.StringField(max_length=255, blank=True)
    banners_2 = fields.StringField(max_length=255, blank=True)
    banners_3 = fields.StringField(max_length=255, blank=True)
    banners_4 = fields.StringField(max_length=255, blank=True)
    google_map = fields.StringField(max_length=1000, blank=True, default='')
    google_map_lat = fields.StringField(max_length=20, blank=True)
    google_map_lng = fields.StringField(max_length=20, blank=True)
    google_map_yaw = fields.StringField(max_length=255, blank=True)
    google_map_pitch = fields.StringField(max_length=255, blank=True)
    google_map_zoom = fields.StringField(max_length=255, blank=True)
    transports = fields.ListField(
        fields.EmbeddedDocumentField('Transports'),
        blank=True,
        default=[]
    )
    elementary_school_district = fields.StringField(max_length=100, blank=True)
    junior_high_school_district = fields.StringField(max_length=100, blank=True)
    price = fields.StringField(max_length=255, blank=True)
    tatemono_menseki = fields.StringField(max_length=255, blank=True)
    balcony_space = fields.IntField(blank=False, default=0)
    room_floor = fields.StringField(max_length=255, blank=True)
    direction = fields.StringField(max_length=255, blank=True)
    room_count = fields.StringField(max_length=255, blank=True)
    room_kind = fields.StringField(max_length=255, blank=True, default='')
    management_fee = fields.StringField(max_length=255, blank=True)
    repair_reserve_fee = fields.StringField(max_length=255, blank=True)
    other_fee = fields.StringField(max_length=50, blank=True, default='')
    when_to_move_in = fields.DateField(default=datetime.datetime.now, blank=True)
    limitations = fields.ListField(
        fields.StringField(max_length=255, blank=True),
        blank=True,
        default=[]
    )
    price_full_renovation = fields.StringField(max_length=255, blank=True)
    link_2d = fields.StringField(max_length=255, blank=True)
    link_3d = fields.StringField(max_length=255, blank=True)
    specification_description = fields.StringField(max_length=1000, blank=True)
    one_stop_price = fields.StringField(max_length=255, blank=True)
    loan_borrowing = fields.StringField(max_length=255, blank=True)
    loan_interest_rate = fields.DecimalField(max_digits=2, decimal_places=2)
    loan_repayment_method = fields.StringField(max_length=255, blank=True)
    repayment_period = fields.IntField(blank=False, default=25)
    monthly_payment = fields.StringField(max_length=255, blank=True)
    bonus_payment = fields.StringField(max_length=255, blank=True)

    @staticmethod
    def building_name_validation(building_name):
        if not building_name:
            raise ValidationError('Not have building name')

    def clean(self):
        self.building_name_validation(self.building_name)

    def query(self, request, removed=False):
        q = Q(removed=removed)
        if request.GET.get('building_name', None):
            q &= Q(building_name=request.GET.get('building_name', None))
        return q

    def update(self, request):
        for k, v in request.POST.items():
            if k not in IGNORE:
                self.__setitem__(k, request.POST.get(k))

        self.last_time_update = datetime.datetime.now
        self.update_by = str(request.user)
        self.photos = []
        path = request.POST.getlist('path', [])
        category = request.POST.getlist('category', [])
        comment = request.POST.getlist('comment', [])
        if path:
            for i in range(0, len(path)):
                photos = Photos()
                photos.path = path[i]
                if category and len(category):
                    photos.category = category[i]
                if comment and len(comment):
                    photos.comment = comment[i]
                self.photos.append(photos)

        land_rights = request.POST.getlist('land_rights')
        self.land_rights = []
        if land_rights:
            for l in land_rights:
                self.land_rights.append(l)

        limitations = request.POST.getlist('limitations')
        self.limitations = []
        if limitations:
            for l in limitations:
                self.limitations.append(l)

        google_map = request.POST.get('google_map')
        if google_map:
            self.google_map = html.unescape(google_map)

        address = Address()
        address.pref = request.POST.get('pref', '')
        address.city = request.POST.get('city', '')
        address.ooaza = request.POST.get('ooaza', '')
        address.tyoume = request.POST.get('tyoume', '')
        address.hidden = request.POST.get('hidden', '')
        self.address = {
            'pref': address.pref,
            'city': address.city,
            'ooaza': address.ooaza,
            'tyoume': address.tyoume,
            'hidden': address.hidden,
        }

        return self

    def remove(self, request):
        self.removed = True
        self.last_time_remove = datetime.datetime.now
        self.remove_by = str(request.user)
        return self

    def add(self, request):
        for k, v in request.POST.items():
            if k not in IGNORE:
                self.__setitem__(k, request.POST.get(k))

        if request.POST.get('built_date'):
            self.built_date = datetime.datetime.strptime(
                '{}'.format(request.POST.get('built_date')),
                '%Y-%m-%d'
            )

        land_rights = request.POST.getlist('land_rights')
        if land_rights:
            self.land_rights = []
            for l in land_rights:
                self.land_rights.append(l)

        limitations = request.POST.getlist('limitations')
        if limitations:
            self.limitations = []
            for l in limitations:
                self.limitations.append(l)

        google_map = request.POST.get('google_map')
        if google_map:
            self.google_map = html.unescape(google_map)

        address = Address()
        address.pref = request.POST.get('pref', '')
        address.city = request.POST.get('city', '')
        address.ooaza = request.POST.get('ooaza', '')
        address.tyoume = request.POST.get('tyoume', '')
        address.hidden = request.POST.get('hidden', '')
        self.address = {
            'pref': address.pref,
            'city': address.city,
            'ooaza': address.ooaza,
            'tyoume': address.tyoume,
            'hidden': address.hidden,
        }

        self.create_by = str(request.user)
        return self
