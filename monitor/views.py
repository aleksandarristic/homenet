import threading
import logging
from datetime import datetime, timedelta, time

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from monitor.forms import DeviceForm
from monitor.models import Device, Scan
from monitor.utils import arp_scan
from monitor.view_helpers import get_dt_format

log = logging.getLogger()


@require_GET
def device_day(request, day=None):
    """
    ALL DEVICES SEEN IN A DAY
    :param request:
    :type request:
    :param day:
    :type day:
    :return:
    :rtype:
    """
    today = datetime.today().date()

    end_time = datetime.combine(day or today, time.max)
    start_time = datetime.combine(day or today, time.min)

    day_scans = Scan.objects.filter(time__range=[start_time, end_time])
    devices = Device.objects.filter(scan__in=day_scans).distinct()

    try:
        menu_page = int(request.GET.get('p', 0))
    except ValueError:
        menu_page = 0

    offset = 15 * menu_page
    menu_items = list(reversed(Scan.objects.dates('time', 'day')))[0+offset:10+offset]
    template = 'monitor/index.html'

    context = {
        'datum': day,
        'today': today,
        'menu_items': menu_items,
        'menu_page': menu_page,
        'devices': devices,
        'start_time': start_time,
        'end_time': end_time,
        'scan_running': bool(Scan.objects.filter(running=True))
    }

    return render(request, template, context)


@require_GET
def device_filter(request):

    start = request.GET.get('from')
    end = request.GET.get('to')
    try:
        end_time = datetime.strptime(end, get_dt_format(end))
    except (ValueError, TypeError):
        end_time = datetime.now()

    try:
        start_time = datetime.strptime(start, get_dt_format(start))
    except (ValueError, TypeError):
        start_time = end_time - timedelta(days=1)

    devices = Device.objects.filter(last_seen__range=[start_time, end_time])

    today = datetime.date(datetime.today())
    template = 'monitor/time_filter.html'
    context = {
        'today': today,
        'devices': devices,
        'start_time': start_time,
        'end_time': end_time,
    }
    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
def device_edit(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    datum = request.GET.get('datum')
    try:
        datetime.date(datum)
    except (ValueError, TypeError):
        datum = datetime.date(datetime.today()).strftime('%Y-%m-%d')

    if request.method == 'POST':
        device_form = DeviceForm(request.POST, instance=device)
        if device_form.is_valid():
            device = device_form.save()
            messages.success(request, 'Device saved')
            return redirect('monitor:device_details', device_id=device.id)
    else:
        device_form = DeviceForm(instance=device)
    context = {
        'datum': datum,
        'device_form': device_form,
        'device': device
    }
    return render(request, 'monitor/device_edit.html', context)


@require_GET
def device_details(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    context = {'entry': device}
    template = 'monitor/device_details.html'

    return render(request, template, context)


@require_GET
def device_history(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    context = {
        'entry': device,
    }
    template = 'monitor/device_history.html'

    return render(request, template, context)


@require_POST
def scan_start(request):
    t = threading.Thread(target=arp_scan,
                         daemon=True)
    t.start()
    # TODO: implement messages
    return redirect('monitor:index')


@require_GET
def scan_details(request, device_id):
    try:
        menu_page = int(request.GET.get('p', 0))
    except ValueError:
        menu_page = 0
    scan = get_object_or_404(Scan, pk=device_id)

    context = {
        'menu_page': menu_page,
        'scan': scan,
        'devices': scan.devices.all()
    }
    return render(request, 'monitor/scan_details.html', context)