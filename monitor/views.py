import threading
import logging
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from monitor.forms import DeviceForm
from monitor.models import Device, Scan
from monitor.utils import arp_scan
from monitor.view_helpers import get_dt_format

log = logging.getLogger()


@require_GET
def index(request):
    latest_scans = Scan.objects.all()[:5]
    try:
        last_scan = Scan.objects.latest('time')
    except Scan.DoesNotExist:
        last_scan = None

    start = request.GET.get('from')
    if start:
        end = request.GET.get('to')
        try:
            end_time = datetime.strptime(end, get_dt_format(end))
        except (ValueError, TypeError):
            end_time = datetime.now()

        try:
            start_time = datetime.strptime(start, get_dt_format(start))
        except (ValueError, TypeError):
            start_time = end_time - timedelta(minutes=30)

        recent_devices = Device.objects.filter(last_seen__range=[start_time, end_time])
    else:
        recent_devices = last_scan.devices.all() if last_scan is not None else []
        start_time, end_time = None, None

    template = 'monitor/index.html'
    context = {
        'last_scan': last_scan,
        'latest_scans': latest_scans,
        'recent_devices': recent_devices,
        'start_time': start_time,
        'end_time': end_time,
        'scan_running': last_scan.running if last_scan else False
    }
    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
def device_edit(request, device_id):
    device = get_object_or_404(Device, pk=device_id)

    if request.method == 'POST':
        device_form = DeviceForm(request.POST, instance=device)
        if device_form.is_valid():
            device = device_form.save()
            return redirect('monitor:device_edit', device_id=device.id)

    else:
        device_form = DeviceForm(instance=device)

    context = {
        'device_form': device_form,
        'device': device
    }

    return render(request, 'monitor/device_edit.html', context)


@require_POST
def scan_start(request):
    t = threading.Thread(target=arp_scan,
                         daemon=True)
    t.start()
    # TODO: implement messages
    return redirect('monitor:index')


@require_GET
def scan_details(request, device_id):
    scan = get_object_or_404(Scan, pk=device_id)

    context = {
        'scan': scan,
        'devices': scan.devices.all()
    }
    return render(request, 'monitor/scan_details.html', context)