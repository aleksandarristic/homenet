import os
import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

log = logging.getLogger()


class Command(BaseCommand):
    help = 'Speedtest command runner wrapper'

    def handle(self, *args, **options):
        script = settings.RUNNER_CONFIG.get('speedtest', '~/speedtest.py')
        log.info('Starting speedtest command')
        speedtest_env = settings.RUNNER_CONFIG.get('speedtest_env', {})
        env = os.environ.copy()
        env.update(speedtest_env)
        proc = subprocess.run([script], capture_output=True, env=env)
        print(proc.stdout.decode('utf-8'))
        if proc.returncode == 0:
            print('Success!')
        else:
            print(proc.stderr.decode('utf-8'))
        print('All done.')
