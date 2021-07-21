from bson import ObjectId
import yaml
import re
import sys
import itertools
import os
import warnings
from .helpers import *  # noqa

basepath = os.path.dirname(os.path.abspath(__file__))

VALID_RULES = frozenset([
    'index', 'check_index', 'map', 'converter', 'processor',
    'key', 'type', 'default', 'max_bytes', 'if', 'true', 'false', 'max_chars',
    'match', 'format', 'repeat', 'rules', 'nrepeat', 'r2l_map', 'multiplier', 'args', 'has',
    'switch', 'mapr', 'if_r2l', 'if_l2r', 'if_estate_type', 'limit_characters',
    'check',
    True, False])

ALLOW_CRLF = 0
ESCAPE_CRLF = 1
CLEAR_CRLF = 2
ALLOW_LF = 3
ALLOW_CRLF_WINDOWS = 4


def trim_string(source, encoding, maxlength, append_tail_ellipsis=False):
    assert isinstance(maxlength, int)
    if not isinstance(source, unicode):
        source = source.decode(encoding)

    s = source
    tail = len(s)
    while tail:
        current_length = len(s.encode(encoding))
        if current_length <= maxlength:
            break

        tail = max(0, tail - max((current_length - maxlength) / 3, 1))
        s = source[:tail]
        if append_tail_ellipsis:
            s += u'…'
    return s


class InvalidDataException(Exception):
    pass


class DataConverterBase(object):
    def convert_l2r(self, val, left, right, rule):
        raise NotImplementedError

    def convert_r2l(self, val, right, rule):
        raise NotImplementedError


class BoolConverter(DataConverterBase):
    def convert_l2r(self, val, left, right, rule):
        return True if val == '1' else False

    def convert_r2l(self, val, right, rule):
        return '1' if val else '0'


class IntegerConverter(DataConverterBase):
    def convert_l2r(self, val, left, right, rule):
        if not val:
            return None
        val = int(val, 10)
        if 'multiplier' in rule:
            val /= rule['multiplier']
        return val

    def convert_r2l(self, val, right, rule):
        if val is None or val == '':
            return None
        if 'multiplier' in rule:
            val *= rule['multiplier']
        return '%d' % val


class IntegerConverterZero(IntegerConverter):
    def convert_r2l(self, val, right, rule):
        if val is None or val == '':
            return '0'
        if 'multiplier' in rule:
            val *= rule['multiplier']
        return '%d' % val


class FloatConverter(DataConverterBase):
    def convert_l2r(self, source, left, right, rule):
        val = source.strip()
        if not val:
            return None

        try:
            val = float(val)
        except ValueError:
            print(sys.stderr, 'convert to string failed {!r}'.format(val))
            raise

        if 'multiplier' in rule:
            val /= rule['multiplier']
        return val

    def convert_r2l(self, val, right, rule):
        if val is None or val == '':
            return None

        if 'multiplier' in rule:
            val *= rule['multiplier']
        if 'format' in rule:
            try:
                return rule['format'].format(val)
            except:
                print('format error', rule, repr(val))
                raise
        return str(val)


class DefaultConverter(DataConverterBase):
    def convert_l2r(self, val, left, right, rule):
        return val

    def convert_r2l(self, val, right, rule):
        if val is None or val == '':
            return None

        if 'format' in rule:
            format = rule['format']
            if isinstance(val, list):
                return format.format(*val)
            return format.format(val)
        if isinstance(val, str):
            return val
        return str(val)


class RegexConverter(DataConverterBase):
    def convert_l2r(self, val, left, right, rule):
        if not val:
            return None

        mo = re.match(rule['match'], val)
        if not mo:
            val = None

        if val and 'format' in rule:
            val = str(val).format(*mo.groups())
        return val

    def convert_r2l(self, val, right, rule):
        if not val:
            return None

        mo = re.match(rule['match'], val)
        if not mo:
            # raise ValueError('not match %r (expecet %r)' % (val, rule['match']))
            return None

        if 'format' in rule:
            val = str(val).format(*mo.groups())
        return val

