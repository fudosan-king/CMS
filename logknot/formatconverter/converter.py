from .core import Left2RightConverterBase
from dashboard.models import Transports


class NotFoundError(Exception):
    pass


class FromCSVConverter(Left2RightConverterBase):
    def __init__(self):
        super(FromCSVConverter, self).__init__(self.__ruleset__)

    __ruleset__ = 'converter.yaml'

    def converter_building_name(self, val, left, right, rule):
        return '{}'.format(val.replace('\u3000', ' '))

    def converter_structure(self, val, left, right, rule):
        structure = {
            'PC（プレキャストコンクリート）': 'PC',
            'RC（鉄筋コンクリート）': 'RC',
            'RC一部SRC（鉄筋コンクリート一部鉄骨鉄筋コンクリート）': 'RC',
            'SRC（鉄骨鉄筋コンクリート）': 'SRC',
            'SRC一部RC（鉄骨鉄筋コンクリート一部鉄筋コンクリート）': 'SRC',
            'SRC一部S（鉄骨鉄筋コンクリート一部鉄骨）': 'SRC',
            '軽量鉄骨造': '軽量鉄骨造',
            '鉄骨造': '鉄骨'
        }
        return structure.get(val, u'')

    def converter_list(self, val, left, right, rule):
        val = val.split('、')
        return val

    def converter_int(self, val, left, right, rule):
        try:
            val = int(val)
        except:
            val = 0
        return val

    def process_structure(self, rule, left, right):
        structure = left.pop()
        structure_format = {
            'PC（プレキャストコンクリート）': 'PC',
            'RC（鉄筋コンクリート）': 'RC',
            'RC一部SRC（鉄筋コンクリート一部鉄骨鉄筋コンクリート）': 'RC',
            'SRC（鉄骨鉄筋コンクリート）': 'SRC',
            'SRC一部RC（鉄骨鉄筋コンクリート一部鉄筋コンクリート）': 'SRC',
            'SRC一部S（鉄骨鉄筋コンクリート一部鉄骨）': 'SRC',
            '軽量鉄骨造': '軽量鉄骨造',
            '鉄骨造': '鉄骨'
        }
        right.set('structure', structure_format.get(structure, u'その他'))
        right.set('structure_part', structure_format.get(structure, u'その他'))

    def processor_built_date(self, rule, left, right):
        built_date = left.pop().split('年')
        if built_date and len(built_date) == 2:
            right.set('built_date_year', built_date[0])
            right.set('built_date_month', built_date[1].replace('月', ''))

    def process_zipcode(self, rule, left, right):
        zipcode = left.pop().split('-')
        if zipcode and len(zipcode) == 2:
            right.set('zipcode_1', zipcode[0])
            right.set('zipcode_2', zipcode[1])

    def process_address(self, rule, left, right):
        pref = left.pop()
        city = left.pop()
        ooaza = left.pop()
        tyoume_hidden = left.pop().split(u'丁目')

        right.set('address.pref', pref)
        right.set('address.city', city)
        right.set('address.ooaza', ooaza)
        if tyoume_hidden and len(tyoume_hidden) == 2:
            right.set('address.tyoume', u'{}丁目'.format(tyoume_hidden[0]))
            right.set('address.hidden', tyoume_hidden[1])
        elif tyoume_hidden and len(tyoume_hidden) == 1:
            right.set('address.tyoume', u'')
            right.set('address.hidden', tyoume_hidden[0])

    def process_room(self, rule, left, right):
        room = left.pop()
        if room:
            try:
                room_count = room[:1]
            except:
                room_count = 0
            right.set('room_count', room_count)
            right.set('room_kind', room[1:])

    def process_transports(self, rule, left, right):
        transports = []
        for i in range(0, 3):
            transport = Transports()
            transport_company = left.pop().split('/')
            if transport_company and len(transport_company) >= 1:
                transport.transport_company = transport_company[0]
            transport.station_name = left.pop()
            station_to = left.pop()
            mins = left.pop()
            if station_to == '徒歩':
                transport.station_to = 'walk'
                transport.walk_mins = mins
            elif station_to == '徒歩':
                transports.station_to = 'bus'
                transport.bus_walk_mins = mins
            elif station_to == '車':
                transports.station_to = 'car'
                transport.car_mins = mins
            transports.append(transport)

        right.set('transports', transports)
