from django import template
register = template.Library()

@register.filter
def hashval(dictionary, key):
    return dictionary.get(key)