type_converters = {
    'default': DefaultConverter(),
    'boolean': BoolConverter(),
    'integer': IntegerConverter(),
    'integer_zero': IntegerConverterZero(),
    'float': FloatConverter(),
    'regex': RegexConverter()
}


class FlexRow(list):
    def __init__(self, row=None, encoding='cp932', allow_crlf=ALLOW_CRLF):
        super(FlexRow, self).__init__()
        if row:
            super(FlexRow, self).extend(row)

        self.cursor = 0
        self.encoding = encoding
        self.allow_crlf = allow_crlf
        self.media = []
        self.xml = False

    def finalize(self):
        while len(self) < self.cursor:
            super(FlexRow, self).append(None)

    def append(self, val, max_bytes=None, max_chars=None, append_tail_ellipsis=False):
        if self.allow_crlf != ALLOW_CRLF:
            if isinstance(val, str):
                if self.allow_crlf == ESCAPE_CRLF:
                    val = val.replace(u'\r\n', '\\n').replace(u'\n', u'\\n')
                elif self.allow_crlf == CLEAR_CRLF:
                    val = val.replace(u'\r\n', u' ').replace(u'\n', u' ')
                elif self.allow_crlf == ALLOW_LF:
                    val = val.replace(u'\r', u'')
                elif self.allow_crlf == ALLOW_CRLF_WINDOWS:
                    # only '\r\n' or '\n'
                    # replace all '\r\n' -> '\n', '\n' -> '\n'
                    # replace '\n' -> '\r\n'
                    val = val.replace(u'\r\n', u'\n').replace(u'\n', u'\r\n')

        if isinstance(val, unicode):
            val = val.strip().encode(self.encoding, 'replace')
        elif isinstance(val, str):
            val = val.strip()

        if max_bytes and val and len(val) > max_bytes:
            print('bytes exceeded {} > {}'.format(max_bytes, len(val)))
            val = trim_string(val, self.encoding, max_bytes, append_tail_ellipsis=append_tail_ellipsis)

        if max_chars and val and len(val) > max_chars:
            print('characters exceeded {} > {}'.format(max_chars, len(val)))
            val = val[:max_chars]

        if self.cursor < len(self):
            assert self[self.cursor] is None, '{}:{!r}'.format(self.cursor, self[self.cursor])
            super(FlexRow, self).__setitem__(self.cursor, val)
        else:
            while len(self) < self.cursor:
                super(FlexRow, self).append(None)
            assert len(self) == self.cursor
            super(FlexRow, self).append(val)
        self.cursor += 1

    def extend(self, val):
        for x in val:
            self.append(x)

    def move_to(self, new_pos):
        self.cursor = new_pos

    def pop_raw(self):
        if len(self) > self.cursor:
            val = self[self.cursor]
        else:
            val = ''
        self.cursor += 1
        return val

    def pop(self):
        return self.pop_raw()

    def pop_integer(self):
        v = self.pop_raw()
        if not v:
            return None
        return int(v, 10)

    def pop_float(self):
        v = self.pop_raw()
        if not v:
            return None
        return float(v)

    def push_media(self, filename, media_id):
        self.media.append((filename, ObjectId(media_id)))

    def __setitem__(self, idx, val):  # noqa
        while idx >= len(self):
            super(FlexRow, self).append(None)
        super(FlexRow, self).__setitem__(idx, val)


class RightBuilder(dict):
    def __init__(self):
        self.images = []

    def set(self, key, val):
        d = self
        key = key.split('.')
        for k in key[:-1]:
            d.setdefault(k, {})
            d = d[k]
        d[key[-1]] = val

    def append(self, key, val):
        d = self
        key = key.split('.')
        for k in key[:-1]:
            d.setdefault(k, {})
            d = d[k]
        d.setdefault(key[-1], [])
        d[key[-1]].append(val)


