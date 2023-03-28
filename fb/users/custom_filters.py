from django import template

register = template.Library()

@register.filter
def total(items):
    return sum(item.price for item in items)