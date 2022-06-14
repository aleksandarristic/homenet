import logging

from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from monitor.models import Scan

log = logging.getLogger()

DAYS_TO_KEEP = settings.MONITOR_CONFIG.get('default', {}).get('days_to_keep', 30)


class Command(BaseCommand):
    help = f'Removes scans and scan<>device relationships older than {DAYS_TO_KEEP} from the database.'

    def handle(self, *args, **options):
        log.info(f'Removing scans and scan<>device relationships older than {DAYS_TO_KEEP} days...')
        result = Scan.objects.filter(time__lte=datetime.now() - timedelta(days=DAYS_TO_KEEP)).delete()
        log.info('Removal complete.')
        log.info(result)

        # vacuum sqlite3 db after speed test
        if settings.DATABASES.get('default', {}).get('ENGINE') == 'django.db.backends.sqlite3':
            log.info('Vacuuming db...')
            from django.db import connection, transaction
            cursor = connection.cursor()
            cursor.execute("vacuum")
            transaction.commit()
            log.info('VACUUM DB - Done.')

        log.info('Bye!')
