from .core import Left2RightConverterBase


class FromCSVConverter(Left2RightConverterBase):
    def __init__(self):
        super(FromCSVConverter, self).__init__(self.__ruleset__)

    __ruleset__ = 'converter.yaml'

    def converter_building_name(self, val, left, right, rule):
        return '{}'.format(val)
