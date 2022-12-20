import logging
from datetime import datetime, timedelta

from django import template

register = template.Library()


@register.filter
def to_megabit(value):
    return float(value) / 125000.00


@register.filter
def to_dt(dt_string, hour_delta=1):
    fmt = '%Y-%m-%dT%H:%M:%SZ'
    try:
        dt = datetime.strptime(dt_string, fmt) + timedelta(hours=hour_delta)  # hack; need to parse TZ
    except ValueError as e:
        logging.error(f'Error parsing datetime: {e}')
        dt = None
    return dt
