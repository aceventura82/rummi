from django import template

register = template.Library()


@register.simple_tag
def getSetPercent(val):
    return int(100 // (6/val))
