from .core import Left2RightConverterBase
from dashboard.models import Transports
from dashboard.views import railroad_from_fdk
import datetime

NUM_JP = {
    '0': '０',
    '1': '１',
    '2': '２',
    '3': '３',
    '4': '４',
    '5': '５',
    '6': '６',
    '7': '７',
    '8': '８',
    '9': '９',
}


def covert_boolean(val):
    if val and val == 'False':
        return False
    if val and val == 'True':
        return True
    return False


class FromFDKConverter(Left2RightConverterBase):
    def __init__(self):
        super(FromFDKConverter, self).__init__(self.__ruleset__)

    __ruleset__ = 'import_fdk.yaml'

    def process_address(self, rule, left, right):
        zipcode = left.pop()
        address = {}
        if zipcode:
            zipcode = zipcode.split('-')
            right.set('zipcode_1', zipcode[0])
            right.set('zipcode_2', zipcode[1])
        else:
            right.set('zipcode_1', '000')
            right.set('zipcode_2', '0000')

        address['pref'] = left.pop()
        address['city'] = left.pop()
        address['ooaza'] = left.pop()
        tyoume = left.pop()
        if tyoume:
            tyoume = tyoume.split(u'丁目')
            address['tyoume'] = u'{}丁目'.format(NUM_JP.get(tyoume[0], tyoume[0]))
        address['gaikutiban'] = left.pop()
        right.set('address', address)
        right.set('cache.address', '{}{}{}{}{}'.format(
            address.get('pref'), address.get('city'), address.get('ooaza'),
            address.get('tyoume'), address.get('gaikutiban')
        ))

    def process_transports(self, rule, left, right):
        transports = []
        for idx in range(0, 3):
            val = Transports()
            transport_company = left.pop()
            if transport_company:
                data = railroad_from_fdk(transport_company)
                val.transport_company = data[0]
                val.map_pref = data[1]
            val.station_name = left.pop()
            val.station_to = left.pop()
            val.walk_mins = left.pop()
            val.bus_company = left.pop()
            val.bus_mins = left.pop()
            val.bus_station = left.pop()
            val.bus_walk_mins = left.pop()
            val.car_distance = left.pop()
            val.car_mins = left.pop()
            transports.append(val)
        right.set('transports', transports)

    def process_initial_repeat_fee(self, rule, left, right):
        key = rule.get('key')
        val = {}
        repeat_cost = {}
        val['initial_no'] = covert_boolean(left.pop())
        val['initial_unfixed'] = covert_boolean(left.pop())
        val['initial_cost'] = left.pop()

        repeat_cost['no'] = covert_boolean(left.pop())
        repeat_cost['unfixed'] = covert_boolean(left.pop())
        repeat_cost['price'] = left.pop()
        repeat_cost['per'] = left.pop()

        val['repeat_cost'] = repeat_cost

        right.set(key, val)

    def process_other_fee(self, rule, left, right):
        other_fee = []
        for idx in range(0, 3):
            val = {}
            val['name'] = left.pop()
            val['price'] = left.pop()
            val['per'] = left.pop()
            other_fee.append(val)
        right.get('other_fee', other_fee)

    def process_built_date(self, rule, left, right):
        built_date = left.pop()
        built_date = datetime.datetime.strptime(built_date, '%Y/%m/%d')
        right.set('built_date_year', built_date.year)
        right.set('built_date_month', built_date.month)

    def convert_list(self, val, left, right, rule):
        if val:
            val = val.split('/')
            return(val)
        return []

    def covert_true_false(self, val, left, right, rule):
        return covert_boolean(val)

    def process_carpark_note(self, rule, left, right):
        carpark_note = left.pop()
        right.set('carpark_note', carpark_note.replace(u'.', u','))
