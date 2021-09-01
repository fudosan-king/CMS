from django_mongoengine import Document, EmbeddedDocument, fields  # noqa
import datetime
from mongoengine.queryset.visitor import Q
from django.core.validators import ValidationError
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
    'transport_company',
    'station_name',
    'station_to',
    'walk_mins',
    'bus_company',
    'bus_mins',
    'bus_station',
    'bus_walk_mins',
    'car_distance',
    'car_mins',
    'csrfmiddlewaretoken',
    'initial-when_to_move_in',
    'limitations',
    'google_map',
    'recommend',
    'map_pref',
    'usen_fee-initial_cost',
    'usen_fee-repeat_cost-price',
    'usen_fee-repeat_cost-per',
    'usen_fee-initial_unfixed',
    'usen_fee-initial_no',
    'usen_fee-repeat_cost-unfixed',
    'usen_fee-repeat_cost-no',
    'internet_fee-initial_cost',
    'internet_fee-repeat_cost-price',
    'internet_fee-repeat_cost-per',
    'internet_fee-initial_unfixed',
    'internet_fee-initial_no',
    'internet_fee-repeat_cost-unfixed',
    'internet_fee-repeat_cost-no',
    'catv_fee-initial_cost',
    'catv_fee-repeat_cost-price',
    'catv_fee-repeat_cost-per',
    'catv_fee-initial_unfixed',
    'catv_fee-initial_no',
    'catv_fee-repeat_cost-unfixed',
    'catv_fee-repeat_cost-no',
    'spa_tags',
    'spa-repeat_cost-price',
    'spa-repeat_cost-per',
    'spa-repeat_cost-unfixed',
    'rights_fee-no_fee',
    'rights_fee-fee',
    'guarantee_fee-no_fee',
    'guarantee_fee-fee',
    'deposit_fee-fee',
    'deposit_fee-no_fee',
    'community_fee-repeat_cost-unfixed',
    'community_fee-repeat_cost-price',
    'community_fee-repeat_cost-per',
    'other_fee-name',
    'other_fee-price',
    'other_fee-per-1',
    'other_fee-per-2',
    'other_fee-per-3',
    'area_purpose-main',
    'area_purpose-sub',
    'law43-type',
    'law43-comment',
    'features',
]


def set_transport(field, index):
    if len(field) >= index + 1:
        return field[index]
    else:
        return ''


def get_fee(field, request):
    initial_cost = request.POST.get('{}-initial_cost'.format(field), '')
    initial_no = request.POST.get('{}-initial_no'.format(field), False)
    if initial_no:
        initial_no = True
    initial_unfixed = request.POST.get('{}-initial_unfixed'.format(field), False)
    if initial_unfixed:
        initial_unfixed = True
    repeat_cost = {}
    repeat_cost['price'] = request.POST.get('{}-repeat_cost-price'.format(field), '')
    repeat_cost_unfixed = request.POST.get('{}-repeat_cost-unfixed'.format(field), False)
    if repeat_cost_unfixed:
        repeat_cost_unfixed = True
    repeat_cost['unfixed'] = repeat_cost_unfixed
    repeat_cost_no = request.POST.get('{}-repeat_cost-no'.format(field), False)
    if repeat_cost_no:
        repeat_cost_no = True
    repeat_cost['no'] = repeat_cost_no
    repeat_cost['per'] = request.POST.get('{}-repeat_cost-per'.format(field), 'm')
    data = {
        'initial_cost': initial_cost,
        'initial_no': initial_no,
        'repeat_cost': repeat_cost,
        'initial_unfixed': initial_unfixed
    }
    return data


def get_repeat_cost(field, request):
    repeat_cost_unfixed = request.POST.get('{}-unfixed'.format(field), False)
    if repeat_cost_unfixed:
        repeat_cost_unfixed = True
    repeat_cost_per = request.POST.get('{}-per'.format(field), 'm')
    repeat_cost_price = request.POST.get('{}-price'.format(field), '')
    data = {
        'price': repeat_cost_price,
        'unfixed': repeat_cost_unfixed,
        'per': repeat_cost_per
    }
    return data


def get_fee_per(field, request):
    rights_fee_no_fee = request.POST.get('{}-no_fee'.format(field), '無')
    rights_fee_fee = request.POST.get('{}-fee'.format(field), '')
    data = {
        'fee': rights_fee_fee,
        'no_fee': rights_fee_no_fee
    }
    return data


class Photos(EmbeddedDocument):
    path = fields.StringField(max_length=100, blank=True)
    category = fields.StringField(max_length=20, blank=True)
    comment = fields.StringField(max_length=100, blank=True)


