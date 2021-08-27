from django import template

register = template.Library()


@register.simple_tag()
def format_money(money, **kwargs):
    if money:
        import locale
        decimal = money % 1
        try:
            locale.setlocale(locale.LC_NUMERIC, 'ja_JP.utf8')
        except:
            locale.setlocale(locale.LC_NUMERIC, 'ja_JP')

        output = locale.format('%d', int(money), True)
        if decimal != 0.0:
            output += str(decimal)[1:]
        return output
    return None


@register.filter
def index(indexable, i):
    try:
        i = int(i)
    except:
        i = 0
    return indexable[i]


@register.filter
def make_list_data(data, loop):
    if data:
        return data
    return [''] * int(loop)
