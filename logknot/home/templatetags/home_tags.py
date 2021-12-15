from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    if 'page' in query:
        query.pop('page')
    if 'limit' in query:
        query.pop('limit')
    if 'order_by' in query:
        query.pop('order_by')
    query.update(kwargs)
    return query.urlencode()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
