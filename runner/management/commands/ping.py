import os
import logging
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

log = logging.getLogger()


class Command(BaseCommand):
    help = 'Ping command runner wrapper'

    def handle(self, *args, **options):
        script = settings.RUNNER_CONFIG.get('ping', '~/ping.py')
        log.info('Starting ping command')
        speedtest_env = settings.RUNNER_CONFIG.get('ping_env', {})
        env = os.environ.copy()
        env.update(speedtest_env)
        proc = subprocess.run([script], capture_output=True, env=env)
        print(proc.stdout.decode('utf-8'))
        if proc.returncode == 0:
            print('Success!')
            log.info('Ping process success')
        else:
            print('ERROR!')
            log.info('Ping process returned an error.')
            print(proc.stderr.decode('utf-8'))
            log.error(proc.stderr.decode('utf-8'))
        print('All done.')
