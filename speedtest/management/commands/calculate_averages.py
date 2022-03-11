import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from speedtest.models import SpeedTest
from speedtest.utils import get_or_create_averages

log = logging.getLogger()


class Command(BaseCommand):
    help = 'Calculate averages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force average recalculation',
            default=False
        )

    def handle(self, *args, **options):
        log.info('Starting min/max/avg recalculation')
        dates = SpeedTest.objects.dates('test_date', 'day')
        today = datetime.date(datetime.today())

        for date in dates:
            do_calc = today == date or options['force']
            if do_calc:
                get_or_create_averages(date, force_recalc=True)
                log.info(f'Recalculated min/max/avg for {date}.')

        log.info(f'Done.')