class Ruleset(object):
    def __init__(self, filename):
        filepath = os.path.join(basepath, filename)
        try:
            ruledata = yaml.load(open(filepath, 'r'), Loader=yaml.CLoader)
        except:
            ruledata = yaml.load(open(filepath, 'r'))
        self.strict = False
        self.load_rule(ruledata)
        self.ruledata = ruledata
        self.maps = {}

    def load_rule(self, ruledata):
        self.direction = ruledata['direction']
        if self.direction not in ('l2r', 'r2l', 'both'):
            raise ValueError('invalid direction rule')

        self.rules = ruledata['rules']
        self.encoding = ruledata.get('encoding', 'utf8')
        self.strict = True if ruledata.get('strict') else False

    def get_map(self, key):
        if key not in self.maps:
            self.maps[key] = sanitize_dict(self.ruledata['maps'][key])
        return self.maps[key]

    @property
    def allow_crlf(self):
        allow_crlf = self.ruledata.get('allow_crlf', CLEAR_CRLF)
        if allow_crlf is None:
            allow_crlf = CLEAR_CRLF
        assert allow_crlf in (ALLOW_CRLF, CLEAR_CRLF, ESCAPE_CRLF, ALLOW_LF, ALLOW_CRLF_WINDOWS)
        return allow_crlf


class JSonRow(list):
    def __init__(self, row=None, encoding=None, allow_crlf=ALLOW_CRLF):
        self.cursor = 0
        self.encoding = encoding
        self.allow_crlf = allow_crlf
        self.xml = True
        self.media = []

        super(JSonRow, self).__init__()

    def finalize(self):
        """終了処理"""
        # cursorがlenより先立ったらNoneを詰める
        while len(self) < self.cursor:
            super(JSonRow, self).append(None, None)

    def append(self, key, val, max_bytes=None, max_chars=None):
        if isinstance(key, (tuple, list)):
            assert len(key) == len(val)
            for k, v in itertools.izip(key, val):
                self._append(k, v)
        else:
            self._append(key, val, max_bytes, max_chars)

    def _append(self, key, val, max_bytes=None, max_chars=None):
        if self.allow_crlf != ALLOW_CRLF:
            if isinstance(val, str):
                if self.allow_crlf == ESCAPE_CRLF:
                    val = val.replace(u'\r\n', '\\n').replace(u'\n', u'\\n')
                elif self.allow_crlf == CLEAR_CRLF:
                    val = val.replace(u'\r\n', u' ').replace(u'\n', u' ')

        if isinstance(val, unicode):
            val = val.strip().encode(self.encoding, 'replace')
        elif isinstance(val, str):
            val = val.strip()

        if max_bytes and val and len(val) > max_bytes:
            val = trim_string(val, self.encoding, max_bytes)

        if max_chars and val and len(val) > max_chars:
            val = val[:max_chars]

        if self.cursor < len(self):
            assert self[self.cursor] is None
            super(JSonRow, self).__setitem__(self.cursor, val)
        else:
            while len(self) < self.cursor:
                super(JSonRow, self).append((key, None))
            assert len(self) == self.cursor
            super(JSonRow, self).append((key, val))
        self.cursor += 1

    def move_to(self, new_pos):
        self.cursor = new_pos

    def pop_raw(self):
        if len(self) > self.cursor:
            val = self[self.cursor]
        else:
            val = ''
        self.cursor += 1
        return val

    def push_media(self, filename, media_id):
        self.media.append((filename, ObjectId(media_id)))

    def __setitem__(self, idx, val):  # noqa
        while idx >= len(self):
            super(JSonRow, self).append(None)
        super(JSonRow, self).__setitem__(idx, val)


