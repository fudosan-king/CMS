# -*- coding:utf-8 -*-
import re
import contextlib
import os

__all__ = [
    'sanitize_dict', 'invert_dict',
    'fix_zenkakusuuji_to_kansuuji', 'zenkakusuuji_to_kansuuji',
    'fix_to_zenkakusuuji'
]

ZENKAKU_SUUJI_REX = re.compile(r'([０-９]+)')
EISUUJI_MAP = {
    u'１': u'一',
    u'１': u'一',
    u'２': u'二',
    u'３': u'三',
    u'４': u'四',
    u'５': u'五',
    u'６': u'六',
    u'７': u'七',
    u'８': u'八',
    u'９': u'九',
}

HANKAKU_SUUJI_REX = re.compile(r'(\d+)')
H_TO_Z_MAP = {
    u'0': u'０',
    u'1': u'１',
    u'2': u'２',
    u'3': u'３',
    u'4': u'４',
    u'5': u'５',
    u'6': u'６',
    u'7': u'７',
    u'8': u'８',
    u'9': u'９',
}

KANSUUJI_REX = re.compile(r'([一二三四五六七八九十])+')
KANSUUJI_MAP = {
    u'一': u'１',
    u'二': u'２',
    u'三': u'３',
    u'四': u'４',
    u'五': u'５',
    u'六': u'６',
    u'七': u'７',
    u'八': u'８',
    u'九': u'９',
}


def build_replace_map(start, end, to):
    m = {}
    delta = ord(to) - ord(start)
    for code in range(ord(start), ord(end) + 1):
        m[chr(code)] = chr(code + delta)
    return m

ALPHA_Z2H = build_replace_map(u'Ａ', u'Ｚ', u'A')


# dict
def sanitize_dict(d):
    rv = {}
    for k, v in d.iteritems():
        if not isinstance(k, str):
            k = unicode(k)
        rv[k] = v
    return rv


def invert_dict(d):
    return dict((v, k) for k, v in d.iteritems())


# characters
def fix_zenkakusuuji_to_kansuuji(s):
    """全角数字含みの文字列を、全部漢数字にする"""
    return ZENKAKU_SUUJI_REX.sub(lambda mo: zenkakusuuji_to_kansuuji(mo.group(1)), s)


def zenkakusuuji_to_kansuuji(num):
    """全角数字を漢数字にする"""
    assert len(num) <= 2

    if len(num) == 1:
        return EISUUJI_MAP[num]
    else:
        a, b = num
        if a == u'１':
            return u'十%s' % (EISUUJI_MAP[b] if b != u'０' else u'')
        else:
            return u'%s十%s' % (EISUUJI_MAP[a], EISUUJI_MAP[b] if b != u'０' else u'')


def fix_kansuuji_to_zenkakusuuji(s):
    return KANSUUJI_REX.sub(lambda mo: kansuuji_to_zenkakusuuji(mo.group(1)), s)


def kansuuji_to_zenkakusuuji(num):
    assert len(num) == 1

    return KANSUUJI_MAP[num[0]]


def fix_to_zenkakusuuji(s):
    return HANKAKU_SUUJI_REX.sub(lambda mo: hankakusuuji_to_zenkaku(mo.group(1)), s)


def hankakusuuji_to_zenkaku(num):
    return u''.join(H_TO_Z_MAP[x] for x in num)


# os
@contextlib.contextmanager
def chdir(path):
    old = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old)
