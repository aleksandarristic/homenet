from datetime import timedelta
from math import ceil

from django import template

register = template.Library()


@register.filter
def convert_speed(value, arg):
    """
    Template filter to convert value from bytes per second to Mbps or Kbps
    :param value: bytes per second value (int)
    :param arg: argument that's either mbps or kbps to signify what to convert the value to
    :return: converted value or zero
    """
    if not value:
        return 0
    bytes_per_second_speed = float(value)

    if arg.lower() == "mbps":
        return round(bytes_per_second_speed * 8e-06, 2)

    if arg.lower() == "kbps":
        return round(bytes_per_second_speed * 8e-03, 2)

    return value


@register.filter
def decimal(value, arg):
    """
    Template filter to round up float values to specific number of decimal places
    :param value: value to round
    :param arg: number of decimal places; if zero - the function will do math.ceil
    :return:
    """
    if not value:
        return 0
    if int(arg) == 0:
        return ceil(float(value))
    return round(float(value), int(arg))


@register.filter
def in_mb(value):
    """
    Template filter to convert bytes value to megabytes
    :param value: value to convert
    :return: value in megabytes
    """
    if not value:
        return 0
    bytes_val = int(value)
    return bytes_val / (1024 * 1024)


@register.filter
def in_ms(value, force=False):
    """
    Template filter to convert duration to miliseconds
    :param force:
    :type force:
    :param value:
    :return:
    """
    if not value:
        return 0
    val = float(value)
    if val < 1 or force:
        return "%.2f ms" % (val * 1000)
    return "%.2f s" % val


@register.filter
def percent_of(part, whole):
    """
    Template filter to calculate percentages
    :param part:
    :param whole:
    :return:
    """
    try:
        return "%.2f" % (float(part) / whole * 100)
    except (ValueError, ZeroDivisionError):
        return 0


@register.filter
def adjust_days(value, days):
    return value + timedelta(days=days)
