import logging

from django.shortcuts import render

from dashboard.models import MenuURL, UrlGroup
from common.influxcli import cli


def transform_ping(d):
    status = "UP" if d['values'][0][1] else "DOWN"
    return {'name': d['tags']['name'], 'time': d['values'][0][0], 'status': status}


def index(request):
    try:
        speedtest = cli.get_speedtest()
        ping = cli.get_ping()
    except Exception as e:
        speedtest = None
        ping = None
        logging.error(f'Could not get data from influxdb: "{e}"')

    context = {
        'url_groups': UrlGroup.objects.filter(active=True),
        'menu_items': MenuURL.objects.filter(active=True, url_group=None),
        'speedtest': speedtest,
        'ping': list(map(transform_ping, ping)) if ping else None
    }
    template = 'dashboard/index.html'
    return render(request, template, context)
