from django import template
register = template.Library()

# @register.filter
# def replaceDash(obj):
#     print(obj)
#     obj = obj.replace('>-<', '> to <')
#     return obj