class ConverterBase(object):
    encoding = 'cp932'

    def __init__(self, ruleset, direction):
        if isinstance(ruleset, str):
            ruleset = Ruleset(ruleset)
        self.ruleset = ruleset
        self.direction = direction

        if self.ruleset.direction not in (self.direction, 'both'):
            raise ValueError('%s direction not supported', direction)

    def get_map(self, map_or_key):
        if isinstance(map_or_key, dict):
            return sanitize_dict(map_or_key)
        else:
            return self.ruleset.get_map(map_or_key)

    def process_rule(self, rule, left, right):
        if isinstance(rule, str):
            if rule == 'pass':
                left.cursor += 1
                return
            raise ValueError('invalid rule {!r}'.format(rule))

        # check keys
        badkeys = frozenset(rule.keys()) - VALID_RULES
        if badkeys:
            raise ValueError('invalid rule key %r in %r' % (badkeys, rule))

        if 'check_index' in rule:
            if rule['check_index'] != left.cursor:
                raise ValueError('invalid position %d (expect %d)' % (left.cursor, rule['check_index']))
        if 'index' in rule:
            left.move_to(rule['index'])

        for repeat in range(rule.get('repeat', 1)):
            rule['nrepeat'] = repeat
            try:
                if 'if' in rule or 'if_r2l' in rule or 'if_l2r' in rule:
                    self.process_if(rule, left, right)
                elif 'switch' in rule:
                    self.process_switch(rule, left, right)
                elif 'processor' in rule:
                    self.process_processor(rule, left, right)
                elif 'rules' in rule:
                    self.process_rules(rule, left, right)
                elif 'key' in rule or 'converter' in rule:
                    rule.setdefault('type', 'default')
                    self.process(rule, left, right)
                elif 'check' in rule:
                    self.process_check(rule, left, right)
                else:
                    if 'index' in rule:
                        if self.direction == 'r2l':
                            left.cursor += 1
                    elif 'check_index' in rule:
                        left.cursor += 1
                    elif 'default' in rule:
                        default = rule['default']
                        need_inc = True
                        if isinstance(default, dict):
                            if self.direction == 'r2l':
                                if 'r2l' in default:
                                    left.append(default['r2l'])
                                    need_inc = False
                        else:
                            if self.direction == 'r2l':
                                left.append(default)
                                need_inc = False
                        if need_inc:
                            left.cursor += 1
                    else:
                        raise ValueError
            except Exception as e:
                print('Have problem: {}'.format(e))

    def process_if(self, rule, left, right):
        if_settings = []
        if_settings.extend(self.normalize_if_settings(rule.get('if_' + self.direction, [])))
        if_settings.extend(self.normalize_if_settings(rule.get('if', [])))

        ifresult = True
        for handlername, args in if_settings:
            handler = self.get_if_handler(handlername)
            if isinstance(args, list):
                args, kwds = args, {}
            else:
                args, kwds = (), args
            if not handler(self.direction, rule, left, right, *args, **kwds):
                ifresult = False
                break
        else:
            ifresult = True

        rules = None
        good, bad = True, False
        if 'true' in rule or 'false' in rule:
            warnings.warn("'true' or 'false' is deprecated in `if` rule", DeprecationWarning)
            good, bad = 'true', 'false'

        if good in rule or bad in rule:
            rules = rule.get(good if ifresult else bad, [])
            for rule in rules:
                self.process_rule(rule, left, right)
        else:
            r = rule.copy()
            del r['if']
            if ifresult:
                self.process_rule(r, left, right)
            else:
                if self.direction == 'r2l':
                    left.append(None)

    def normalize_if_settings(self, if_settings):
        if isinstance(if_settings, str):
            return [(if_settings, {})]
        elif isinstance(if_settings, list):
            if not if_settings:
                return []
            if not isinstance(if_settings[0], list):
                return [if_settings]
            else:
                return if_settings
        else:
            raise ValueError('invalid if settings')

    def process_switch(self, rule, left, right):
        if self.direction == 'l2r':
            raise NotImplementedError
        val = get_right_value(right, rule['switch'])

        rules = None
        if val in rule['map']:
            rules = rule['map'][val]
        if rules is None:
            rules = rule.get('default', [])

        for rule in rules:
            self.process_rule(rule, left, right)

    def process_processor(self, rule, left, right):
        processor = self.get_processor(rule['processor'])
        args = rule.get('args', {})
        processor(rule, left, right, **args)

    def process_rules(self, rule, right, row):
        raise NotImplementedError

    def process(self, rule, left, right):
        raise NotImplementedError

    def get_if_handler(self, name):
        handler = getattr(DefaultIfHandlers, name, None)
        if handler:
            return handler

    def get_processor(self, name):
        raise NotImplementedError

    def pre_process(self, left, right):
        pass

    def post_process(self, left, right):
        pass


