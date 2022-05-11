import threading

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


@require_POST
def run_speedtest(request):
    from django.core.management import call_command

    def fn():
        call_command('speedtest')

    t = threading.Thread(target=fn, daemon=True)
    t.start()
    messages.success(request, 'New speedtest started!')
    return redirect('dashboard:index')
