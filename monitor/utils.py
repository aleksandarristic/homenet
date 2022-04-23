import logging

from django.utils import timezone as tz

from common.utils import get_command_output
from monitor.models import Device, Scan

log = logging.getLogger()


def arp_scan(interface="eth0", network="--localnet"):
    command = f"sudo arp-scan -x --interface={interface} {network}"
    log.debug(f'ARP - Running scan with command: "{command}"')
    scan = Scan(
        type='ARP',
        command=command,
        running=True
    )
    scan.save()
    out, err = get_command_output(command)
    all_out = "\n".join([out, err])
    log.debug(f'ARP - Scan output: \n{all_out}')
    scan.output = all_out
    scan.running = False
    scan.save()
    devices = parse_arp_out(out, scan)
    return devices


def parse_arp_out(output, scan):
    devices = []
    for line in output.splitlines():

        try:
            ip, mac, manufacturer = line.split('\t')
        except ValueError as e:
            log.error(f'Error parsing arp-scan output: {e}')
            continue

        devices.append(get_or_create_device(mac, ip, manufacturer, scan))

    return devices


def get_or_create_device(mac, ip, manufacturer, scan):
    log.debug(f'Get or create device received: mac={mac}, ip={ip}, manufacturer={manufacturer}, scan={scan}')
    device, created = Device.objects.get_or_create(
        mac_address=mac,
        defaults={
            'manufacturer': manufacturer,
            'name': f'Device {mac}',
            'last_ip': {ip}
        }
    )
    device.last_ip = ip
    device.scan_set.add(scan)
    device.last_seen = tz.now()
    device.save()
    return device
