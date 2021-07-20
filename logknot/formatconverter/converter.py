from .core import Left2RightConverterBase
from dashboard.models import Transports


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
            'RC一部SRC（鉄筋コンクリート一部鉄骨鉄筋コンクリート）': 'RC一部SRC',
            'SRC（鉄骨鉄筋コンクリート）': 'SRC',
            'SRC一部RC（鉄骨鉄筋コンクリート一部鉄筋コンクリート）': 'SRC一部RC',
            'SRC一部S（鉄骨鉄筋コンクリート一部鉄骨）': 'SRC一部S',
            '軽量鉄骨造': '軽量鉄骨造',
            '鉄骨造': '鉄骨造'
        }
        return structure.get(val, u'')

    def converter_land_rights(self, val, left, right, rule):
        val = val.split('、')
        return val

    def processor_built_date(self, rule, left, right):
        built_date = left.pop().split('年')
        if built_date and len(built_date) == 2:
            right.set('built_date_year', built_date[0])
            right.set('built_date_month', built_date[1].replace('月', ''))

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
            station_name = left.pop().split('/')
            if station_name and len(station_name) >= 1:
                transport.station_name = station_name[0]
            transport.station_to = left.pop()
            left.pop()
            transport.walk_mins = left.pop()
            transports.append(transport)

        right.set('transports', transports)
