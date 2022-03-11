import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from monitor.utils import arp_scan

log = logging.getLogger()

DEFAULT_CONFIG = settings.MONITOR_CONFIG.get('default', {})
INTERFACE = DEFAULT_CONFIG.get('interface', 'eth0')
NETWORK = DEFAULT_CONFIG.get('network', '--localnet')


class Command(BaseCommand):
    help = 'Calculate averages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interface',
            action='store',
            help=f'Interface to use. Default: "{INTERFACE}"',
            default=None
        )

        parser.add_argument(
            '--network',
            action='store',
            help=f'Network to scan. Default: "{NETWORK}"',
            default=None
        )

    def handle(self, *args, **options):
        log.info('Starting min/max/avg recalculation')
        log.debug(f'Default interface: "{INTERFACE}"; Default network: "{NETWORK}".')

        if options['interface'] and options['network']:
            log.debug('Config overridden!')
            log.debug(f'Selected interface: "{options["interface"]}"; Default network: "{options["network"]}".')
            devices = arp_scan(interface=options['interface'], network=options['network'])
            log.info(f'Done. Devices detected: {len(devices)}')
            log.debug(f'Devices: {devices}')
            return

        for config_name, config in settings.MONITOR_CONFIG.items():
            log.debug(f'Config: "{config_name}"; Selected interface: "{config["interface"]}"; Default network: '
                      f'"{config["network"]}".')
            devices = arp_scan(interface=config['interface'], network=config['network'])
            log.info(f'Done. Devices detected: {len(devices)}')
            log.debug(f'Devices: {devices}')
