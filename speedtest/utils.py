import logging
import json
import re
from datetime import datetime
from json import JSONDecodeError

from common.utils import get_command_output
from speedtest.models import PingTest, SpeedTest, DnsTest

log = logging.getLogger()


def populate_and_save(obj, start_date, success, values):
    obj.download, obj.upload, obj.latency, obj.jitter = values
    obj.start_time = start_date
    obj.success = success
    obj.save()
    return obj


def get_or_create_averages(start_date, force_recalc=False):
    recalculate = force_recalc
    averages = calculate_speedtest_averages(start_date)

    speed_avg, avg_created = SpeedTest.objects.get_or_create(
        is_average=True,
        test_date=start_date,
        entry_type="SPEED_AVG",
        defaults={'start_time': start_date, 'share_url': None}
    )

    speed_worst, min_created = SpeedTest.objects.get_or_create(
        is_average=True,
        test_date=start_date,
        entry_type='SPEED_MIN',
        defaults={'start_time': start_date, 'share_url': None}
    )

    speed_best, max_created = SpeedTest.objects.get_or_create(
        is_average=True,
        test_date=start_date,
        entry_type='SPEED_MAX',
        defaults={'start_time': start_date, 'share_url': None}
    )

    success = not bool(SpeedTest.objects.filter(success=False, test_date=start_date, is_average=False).count())
    if recalculate:
        speed_avg = populate_and_save(speed_avg, start_date, success, averages['avg'])
        speed_worst = populate_and_save(speed_worst, start_date, success, averages['worst'])
        speed_best = populate_and_save(speed_best, start_date, success, averages['best'])
    else:
        if avg_created:
            speed_avg = populate_and_save(speed_avg, start_date, success, averages['avg'])
        if min_created:
            speed_worst = populate_and_save(speed_worst, start_date, success, averages['worst'])
        if max_created:
            speed_best = populate_and_save(speed_best, start_date, success, averages['best'])

    return speed_worst, speed_avg, speed_best


def calculate_speedtest_averages(day):
    tests = SpeedTest.objects.filter(test_date=day, is_average=False, success=True, running=False,
                                     latency__isnull=False, jitter__isnull=False, download__isnull=False,
                                     upload__isnull=False)
    count = tests.count()

    if not count:
        return {
            'worst': [0, 0, 0, 0],
            'avg': [0, 0, 0, 0],
            'best': [0, 0, 0, 0],
        }

    avg_download = sum([t.download for t in tests]) / count
    avg_upload = sum([t.upload for t in tests]) / count
    avg_latency = sum([t.latency for t in tests]) / count
    avg_jitter = sum([t.jitter for t in tests]) / count

    worst_download = tests.order_by('download').first().download
    worst_upload = tests.order_by('upload').first().upload
    worst_latency = tests.order_by('-latency').first().latency
    worst_jitter = tests.order_by('-jitter').first().jitter

    best_download = tests.order_by('-download').first().download
    best_upload = tests.order_by('-upload').first().upload
    best_latency = tests.order_by('latency').first().latency
    best_jitter = tests.order_by('jitter').first().jitter

    return {
        'worst': [worst_download, worst_upload, worst_latency, worst_jitter],
        'avg': [avg_download, avg_upload, avg_latency, avg_jitter],
        'best': [best_download, best_upload, best_latency, best_jitter],
    }


def ping_server(server, interval='1', num=4, wait=1):
    command = f'ping -i{interval} -W{wait} -c{num} {server}'
    log.debug(f'PING - Running test with command: "{command}"')
    out, err = get_command_output(command)
    all_out = "\n".join([command, out, err])
    log.debug(f'PING - Output of ping command: \n{all_out}')
    try:
        packet_loss = float(re.findall(r'received,\s(.*)%\spacket\sloss', out, re.MULTILINE)[0])
    except IndexError:
        log.error(f'PING - Failed extracting packet loss from output string. Output was: \n{out}')
        packet_loss = None

    try:
        stats = re.findall(r'(round-trip|rtt).*=\s(.*)', out, re.MULTILINE)[0][-1]
    except IndexError:
        log.error(f'PING - Failed extracting stats from output string. Output was: \n{out}')
        stats = None

    try:
        ping = float(stats.split('/')[1])
    except (IndexError, AttributeError):
        log.error(f'PING - Failed extracting ping from output string. Output was: \n{out}\nStats was: {stats}.')
        ping = None

    success = packet_loss == 0.0
    log.info(f'PING - test done: success={success}, host={server}, ping={ping}, loss={packet_loss}.')
    return server, ping, packet_loss, stats, success, all_out


