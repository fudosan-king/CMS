from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    if 'page' in query:
        query.pop('page')
    if 'limit' in query:
        query.pop('limit')
    query.update(kwargs)
    return query.urlencode()