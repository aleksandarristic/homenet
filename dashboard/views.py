import logging

from django.shortcuts import render

from dashboard.models import MenuURL, UrlGroup
from common.influxcli import cli


def index(request):
    try:
        speedtest = cli.get_speedtest()
        ping = cli.get_ping()
    except Exception as e:
        speedtest = None
        ping = None
        logging.error(f'Could not get influxdb data: {e}')

    context = {
        'url_groups': UrlGroup.objects.filter(active=True),
        'menu_items': MenuURL.objects.filter(active=True, url_group=None),
        'speedtest': speedtest,
        'ping': ping
    }
    template = 'dashboard/index.html'
    return render(request, template, context)