# Left2Right
class Left2RightConverterBase(ConverterBase):
    def __init__(self, ruleset):
        super(Left2RightConverterBase, self).__init__(ruleset, 'l2r')

    def convert(self, row):
        left = FlexRow(row, self.ruleset.encoding)
        right = RightBuilder()

        self.pre_process(left, right)

        for rule in self.ruleset.rules:
            self.process_rule(rule, left, right)

        self.post_process(left, right)

        return right, right.images

    def process_rules(self, rule, left, right):
        """子ルール"""
        assert isinstance(rule['key'], str)
        sub = RightBuilder()

        for r in rule['rules']:
            self.process_rule(r, left, sub)
        right.append(rule['key'], sub.copy())

    def process(self, rule, left, right):
        val = left.pop()

        if 'converter' in rule:
            val = self.get_converter(rule['converter'])(val, left, right, rule)
        elif 'map' in rule:
            d = sanitize_dict(rule['map'])
            if val not in d and val:
                if self.ruleset.strict:
                    raise ValueError(val)
                # print >>sys.stderr, '%r not found in %r (%r)' % (val, rule['map'], rule)
                pass
            val = d.get(val)
        else:
            val = type_converters[rule['type']].convert_l2r(val, left, right, rule)

        if 'key' in rule:
            key = rule['key']
            if isinstance(key, list):
                assert len(key) == len(val)
                for k, v in itertools.izip(key, val):
                    self.set_right_value(right, k, v)
            else:
                self.set_right_value(right, key, val)

    def set_right_value(self, right, key, val):
        if key.startswith('_publish_properties'):
            if not self.media_key:
                return

            t = key.split('.', 1)
            key = '{}.{}'.format('publish_status.{}.properties'.format(self.media_key), t[1])
        right.set(key, val)

    def get_converter(self, name):
        return getattr(self, name)

    def get_processor(self, name):
        return getattr(self, name)

    def get_if_handler(self, name):
        handler = super(Left2RightConverterBase, self).get_if_handler(name)
        if handler:
            return handler

        return getattr(self, name)

    def process_check(self, rule, left, right):
        val = left.pop()
        if val != str(rule['check']):
            raise InvalidDataException('Invalid data {!r} @ {!r}'.format(val, rule))


