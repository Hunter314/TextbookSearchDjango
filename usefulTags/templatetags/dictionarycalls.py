from django import template
from django.template.defaulttags import register
# for creating custom template tags:
#register = template.Library()

@register.filter(name='lookup')
def lookup(value, arg):
    return value[arg]
