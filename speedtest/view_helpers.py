import logging
from datetime import datetime

from django.db.models import Count

from speedtest.models import SpeedTest, PingTest, DnsTest
from speedtest.utils import get_or_create_averages

log = logging.getLogger()


def dashboard_context(day=None, selected=None, page_offset=0) -> dict:
    """
    :return: dashboard context
    :rtype: dict
    """
    today = datetime.date(datetime.today())
    day = day or today

    speed_tests = SpeedTest.objects.order_by('-start_time').filter(test_date=day, is_average=False, entry_type="SPEED")
    running = speed_tests.filter(running=True)
    speed_worst, speed_avg, speed_best = get_or_create_averages(day)

    dns_tests = DnsTest.objects.order_by('-start_time').filter(test_date=day, entry_type="DNS")
    ping_tests = PingTest.objects.order_by('-start_time').filter(test_date=day, entry_type="PING")

    dns_hosts = [item.get('server') for item in dns_tests.values('server').annotate(Count('id')).order_by()]
    ping_hosts = [item.get('server') for item in ping_tests.values('server').annotate(Count('id')).order_by()]

    latest_dns = []
    for dns_host in dns_hosts:
        latest_dns.append(
            dns_tests.filter(server=dns_host).first()
        )

    latest_ping = []
    for ping_host in ping_hosts:
        latest_ping.append(
            ping_tests.filter(server=ping_host).first()
        )

    # menu items for day selection
    offset = 10 * page_offset
    dates = list(
        reversed(SpeedTest.objects.order_by('-test_date').filter(is_average=False).dates('test_date', 'day'))
    )[0+offset:10+offset]

    context = {
        'day': day,
        'today': today,
        'is_today': day == today,
        'dates': dates,
        'page_offset': page_offset,

        # enum hosts
        'dns_hosts': dns_hosts,
        'ping_hosts': ping_hosts,

        # latest dns, ping and speed tests
        'latest_dns': latest_dns,
        'dns_tests_total': dns_tests.count(),
        'dns_tests_failed': dns_tests.filter(success=False).count(),

        'latest_ping': latest_ping,
        'ping_tests_total': ping_tests.count(),
        'ping_tests_failed': ping_tests.filter(success=False).count(),

        # averages table
        'speed_avg': speed_avg,
        'speed_worst': speed_worst,
        'speed_best': speed_best,
        'total_today': speed_tests.count(),
        'failed_today': speed_tests.filter(success=False).count(),

        # all entries
        'speed': speed_tests,
        'speed_failed': speed_tests.filter(success=False),
        'ping': ping_tests,
        'ping_failed': ping_tests.filter(success=False),
        'dns': dns_tests,
        'dns_failed': dns_tests.filter(success=False),

        'running': running,
        'test_running': bool(running),

        # selected
        'selected': selected
    }

    return context