def do_ping_tests(servers):
    objs = []
    log.debug(f"PING - About to do test for hosts: {servers}.")
    for server in servers:
        test_start = datetime.now()
        srv_host, srv_ping, p_loss, srv_stats, success, out = ping_server(server)
        test_duration = (datetime.now() - test_start).total_seconds()
        obj = PingTest.create(
            server=srv_host,
            ping=srv_ping or -1,
            packet_loss=p_loss or -1,
            stats=srv_stats or '',
            success=success,
            start_time=test_start,
            duration=test_duration,
            data=out
        )
        objs.append(obj)
    # cleanup previous non-failed ping tests
    if objs:
        log.debug('PING - Cleaning up old non-failed PING tests')
        PingTest.objects.filter(success=True).exclude(id__in=[o.id for o in objs]).delete()

    return len(objs)


def dns_resolve(server, wait=3):
    command = f'host -4 -W{wait} {server}'
    log.debug(f'DNS - Running resolution test with command: "{command}"')
    out, err = get_command_output(command)
    all_out = "\n".join([command, out, err])
    log.debug(f'DNS - Output of DNS command: \n{all_out}')
    try:
        ip = re.findall(r'has\saddress\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$', out, re.MULTILINE)[0]
        success = True
    except IndexError as e:
        log.error(f'DNS - Error parsing DNS test result with message: {e}')
        ip = None
        success = False
    log.info(f'DNS - test done: success={success}, host={server}, ip={ip}.')
    return server, ip, success, all_out


def do_dns_tests(hosts):
    objs = []
    log.debug(f"DNS - About to do test for hosts: {hosts}.")
    for host in hosts:
        test_start = datetime.now()
        _, ip, success, out = dns_resolve(host)
        test_duration = (datetime.now() - test_start).total_seconds()
        obj = DnsTest.create(
            host=host,
            ip=ip,
            success=success,
            start_time=test_start,
            duration=test_duration,
            data=out
        )
        objs.append(obj)

    if objs:
        log.debug('DNS - Cleaning up old non-failed DNS tests')
        DnsTest.objects.filter(success=True).exclude(id__in=[o.id for o in objs]).delete()

    return len(objs)


def do_speed_test(server=None, calc_average=False):
    command = 'speedtest -p no -f json'
    if server:
        command += f' -s {server}'

    start_time = datetime.now()
    speed_test = SpeedTest.start(
        server_id=server,
        start_time=start_time,
        data=command
    )
    log.info(f'SPEED - starting with command="{command}" (id={speed_test.id}).')
    out, err = get_command_output(command)
    all_out = "\n".join([command, out, err])
    duration = (datetime.now() - start_time).total_seconds()
    try:
        test_data = json.loads(out)
    except (TypeError, JSONDecodeError) as e:
        log.error(f'SPEED - failed parsing JSON with error: {e}')
        test_data = {}

    server = test_data.get('server', {}).get('name')
    server_id = test_data.get('server', {}).get('id')
    download = test_data.get('download', {}).get('bandwidth', 0)
    upload = test_data.get('upload', {}).get('bandwidth', 0)
    dl_bytes = test_data.get('download', {}).get('bytes', 0)
    ul_bytes = test_data.get('upload', {}).get('bytes', 0)
    latency = test_data.get('ping', {}).get('latency')
    jitter = test_data.get('ping', {}).get('jitter')
    share_url = test_data.get('result', {}).get('url')

    success = test_data and download > 0 and upload > 0 and share_url is not None and latency is not None

    speed_test.stop(
        server=server,
        success=success,
        duration=duration,
        server_id=server_id,
        latency=latency,
        jitter=jitter,
        download=download,
        upload=upload,
        dl_bytes=dl_bytes,
        ul_bytes=ul_bytes,
        share_url=share_url,
        data=None if success else all_out
    )
    log.info(f'SPEED - test done: success={success}, dl={download}, ul={upload}, latency={latency}, jitter={jitter}.')
    if calc_average:
        get_or_create_averages(speed_test.test_date, force_recalc=True)
        log.info(f'SPEED - recalculated daily averages.')
    return speed_test.success
