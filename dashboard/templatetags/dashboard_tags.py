from datetime import datetime

from django import template

register = template.Library()


@register.filter
def to_megabit(value):
    return float(value) / 125000.00


@register.filter
def nice_dt(dt_string):
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    try:
        dt = datetime.strptime(dt_string, fmt)
    except Exception as e:
        dt = None
        return ''
    return dt.strftime('%H:%M on %b %-d.')
