import threading
import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from runner.util import is_running

log = logging.getLogger()


@require_POST
def run_speedtest(request):
    log.info("Requested to run speedtest via web interface.")
    # check if speedtest is running now
    if is_running('speedtest'):
        log.info("Speedtest already detected as running, not starting.")
        messages.error(request, 'NOT STARTED: Speedtest process already running!')
    else:
        log.info('Speedtest not detected as running, starting speedtest now.')
        from django.core.management import call_command

        def fn():
            call_command('speedtest')

        t = threading.Thread(target=fn, daemon=True)
        t.start()
        messages.success(request, 'New speedtest started!')

    return redirect('dashboard:index')