class Address(EmbeddedDocument):
    pref = fields.StringField(max_length=20, blank=False)
    city = fields.StringField(max_length=20, blank=False)
    ooaza = fields.StringField(max_length=20, blank=False)
    tyoume = fields.StringField(max_length=20, blank=True)
    hidden = fields.StringField(max_length=20, blank=True)


class Transports(EmbeddedDocument):
    map_pref = fields.StringField(max_length=20, blank=True)
    transport_company = fields.StringField(max_length=20, blank=True)
    station_name = fields.StringField(max_length=20, blank=True)
    station_to = fields.StringField(max_length=20, blank=True)
    walk_mins = fields.StringField(max_length=20, blank=True)
    bus_company = fields.StringField(max_length=20, blank=True)
    bus_mins = fields.StringField(max_length=20, blank=True)
    bus_station = fields.StringField(max_length=20, blank=True)
    bus_walk_mins = fields.StringField(max_length=20, blank=True)
    car_distance = fields.StringField(max_length=20, blank=True)
    car_mins = fields.StringField(max_length=20, blank=True)


class OtherFee(EmbeddedDocument):
    fee = fields.DictField(blank=True, default={})
    name = fields.StringField(max_length=20, blank=True)


class Buildings(Document):
    # Default update by system
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    removed = fields.BooleanField(default=False, blank=True)
    homepage = fields.BooleanField(default=False, blank=True)
    recommend = fields.BooleanField(default=False, blank=True)
    create_by = fields.StringField(max_length=20, default='system', blank=True)
    last_time_remove = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    remove_by = fields.StringField(max_length=20, default='system', blank=True)
    last_time_update = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    update_by = fields.StringField(max_length=20, default='system', blank=True)
    last_time_rollback = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    rollback_by = fields.StringField(max_length=20, default='system', blank=True)
    import_date = fields.DateTimeField(blank=True)

    # Update by form
    estate_subtype = fields.StringField(max_length=20, default='マンション')
    building_name = fields.StringField(max_length=50)
    building_name_kana = fields.StringField(max_length=50, blank=True)
    zipcode_1 = fields.StringField(max_length=3)
    zipcode_2 = fields.StringField(max_length=4)
    photos = fields.ListField(
        fields.EmbeddedDocumentField('Photos'),
        blank=True,
        default=[]
    )
    address = fields.DictField(blank=False)
    cache = fields.DictField(blank=False)
    structure = fields.StringField(max_length=20, blank=False, default='')
    structure_part = fields.StringField(max_length=20, blank=True, default='')
    ground_floors = fields.IntField(blank=False, default=0)
    underground_floors = fields.IntField(blank=True, default=0)
    building_confirmation_number = fields.StringField(max_length=50, blank=True)
    built_date_year = fields.IntField(blank=False, default=datetime.datetime.now().year)
    built_date_month = fields.IntField(blank=False, default=datetime.datetime.now().month)
    total_houses = fields.StringField(max_length=20, blank=True)
    management_scope = fields.StringField(max_length=20, blank=False)
    superintendent = fields.StringField(max_length=10, blank=True)
    land_rights = fields.StringField(max_length=10, blank=False)
    waterworks = fields.StringField(max_length=50, blank=True)
    sewer = fields.StringField(max_length=50, blank=True)
    gas = fields.StringField(max_length=50, blank=True)
    land_law_report = fields.StringField(max_length=50, blank=False, default='要')
    area_purpose = fields.DictField(blank=True, default={})
    constructor_label = fields.StringField(max_length=50, blank=True)
    constructor = fields.StringField(max_length=100, blank=True)
    management_company = fields.StringField(max_length=50, blank=True, defaul='')

    carpark_type = fields.StringField(max_length=20, blank=True)
    carpark_space = fields.StringField(max_length=20, blank=True)
    carpark_space_cars = fields.StringField(max_length=20, blank=True)
    carpark_place = fields.StringField(max_length=20, blank=True)
    carpark_fee_min = fields.StringField(max_length=20, blank=True)
    carpark_fee_per = fields.StringField(max_length=20, blank=True)
    carpark_fee_tax_inc = fields.StringField(max_length=20, blank=True)
    carpark_note = fields.StringField(max_length=100, blank=True)

    bike_park = fields.StringField(max_length=20, blank=True)
    bike_park_price = fields.StringField(max_length=20, blank=True)
    bike_park_price_per = fields.StringField(max_length=20, blank=True)
    bicycles_park = fields.StringField(max_length=20, blank=True)
    bicycles_park_price = fields.StringField(max_length=20, blank=True)
    bicycles_park_price_per = fields.StringField(max_length=20, blank=True)

    usen_fee = fields.DictField(blank=True, default={})
    internet_fee = fields.DictField(blank=True, default={})
    catv_fee = fields.DictField(blank=True, default={})
    community_fee_type = fields.StringField(max_length=255, blank=True)
    community_fee = fields.DictField(blank=True, default={})
    other_fee = fields.ListField(
        fields.EmbeddedDocumentField('OtherFee'),
        blank=True,
        default=[]
    )
    rights_fee = fields.DictField(blank=True, default={})
    guarantee_fee = fields.DictField(blank=True, default={})
    deposit_fee = fields.DictField(blank=True, default={})
    spa_type = fields.StringField(max_length=20, blank=True, default='')
    spa_fee = fields.DictField(blank=True, default={})
    spa_tags = fields.ListField(
        fields.StringField(max_length=20, blank=True),
        blank=True,
        default=[]
    )
    guarantee_fee_depreciation = fields.StringField(max_length=20, blank=True, default='')

    google_map = fields.StringField(max_length=1000, blank=True, default='')
    google_map_lat = fields.StringField(max_length=20, blank=True)
    google_map_lng = fields.StringField(max_length=20, blank=True)
    google_map_yaw = fields.StringField(max_length=20, blank=True)
    google_map_pitch = fields.StringField(max_length=20, blank=True)
    google_map_zoom = fields.StringField(max_length=20, blank=True)
    transports = fields.ListField(
        fields.EmbeddedDocumentField('Transports'),
        blank=True,
        default=[]
    )
    elementary_school_district = fields.StringField(max_length=100, blank=True)
    junior_high_school_district = fields.StringField(max_length=100, blank=True)
    price = fields.StringField(max_length=20, blank=True)
    tatemono_menseki = fields.StringField(max_length=20, blank=True)
    balcony_space = fields.IntField(blank=False, default=0)
    room_floor = fields.StringField(max_length=20, blank=True)
    direction = fields.StringField(max_length=20, blank=True)
    room_count = fields.StringField(max_length=20, blank=True)
    room_kind = fields.StringField(max_length=20, blank=True, default='')
    management_fee = fields.StringField(max_length=20, blank=True)
    repair_reserve_fee = fields.StringField(max_length=20, blank=True)
    when_to_move_in = fields.DateField(default=datetime.datetime.now, blank=True)
    limitations = fields.ListField(
        fields.StringField(max_length=20, blank=True),
        blank=True,
        default=[]
    )
    limitations_etc = fields.StringField(max_length=60, blank=True)
    law43 = fields.DictField(blank=True, default={})
    price_full_renovation = fields.StringField(max_length=20, blank=True)
    link_2d = fields.StringField(max_length=100, blank=True)
    link_3d = fields.StringField(max_length=100, blank=True)
    specification_description = fields.StringField(max_length=1000, blank=True)
    features = fields.ListField(
        fields.StringField(max_length=20, blank=True),
        blank=True,
        default=[]
    )

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

    @staticmethod
    def update_data(data, request):
        for k, v in request.POST.items():
            if k not in IGNORE:
                try:
                    data.__setitem__(k, request.POST.get(k))
                except Exception as e:
                    print('Please check input: {}'.format(e))
                    continue

        limitations = request.POST.getlist('limitations')
        data.limitations = []
        if limitations:
            for land in limitations:
                data.limitations.append(land)

        google_map = request.POST.get('google_map')
        if google_map:
            data.google_map = html.unescape(google_map)

        address = Address()
        address.pref = request.POST.get('pref', None)
        address.city = request.POST.get('city', None)
        address.ooaza = request.POST.get('ooaza', None)
        address.tyoume = request.POST.get('tyoume', '')
        address.hidden = request.POST.get('hidden', '')
        if address.pref and address.city and address.ooaza:
            data.address = {
                'pref': address.pref,
                'city': address.city,
                'ooaza': address.ooaza,
                'tyoume': address.tyoume,
                'hidden': address.hidden,
            }
            data['cache']['address'] = '{}{}{}{}{}'.format(
                address.pref, address.city, address.ooaza, address.tyoume, address.hidden
            )

        data.transports = []
        map_pref = request.POST.getlist('map_pref', [])
        transport_company = request.POST.getlist('transport_company', [])
        station_name = request.POST.getlist('station_name', [])
        station_to = request.POST.getlist('station_to', [])
        walk_mins = request.POST.getlist('walk_mins', [])
        bus_company = request.POST.getlist('bus_company', [])
        bus_mins = request.POST.getlist('bus_mins', [])
        bus_station = request.POST.getlist('bus_station', [])
        bus_walk_mins = request.POST.getlist('bus_walk_mins', [])
        car_distance = request.POST.getlist('car_distance', [])
        car_mins = request.POST.getlist('car_mins', [])

        if transport_company:
            for i in range(0, len(transport_company)):
                transport = Transports()
                transport.map_pref = set_transport(map_pref, i)
                transport.transport_company = set_transport(transport_company, i)
                transport.station_name = set_transport(station_name, i)
                transport.station_to = set_transport(station_to, i)
                transport.walk_mins = set_transport(walk_mins, i)
                transport.bus_company = set_transport(bus_company, i)
                transport.bus_mins = set_transport(bus_mins, i)
                transport.bus_station = set_transport(bus_station, i)
                transport.bus_walk_mins = set_transport(bus_walk_mins, i)
                transport.car_distance = set_transport(car_distance, i)
                transport.car_mins = set_transport(car_mins, i)
                data.transports.append(transport)

        data.usen_fee = get_fee('usen_fee', request)
        data.internet_fee = get_fee('internet_fee', request)
        data.catv_fee = get_fee('catv_fee', request)

        spa_tags = request.POST.getlist('spa_tags', [])
        data.spa_tags = []
        data.spa_tags.extend(spa_tags)
        data.spa_fee = get_repeat_cost('spa-repeat_cost', request)
        data.community_fee = get_repeat_cost('community_fee-repeat_cost', request)
        data.rights_fee = get_fee_per('rights_fee', request)
        data.guarantee_fee = get_fee_per('guarantee_fee', request)
        data.deposit_fee = get_fee_per('deposit_fee', request)

        other_fee_name = request.POST.getlist('other_fee-name', [])
        other_fee_price = request.POST.getlist('other_fee-price', [])
        data.other_fee = []
        for i in range(0, 3):
            other_fee = OtherFee()
            try:
                price = other_fee_price[i]
            except:
                price = ''
            other_fee.fee = {
                'price': price,
                'per': request.POST.get('other_fee-per-{}'.format(i + 1), 'm')
            }
            try:
                name = other_fee_name[i]
            except:
                name = ''
            other_fee.name = name
            data.other_fee.append(other_fee)

        area_purpose_main = request.POST.get('area_purpose-main', '')
        area_purpose_sub = request.POST.get('area_purpose-sub', '')
        data.area_purpose = {
            'main': area_purpose_main,
            'sub': area_purpose_sub
        }

        law43_type = request.POST.get('law43-type', '')
        law43_comment = request.POST.get('law43-comment', '')[:60]
        data.law43 = {
            'type': law43_type,
            'comment': law43_comment
        }

        data.features = request.POST.getlist('features', [])

        recommend = request.POST.get('recommend', False)
        if recommend:
            recommend = True
        data.recommend = recommend

        return data

    def update(self, request):
        self = self.update_data(self, request)
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

        return self

    def remove(self, request):
        self.removed = True
        self.last_time_remove = datetime.datetime.now
        self.remove_by = str(request.user)
        return self

    def add(self, request):
        self = self.update_data(self, request)
        self.create_by = str(request.user)
        return self

    def get_photo_first(self):
        for photo in self.photos:
            if photo and photo.path:
                return photo.path
        return '/static/images/no-image.png'


class LogsImport(Document):
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    import_done = fields.DictField(blank=True, default={})
    ignore_buildings = fields.DictField(blank=True, default={})
    import_fail = fields.ListField(blank=True, default=[])
    import_by = fields.StringField(max_length=255, blank=True, defaul='system')


class CountInfoBuildings(Document):
    city = fields.DictField(blank=True, default={})
    station = fields.DictField(blank=True, default={})


class SearchSortByPref(Document):
    pref = fields.StringField(max_length=20, blank=False)
    city = fields.ListField(
        fields.StringField(max_length=255, blank=True),
        blank=True,
        default=[]
    )
    transport_company = fields.ListField(
        fields.StringField(max_length=255, blank=True),
        blank=True,
        default=[]
    )

    def update(self, request):
        city = request.POST.getlist('city')
        if city:
            self.city = []
            for ct in city:
                self.city.append(ct)

        transport_company = request.POST.getlist('transport_company')
        if transport_company:
            self.transport_company = []
            for sn in transport_company:
                self.transport_company.append(sn)
        return self
