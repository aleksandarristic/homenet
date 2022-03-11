import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from speedtest.utils import do_speed_test, do_dns_tests, do_ping_tests

log = logging.getLogger()


class Command(BaseCommand):
    help = 'Run speedtest'

    def add_arguments(self, parser):
        parser.add_argument(
            '--short',
            action='store_true',
            help='Do only ping and dns tests.',
            default=False
        )

    def handle(self, *args, **options):
        log.info(f'Running run_speedtest management command with argument short={options["short"]}.')
        dns_hosts = settings.SPEEDTEST_CONFIG.get('DNS_TEST_HOSTS')
        ping_hosts = settings.SPEEDTEST_CONFIG.get('PING_TEST_HOSTS')

        do_dns_tests(dns_hosts)
        do_ping_tests(ping_hosts)

        if options['short']:
            return

        speedtest_server = settings.SPEEDTEST_CONFIG.get('SPEED_TEST_SERVER')
        do_speed_test(speedtest_server)

        # vacuum sqlite3 db after speed test
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("vacuum")
        transaction.commit()
        log.info('VACUUM DB - Done.')