# Right2Left
class Right2LeftConverterBase(ConverterBase):
    returncode = None

    def __init__(self, ruleset):
        super(Right2LeftConverterBase, self).__init__(ruleset, 'r2l')

    def convert(self, right):
        left = FlexRow(encoding=self.ruleset.encoding, allow_crlf=self.ruleset.allow_crlf)

        self.pre_process(left, right)
        for rule in self.ruleset.rules:
            self.process_rule(rule, left, right)
        self.post_process(left, right)

        left.finalize()
        return map(self.sanitize, left), left.media

    def sanitize(self, x):
        if x is None:
            x = ''
        elif isinstance(x, unicode):
            x = x.encode(self.ruleset.encoding)
        elif not isinstance(x, str):
            x = str(x)
        return x

    def process_rules(self, rule, left, right):
        """子ルール"""
        val = self.get_right_value(right, rule['key'])
        rules = rule['rules']

        if isinstance(val, list) and rule['nrepeat'] < len(val):
            data = val[rule['nrepeat']]
        else:
            data = {}

        for r in rules:
            self.process_rule(r, left, data)

    def process(self, rule, left, right):
        key = val = None
        if 'key' in rule:
            key = rule['key']
            if isinstance(key, list):
                val = [self.get_right_value(right, k) for k in key]
            else:
                val = self.get_right_value(right, rule['key'])

        if 'converter' in rule:
            val = self.get_converter(rule['converter'])(val, right, rule)
        elif 'mapr' in rule and val is not None:
            d = self.get_map(rule['mapr'])
            if val not in d and val:
                pass
            val = d.get(val)
        elif 'map' in rule and val is not None:
            d = invert_dict(self.get_map(rule['map']))
            if val not in d and val:
                pass
            val = d.get(val)
        elif 'type' in rule:
            val = type_converters[rule['type']].convert_r2l(val, right, rule)
        elif 'has' in rule:
            val = rule[True] if rule['has'] in val else rule[False]

        # 改行コードをエスケープする
        if isinstance(val, (int, long)):
            val = '%d' % val

        # checkers
        if 'limit_characters' in rule and isinstance(val, str):
            val = val[:rule['limit_characters']]

        if 'max_bytes' in rule and val is not None:
            if rule['max_bytes'] < len(val):
                # TODO: 切り詰めWarningを出す
                # raise ValueError('overflow %r for index %d' % (val, left.cursor))
                val = trim_string(val, self.ruleset.encoding, rule['max_bytes'])

        if 'max_chars' in rule and isinstance(val, str):
            if rule['max_chars'] < len(val):
                val = val[:rule['max_chars']]

        if val is None and 'default' in rule:
            default = rule['default']
            if isinstance(default, dict):
                default = default['r2l']
            val = default

        if left.xml:
            left.append(key, val, max_bytes=rule.get('max_bytes'))
        else:
            left.append(val, max_bytes=rule.get('max_bytes'))

    def get_right_value(self, right, key):
        keys = key.split('.')
        if key == '_id':
            return right[key]
        elif key.startswith('_'):
            if key.startswith('_publish_properties'):
                d = self.get_publish_properties(right)
                keys = keys[1:]
            else:
                print(key)
                raise ValueError('invalid key')
        else:
            d = right

        for k in keys:
            d = d.get(k)
            if d is None:
                return None

        # バグで'None'とはいっていることがあるので、adhocに修正する
        if d == 'None':
            d = None
        return d

    def get_converter(self, name):
        return getattr(self, name)

    def get_processor(self, name):
        return getattr(self, name)

    def get_if_handler(self, name):
        handler = super(Right2LeftConverterBase, self).get_if_handler(name)
        if handler:
            return handler

        return getattr(self, name)

    def get_publish_properties(self, right):
        assert hasattr(self, 'account')
        right.setdefault('publish_status', {})
        right['publish_status'].setdefault(self.account.key, {})
        right['publish_status'][self.account.key].setdefault('properties', {})
        return right.get2('publish_status.{}.properties'.format(self.account.key)) or {}


class ToXMLConverter(Right2LeftConverterBase):
    def convert_for_xml(self, right):
        left = JSonRow(encoding=self.ruleset.encoding, allow_crlf=self.ruleset.allow_crlf)

        self.pre_process(left, right)
        for rule in self.ruleset.rules:
            self.process_rule(rule, left, right)
        self.post_process(left, right)

        left.finalize()
        return left, left.media


class DefaultIfHandlers(object):
    @staticmethod
    def always_true(direction, rule, left, right):
        return True

    @staticmethod
    def is_value(direction, rule, left, right, key, value):
        # assert direction == 'r2l'
        test = get_right_value(right, key)
        return test == value

    @staticmethod
    def is_not_value(*args, **kwds):
        return not DefaultIfHandlers.is_value(*args, **kwds)

    @staticmethod
    def is_not_empty(direction, rule, left, right, key):
        assert direction == 'r2l'
        test = get_right_value(right, key)
        return test not in (None, '')

    @staticmethod
    def is_left_value(direction, rule, left, right, col, value):
        # assert isinstance(col, int)
        # assert type(left[col]) == type(value)
        return left[col] == value

    @staticmethod
    def has_value(direction, rule, left, right, key, value):
        """arrayにvalueが含まれるか"""
        assert direction == 'r2l'
        array = get_right_value(right, key)
        if array is None:
            return False
        elif isinstance(array, list):
            return value in array
        raise ValueError

    @staticmethod
    def is_not_zero(direction, rule, left, right, key):
        assert direction == 'r2l'
        test = get_right_value(right, key)
        return test


def get_right_value(right, key):
    d = right
    for k in key.split('.'):
        d = d.get(k)
        if d is None:
            return None

    # バグで'None'とはいっていることがあるので、adhocに修正する
    if d == 'None':
        d = None
    return d
