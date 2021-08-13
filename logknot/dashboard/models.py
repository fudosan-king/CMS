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
    'station_name',
    'station_to',
    'walk_mins',
    'csrfmiddlewaretoken',
    'initial-when_to_move_in',
    'land_rights',
    'limitations',
    'google_map',
    'recommend',
    'map_pref'
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
    map_pref = fields.StringField(max_length=255, blank=True)
    station_name = fields.StringField(max_length=255, blank=True)
    station_to = fields.StringField(max_length=255, blank=True)
    walk_mins = fields.StringField(max_length=255, blank=True)


class Buildings(Document):
    # Default update by system
    created_at = fields.DateTimeField(
        default=datetime.datetime.now, editable=False,
    )
    removed = fields.BooleanField(default=False, blank=True)
    homepage = fields.BooleanField(default=False, blank=True)
    recommend = fields.BooleanField(default=False, blank=True)
    create_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_remove = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    remove_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_update = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    update_by = fields.StringField(max_length=255, default='system', blank=True)
    last_time_rollback = fields.DateTimeField(default=datetime.datetime.now, blank=True)
    rollback_by = fields.StringField(max_length=255, default='system', blank=True)
    import_date = fields.DateTimeField(blank=True)

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
    built_date_year = fields.IntField(blank=False, default=datetime.datetime.now().year)
    built_date_month = fields.IntField(blank=False, default=datetime.datetime.now().month)
    total_houses = fields.StringField(max_length=255, blank=True)
    management_scope = fields.StringField(max_length=255, blank=True)
    land_rights = fields.ListField(
        fields.StringField(max_length=255, blank=True),
        blank=True,
        default=[]
    )
    area_purpose = fields.StringField(max_length=255, blank=True)
    company = fields.StringField(max_length=50, blank=False, default='')
    constructor_label = fields.StringField(max_length=50, blank=True)
    design_club = fields.StringField(max_length=50, blank=True)
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
            for land in land_rights:
                self.land_rights.append(land)

        limitations = request.POST.getlist('limitations')
        self.limitations = []
        if limitations:
            for land in limitations:
                self.limitations.append(land)

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

        self.transports = []
        map_pref = request.POST.getlist('map_pref', [])
        station_name = request.POST.getlist('station_name', [])
        station_to = request.POST.getlist('station_to', [])
        walk_mins = request.POST.getlist('walk_mins', [])
        if station_name:
            for i in range(0, len(station_name)):
                transport = Transports()
                transport.map_pref = map_pref[i]
                transport.station_name = station_name[i]
                transport.station_to = station_to[i]
                transport.walk_mins = walk_mins[i]
                self.transports.append(transport)

        recommend = request.POST.get('recommend')
        if recommend:
            self.recommend = True
        else:
            self.recommend = False

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

        land_rights = request.POST.getlist('land_rights')
        if land_rights:
            self.land_rights = []
            for land in land_rights:
                self.land_rights.append(land)

        limitations = request.POST.getlist('limitations')
        if limitations:
            self.limitations = []
            for land in limitations:
                self.limitations.append(land)

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

        self.transports = []
        map_pref = request.POST.getlist('map_pref', [])
        station_name = request.POST.getlist('station_name', [])
        station_to = request.POST.getlist('station_to', [])
        walk_mins = request.POST.getlist('walk_mins', [])
        if station_name:
            for i in range(0, len(station_name)):
                transport = Transports()
                transport.map_pref = map_pref[i]
                transport.station_name = station_name[i]
                transport.station_to = station_to[i]
                transport.walk_mins = walk_mins[i]
                self.transports.append(transport)

        recommend = request.POST.get('recommend')
        if recommend:
            self.recommend = True
        else:
            self.recommend = False

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
    station_name = fields.ListField(
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

        station_name = request.POST.getlist('station_name')
        if station_name:
            self.station_name = []
            for sn in station_name:
                self.station_name.append(sn)
        return self
