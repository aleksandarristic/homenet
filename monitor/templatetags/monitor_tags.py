from django import template

register = template.Library()


@register.filter
def days_seen(device_instance, max_days):
    return device_instance.days_seen(max_days=max_days)


@register.filter
def on_date(device_instance, day):
    return device_instance.scans_on_date(day)
