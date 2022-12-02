from django.shortcuts import render

from dashboard.models import MenuURL, UrlGroup
from common.influxcli import cli


def index(request):
    try:
        speedtest = cli.get_speedtest()
    except Exception as e:
        speedtest = None
        # todo: log

    context = {
        'url_groups': UrlGroup.objects.filter(active=True),
        'menu_items': MenuURL.objects.filter(active=True, url_group=None),
        'speedtest': speedtest
    }
    template = 'dashboard/index.html'
    return render(request, template, context)
