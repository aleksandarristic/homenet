import threading

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from runner.util import is_running


@require_POST
def run_speedtest(request):

    # check if speedtest is running now
    if is_running('speedtest'):
        messages.success(request, 'NOT STARTED: Speedtest process already running!')
    else:
        from django.core.management import call_command

        def fn():
            call_command('speedtest')

        t = threading.Thread(target=fn, daemon=True)
        t.start()
        messages.success(request, 'New speedtest started!')

    return redirect('dashboard:index')
