import logging

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_POST

from speedtest.models import SpeedTest, PingTest, DnsTest
from speedtest.utils import do_speed_test
from speedtest.view_helpers import dashboard_context

log = logging.getLogger()


@require_GET
def index(request, day=None):
    selected = request.GET.get('t', 'speed')
    try:
        days_page = int(request.GET.get('p', 0))
    except ValueError:
        days_page = 0
    context = dashboard_context(day, selected, days_page)

    template = 'speedtest/index.html'
    return render(request, template, context)


@require_GET
def speedtest_detail(request, entry_id):
    entry = get_object_or_404(SpeedTest, pk=entry_id)
    context = {
        'entry': entry,
        'day': entry.test_date,
    }
    return render(request, 'speedtest/speedtest_detail.html', context)


@require_POST
def speedtest_start(request):
    speedtest_server = settings.SPEEDTEST_CONFIG.get('SPEED_TEST_SERVER')
    import threading
    t = threading.Thread(target=do_speed_test,
                         args=[speedtest_server, True],
                         daemon=True)
    t.start()
    return redirect('speedtest:index')


@require_POST
def speedtest_stop(request, entry_id=None):
    if entry_id:
        entry = get_object_or_404(SpeedTest, pk=entry_id)
        entry.stop()
    else:
        [test.stop() for test in SpeedTest.objects.filter(running=True)]
    return redirect('speedtest:index')


@require_GET
def pingtest_detail(request, entry_id):
    entry = get_object_or_404(PingTest, pk=entry_id)
    context = {
        'entry': entry,
        'day': entry.test_date
    }
    return render(request, 'speedtest/pingtest_detail.html', context)


@require_GET
def dnstest_detail(request, entry_id):
    entry = get_object_or_404(DnsTest, pk=entry_id)
    context = {
        'entry': entry,
        'day': entry.test_date
    }
    return render(request, 'speedtest/dnstest_detail.html', context)
