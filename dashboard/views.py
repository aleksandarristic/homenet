from django.shortcuts import render

from dashboard.models import MenuURL, UrlGroup


def index(request):
    context = {
        'url_groups': UrlGroup.objects.filter(active=True),
        'menu_items': MenuURL.objects.filter(active=True, url_group=None)
    }
    template = 'dashboard/index.html'
    return render(request, template, context)
