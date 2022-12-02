from django import template
register = template.Library()


@register.filter
def to_megabit(value):
    return float(value) / 120000.00
